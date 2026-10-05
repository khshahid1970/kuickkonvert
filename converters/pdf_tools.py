"""Core PDF toolkit: merge, split, compress, rotate, watermark, protect."""
import os
import shutil
import subprocess

import pikepdf
from pikepdf import Pdf
from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError

from .office import ConversionError

GS_BIN = os.environ.get("GS_BIN", "gs")


LOCKED_PDF_MESSAGE = (
    "{name} is password-protected, so it can't be opened here. Open it with "
    "its password in your PDF reader, save or print a copy without a "
    "password, and upload that copy."
)


def ensure_pdf_unlocked(path: str, display_name: str = "This PDF") -> None:
    """Raise a clear ConversionError if a PDF needs a password to open.

    Called once for every uploaded PDF (see _save_uploads in app.py) so that
    EVERY PDF tool -- not only the pypdf-based ones -- gives the same clear
    message instead of a generic "Something went wrong" error.

    Before 2026-10-05 a password-protected upload reached pypdf, whose
    decrypt("") returns PasswordType.NOT_DECRYPTED (it does not raise) when
    the password is wrong, so the tool crashed later with an unhandled
    FileNotDecryptedError and the user saw the generic 500 message.

    PDFs with only an owner password (permission restrictions, no password
    needed to open) still open here and are processed as before. Any other
    problem with the file is left for the tool itself to report.
    """
    try:
        with pikepdf.open(path):
            pass
    except pikepdf.PasswordError:
        raise ConversionError(LOCKED_PDF_MESSAGE.format(name=display_name))
    except Exception:
        pass


def _open_reader(path):
    try:
        reader = PdfReader(path)
        if reader.is_encrypted:
            # Owner-password-only PDFs open with an empty user password.
            # decrypt() RETURNS PasswordType.NOT_DECRYPTED (0) on failure
            # rather than raising, so the result has to be checked.
            try:
                result = reader.decrypt("")
            except Exception:
                result = 0
            if not result:
                raise ConversionError(LOCKED_PDF_MESSAGE.format(name="This PDF"))
        return reader
    except PdfReadError as exc:
        raise ConversionError("This file doesn't look like a valid PDF.") from exc


def merge_pdfs(input_paths: list, out_path: str) -> str:
    writer = PdfWriter()
    for p in input_paths:
        reader = _open_reader(p)
        for page in reader.pages:
            writer.add_page(page)
    if len(writer.pages) == 0:
        raise ConversionError("No pages found to merge.")
    with open(out_path, "wb") as f:
        writer.write(f)
    return out_path


def split_pdf(input_path: str, out_dir: str) -> list:
    """Split every page of a PDF into its own single-page PDF file."""
    reader = _open_reader(input_path)
    out_paths = []
    n = len(reader.pages)
    if n == 0:
        raise ConversionError("This PDF has no pages to split.")
    for i in range(n):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])
        out_path = os.path.join(out_dir, f"page-{i + 1:03d}.pdf")
        with open(out_path, "wb") as f:
            writer.write(f)
        out_paths.append(out_path)
    return out_paths


def rotate_pdf(input_path: str, out_path: str, degrees: int) -> str:
    degrees = int(degrees) % 360
    if degrees % 90 != 0:
        raise ConversionError("Rotation must be a multiple of 90 degrees.")
    reader = _open_reader(input_path)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(degrees)
        writer.add_page(page)
    with open(out_path, "wb") as f:
        writer.write(f)
    return out_path


def watermark_pdf(input_path: str, out_path: str, text: str) -> str:
    """Stamp a diagonal, semi-transparent text watermark on every page."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import Color
    import io

    reader = _open_reader(input_path)
    writer = PdfWriter()

    # Build one watermark overlay sized to the first page, then reuse it.
    # (Good enough for the common case of uniformly-sized pages; pages of a
    # different size still get the overlay scaled to their own box below.)
    def make_overlay(width, height):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(width, height))
        c.saveState()
        c.setFillColor(Color(0.5, 0.5, 0.5, alpha=0.35))
        c.setFont("Helvetica-Bold", max(24, int(min(width, height) / 12)))
        c.translate(width / 2, height / 2)
        c.rotate(45)
        c.drawCentredString(0, 0, text[:120])
        c.restoreState()
        c.save()
        buf.seek(0)
        return PdfReader(buf).pages[0]

    overlay_cache = {}
    for page in reader.pages:
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)
        key = (round(w), round(h))
        if key not in overlay_cache:
            overlay_cache[key] = make_overlay(w, h)
        page.merge_page(overlay_cache[key])
        writer.add_page(page)

    with open(out_path, "wb") as f:
        writer.write(f)
    return out_path


def protect_pdf(input_path: str, out_path: str, password: str) -> str:
    """Encrypt a PDF with AES-256 (security handler revision 6).

    Until 2026-10-05 this used pypdf's 128-bit RC4 (revision 3). PDF 2.0
    (ISO 32000-2) deprecates every use of RC4 and makes 256-bit AES the
    standard for password-protected PDFs, so the file is now written with
    pikepdf/qpdf using R=6 AES-256. Adobe Acrobat/Reader has supported
    256-bit AES since version 9.

    The same password is used as both the user (open) and owner password and
    all permissions are left allowed, exactly as before: anyone with the
    password can use the document normally.
    """
    if not password or len(password) < 4:
        raise ConversionError("Choose a password with at least 4 characters.")
    try:
        with pikepdf.open(input_path) as pdf:
            pdf.save(
                out_path,
                encryption=pikepdf.Encryption(
                    user=password,
                    owner=password,
                    R=6,
                    # pikepdf's default Permissions() disallows "modify
                    # assembly"; allow everything, as the old RC4 output did.
                    allow=pikepdf.Permissions(modify_assembly=True),
                ),
            )
    except pikepdf.PasswordError as exc:
        raise ConversionError(LOCKED_PDF_MESSAGE.format(name="This PDF")) from exc
    except pikepdf.PdfError as exc:
        raise ConversionError("This file doesn't look like a valid PDF.") from exc
    return out_path


def compress_pdf(input_path: str, out_path: str, level: str = "ebook") -> str:
    """Shrink a PDF's file size.

    Prefers Ghostscript (best real-world compression via image downsampling).
    Falls back to pikepdf stream recompression if Ghostscript isn't
    installed in this environment.

    Ghostscript's own documentation says rewriting a PDF can produce a
    LARGER file (tested 2026-09-27: text-only PDFs grew 24-170%, and a
    200-dpi scan grew ~6% on "ebook"/"printer", which don't downsample it).
    So if the result isn't smaller than the upload, the user gets their
    original file back unchanged instead of a bigger one.
    """
    level = level if level in ("screen", "ebook", "printer") else "ebook"
    if shutil.which(GS_BIN):
        cmd = [
            GS_BIN,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS=/{level}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={out_path}",
            input_path,
        ]
        try:
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120, text=True
            )
        except subprocess.TimeoutExpired as exc:
            raise ConversionError("Compression took too long for this file.") from exc
        if result.returncode == 0 and os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            return _keep_smaller(input_path, out_path)
        # fall through to pikepdf fallback if Ghostscript failed

    try:
        with Pdf.open(input_path) as pdf:
            pdf.save(out_path, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate)
        return _keep_smaller(input_path, out_path)
    except Exception as exc:
        raise ConversionError(f"Could not compress this PDF: {exc}") from exc


def _keep_smaller(input_path: str, out_path: str) -> str:
    """If compression didn't shrink the file, replace the output with the original."""
    if os.path.getsize(out_path) >= os.path.getsize(input_path):
        shutil.copyfile(input_path, out_path)
    return out_path
