"""Release 7, WP14 (conversion-failure Package 2) server-side checks, 11 Nov 2026.

Run from the repo root:  python -m pytest -q tests/test_release7_package2.py
Browser behaviour (retries, Download again, repeat refusals, image reduction)
is covered by tests/test_release7_package2_browser.js.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app as kk  # noqa: E402
from converters import pdf_tools  # noqa: E402

client = kk.app.test_client()


def test_named_codes_r7_65():
    cases = {
        "Conversion finished but produced no output file.": "office_failed",
        "Please upload a .doc or .docx file.": "wrong_type",
        "Could not compress this PDF: broken xref": "compress_failed",
        "Could not build a PDF from these images: bad data": "images_pdf_failed",
        pdf_tools.LOCKED_PDF_MESSAGE.format(name="'x'"): "pdf_locked",
        pdf_tools.DAMAGED_PDF_MESSAGE.format(name="'x'"): "pdf_damaged",
    }
    for msg, code in cases.items():
        assert kk._error_code(msg) == code, msg


def test_no_known_message_falls_to_other_400():
    # Every ConversionError text written in the code maps to a named code.
    import glob
    root = Path(__file__).resolve().parents[1]
    texts = []
    for f in glob.glob(str(root / "converters" / "*.py")) + [str(root / "app.py")]:
        s = open(f, encoding="utf-8").read()
        for m in re.finditer(r'ConversionError\(\s*((?:f?"[^"]*"\s*)+)', s):
            texts.append("".join(re.findall(r'"([^"]*)"', m.group(1))))
    texts += [pdf_tools.LOCKED_PDF_MESSAGE, pdf_tools.DAMAGED_PDF_MESSAGE,
              pdf_tools.RESTRICTED_MERGE_MESSAGE]
    left = [t for t in texts if kk._error_code(t) == "other_400" and len(t) > 3]
    assert not left, left


def _form(html):
    return re.search(r'<form id="convert-form"(.*?)>', html, re.S).group(1)


def test_upload_notes_r7_62():
    for slug in ("pdf-to-word", "pdf-to-excel", "pdf-to-ppt"):
        html = client.get(f"/tools/{slug}").data.decode()
        assert 'id="upload-note"' in html and "password-protected" in html, slug
        assert 'aria-describedby="upload-limits upload-note"' in html, slug
    for slug in ("jpg-to-pdf", "merge-pdf", "watermark-pdf"):
        html = client.get(f"/tools/{slug}").data.decode()
        assert 'id="upload-note"' not in html, slug
    # never an OCR claim
    for slug in ("pdf-to-word", "pdf-to-excel"):
        import html as _h
        page = _h.unescape(client.get(f"/tools/{slug}").data.decode())
        assert "doesn't do OCR" in page


def test_pixel_limit_attribute_r7_64():
    for slug in ("jpg-to-pdf", "png-to-pdf", "png-to-jpg", "jpg-to-png", "webp-to-jpg"):
        html = client.get(f"/tools/{slug}").data.decode()
        assert f'data-max-mp="{kk.MAX_IMAGE_MEGAPIXELS}"' in _form(html), slug
    for slug in ("heic-to-jpg", "pdf-to-word", "merge-pdf"):
        html = client.get(f"/tools/{slug}").data.decode()
        assert 'data-max-mp="0"' in _form(html), slug
