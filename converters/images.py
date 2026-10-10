"""Image <-> PDF conversions, and image to image (HEIC/WEBP/PNG to JPG, JPG to PNG)."""
import os

import img2pdf
from pdf2image import convert_from_path
from PIL import Image, ImageOps, UnidentifiedImageError

from .office import ConversionError
from .isolate import is_out_of_memory


def _has_transparency(im) -> bool:
    return im.mode in ("RGBA", "LA", "PA") or "transparency" in im.info


def _flatten_on_white(im):
    """RGB copy of an image with transparency, transparent areas on WHITE."""
    rgba = im.convert("RGBA")
    flat = Image.new("RGB", rgba.size, (255, 255, 255))
    flat.paste(rgba, mask=rgba.getchannel("A"))
    return flat


def _to_8bit(im):
    """RGB or greyscale (L) copy of an image in any other colour mode.

    16-bit greyscale images (mode I;16 / I, e.g. some scans and medical or
    scientific PNGs) are scaled down to 8 bits first. A plain convert("RGB")
    clips every value above 255 to white -- found 9 Oct 2026: a 16-bit
    greyscale PNG came out as an almost completely white page in JPG to PDF.
    """
    if im.mode in ("RGB", "L"):
        return im
    if im.mode.startswith("I;16") or im.mode == "I":
        return im.point(lambda v: v / 256).convert("L")
    if im.mode == "1":
        return im.convert("L")
    return im.convert("RGB")


# F11 (review S-04, 10 Oct 2026): reject PostScript/EPS (and PDF) files in the
# image tools. Pillow would otherwise sniff an EPS and hand it to Ghostscript;
# these tools accept real raster images only, so a file whose magic bytes say
# PostScript/EPS/PDF is refused before anything opens it.
_PS_EPS_PDF_SIGNATURES = (
    b"%!PS",              # PostScript / EPS (ASCII)
    b"\xc5\xd0\xd3\xc6",  # DOS EPS binary header
    b"%PDF",              # PDF -- not a raster image for these tools
)


def _reject_non_raster(path: str, label: str = None) -> None:
    label = label or ("'" + os.path.splitext(os.path.basename(path))[0] + "'")
    try:
        with open(path, "rb") as fh:
            head = fh.read(4)
    except OSError:
        return
    for sig in _PS_EPS_PDF_SIGNATURES:
        if head.startswith(sig):
            raise ConversionError(
                f"{label} is a PostScript/EPS or PDF file, not an image this tool can "
                "convert. Please upload a JPG, PNG, WEBP or HEIC image."
            )


# F7 (review A-03, 10 Oct 2026): strip location/metadata from a JPEG embedded in
# a PDF, losslessly. JPEG metadata lives in APPn/COM marker segments; we drop
# APP1 (Exif, incl. GPS, and XMP) and APP13 (IPTC) and COM, and keep APP0 (JFIF)
# and APP2 (ICC colour profile) and the compressed image data untouched -- so
# GPS and other EXIF are removed without re-encoding the picture.
_JPEG_DROP_MARKERS = frozenset((0xE1, 0xED, 0xFE))  # APP1 (Exif/XMP), APP13 (IPTC), COM


def _strip_jpeg_metadata(data: bytes) -> bytes:
    if len(data) < 2 or data[0] != 0xFF or data[1] != 0xD8:
        return data  # not a JPEG; leave unchanged
    out = bytearray(data[0:2])  # SOI
    i, n = 2, len(data)
    while i + 1 < n:
        if data[i] != 0xFF:
            out.extend(data[i:])
            return bytes(out)
        marker = data[i + 1]
        if marker == 0xDA:  # Start of Scan: copy the rest (entropy data) verbatim
            out.extend(data[i:])
            return bytes(out)
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7 or marker == 0x01:
            out.extend(data[i:i + 2]); i += 2; continue  # standalone, no length
        if i + 3 >= n:
            out.extend(data[i:]); return bytes(out)
        seg_len = (data[i + 2] << 8) | data[i + 3]
        if marker not in _JPEG_DROP_MARKERS:
            out.extend(data[i:i + 2 + seg_len])
        i += 2 + seg_len
    return bytes(out)


def _cmyk_to_srgb(im, icc_bytes):
    """F9 (review A-06, 10 Oct 2026): colour-managed CMYK -> sRGB. Uses the
    image's embedded CMYK profile when present (the common case, e.g. FOGRA39 /
    US Web Coated SWOP); falls back to Pillow's plain conversion only when there
    is no usable profile. A plain CMYK->RGB convert produces the 'neon' colour
    shift the audit measured (dE 54-63)."""
    if icc_bytes:
        try:
            from PIL import ImageCms
            import io as _io
            src = ImageCms.ImageCmsProfile(_io.BytesIO(icc_bytes))
            dst = ImageCms.createProfile("sRGB")
            return ImageCms.profileToProfile(im, src, dst, outputMode="RGB")
        except Exception:
            pass
    return im.convert("RGB")


# Added 11 Oct 2026: keep sideways-stored phone photos upright in JPG to PDF.
# Phones often store a portrait photo sideways plus an EXIF "Orientation"
# flag. img2pdf turns such a page upright with /Rotate -- but it reads that
# flag from the EXIF block, which F7 (_strip_jpeg_metadata) now removes for
# privacy, so the photo came out sideways. We read the flag from the ORIGINAL
# upload here and set the same /Rotate ourselves after img2pdf has run (the
# picture data itself is untouched). Mirrored orientations (2, 4, 5, 7) are
# left as they are, as img2pdf itself cannot express them with /Rotate.
_EXIF_ROTATE = {3: 180, 6: 90, 8: 270}


def _page_rotation(im) -> int:
    try:
        return _EXIF_ROTATE.get(im.getexif().get(0x0112), 0)
    except Exception:
        return 0


def _apply_page_rotations(pdf_path: str, rotations: list) -> None:
    import pikepdf
    with pikepdf.open(pdf_path, allow_overwriting_input=True) as pdf:
        for page, deg in zip(pdf.pages, rotations):
            if deg:
                page.obj["/Rotate"] = deg
        pdf.save(pdf_path)


def images_to_pdf(image_paths: list, out_path: str) -> str:
    """Combine one or more JPG/PNG images into a single PDF, in order.

    img2pdf embeds JPEG data without re-encoding it and PNG data losslessly,
    so the picture in the original upload is passed straight through whenever
    img2pdf supports its colour mode (RGB, greyscale, black-and-white, CMYK).
    A JPEG's metadata segments (EXIF incl. GPS, XMP, IPTC, comments) are
    removed first (F7, _strip_jpeg_metadata); its compressed image data is
    copied unchanged. Only images img2pdf
    can't embed as-is are rewritten first -- and always as lossless PNG:

    * transparent images (RGBA / LA / palette with transparency) are placed
      on a WHITE background first. (Before 2026-09-27 they were converted
      with a plain RGB conversion, which turned transparent areas black,
      and re-saved as JPEG.)
    * any other colour mode (palette, 16-bit, etc.) is converted to RGB or
      greyscale; 16-bit greyscale is scaled to 8 bits (see _to_8bit).
    """
    try:
        normalized = []
        rotations = []  # page /Rotate for each image (see below)
        for p in image_paths:
            _reject_non_raster(p)
            with Image.open(p) as im:
                # JPEG only: the case _strip_jpeg_metadata affects.
                rotations.append(_page_rotation(im) if (im.format or "").upper() == "JPEG" else 0)
                has_alpha = im.mode in ("RGBA", "LA") or (
                    im.mode == "P" and "transparency" in im.info
                )
                if has_alpha:
                    flat = _flatten_on_white(im)
                    fixed = p + ".flat.png"
                    flat.save(fixed, "PNG")
                    normalized.append(fixed)
                elif im.mode in ("RGB", "L", "1", "CMYK"):
                    if (im.format or "").upper() == "JPEG":
                        # F7: embed the JPEG with GPS/EXIF/XMP stripped, losslessly.
                        with open(p, "rb") as _fh:
                            _clean = _strip_jpeg_metadata(_fh.read())
                        _clean_path = p + ".nometa.jpg"
                        with open(_clean_path, "wb") as _fh:
                            _fh.write(_clean)
                        normalized.append(_clean_path)
                    else:
                        normalized.append(p)
                else:
                    fixed = p + ".rgb.png"
                    _to_8bit(im).save(fixed, "PNG")
                    normalized.append(fixed)

        with open(out_path, "wb") as f:
            f.write(img2pdf.convert(normalized))
        if any(rotations):
            _apply_page_rotations(out_path, rotations)
        return out_path
    except UnidentifiedImageError as exc:
        raise ConversionError("One of the uploaded files is not a valid image.") from exc
    except Exception as exc:
        raise ConversionError(f"Could not build a PDF from these images: {exc}") from exc


# Hard page limit for the tools that turn every page into a full-size image
# (PDF to JPG, PDF to PNG, PDF to PPT). Added 2026-10-05 after the server ran
# out of memory three times (Render: "used over 2GB", 4-5 Oct 2026).
MAX_RENDER_PAGES = int(os.environ.get("MAX_RENDER_PAGES", "50"))


def count_pdf_pages(input_path: str) -> int:
    """Page count without rendering anything (cheap)."""
    import pikepdf
    try:
        with pikepdf.open(input_path) as pdf:
            return len(pdf.pages)
    except Exception as exc:
        raise ConversionError(
            "Could not open this PDF to render pages. It may be corrupted or password-protected."
        ) from exc


def check_render_page_limit(n_pages: int) -> None:
    if n_pages == 0:
        raise ConversionError("This PDF has no pages to convert.")
    if n_pages > MAX_RENDER_PAGES:
        raise ConversionError(
            f"This PDF has {n_pages} pages. This tool converts up to "
            f"{MAX_RENDER_PAGES} pages at a time -- split the PDF with Split PDF "
            f"and convert it in parts."
        )


def render_pdf_page(input_path: str, page_no: int, dpi: int, use_cropbox: bool = False):
    """Render ONE page (1-based) to a PIL image.

    Before 2026-10-05 every caller used convert_from_path(input_path, dpi=...)
    with no page range, which decodes ALL pages into memory at once. Measured
    in testing: a 40-page PDF at 300 dpi peaked at about 3 GB of memory
    (over the server's 2 GB limit); rendering one page at a time keeps the
    peak to roughly one page's worth, whatever the page count.

    use_cropbox=True renders the page's crop box (the area a PDF viewer
    shows) instead of the whole media box. PDF to PPT uses it so that the
    picture matches the slide size, which comes from the crop box
    (added 2026-10-10 after the independent pre-release review).
    """
    pages = convert_from_path(input_path, dpi=dpi, first_page=page_no, last_page=page_no,
                              use_cropbox=use_cropbox)
    if not pages:
        raise ConversionError("Could not render a page of this PDF.")
    return pages[0]


def pdf_to_images(input_path: str, out_dir: str, fmt: str = "png", dpi: int = 300):
    """Render each PDF page to an image file. Returns list of file paths in page order.

    300 DPI (bumped from 200 on 2026-08-27) matches the standard print-
    quality threshold, so text and fine detail in the rendered image stay
    sharp -- the trade-off is roughly 2.25x the pixel count (and file size)
    of the previous default. Pages are rendered and saved one at a time to
    keep memory use flat (see render_pdf_page).
    """
    fmt = fmt.lower()
    if fmt not in ("png", "jpg", "jpeg"):
        fmt = "png"
    pil_fmt = "JPEG" if fmt in ("jpg", "jpeg") else "PNG"
    n_pages = count_pdf_pages(input_path)
    check_render_page_limit(n_pages)

    out_paths = []
    ext = "jpg" if pil_fmt == "JPEG" else "png"
    for i in range(1, n_pages + 1):
        try:
            # F6: honour the page's crop box (what a PDF viewer shows) so
            # cropped-out content does not reappear in the rendered image.
            page = render_pdf_page(input_path, i, dpi, use_cropbox=True)
        except ConversionError:
            raise
        except Exception as exc:
            raise ConversionError(
                "Could not open this PDF to render pages. It may be corrupted or password-protected."
            ) from exc
        out_path = os.path.join(out_dir, f"page-{i:03d}.{ext}")
        if pil_fmt == "JPEG" and page.mode != "RGB":
            page = page.convert("RGB")
        page.save(out_path, pil_fmt)
        page.close()
        del page
        out_paths.append(out_path)
    return out_paths


# ---- Image to image: HEIC / WEBP / PNG to JPG, and JPG to PNG ---------------
# Added 9 Oct 2026 (image tools). Pillow reads JPG, PNG and WEBP on its own;
# HEIC/HEIF needs the pi-heif plugin (requirements.txt). pi-heif is the
# decode-only edition of pillow-heif: it can read HEIC files but not write
# them, which is all we need. It is imported only when a HEIC file is
# converted, so nothing else depends on it.
#
# What every converted image gets (and what the tool pages promise):
#   * full size, turned the right way up (EXIF orientation applied), first
#     frame only for an animated WEBP, main image only for a multi-image HEIC
#   * transparent areas on WHITE (JPG has no transparency)
#   * the colour profile (ICC) kept when it matches the output colours
#   * metadata: ONLY the date/time taken and the camera make and model are
#     kept. GPS location, serial numbers, owner names, maker notes, XMP and
#     embedded thumbnails are all dropped (Shahid's choice "A", 9 Oct 2026).
#   * JPG at quality 90 (baseline, works everywhere); PNG lossless.
JPEG_QUALITY = 90
# Largest image accepted, in megapixels. Covers 48 and 64 MP phone photos
# (a "64 MP" photo is 9248 x 6936 = 64.1 MP) and most 45-61 MP cameras.
# Measured 9 Oct 2026 with the 700 MB allowance per conversion: a 64 MP JPG
# that needed rotating, saved as PNG, peaked at 511 MB (25 s); a 90 MP one
# peaked at 710 MB, too close to the limit.
MAX_IMAGE_MEGAPIXELS = int(os.environ.get("MAX_IMAGE_MEGAPIXELS", "65"))
# Largest total size of the converted images (MB). A photo saved as PNG is
# several times bigger than the JPG, and the finished files are held in
# memory while they are sent, so a very big batch is refused with a clear
# message instead of risking the server's memory.
MAX_IMAGE_OUTPUT_MB = int(os.environ.get("MAX_IMAGE_OUTPUT_MB", "150"))

_EXIF_KEEP_MAIN = (0x010F, 0x0110, 0x0132)  # Make, Model, DateTime
_EXIF_KEEP_SUB = (                          # in the Exif sub-IFD (0x8769)
    0x9003, 0x9004,                         # DateTimeOriginal, DateTimeDigitized
    0x9010, 0x9011, 0x9012,                 # OffsetTime, -Original, -Digitized
    0x9290, 0x9291, 0x9292,                 # SubSecTime, -Original, -Digitized
)

_heif_ready = False


def _enable_heif():
    global _heif_ready
    if not _heif_ready:
        import pi_heif
        pi_heif.register_heif_opener()
        _heif_ready = True


def _kept_exif(im):
    """A new EXIF block holding only the date taken and the camera make/model
    (None if the image has none of these)."""
    try:
        src = im.getexif()
    except Exception:
        return None
    out = Image.Exif()
    for tag in _EXIF_KEEP_MAIN:
        value = src.get(tag)
        if value:
            out[tag] = value
    try:
        sub = src.get_ifd(0x8769)
    except Exception:
        sub = {}
    kept_sub = {t: sub[t] for t in _EXIF_KEEP_SUB if sub.get(t)}
    if kept_sub:
        out[0x8769] = kept_sub
    return out if len(out) else None


def _icc_space(icc):
    """Colour space named in an ICC profile header: 'RGB ', 'GRAY', 'CMYK'..."""
    if isinstance(icc, bytes) and len(icc) >= 20:
        return icc[16:20].decode("latin-1")
    return None


def convert_images(src_paths: list, out_dir: str, out_format: str, out_names: list) -> list:
    """Convert each image in src_paths to out_format ("JPEG" or "PNG").

    Writes out_dir/out_names[i] for every input, in order, and returns the
    list of written paths. Raises ConversionError with a message meant for
    the visitor when a file can't be converted.
    """
    out_format = out_format.upper()
    if out_format not in ("JPEG", "PNG"):
        raise ValueError(out_format)
    if any(os.path.splitext(p)[1].lower() in (".heic", ".heif") for p in src_paths):
        _enable_heif()
    max_pixels = MAX_IMAGE_MEGAPIXELS * 1_000_000
    max_bytes = MAX_IMAGE_OUTPUT_MB * 1024 * 1024
    written, total = [], 0
    for src, name in zip(src_paths, out_names):
        label = "'" + os.path.splitext(name)[0] + "'"
        out_path = os.path.join(out_dir, name)
        try:
            _reject_non_raster(src, label)
            with Image.open(src) as im:
                w, h = im.size
                if w * h > max_pixels:
                    raise ConversionError(
                        f"{label} is {w * h / 1e6:.0f} megapixels. This tool converts images "
                        f"up to {MAX_IMAGE_MEGAPIXELS} megapixels -- please use a smaller image."
                    )
                # F8: do NOT seek(0). pi_heif opens a multi-image HEIC on its
                # PRIMARY image, which is not always frame 0, so seeking to 0
                # could pick the wrong picture. Image.open already starts on the
                # first frame of an animated WEBP, so no seek is needed there.
                exif = _kept_exif(im)
                icc = im.info.get("icc_profile")
                if im.getexif().get(0x0112, 1) not in (1, None):
                    img = ImageOps.exif_transpose(im)  # turn it the right way up
                else:
                    img = im
                    img.load()
                if _has_transparency(img):
                    img = _flatten_on_white(img)
                elif img.mode == "CMYK":
                    img = _cmyk_to_srgb(img, icc)  # F9: colour-managed, not naive
                    icc = None                     # output is sRGB now
                else:
                    img = _to_8bit(img)  # RGB or L; palette and 16-bit converted
                wanted_space = "GRAY" if img.mode == "L" else "RGB "
                if _icc_space(icc) != wanted_space:
                    icc = None  # profile doesn't match the colours being saved
                img.info = {}  # nothing from the source carries over unless listed below
                params = {}
                if icc:
                    params["icc_profile"] = icc
                if exif is not None:
                    params["exif"] = exif.tobytes()
                if out_format == "JPEG":
                    img.save(out_path, "JPEG", quality=JPEG_QUALITY, optimize=True, **params)
                else:
                    img.save(out_path, "PNG", compress_level=6, **params)
        except ConversionError:
            raise
        except Image.DecompressionBombError as exc:
            raise ConversionError(
                f"{label} is too large to convert. Please use a smaller image."
            ) from exc
        except UnidentifiedImageError as exc:
            raise ConversionError(
                f"{label} isn't a valid image file, or it's damaged."
            ) from exc
        except (OSError, SyntaxError, ValueError, RuntimeError, EOFError) as exc:
            if is_out_of_memory(exc) or "memory" in str(exc).lower():
                # Let converters/isolate.py report it as "too large" (memory cap).
                raise MemoryError(str(exc)) from exc
            raise ConversionError(
                f"{label} couldn't be read -- it may be damaged or incomplete."
            ) from exc

        total += os.path.getsize(out_path)
        if total > max_bytes:
            raise ConversionError(
                f"The converted images would be larger than {MAX_IMAGE_OUTPUT_MB} MB "
                "together, which is too big to download in one go. Please convert "
                "fewer images at a time."
            )
        written.append(out_path)
    return written
