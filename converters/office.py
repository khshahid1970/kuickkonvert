"""Office <-> PDF conversions, powered by headless LibreOffice (plus a
pdf2docx assist for PDF -> Word -- see convert_pdf_to_word below).

LibreOffice is the only free/open-source engine that reliably round-trips
Word/Excel/PowerPoint <-> PDF with acceptable layout fidelity. Each call
shells out to `soffice --headless --convert-to`, which is CPU-bound and
single-document-at-a-time by nature of the LO profile lock, so callers
should expect a real conversion (not instant) and should not call this
concurrently against the same user profile directory.
"""
import glob
import io
import os
import subprocess

SOFFICE_BIN = os.environ.get("SOFFICE_BIN", "soffice")
CONVERT_TIMEOUT = int(os.environ.get("CONVERT_TIMEOUT_SECONDS", "120"))

SPREADSHEET_EXTS = {"xls", "xlsx"}

_SINGLE_PAGE_SHEETS_FILTER = (
    'pdf:calc_pdf_Export:{"SinglePageSheets":{"type":"boolean","value":"true"}}'
)
# Verified 2026-08-27: this custom calc_pdf_Export filter-data string works on
# LibreOffice 24.2 (this sandbox) but silently fails on production's LibreOffice
# (Render/Debian slim apt package) -- soffice exits 0 but writes no output file
# at all, specifically for sheets wide/tall enough to actually need the option
# (a trivial 2-cell sheet converts fine; a realistic multi-column sheet does
# not). Rather than depend on a filter-data option whose JSON syntax support
# clearly varies by LibreOffice build, convert_office_to_pdf() below now relies
# solely on the standard OOXML page-setup properties (fitToWidth/fitToHeight)
# that _widen_columns_to_fit() already writes into the .xlsx itself -- these
# are ordinary spreadsheet properties, not a custom export filter option, and
# LibreOffice's plain "pdf" export honours them on every version tested.
# Re-verified same day: plain "pdf" export of the widened file produces an
# identical single-page, non-truncated result. Kept here only in case a size
# analysis of the *production* LibreOffice version is done later.


class ConversionError(Exception):
    pass


def _run_soffice(input_path: str, out_dir: str, target_filter: str, infilter: str = None):
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

    stem = os.path.splitext(os.path.basename(input_path))[0]
    target_ext = target_filter.split(":", 1)[0].lstrip(".").lower()
    matches = [
        m for m in glob.glob(os.path.join(out_subdir, f"{stem}.*"))
        if os.path.isfile(m) and m.lower().endswith("." + target_ext)
    ]
    if not matches:
        raise ConversionError("Conversion finished but produced no output file.")
    return matches[0]


def _widen_columns_to_fit(xlsx_path: str) -> None:
    import openpyxl
    from openpyxl.utils import get_column_letter

    wb = openpyxl.load_workbook(xlsx_path)
    for ws in wb.worksheets:
        widths = {}
        for row in ws.iter_rows():
            for cell in row:
                if cell.value is None:
                    continue
                length = len(str(cell.value))
                col = cell.column
                if length > widths.get(col, 0):
                    widths[col] = length
        for col, length in widths.items():
            ws.column_dimensions[get_column_letter(col)].width = min(max(length + 2, 8), 60)
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(xlsx_path)


def convert_office_to_pdf(input_path: str, out_dir: str) -> str:
    ext = os.path.splitext(input_path)[1].lower().lstrip(".")
    if ext not in SPREADSHEET_EXTS:
        return _run_soffice(input_path, out_dir, "pdf")

    xlsx_path = input_path
    if ext == "xls":
        xlsx_path = _run_soffice(input_path, out_dir, "xlsx:Calc MS Excel 2007 XML")

    try:
        _widen_columns_to_fit(xlsx_path)
    except Exception:
        pass

    # Plain "pdf" export -- see the note on _SINGLE_PAGE_SHEETS_FILTER above
    # for why the custom filter-data variant was dropped.
    return _run_soffice(xlsx_path, out_dir, "pdf")


def convert_pdf_to_word(input_path: str, out_dir: str) -> str:
    out_path = os.path.join(out_dir, "converted_via_pdf2docx.docx")
    try:
        from pdf2docx import Converter

        cv = Converter(input_path)
        try:
            cv.convert(out_path)
        finally:
            cv.close()
        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            return out_path
    except Exception:
        pass

    return _run_soffice(
        input_path, out_dir, "docx:MS Word 2007 XML", infilter="writer_pdf_import"
    )


def convert_pdf_to_ppt(input_path: str, out_dir: str) -> str:
    """PDF -> .pptx, one slide per page, each slide holding a full-page
    image of that page.

    Verified 2026-08-27: LibreOffice's headless --convert-to path (PDF
    opened as a Draw document, exported to "Impress MS PowerPoint 2007
    XML") silently produced an EMPTY .pptx -- zero slides, no slide master
    -- for every test PDF tried, including the simplest possible two-page
    text-only document, while still reporting success (exit code 0).
    Re-typing a Draw document as an Impress one doesn't work reliably via
    --convert-to, and going through Draw's own native format (.odg) as an
    intermediate step produced the same empty result -- the PDF imports
    into Draw correctly (confirmed via its content.xml), but nothing
    survives the Draw-to-Impress step.
    Given that, each page is rendered to an image (via pdf2image/poppler,
    the same renderer the PDF-to-JPG/PNG tools use) and placed as a single
    image sized to that page's exact original dimensions, with the overall
    slide size fixed to the first page's dimensions. This trades away
    editable text -- each slide is a picture, not text you can click into
    -- for a guaranteed, visually exact replica of every page, which is a
    more honest result than a broken "editable" file that silently has
    nothing in it.
    """
    import pypdf
    from pdf2image import convert_from_path
    from pptx import Presentation
    from pptx.util import Emu

    try:
        reader = pypdf.PdfReader(input_path)
        if len(reader.pages) == 0:
            raise ConversionError("This PDF has no pages to convert.")

        first_box = reader.pages[0].mediabox
        slide_w = Emu(max(int(float(first_box.width) * 12700), 1))
        slide_h = Emu(max(int(float(first_box.height) * 12700), 1))

        prs = Presentation()
        prs.slide_width = slide_w
        prs.slide_height = slide_h
        blank_layout = prs.slide_layouts[6]

        images = convert_from_path(input_path, dpi=200)
        for i, img in enumerate(images):
            page_box = reader.pages[i].mediabox
            page_w = max(int(float(page_box.width) * 12700), 1)
            page_h = max(int(float(page_box.height) * 12700), 1)

            # Fit this page's image inside the fixed slide size, preserving
            # its own aspect ratio, in case pages aren't all the same size.
            scale = min(slide_w / page_w, slide_h / page_h)
            draw_w, draw_h = int(page_w * scale), int(page_h * scale)
            left, top = (slide_w - draw_w) // 2, (slide_h - draw_h) // 2

            slide = prs.slides.add_slide(blank_layout)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            slide.shapes.add_picture(buf, left, top, width=draw_w, height=draw_h)

        out_path = os.path.join(out_dir, "converted.pptx")
        prs.save(out_path)
        return out_path
    except ConversionError:
        raise
    except Exception as exc:
        raise ConversionError(
            "Could not convert this PDF to a presentation. It may be "
            "corrupted or password-protected."
        ) from exc
