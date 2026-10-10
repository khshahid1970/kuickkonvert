"""Core PDF toolkit: merge, split, compress, rotate, watermark, protect."""
import os
import shutil
import subprocess

import pikepdf
from pikepdf import Pdf
from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError

from .office import ConversionError
from .utils import subprocess_env

GS_BIN = os.environ.get("GS_BIN", "gs")


LOCKED_PDF_MESSAGE = (
    "{name} is password-protected, so it can't be opened here. Open it with "
    "its password in your PDF reader, save or print a copy without a "
    "password, and upload that copy."
)


DAMAGED_PDF_MESSAGE = (
    "{name} doesn't look like a valid PDF, or it's damaged -- we couldn't "
    "read any pages from it. Please open it in a PDF reader, save a fresh "
    "copy, and upload that."
)


def ensure_pdf_unlocked(path: str, display_name: str = "This PDF") -> None:
    """Raise a clear ConversionError if a PDF needs a password to open, OR if
    it is damaged / has no readable pages.

    Called once for every uploaded PDF (see _save_uploads in app.py) so that
    EVERY PDF tool -- not only the pypdf-based ones -- gives the same clear
    message instead of a generic "Something went wrong" error, a blank
    output, or (for Compress / PDF to Word) a "successful" but empty download.

    Before 2026-10-05 a password-protected upload reached pypdf, whose
    decrypt("") returns PasswordType.NOT_DECRYPTED (it does not raise) when
    the password is wrong, so the tool crashed later with an unhandled
    FileNotDecryptedError and the user saw the generic 500 message.

    Fail-closed on damaged files (added 2026-10-10, Round 1 finding F2):
    previously any non-password error here was swallowed (`except Exception:
    pass`) and "left for the tool to report". The pypdf-based tools (merge,
    split, rotate, watermark) do report it via _open_reader, but Compress
    (Ghostscript) and PDF to Word (LibreOffice) do NOT -- Ghostscript exits 0
    and writes a blank page for a damaged PDF, and LibreOffice writes an empty
    .docx, so the visitor got a 200 "success" with blank/empty content and
    could lose their document. We now reject here any PDF that pikepdf cannot
    open, or that opens with zero pages, for every PDF tool at once.

    PDFs with only an owner password (permission restrictions, no password
    needed to open) still open here and are processed as before.
    """
    try:
        with pikepdf.open(path) as pdf:
            if len(pdf.pages) == 0:
                raise ConversionError(
                    DAMAGED_PDF_MESSAGE.format(name=display_name)
                )
    except pikepdf.PasswordError:
        raise ConversionError(LOCKED_PDF_MESSAGE.format(name=display_name))
    except ConversionError:
        raise
    except Exception:
        raise ConversionError(DAMAGED_PDF_MESSAGE.format(name=display_name))


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


# ---- F10 (review A-07, 10 Oct 2026): owner-set usage restrictions ----------
# An owner-restricted PDF (opens with no password, but limits printing, copying,
# editing, etc.) was silently losing those restrictions when Rotate / Watermark
# / Split rewrote it with pypdf (output unencrypted), and Protect was widening
# them to "allow everything". We now detect the original restrictions and
# RE-APPLY them to the output (empty user password, so it still opens freely,
# plus a fresh random owner password that carries the same permission flags);
# Merge refuses when an input is restricted, because combining documents with
# different owner permissions is ambiguous.
_PERM_FIELDS = (
    "accessibility", "extract", "modify_annotation", "modify_assembly",
    "modify_form", "modify_other", "print_lowres", "print_highres",
)
RESTRICTED_MERGE_MESSAGE = (
    "{name} has usage restrictions set by its owner, so we can't merge it while "
    "keeping those restrictions. Please remove the restrictions in your PDF "
    "editor (or use a copy without them) and try again."
)


def _owner_restrictions(input_path: str):
    """Return (pikepdf.Permissions, R) if the PDF is encrypted with real
    owner-set restrictions (something is disallowed); otherwise None."""
    try:
        with pikepdf.open(input_path) as pdf:
            if not pdf.is_encrypted:
                return None
            allow = pdf.allow
            if all(bool(getattr(allow, f)) for f in _PERM_FIELDS):
                return None  # encrypted but nothing restricted -> nothing to keep
            perms = pikepdf.Permissions(**{f: bool(getattr(allow, f)) for f in _PERM_FIELDS})
            try:
                R = pdf.encryption.R
            except Exception:
                R = 6
            return (perms, R if R in (4, 6) else 6)
    except Exception:
        return None


def _reapply_restrictions(out_path: str, perms, R) -> None:
    """Re-encrypt out_path in place so it opens without a password but carries
    the same permission flags (fresh random owner password)."""
    import secrets
    owner = secrets.token_urlsafe(24)
    with pikepdf.open(out_path, allow_overwriting_input=True) as pdf:
        pdf.save(out_path, encryption=pikepdf.Encryption(user="", owner=owner, R=R, allow=perms))


def merge_pdfs(input_paths: list, out_path: str) -> str:
    for p in input_paths:
        if _owner_restrictions(p):  # F10: ambiguous to merge restricted docs
            raise ConversionError(RESTRICTED_MERGE_MESSAGE.format(name="One of these PDFs"))
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
    restr = _owner_restrictions(input_path)  # F10
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
        if restr:
            _reapply_restrictions(out_path, *restr)
        out_paths.append(out_path)
    return out_paths


def rotate_pdf(input_path: str, out_path: str, degrees: int) -> str:
    degrees = int(degrees) % 360
    if degrees % 90 != 0:
        raise ConversionError("Rotation must be a multiple of 90 degrees.")
    restr = _owner_restrictions(input_path)  # F10
    reader = _open_reader(input_path)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(degrees)
        writer.add_page(page)
    with open(out_path, "wb") as f:
        writer.write(f)
    if restr:
        _reapply_restrictions(out_path, *restr)
    return out_path


def watermark_pdf(input_path: str, out_path: str, text: str) -> str:
    """Stamp a diagonal, semi-transparent text watermark on every page."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import Color
    import io

    restr = _owner_restrictions(input_path)  # F10
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
    if restr:
        _reapply_restrictions(out_path, *restr)
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
    # F10: if the input already had owner-set restrictions, carry them into the
    # protected output rather than widening to "allow everything". Otherwise
    # allow everything (as before), since the holder of the new password is the
    # owner of their own document.
    restr = _owner_restrictions(input_path)
    allow_perms = restr[0] if restr else pikepdf.Permissions(modify_assembly=True)
    try:
        with pikepdf.open(input_path) as pdf:
            pdf.save(
                out_path,
                encryption=pikepdf.Encryption(
                    user=password,
                    owner=password,
                    R=6,
                    allow=allow_perms,
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
            "-dAutoRotatePages=/None",  # keep every page's orientation (9 Oct 2026)
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={out_path}",
            input_path,
        ]
        try:
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120, text=True,
                env=subprocess_env(os.path.dirname(os.path.abspath(out_path))),  # gs temp files in the job folder
            )
        except subprocess.TimeoutExpired as exc:
            raise ConversionError("Compression took too long for this file.") from exc
        if (
            result.returncode == 0
            and os.path.exists(out_path)
            and os.path.getsize(out_path) > 0
            and _same_page_count(input_path, out_path)
        ):
            # Defence in depth for finding F2: Ghostscript exits 0 and writes a
            # blank single-page PDF for some damaged inputs. The upload gate
            # (ensure_pdf_unlocked) already rejects unreadable / zero-page
            # PDFs, but if a file slips through with the wrong page count we
            # treat Ghostscript as failed and fall back to pikepdf rather than
            # hand the visitor a blank "compressed" file.
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


def _same_page_count(input_path: str, out_path: str) -> bool:
    """True if both PDFs open and have the same, non-zero page count.

    Used by compress_pdf as a safety net (finding F2): a mismatch means the
    compressor produced something other than a faithful copy (e.g. a blank
    page from a damaged input), so the caller should not treat it as success.
    On any read error we return False (fail safe).
    """
    try:
        with pikepdf.open(input_path) as a, pikepdf.open(out_path) as b:
            return len(a.pages) > 0 and len(a.pages) == len(b.pages)
    except Exception:
        return False
