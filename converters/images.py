"""Image <-> PDF conversions."""
import os

import img2pdf
from pdf2image import convert_from_path
from PIL import Image, UnidentifiedImageError

from .office import ConversionError


def images_to_pdf(image_paths: list, out_path: str) -> str:
    """Combine one or more JPG/PNG images into a single PDF, in order.

    img2pdf embeds JPEG files byte-for-byte and PNG data losslessly, so the
    original upload is passed straight through whenever img2pdf supports its
    colour mode (RGB, greyscale, black-and-white, CMYK). Only images img2pdf
    can't embed as-is are rewritten first -- and always as lossless PNG:

    * transparent images (RGBA / LA / palette with transparency) are placed
      on a WHITE background first. (Before 2026-09-27 they were converted
      with a plain RGB conversion, which turned transparent areas black,
      and re-saved as JPEG.)
    * any other colour mode (palette, 16-bit, etc.) is converted to RGB.
    """
    try:
        normalized = []
        for p in image_paths:
            with Image.open(p) as im:
                has_alpha = im.mode in ("RGBA", "LA") or (
                    im.mode == "P" and "transparency" in im.info
                )
                if has_alpha:
                    rgba = im.convert("RGBA")
                    flat = Image.new("RGB", rgba.size, (255, 255, 255))
                    flat.paste(rgba, mask=rgba.getchannel("A"))
                    fixed = p + ".flat.png"
                    flat.save(fixed, "PNG")
                    normalized.append(fixed)
                elif im.mode in ("RGB", "L", "1", "CMYK"):
                    normalized.append(p)
                else:
                    fixed = p + ".rgb.png"
                    im.convert("RGB").save(fixed, "PNG")
                    normalized.append(fixed)

        with open(out_path, "wb") as f:
            f.write(img2pdf.convert(normalized))
        return out_path
    except UnidentifiedImageError as exc:
        raise ConversionError("One of the uploaded files is not a valid image.") from exc
    except Exception as exc:
        raise ConversionError(f"Could not build a PDF from these images: {exc}") from exc


def pdf_to_images(input_path: str, out_dir: str, fmt: str = "png", dpi: int = 300):
    """Render each PDF page to an image file. Returns list of file paths in page order.

    300 DPI (bumped from 200 on 2026-08-27) matches the standard print-
    quality threshold, so text and fine detail in the rendered image stay
    sharp -- the trade-off is roughly 2.25x the pixel count (and file size)
    of the previous default.
    """
    fmt = fmt.lower()
    if fmt not in ("png", "jpg", "jpeg"):
        fmt = "png"
    pil_fmt = "JPEG" if fmt in ("jpg", "jpeg") else "PNG"
    try:
        pages = convert_from_path(input_path, dpi=dpi)
    except Exception as exc:
        raise ConversionError(
            "Could not open this PDF to render pages. It may be corrupted or password-protected."
        ) from exc

    if not pages:
        raise ConversionError("This PDF has no pages to convert.")

    out_paths = []
    ext = "jpg" if pil_fmt == "JPEG" else "png"
    for i, page in enumerate(pages, start=1):
        out_path = os.path.join(out_dir, f"page-{i:03d}.{ext}")
        if pil_fmt == "JPEG" and page.mode != "RGB":
            page = page.convert("RGB")
        page.save(out_path, pil_fmt)
        out_paths.append(out_path)
    return out_paths
