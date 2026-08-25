"""Office <-> PDF conversions, powered by headless LibreOffice.

LibreOffice is the only free/open-source engine that reliably round-trips
Word/Excel/PowerPoint <-> PDF with acceptable layout fidelity. Each call
shells out to `soffice --headless --convert-to`, which is CPU-bound and
single-document-at-a-time by nature of the LO profile lock, so callers
should expect a real conversion (not instant) and should not call this
concurrently against the same user profile directory.
"""
import glob
import os
import subprocess

from .utils import safe_name

SOFFICE_BIN = os.environ.get("SOFFICE_BIN", "soffice")
CONVERT_TIMEOUT = int(os.environ.get("CONVERT_TIMEOUT_SECONDS", "120"))


class ConversionError(Exception):
    pass


def _run_soffice(input_path: str, out_dir: str, target_filter: str, infilter: str = None):
    """Run soffice --convert-to and return the produced file path.

    Output is written to a dedicated subdirectory, never the same directory
    the input file lives in -- if input and output shared a directory, an
    input like "report.pdf" being converted to "report.pdf"-named output
    (or a glob matching both the original upload and the new file when they
    share a stem) could get confused for one another and the wrong file
    would be returned to the user.

    `infilter` forces how LibreOffice interprets the *input* file. This
    matters specifically for PDF input: LibreOffice opens a PDF as a Draw
    (graphics) document by default, which can export fine to PPTX (another
    graphics-ish format) but fails outright when asked to save as DOCX --
    Draw has no Writer text model to save from. Passing
    infilter="writer_pdf_import" makes LibreOffice reimport the PDF as an
    editable Writer document instead, which is what a PDF->Word conversion
    actually needs.
    """
    # Give each invocation its own LO user profile so concurrent requests
    # (different jobs, different temp dirs) never collide on a lock file.
    profile_dir = os.path.join(out_dir, "_lo_profile")
    os.makedirs(profile_dir, exist_ok=True)
    profile_uri = f"file://{profile_dir}"

    out_subdir = os.path.join(out_dir, "_lo_output")
    os.makedirs(out_subdir, exist_ok=True)

    cmd = [
        SOFFICE_BIN,
        "--headless",
        "--norestore",
        "--nolockcheck",
        f"-env:UserInstallation={profile_uri}",
    ]
    if infilter:
        cmd += [f"--infilter={infilter}"]
    cmd += [
        "--convert-to",
        target_filter,
        "--outdir",
        out_subdir,
        input_path,
    ]
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=CONVERT_TIMEOUT,
            text=True,
        )
    except subprocess.TimeoutExpired as exc:
        raise ConversionError(
            "The conversion took too long. The file may be very large or complex."
        ) from exc

    if result.returncode != 0:
        raise ConversionError(
            "LibreOffice could not convert this file. It may be corrupted, "
            "password-protected, or in an unsupported format."
        )

    # LibreOffice names the output after the input's basename with the new
    # extension; locate it rather than assuming the exact extension string.
    # Filter by the target extension too, defensively, in case the input
    # file's own copy ever ends up alongside it.
    stem = os.path.splitext(os.path.basename(input_path))[0]
    target_ext = target_filter.split(":", 1)[0].lstrip(".").lower()
    matches = [
        m for m in glob.glob(os.path.join(out_subdir, f"{stem}.*"))
        if os.path.isfile(m) and m.lower().endswith("." + target_ext)
    ]
    if not matches:
        raise ConversionError("Conversion finished but produced no output file.")
    return matches[0]


def convert_office_to_pdf(input_path: str, out_dir: str) -> str:
    """Word/Excel/PowerPoint (and ODT/RTF/TXT) -> PDF."""
    return _run_soffice(input_path, out_dir, "pdf")


def convert_pdf_to_word(input_path: str, out_dir: str) -> str:
    """PDF -> editable .docx. Best results with text-based (not scanned) PDFs."""
    return _run_soffice(
        input_path, out_dir, "docx:MS Word 2007 XML", infilter="writer_pdf_import"
    )


def convert_pdf_to_ppt(input_path: str, out_dir: str) -> str:
    """PDF -> .pptx, one slide per page. Best results with text-based PDFs."""
    return _run_soffice(input_path, out_dir, "pptx:Impress MS PowerPoint 2007 XML")
