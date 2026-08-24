"""PDF -> Excel.

LibreOffice has no native PDF-to-Calc export path (a PDF opens as a Draw or
Writer document internally, and neither can be saved as a spreadsheet), so
this tool takes a different, purpose-built approach: detect table
structures with pdfplumber and write each one to its own worksheet with
openpyxl. Pages with no detected table still contribute their text, one
line per row, so nothing from the source PDF is silently dropped -- but
expect best results on PDFs with real ruled/structured tables rather than
free-form text or scanned images.
"""
import re

import pdfplumber
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

from .office import ConversionError

_INVALID_SHEET_CHARS = re.compile(r"[\[\]:\\/?*]")


def _safe_sheet_name(name: str) -> str:
    name = _INVALID_SHEET_CHARS.sub("-", name).strip() or "Sheet"
    return name[:31]


def convert_pdf_to_excel(input_path: str, out_dir: str) -> str:
    import os

    out_path = os.path.join(out_dir, "converted.xlsx")
    wb = Workbook()
    wb.remove(wb.active)  # replaced by real sheets below
    any_content = False

    try:
        with pdfplumber.open(input_path) as pdf:
            if len(pdf.pages) == 0:
                raise ConversionError("This PDF has no pages to convert.")

            for page_num, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables() or []
                if tables:
                    for t_idx, table in enumerate(tables, start=1):
                        sheet_name = _safe_sheet_name(
                            f"Page {page_num}" + (f" Table {t_idx}" if len(tables) > 1 else "")
                        )
                        ws = wb.create_sheet(title=sheet_name)
                        for row in table:
                            ws.append(["" if c is None else str(c) for c in row])
                        for col_idx in range(1, (max((len(r) for r in table), default=1)) + 1):
                            ws.column_dimensions[get_column_letter(col_idx)].width = 22
                        any_content = True
                else:
                    text = page.extract_text() or ""
                    lines = [ln for ln in text.splitlines() if ln.strip()]
                    if lines:
                        ws = wb.create_sheet(title=_safe_sheet_name(f"Page {page_num}"))
                        for line in lines:
                            ws.append([line])
                        ws.column_dimensions["A"].width = 100
                        any_content = True
    except ConversionError:
        raise
    except Exception as exc:
        raise ConversionError(
            "Could not read this PDF. It may be corrupted, password-protected, "
            "or a scanned image without extractable text."
        ) from exc

    if not any_content:
        raise ConversionError(
            "No text or tables could be found in this PDF -- it may be a scanned "
            "image. Try PDF OCR first (coming soon), or a text-based PDF."
        )

    wb.save(out_path)
    return out_path
