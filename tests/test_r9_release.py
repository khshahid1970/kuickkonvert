"""Release 9 (21 Nov 2026): C1 image-tool pages and R9-08 priority pages (steps per device, fixes),
R9-09 Limits row, R9-10 llms.txt limits line, C3 guide how-to sections."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app as kk  # noqa: E402
import config  # noqa: E402

IMAGE_TOOLS = ["png-to-pdf", "pdf-to-png", "png-to-jpg", "jpg-to-png", "webp-to-jpg", "heic-to-jpg"]
TOOLS = IMAGE_TOOLS + list(config.R9_PRIORITY_TOOLS)
BANNED = ["secure", "security", "100%", "unlimited", "no limits", "fast", "faster", "fastest", "best",
          "guaranteed", "instantly", "private by design", "in your browser", "ocr"]
COPILOT_CITED = ("docx-vs-doc", "jpg-vs-png", "why-pdf-layout-shifts",
                 "pdf-to-excel-table-conversion-results", "ppt-vs-pptx", "pdf-compression-levels-explained")


def _get(path):
    r = kk.app.test_client().get(path)
    assert r.status_code == 200, path
    return r.data.decode()


def _visible(html):
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


def _banned(text):
    low = text.lower()
    # "OCR" may appear only to say KuickKonvert doesn't do it (no OCR claim).
    for ok in ("doesn't do ocr", "no ocr", "free ocr option"):
        low = low.replace(ok, " ")
    return [w for w in BANNED if re.search(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", low)]


def test_tool_pages_show_device_steps_and_fixes():
    sm = _get("/sitemap.xml")
    for slug in TOOLS:
        t = config.TOOLS_BY_SLUG[slug]
        html = _get(f"/tools/{slug}")
        assert f"<h2>{t['device_steps']['heading']}</h2>" in html, slug
        for label, steps in t["device_steps"]["devices"]:
            assert f"<h3>{label}</h3>" in html and len(steps) == 3, slug
        assert f"<h2>{t['troubleshooting']['heading']}</h2>" in html, slug
        assert len(t["troubleshooting"]["fixes"]) >= 4, slug
        assert f"/tools/{slug}</loc><lastmod>{config.R9_DATE}</lastmod>" in sm, slug


def _upd(slug):
    return config._R9_TOOL_UPDATES.get(slug) or config._R9_PRIORITY_UPDATES[slug]


def test_tool_page_copy_rules_and_measured_fact():
    for slug in TOOLS:
        t = config.TOOLS_BY_SLUG[slug]
        blob = " ".join([s for _, steps in t["device_steps"]["devices"] for s in steps] +
                        [t["device_steps"].get("note") or ""] +
                        [p + " " + f for p, f in t["troubleshooting"]["fixes"]] +
                        [q + " " + a for q, a in _upd(slug).get("faq_add", []) + _upd(slug).get("faq_replace", [])])
        assert not _banned(blob), (slug, _banned(blob))
        assert re.search(r"our test \((September|October|November) 2026\)", blob), slug   # a result from our own tests


def test_tool_page_numbers_match_test_results():
    # Spot checks against r9-test-results.json (21 Nov 2026).
    f = lambda s: " ".join(p + " " + x for p, x in config.TOOLS_BY_SLUG[s]["troubleshooting"]["fixes"]) + \
        " ".join(a for _, a in config.TOOLS_BY_SLUG[s]["faq"])
    assert "580 KB" in f("png-to-pdf") and "583 KB" in f("png-to-pdf") and "20 x 11.25" in f("png-to-pdf")
    assert "607, 636 and 410 KB" in f("pdf-to-png") and "2,550 x 3,300" in f("pdf-to-png")
    assert "116 KB" in f("png-to-jpg") and "294 KB" in f("png-to-jpg") and "1,587 KB" in f("png-to-jpg")
    assert "1,762 KB" in f("jpg-to-png") and "10,652 KB" in f("jpg-to-png")
    assert "608 KB" in f("webp-to-jpg") and "1,328 KB" in f("webp-to-jpg")
    assert "3024 x 4032" in f("heic-to-jpg") and "no GPS data" in f("heic-to-jpg")


def test_guides_have_how_to_sections():
    for slug in config.R9_UPDATED_GUIDES:
        g = config.GUIDES_BY_SLUG[slug]
        secs = [s for s in g["sections"] if s["heading"].lower().startswith("how to")]
        assert secs and secs[-1].get("steps"), slug
        sec = secs[-1]
        text = " ".join(sec.get("paragraphs", []) + sec["steps"])
        assert "November 2026" in text, slug                      # one result from our own tests
        assert not _banned(text), (slug, _banned(text))
        html = _get(f"/guides/{slug}")
        assert f"<h2>{sec['heading']}</h2>" in html, slug
        assert f'Updated <time datetime="{config.R9_DATE}"' in html, slug
        assert "[[" not in _visible(html), slug                  # tool links rendered


def test_guide_sources_and_no_duplicate_pages():
    assert len(config.GUIDES) == 30                              # updated, not duplicated
    for slug in ("word-to-pdf-what-carries-over", "photos-to-one-pdf-jpg-to-pdf-tips"):
        html = _get(f"/guides/{slug}")
        assert "<h2>Official sources</h2>" in html
        for _, url in config.GUIDES_BY_SLUG[slug]["sources"]:
            assert url.startswith("https://") and f'href="{url}"' in html, (slug, url)


def test_copilot_cited_guides_untouched():
    for slug in COPILOT_CITED:
        assert config.GUIDES_BY_SLUG[slug].get("updated") not in (config.R8_DATE, config.R9_DATE), slug
        assert slug not in config.R9_UPDATED_GUIDES


def test_priority_page_numbers_match_published_results():
    f = lambda s: " ".join(p + " " + x for p, x in config.TOOLS_BY_SLUG[s]["troubleshooting"]["fixes"]) + \
        " ".join(a for _, a in config.TOOLS_BY_SLUG[s]["faq"])
    assert "41 paragraphs" in f("pdf-to-word") and "37 KB" in f("pdf-to-word")
    assert "892 words" in f("word-to-pdf") and "5,510 KB" in f("word-to-pdf") and "544 KB" in f("word-to-pdf")
    assert "24,230 KB" in f("jpg-to-pdf") and "134 KB" in f("jpg-to-pdf") and "5,456 KB" in f("jpg-to-pdf")
    assert "column A" in f("pdf-to-excel") and "all 5 columns" in f("pdf-to-excel")
    assert "3.6 pt" in f("excel-to-pdf") and "9.3 pt" in f("excel-to-pdf") and "24 formulas" in f("excel-to-pdf")
    assert "4-page PDF" in f("ppt-to-pdf") and "20.5 KB" in f("ppt-to-pdf")
    assert "50 KB" in f("compress-pdf") and "5,456 KB" in f("compress-pdf")
    assert "6 pages" in f("merge-pdf") and "3 bookmarks" in f("merge-pdf")


def test_limits_row_on_every_tool_page():
    sm = _get("/sitemap.xml")
    for t in config.TOOLS:
        html = _get(f"/tools/{t['slug']}")
        assert t.get("limits"), t["slug"]
        assert '<th scope="row">Limits</th>' in html, t["slug"]
        assert not _banned(t["limits"]), t["slug"]
        assert f"/tools/{t['slug']}</loc><lastmod>{config.R9_DATE}</lastmod>" in sm, t["slug"]
    lim = config.R9_TOOL_LIMITS
    assert "20 images" in lim["heic-to-jpg"] and "65 megapixels" in lim["png-to-jpg"]
    assert "50 pages" in lim["pdf-to-jpg"] and "50 pages" in lim["pdf-to-ppt"]
    assert "200 pages" in lim["pdf-to-word"] and "200 pages" in lim["pdf-to-excel"]
    assert "120 characters" in lim["watermark-pdf"] and "4 characters" in lim["protect-pdf"]


def test_limits_match_code_constants():
    from converters.images import MAX_IMAGE_MEGAPIXELS, MAX_RENDER_PAGES, MAX_IMAGE_OUTPUT_MB
    from converters.pdf_tools import MAX_WORD_PAGES, MAX_EXCEL_PAGES, MAX_WORD_SCANNED_PAGES
    assert (kk.MAX_IMAGES_PER_CONVERSION, MAX_IMAGE_MEGAPIXELS, MAX_IMAGE_OUTPUT_MB) == (20, 65, 150)
    assert (MAX_RENDER_PAGES, MAX_WORD_PAGES, MAX_EXCEL_PAGES, MAX_WORD_SCANNED_PAGES) == (50, 200, 200, 10)


def test_llms_txt_limits_line():
    body = _get("/llms.txt")
    assert "- Limits: up to 20 images at a time in the image converters, each up to 65 megapixels; " \
           "PDF to JPG, PDF to PNG and PDF to PPT convert up to 50 pages at a time; " \
           "PDF to Word and PDF to Excel up to 200 pages; password-protected PDFs must be unlocked first." in body
