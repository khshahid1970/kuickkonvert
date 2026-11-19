"""Release 7 final fix (19 Nov 2026): R7-87 (+ spec section 9), R7-88, R7-89,
R7-90 a-j and R7-92 (internal linking P2). Run from the repo root:
    python -m pytest -q tests/test_release7_final_fix.py
"""
import html as _html
import json
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app as kk  # noqa: E402
import config  # noqa: E402


@pytest.fixture(scope="module")
def client():
    # Many page renders in one module; rate limits are not under test here.
    # The previous state is restored so later test modules see the normal limiter.
    was = kk.limiter.enabled
    kk.limiter.enabled = False
    yield kk.app.test_client()
    kk.limiter.enabled = was
    kk.limiter.reset()


def _get(client, path):
    r = client.get(path)
    assert r.status_code == 200, path
    return r.data.decode()


def _visible(html):
    body = re.search(r"<body.*?</body>", html, re.S).group(0)
    body = re.sub(r"<(script|style)\b.*?</\1>", " ", body, flags=re.S)
    return _html.unescape(re.sub(r"<[^>]+>", " ", body))


def _h1s(html):
    return [_html.unescape(re.sub(r"<[^>]+>", "", h)).strip()
            for h in re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S)]


def _title(html):
    return _html.unescape(re.search(r"<title>(.*?)</title>", html, re.S).group(1)).strip()


def _meta(html):
    return _html.unescape(re.search(r'name="description" content="(.*?)"', html, re.S).group(1))


# ---- R7-87 ------------------------------------------------------------------
PHRASES = {
    "/tools/png-to-jpg": ["Convert PNG to JPG (JPEG) online for free", "How to convert PNG to JPG",
                          "Can I convert PNG to JPG without losing quality?",
                          "Almost, on photos: images are saved at quality 90"],
    "/tools/protect-pdf": ["Password protect a PDF online for free", "How does Protect PDF encrypt the PDF?",
                           "With 256-bit AES encryption"],
    "/tools/compress-pdf": ["Can I compress a PDF to 100 KB, 200 KB, 500 KB or 1 MB?",
                            "a 3.2 MB PDF holding one photo came out at 50 KB on Screen and 127 KB on Ebook",
                            "If your PDF was made from phone photos, Compress PDF may not shrink it at all"],
    "/tools/merge-pdf": ["can also join PDF files"],
    "/tools/pdf-to-ppt": ["PowerPoint (PPTX) file", "Is this PDF to PPTX or PDF to PPT?"],
    "/tools/split-pdf": ["separates PDF pages into individual files",
                         "How do I separate PDF pages into separate files?"],
    "/tools/pdf-to-excel": ["PDF to Excel (PDF to XLSX)"],
    "/tools/heic-to-jpg": ["HEIC to JPG is a free HEIC converter", "ordinary JPG (JPEG) files"],
    "/tools/webp-to-jpg": ["ordinary JPG (JPEG) files"],
    "/tools/pdf-to-jpg": ["its own JPG (JPEG) image"],
    "/tools/jpg-to-pdf": ["a single JPG (JPEG) photo"],
}
H1 = {
    "/tools/protect-pdf": "Password Protect PDF - Lock PDF Files with a Password",
    "/tools/split-pdf": "Split PDF - Separate PDF Pages into Single Files",
    "/tools/pdf-to-ppt": "PDF to PPT Converter - PDF to PowerPoint (PPTX)",
    "/tools/pdf-to-excel": "PDF to Excel Converter - PDF to XLSX",
    "/tools/png-to-jpg": "PNG to JPG - Convert PNG Images to JPG",
}


def test_r7_87_phrases_present(client):
    for path, phrases in PHRASES.items():
        text = _visible(_get(client, path))
        for p in phrases:
            assert p in text, (path, p)


def test_r7_87_h1_titles_meta(client):
    for path, h1 in H1.items():
        html = _get(client, path)
        assert _h1s(html) == [h1], path
    protect = _get(client, "/tools/protect-pdf")
    assert _title(protect) == "Password Protect PDF Online Free - Lock PDF | KuickKonvert"
    assert "PNG to JPG" in _title(_get(client, "/tools/png-to-jpg"))
    assert config.TOOLS_BY_SLUG["png-to-jpg"]["seo_title"] == _title(_get(client, "/tools/png-to-jpg"))
    for t in config.TOOLS:
        html = _get(client, f"/tools/{t['slug']}")
        assert len(_title(html)) <= 60, t["slug"]
        assert 110 <= len(_meta(html)) <= 160, (t["slug"], len(_meta(html)))
        assert len(_h1s(html)) == 1, t["slug"]
    assert "join PDFs" in _meta(_get(client, "/tools/merge-pdf"))
    assert "PDF to PPTX" in _meta(_get(client, "/tools/pdf-to-ppt"))


def test_r7_87_png_to_jpg_title_frozen():
    # Q5: the PNG to JPG title is not changed by R7-87.
    assert config.TOOLS_BY_SLUG["png-to-jpg"]["seo_title"].startswith("PNG to JPG")


def test_r7_87_pdf_to_ppt_really_outputs_pptx():
    src = Path(kk.__file__).resolve().parent.joinpath("converters").glob("*.py")
    assert any(".pptx" in p.read_text() for p in src)


# ---- R7-88 ------------------------------------------------------------------
def test_r7_88_server_wording(client):
    home = _visible(_get(client, "/"))
    assert "Your file is uploaded, converted on our server and deleted automatically after conversion." in home
    assert "directly from your browser" not in home
    webp = _visible(_get(client, "/tools/webp-to-jpg"))
    assert "they're converted on our server" in webp
    split = _get(client, "/guides/how-to-split-pdf-files")
    assert "Split a PDF online, in any browser" in split and "Split a PDF in your browser" not in split
    for path in ["/"] + [f"/tools/{t['slug']}" for t in config.TOOLS] + [f"/guides/{g['slug']}" for g in config.GUIDES]:
        text = _visible(_get(client, path)).lower()
        for bad in ("client-side", "no upload", "without uploading", "never leaves your device"):
            assert bad not in text, (path, bad)


# ---- R7-89 ------------------------------------------------------------------
def test_r7_89_form_size_table(client):
    html = _get(client, "/guides/photos-to-one-pdf-jpg-to-pdf-tips")
    text = _visible(html)
    assert "Meeting a form's size limit (100 KB, 200 KB or 500 KB)" in text
    for row in ("253 KB / 254 KB", "134 KB / 135 KB", "87 KB / 89 KB", "55 KB / 56 KB"):
        assert row in text
    assert "three pages at 1,200 pixels came to 404 KB" in text
    assert "at 800 pixels it was only just readable" in text
    order = [h for h in re.findall(r"<h2>(.*?)</h2>", html)]
    i = order.index("The reliable fix: resize the photos first")
    assert _html.unescape(order[i + 1]) == "Meeting a form's size limit (100 KB, 200 KB or 500 KB)"


# ---- R7-90 ------------------------------------------------------------------
def test_r7_90_brand_entity(client):
    home = _get(client, "/")
    hero = re.search(r'<p class="hero-sub">(.*?)</p>', home, re.S).group(1)
    assert hero.startswith("KuickKonvert is a free online file converter that turns")
    about = _visible(_get(client, "/about"))
    assert "Kuick + Konvert" in about and "spelled with two Ks" in about
    assert 'class="footer-tagline">KuickKonvert: free online tools' in home
    org = [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', home, re.S)]
    org = [o for o in org if o.get("@type") == "Organization"][0]
    assert org["founder"] == {"@id": kk.SITE_URL + "/about#shahid-iqbal"}
    assert org["foundingDate"] == "2026-08"
    assert "https://www.facebook.com/kuickkonvert/" in org["sameAs"]
    assert "https://peerlist.io/kuickkonvert/project/kuickkonvert" in org["sameAs"]
    about_html = _get(client, "/about")
    person = [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', about_html, re.S)]
    assert any(p.get("@id") == org["founder"]["@id"] for p in person)


def test_r7_90_links_and_copy(client):
    root = Path(kk.__file__).resolve().parent
    for p in list(root.joinpath("templates").glob("*.html")) + [root / "README.md"]:
        s = p.read_text()
        assert "profile.php?id=61594014512417" not in s, p.name
        assert "peerlist.io/kuickkonvert/project/kuick-konvert" not in s, p.name
        assert "nxgntools.com/tools/shahid-iqbal" not in s, p.name
    assert "Private by design" not in (root / "README.md").read_text()
    home = _visible(_get(client, "/"))
    for bad in ("built to be fast", "Fast conversions", "keep conversions fast", "Fast, free, private", "100% free"):
        assert bad not in home, bad
    assert "keep conversions fast" not in _visible(_get(client, "/about"))


# ---- R7-92 ------------------------------------------------------------------
def test_r7_92_internal_links(client):
    home = _get(client, "/")
    teaser = re.search(r'<ul class="guides-teaser-list">(.*?)</ul>', home, re.S).group(1)
    first3 = re.findall(r'href="/guides/([a-z0-9-]+)"', teaser)[:3]
    assert first3 == list(config.HOME_PILLAR_GUIDES)
    tools = _get(client, "/tools")
    for slug in config.HOME_PILLAR_GUIDES:
        assert f'href="/guides/{slug}"' in tools, slug
    doc = _get(client, "/guides/docx-vs-doc")
    for href in ("/tools/excel-to-pdf", "/tools/pdf-to-excel", "/tools/ppt-to-pdf", "/tools/pdf-to-ppt",
                 "/guides/xls-vs-xlsx", "/guides/ppt-vs-pptx"):
        assert f'href="{href}"' in doc, href
    comp = _get(client, "/guides/pdf-compression-levels-explained")
    for t in ("merge-pdf", "split-pdf", "rotate-pdf", "watermark-pdf", "protect-pdf"):
        assert f'href="/tools/{t}"' in comp, t
    for g in config.GUIDES:
        html = _get(client, f"/guides/{g['slug']}")
        dek = re.search(r'<p class="tool-page-desc">(.*?)</p>', html, re.S).group(1)
        assert 'href="/tools/' in dek, g["slug"]


def test_r7_92_guide_not_added_to_other_tool_pages():
    # L14 is body text only: the compression guide stays off Rotate/Watermark/Protect.
    for t in ("rotate-pdf", "watermark-pdf", "protect-pdf"):
        assert all(g["slug"] != "pdf-compression-levels-explained" for g in config.GUIDES_BY_TOOL.get(t, []))


# ---- Release date ------------------------------------------------------------
def test_release_date_consistent(client):
    from datetime import date
    d = date.fromisoformat(config.RELEASE7_DATE)
    privacy = _visible(_get(client, "/privacy"))
    assert f"Last updated: {d.day} {d.strftime('%B %Y')}" in privacy
