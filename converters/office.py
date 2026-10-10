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
import logging
import os
import re
import subprocess
import zipfile

from converters.isolate import is_out_of_memory
from converters.utils import subprocess_env

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


# --- Office SSRF hardening (added 2026-10-10, Round 1 finding F5) -----------
# A Word/Excel/PowerPoint file can carry "external" relationships -- linked
# images, linked workbooks, attached templates -- whose target is a URL. When
# LibreOffice opens such a file it tries to FETCH those targets, which turns an
# anonymous upload into a server-side request to an attacker-chosen host (SSRF).
# Before converting any OOXML file we remove every external relationship, so
# LibreOffice has nothing remote to fetch. OOXML files are zip archives whose
# relationships live in "*.rels" parts as <Relationship ... TargetMode=
# "External" .../> elements; we delete exactly those self-closing elements and
# leave everything else byte-for-byte, so document content (text, tables,
# shapes, charts, embedded images) is untouched.
_EXTERNAL_REL_RE = re.compile(rb'<Relationship\b[^>]*\bTargetMode="External"[^>]*/>')


def strip_external_links(path: str) -> None:
    """Remove external (remote) relationships from an OOXML file, in place.

    No-op for legacy binary .doc/.xls/.ppt (not zip archives) and for any file
    that has no external relationships. Never raises -- if the file can't be
    rewritten for any reason it is left unchanged and conversion proceeds.
    """
    if not zipfile.is_zipfile(path):
        return  # legacy binary Office format -- see the limitation note in the audit
    try:
        with zipfile.ZipFile(path) as zin:
            names = zin.namelist()
            blobs = {n: zin.read(n) for n in names}
    except Exception:
        return

    changed = False
    for name in list(blobs):
        if name.endswith(".rels") and b'TargetMode="External"' in blobs[name]:
            new = _EXTERNAL_REL_RE.sub(b"", blobs[name])
            if new != blobs[name]:
                blobs[name] = new
                changed = True
    if not changed:
        return

    tmp = path + ".nolinks"
    try:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
            for name in names:  # keep the original part order
                zout.writestr(name, blobs[name])
        os.replace(tmp, path)
    except Exception:
        try:
            os.remove(tmp)
        except OSError:
            pass


# --- Preserve shapes in Excel to PDF (added 2026-10-10, Round 1 finding F3) -
# _widen_columns_to_fit() below opens the workbook with openpyxl and saves it
# again to apply "fit to page width". openpyxl does not model drawing shapes
# (text boxes, arrows, callouts, form controls), so saving silently DROPS them
# -- an invoice's "APPROVED" text box, say, vanishes from the PDF. To avoid
# that, convert_office_to_pdf() checks for drawings first: a workbook WITHOUT
# drawings keeps the proven openpyxl path unchanged; a workbook WITH drawings
# skips openpyxl entirely and gets fit-to-page applied by a minimal, direct
# edit of the sheet XML that leaves the drawings untouched.
_FIT_SHEET_WIDE_COLS = 8  # more columns than this -> landscape, to shrink less


def _xlsx_has_drawings(xlsx_path: str) -> bool:
    try:
        with zipfile.ZipFile(xlsx_path) as z:
            for n in z.namelist():
                if n.startswith("xl/drawings/") and n.endswith(".xml"):
                    return True
                if n.startswith("xl/ctrlProps/") or n.startswith("xl/activeX/"):
                    return True
            # A sheet that references a drawing / legacy drawing / OLE object.
            for n in z.namelist():
                if re.match(r"xl/worksheets/sheet\d+\.xml$", n):
                    head = z.read(n)
                    if (b"<drawing " in head or b"<legacyDrawing" in head
                            or b"<oleObject" in head or b"<control " in head):
                        return True
    except Exception:
        return False
    return False


def _edit_sheet_fit_to_page(xml: bytes) -> bytes:
    """Return the worksheet XML with fit-to-page-width turned on, editing only
    the page-setup elements and leaving drawings and data untouched."""
    # Decide orientation from the column span in <dimension ref="A1:H23"/>.
    landscape = False
    m = re.search(rb'<dimension ref="[A-Z]+\d+:([A-Z]+)\d+"', xml)
    if m:
        col = m.group(1).decode()
        n = 0
        for ch in col:
            n = n * 26 + (ord(ch) - 64)
        landscape = n > _FIT_SHEET_WIDE_COLS
    orient = b"landscape" if landscape else b"portrait"

    # 1) <pageSetUpPr fitToPage="1"/> inside <sheetPr>.
    if b"<pageSetUpPr" in xml:
        xml = re.sub(rb"<pageSetUpPr\b[^>]*/>", b'<pageSetUpPr fitToPage="1"/>', xml, count=1)
    elif b"<sheetPr" in xml:
        xml = re.sub(rb"(</sheetPr>)", rb'<pageSetUpPr fitToPage="1"/>\1', xml, count=1)
        # If <sheetPr> was self-closing (<sheetPr/>), the above didn't match.
        if b'<pageSetUpPr fitToPage="1"/>' not in xml:
            xml = re.sub(rb"<sheetPr\b([^>]*)/>",
                         rb'<sheetPr\1><pageSetUpPr fitToPage="1"/></sheetPr>', xml, count=1)
    else:
        xml = re.sub(rb"(<worksheet\b[^>]*>)",
                     rb'\1<sheetPr><pageSetUpPr fitToPage="1"/></sheetPr>', xml, count=1)

    # 2) <pageSetup fitToWidth="1" fitToHeight="0" orientation=.../>.
    setup = b'<pageSetup fitToWidth="1" fitToHeight="0" orientation="' + orient + b'"/>'
    if b"<pageSetup" in xml:
        xml = re.sub(rb"<pageSetup\b[^>]*/>", setup, xml, count=1)
    elif b"<pageMargins" in xml:
        xml = re.sub(rb"(<pageMargins\b[^>]*/>)", rb"\1" + setup, xml, count=1)
    else:
        xml = re.sub(rb"(</worksheet>)", setup + rb"\1", xml, count=1)
    return xml


def _apply_fit_to_page_preserving_drawings(xlsx_path: str) -> None:
    """Turn on fit-to-page-width for every sheet by editing the sheet XML in
    place, without going through openpyxl (so drawings survive)."""
    with zipfile.ZipFile(xlsx_path) as z:
        names = z.namelist()
        blobs = {n: z.read(n) for n in names}
    for n in names:
        if re.match(r"xl/worksheets/sheet\d+\.xml$", n):
            blobs[n] = _edit_sheet_fit_to_page(blobs[n])
    tmp = xlsx_path + ".fit"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in names:
            zout.writestr(n, blobs[n])
    os.replace(tmp, xlsx_path)


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
            env=subprocess_env(out_dir),  # LibreOffice temp files stay in the job folder
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

    # Sum of a sheet's (capped) column widths, in the same "characters"
    # unit openpyxl column widths use, above which we switch that sheet
    # to landscape before LibreOffice's fitToWidth scaling runs. This
    # doesn't change *whether* every column survives -- fitToWidth
    # already guarantees that on its own -- it only reduces how far the
    # font has to shrink to get there, since landscape gives roughly
    # 30% more usable width than portrait at the same margins. Verified
    # 2026-08-27 against a real ~19-column bank statement (which totals
    # well past this threshold) and a narrow synthetic sheet (which
    # doesn't) -- only the wide one flips to landscape.
    LANDSCAPE_WIDTH_THRESHOLD = 80

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
        capped_widths = {}
        for col, length in widths.items():
            capped = min(max(length + 2, 8), 60)
            capped_widths[col] = capped
            ws.column_dimensions[get_column_letter(col)].width = capped
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        if sum(capped_widths.values()) > LANDSCAPE_WIDTH_THRESHOLD:
            ws.page_setup.orientation = "landscape"
    wb.save(xlsx_path)


def convert_office_to_pdf(input_path: str, out_dir: str) -> str:
    ext = os.path.splitext(input_path)[1].lower().lstrip(".")

    # F5 (SSRF): remove external linked resources before LibreOffice opens the
    # file, so it cannot fetch remote images/templates/workbooks. No-op for
    # legacy binary formats (see the audit's limitation note).
    strip_external_links(input_path)

    if ext not in SPREADSHEET_EXTS:
        return _run_soffice(input_path, out_dir, "pdf")

    xlsx_path = input_path
    if ext == "xls":
        xlsx_path = _run_soffice(input_path, out_dir, "xlsx:Calc MS Excel 2007 XML")

    # F3: a workbook with drawing shapes must NOT be re-saved by openpyxl
    # (it drops shapes). Apply fit-to-page by editing the sheet XML instead,
    # which leaves the drawings intact. Workbooks without drawings keep the
    # original, proven openpyxl path. Either way, if the optimisation fails we
    # still convert -- all cell content and shapes are preserved regardless.
    try:
        if _xlsx_has_drawings(xlsx_path):
            _apply_fit_to_page_preserving_drawings(xlsx_path)
        else:
            _widen_columns_to_fit(xlsx_path)
    except Exception:
        pass

    # Plain "pdf" export -- see the note on _SINGLE_PAGE_SHEETS_FILTER above
    # for why the custom filter-data variant was dropped.
    return _run_soffice(xlsx_path, out_dir, "pdf")


def convert_pdf_to_word(input_path: str, out_dir: str) -> str:
    out_path = os.path.join(out_dir, "converted_via_pdf2docx.docx")
    # Privacy (added 2026-10-07): pdf2docx writes to the server log through
    # Python's root logger -- "Start to convert <full file path>" (the path
    # contains the visitor's original file name), page-by-page progress, and
    # in some cases lines of the document's own text. Visitors' file names
    # and content must never appear in the Render logs, so all logging is
    # switched off while pdf2docx runs and switched back on afterwards.
    # (This runs inside the isolated child process -- see converters/isolate.py
    # -- so it does not silence the website's own logs.)
    logging.disable(logging.CRITICAL)
    try:
        from pdf2docx import Converter

        cv = Converter(input_path)
        try:
            cv.convert(out_path)
        finally:
            cv.close()
        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            return out_path
    except Exception as exc:
        # Hit the per-conversion memory cap (converters/isolate.py)? Then don't
        # fall back to LibreOffice -- it would need even more memory and then
        # show a misleading "could not convert" message. The visitor gets the
        # "file too large" message instead.
        if is_out_of_memory(exc):
            raise MemoryError() from None
    finally:
        logging.disable(logging.NOTSET)

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
    image, with the overall slide size fixed to the first page's displayed
    size. (Fixed 9 Oct 2026: sizes now follow how each page is DISPLAYED --
    its crop box and /Rotate -- so a rotated page is no longer stretched.) This trades away
    editable text -- each slide is a picture, not text you can click into
    -- for a guaranteed, visually exact replica of every page, which is a
    more honest result than a broken "editable" file that silently has
    nothing in it.
    """
    import pypdf
    from pptx import Presentation
    from pptx.util import Emu
    from .images import check_render_page_limit, render_pdf_page

    try:
        reader = pypdf.PdfReader(input_path)
        check_render_page_limit(len(reader.pages))

        # Slide size = the first page as it is displayed: its crop box,
        # with width and height swapped when the page has /Rotate 90 or 270.
        first = reader.pages[0]
        first_w, first_h = float(first.cropbox.width), float(first.cropbox.height)
        if int(first.get("/Rotate", 0) or 0) % 180 == 90:
            first_w, first_h = first_h, first_w
        slide_w = Emu(max(int(first_w * 12700), 1))
        slide_h = Emu(max(int(first_h * 12700), 1))

        prs = Presentation()
        prs.slide_width = slide_w
        prs.slide_height = slide_h
        blank_layout = prs.slide_layouts[6]

        # One page at a time (see images.render_pdf_page): rendering every
        # page up front peaked at about 1.4 GB for a 40-page PDF in testing.
        for i in range(len(reader.pages)):
            img = render_pdf_page(input_path, i + 1, 200, use_cropbox=True)
            # The rendered image shows the page as displayed (use_cropbox=True:
            # poppler renders the crop box and applies /Rotate), so its proportions are used.
            page_w, page_h = max(img.width, 1), max(img.height, 1)

            # Fit this page's image inside the fixed slide size, preserving
            # its own aspect ratio, in case pages aren't all the same size.
            scale = min(slide_w / page_w, slide_h / page_h)
            draw_w, draw_h = int(page_w * scale), int(page_h * scale)
            left, top = (slide_w - draw_w) // 2, (slide_h - draw_h) // 2

            slide = prs.slides.add_slide(blank_layout)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            img.close()
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
