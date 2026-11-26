"""Release 10 (commit 1, prepared 25 Nov 2026): R-2 tracking flag, security.txt, sitemap
entries, author page identity, /guides dek links, phone upload row (CSS) and README Docker."""
import os
import re
import sys
from pathlib import Path
import html as _h

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import app as kk  # noqa: E402
import config  # noqa: E402

TRACKING = re.compile(
    r"G-K0VJLC113K|AW-18473004328|ca-pub-2468332370767807|googletagmanager\.com|"
    r"adsbygoogle|js/consent\.js|id=\"consent-banner\"|id=\"cookie-settings\"|launchnest\.io/badge"
)
PAGES = ["/", "/tools/word-to-pdf", "/guides", "/guides/docx-vs-doc", "/about", "/privacy"]
HEADERS = [{"CF-IPCountry": "US"}, {"CF-IPCountry": "DE"}, {"CF-IPCountry": "US", "Sec-GPC": "1"}]


# ---- R-2: KuickKonvert tracking only on the official site -------------------------------
@pytest.mark.parametrize("path", PAGES)
def test_self_hosted_copy_has_no_kk_tracking(path, monkeypatch):
    monkeypatch.delenv("KK_OFFICIAL_SITE", raising=False)
    client = kk.app.test_client()
    for hdr in HEADERS:
        r = client.get(path, headers=hdr)
        assert r.status_code == 200, (path, hdr)
        found = set(TRACKING.findall(r.data.decode()))
        assert not found, (path, hdr, found)


def test_self_hosted_copy_has_no_ads_txt(monkeypatch):
    monkeypatch.delenv("KK_OFFICIAL_SITE", raising=False)
    assert kk.app.test_client().get("/ads.txt").status_code == 404


@pytest.mark.parametrize("value", ["0", "", "yes", "true"])
def test_only_exact_1_switches_tracking_on(value, monkeypatch):
    monkeypatch.setenv("KK_OFFICIAL_SITE", value)
    html = kk.app.test_client().get("/", headers={"CF-IPCountry": "US"}).data.decode()
    assert "G-K0VJLC113K" not in html


def test_official_site_keeps_tracking(monkeypatch):
    monkeypatch.setenv("KK_OFFICIAL_SITE", "1")
    client = kk.app.test_client()
    us = client.get("/", headers={"CF-IPCountry": "US"}).data.decode()
    assert "gtag('config', 'G-K0VJLC113K')" in us and "AW-18473004328" in us
    assert 'name="google-adsense-account" content="ca-pub-2468332370767807"' in us
    de = client.get("/", headers={"CF-IPCountry": "DE"}).data.decode()
    assert "js/consent.js" in de and 'id="consent-banner"' in de and 'id="cookie-settings"' in de
    ads = client.get("/ads.txt")
    assert ads.status_code == 200 and "pub-2468332370767807, DIRECT" in ads.data.decode()


# ---- F10-27: security.txt ----------------------------------------------------------------
def test_security_txt(monkeypatch):
    monkeypatch.setenv("KK_OFFICIAL_SITE", "1")
    r = kk.app.test_client().get("/.well-known/security.txt")
    assert r.status_code == 200 and r.mimetype == "text/plain"
    body = r.data.decode()
    assert "Contact: mailto:info@kuickkonvert.com\n" in body
    assert "Preferred-Languages: en\n" in body
    assert "Canonical: https://kuickkonvert.com/.well-known/security.txt\n" in body
    exp = re.search(r"^Expires: (\d{4}-\d{2}-\d{2})T\d{2}:\d{2}:\d{2}Z$", body, re.M).group(1)
    from datetime import date, timedelta
    import config
    release = date.fromisoformat(config.RELEASE10_DATE)
    assert release < date.fromisoformat(exp) <= release + timedelta(days=365)
    sm = kk.app.test_client().get("/sitemap.xml").data.decode()
    assert "security.txt" not in sm
    monkeypatch.delenv("KK_OFFICIAL_SITE")
    assert kk.app.test_client().get("/.well-known/security.txt").status_code == 404


# ---- F10-53: sitemap entries for the 2 new pages -----------------------------------------
def test_sitemap_has_61_urls_with_new_pages():
    import config
    client = kk.app.test_client()
    sm = client.get("/sitemap.xml").data.decode()
    locs = re.findall(r"<loc>(.*?)</loc>", sm)
    assert len(locs) == len(set(locs)) == 61
    for path in ("/how-we-test", "/about/shahid-iqbal"):
        assert f"<loc>https://kuickkonvert.com{path}</loc><lastmod>{config.RELEASE10_DATE}</lastmod>" in sm
        html = client.get(path).data.decode()
        assert f'<link rel="canonical" href="https://kuickkonvert.com{path}">' in html


# ---- F10-54: one Person @id site-wide; byline links to the author page -------------------
def test_one_person_id_and_author_links():
    client = kk.app.test_client()
    pid = "https://kuickkonvert.com/about/shahid-iqbal"
    for path in ("/", "/about", "/about/shahid-iqbal", "/guides/docx-vs-doc", "/tools/merge-pdf"):
        html = client.get(path).data.decode()
        assert "about#shahid-iqbal" not in html, path
    guide = client.get("/guides/docx-vs-doc").data.decode()
    assert f'"author": {{"@type": "Person", "@id": "{pid}"' in guide
    assert re.search(r'<div class="guide-meta">\s*By <a href="/about/shahid-iqbal">Shahid Iqbal</a>', guide)
    author = client.get("/about/shahid-iqbal").data.decode()
    assert f'"@id": "{pid}"' in author and '"jobTitle": "Founder"' in author


# ---- F10-20: no raw [[slug|text]] codes on /guides ---------------------------------------
def test_guides_list_has_no_raw_link_codes():
    html = kk.app.test_client().get("/guides").data.decode()
    assert "[[" not in html and "]]" not in html


# ---- F10-41: phone upload row (option D); desktop rules untouched -----------------------
def test_phone_upload_row_css():
    css = (ROOT / "static/css/style.css").read_text(encoding="utf-8")
    block = css[css.index("@media (max-width: 600px) and (pointer: coarse) {\n  .ad-slot--tool"):]
    assert ".dropzone .dropzone-icon { display: none; }" in block
    assert "grid-template-columns: 1fr auto;" in block
    assert ".dropzone #file-input-label { grid-column: 2; margin: 0; }" in block
    assert ".ad-slot--tool { margin: 20px 0 28px; min-height: 90px; }" in css  # desktop unchanged
    served = kk.app.test_client().get("/static/css/style.css").data.decode()
    assert "@media (max-width:600px) and (pointer:coarse)" in served or "(pointer: coarse)" in served


# ---- R-1: README Docker section ----------------------------------------------------------
def test_readme_docker_section():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "## Run with Docker" in readme
    assert readme.index("## Run with Docker") < readme.index("## Privacy")
    assert "docker run -d --name kuickkonvert -p 8080:8080 kuickkonvert" in readme
    assert "Poppler and pypdfium2" not in readme and "KK_OFFICIAL_SITE" in readme


# ---- F10-11: curly apostrophes and dashes in page text -----------------------------------
def test_typography_in_page_text():
    import html as _html
    client = kk.app.test_client()
    sm = client.get("/sitemap.xml").data.decode()
    frozen = {g["title"] for g in kk.GUIDES}  # guide titles are frozen (shown in links too)
    for loc in re.findall(r"<loc>https://kuickkonvert.com(.*?)</loc>", sm):
        if loc in ("/privacy", "/terms"):
            continue  # legal text: typography changes need the adviser
        page = client.get(loc or "/").data.decode()
        main = re.search(r"<main.*?</main>", page, re.S).group(0)
        main = re.sub(r"<script.*?</script>|<h1.*?</h1>", " ", main, flags=re.S)
        text = _html.unescape(re.sub(r"<[^>]+>", " ", main))
        for t in frozen:
            text = text.replace(t, " ")
        assert " -- " not in text, loc
        # /about: the counsel-approved open-source sentence is used verbatim.
        text = text.replace("KuickKonvert's underlying application source code", " ")
        left = re.findall(r".{0,30}[A-Za-z]'[A-Za-z].{0,10}", text)
        assert not left, (loc, left[:3])


# ---- NEW-1 /how-we-test (approved 25 Nov 2026, review copy part 2) ------------------------
def test_how_we_test_page():
    import config
    html = kk.app.test_client().get("/how-we-test").data.decode()
    main = re.search(r"<main.*?</main>", html, re.S).group(0)
    assert main.count("<tr><th scope=\"row\">") == 9
    for doi in ("10.5281/zenodo.24199944", "10.5281/zenodo.24324333"):
        assert f'href="https://doi.org/{doi}"' in main
    assert len(re.findall(r"<h2>[^<]*\?</h2>", main)) >= 2
    d = config.RELEASE10_DATE
    assert f'<time datetime="{d}">' in main
    text = re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", " ", main, flags=re.S)).lower()
    for w in ("secure", "fast", "best", "100%", "unlimited", "guaranteed", "instantly", "in your browser"):
        assert not re.search(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", text), w
    assert len(text.split()) >= 550


# ---- Part 3 fact fixes (built 25 Nov 2026, review copy part 3) ----------------------------
def test_part3_fact_fixes():
    client = kk.app.test_client()
    p10 = client.get("/tools/pdf-to-word").data.decode()
    assert p10.count("Scanned PDFs of up to 10 pages are accepted, but they come out as pictures, not editable text (no OCR).") == 2  # upload note + FAQ
    assert "scanned PDFs whose pages are pictures of text" not in p10
    contact = client.get("/contact").data.decode()
    assert "HEIC to JPG, WEBP to JPG, PNG to JPG and JPG to PNG take up to 20 images at a time" in contact
    assert "PDF to Word and PDF to Excel convert up to 200 pages" in contact
    assert "Up to 50 MB per upload</td>" in client.get("/tools/word-to-pdf").data.decode()
    assert "Up to 50 MB per upload (all files together)</td>" in client.get("/tools/merge-pdf").data.decode()
    assert 'maxlength="120"' in client.get("/tools/watermark-pdf").data.decode()
    assert 'alt="KuickKonvert on LaunchNest"' in client.get("/", headers={"CF-IPCountry": "US"}).data.decode()
    for path in ("/tools/protect-pdf", "/guides/pdf-password-protection-explained", "/guides/why-pdf-layout-shifts"):
        assert "Adobe" not in client.get(path).data.decode(), path
    assert "download is ready" not in (ROOT / "config.py").read_text(encoding="utf-8")


# ---- D1 (approved 25 Nov 2026): tighter gaps on phones, tool pages only ------------------
def test_d1_phone_spacing_tool_pages_only():
    css = (ROOT / "static/css/style.css").read_text(encoding="utf-8")
    assert ".tool-page--tool { padding-top: 16px; }" in css
    assert ".tool-page--tool .dropzone { padding: 10px 16px; }" in css
    client = kk.app.test_client()
    assert '<section class="tool-page tool-page--tool">' in client.get("/tools/split-pdf").data.decode()
    assert "tool-page--tool" not in client.get("/guides/docx-vs-doc").data.decode()


# ---- F10-28 (approved 26 Nov 2026): no 'unsafe-eval' in the CSP ---------------------------
def test_csp_has_no_unsafe_eval():
    r = kk.app.test_client().get("/", headers={"CF-IPCountry": "US"})
    csp = r.headers.get("Content-Security-Policy", "")
    assert "script-src 'nonce-" in csp and "'strict-dynamic'" in csp
    assert "'unsafe-eval'" not in csp


# ---- F10-16 (approved 26 Nov 2026): home page shows the "All 21 tools" video -------------
def test_home_video_is_all_tools():
    html = kk.app.test_client().get("/", headers={"CF-IPCountry": "US"}).data.decode()
    assert "1E_AUIg4tZk" in html and "p8tYDhRRQHc" not in html
    assert "right in your browser" not in html


# ---- L1 (approved 26 Nov 2026): web links survive Office-to-PDF; remote resources do not --
FIX = ROOT / "tests" / "fixtures"


def _rels_after_strip(tmp_path):
    import shutil, zipfile
    from converters.office import strip_external_links
    p = tmp_path / "doc.docx"
    shutil.copy(FIX / "r10-link-and-remote-image.docx", p)
    strip_external_links(str(p))
    return zipfile.ZipFile(p).read("word/_rels/document.xml.rels").decode()


def test_strip_keeps_web_links_and_removes_remote_resources(tmp_path):
    rels = _rels_after_strip(tmp_path)
    assert 'Target="https://kuickkonvert.com/"' in rels                  # web link kept
    assert "169.254.169.254" not in rels and "example.invalid" not in rels  # remote image, template removed


def _link_count(pdf_bytes):
    import io, pikepdf
    pdf = pikepdf.open(io.BytesIO(pdf_bytes))
    uris = []
    for page in pdf.pages:
        for a in page.obj.get("/Annots") or []:
            act = a.get("/A")
            if act is not None and act.get("/URI") is not None:
                uris.append(str(act.get("/URI")))
    return uris


@pytest.mark.parametrize("slug,fixture", [("word-to-pdf", "r10-link-and-remote-image.docx"),
                                          ("ppt-to-pdf", "r10-link-textbox.pptx")])
def test_web_link_still_clickable_in_pdf(slug, fixture):
    import shutil
    if not shutil.which("soffice"):
        pytest.skip("LibreOffice not installed")
    was = kk.limiter.enabled
    kk.limiter.enabled = False
    try:
        with open(FIX / fixture, "rb") as fh:
            r = kk.app.test_client().post(f"/convert/{slug}", data={"file": (fh, fixture)},
                                          content_type="multipart/form-data")
    finally:
        kk.limiter.enabled = was
    assert r.status_code == 200, r.data[:200]
    assert "https://kuickkonvert.com/" in _link_count(r.data)


# ---- Privacy Notice section 1 (adviser's wording, 26 Nov 2026): file lifecycle checks ----
def _job_dirs():
    import re as _re
    from converters.utils import BASE_TMP_DIR
    return {n for n in os.listdir(BASE_TMP_DIR) if _re.fullmatch(r"[0-9a-f]{32}", n)}


def _post(slug, path, name, **form):
    was = kk.limiter.enabled
    kk.limiter.enabled = False
    try:
        with open(path, "rb") as fh:
            data = dict(form, file=(fh, name))
            return kk.app.test_client().post(f"/convert/{slug}", data=data, content_type="multipart/form-data")
    finally:
        kk.limiter.enabled = was


def test_workspace_deleted_before_result_is_sent(monkeypatch):
    import converters.utils as cu
    seen = {}
    real_ws = cu.job_workspace

    from contextlib import contextmanager

    @contextmanager
    def spy_ws():
        with real_ws() as p:
            seen["path"] = p
            yield p

    real_send = kk.send_file

    def spy_send(*a, **k):
        seen["exists_at_send"] = os.path.exists(seen["path"])
        return real_send(*a, **k)

    monkeypatch.setattr(kk, "job_workspace", spy_ws)
    monkeypatch.setattr(kk, "send_file", spy_send)
    before = _job_dirs()
    r = _post("rotate-pdf", FIX / "r10-text.pdf",
              "t.pdf", degrees="90")
    assert r.status_code == 200 and len(r.data) > 0
    assert seen["exists_at_send"] is False          # workspace gone before the result is sent
    assert _job_dirs() == before                    # nothing left behind


def test_workspace_deleted_when_conversion_fails(tmp_path):
    bad = tmp_path / "bad.pdf"
    bad.write_bytes(b"not a pdf at all")
    before = _job_dirs()
    r = _post("rotate-pdf", bad, "bad.pdf", degrees="90")
    assert r.status_code == 400
    assert _job_dirs() == before


def test_abandoned_workspace_removed_by_cleanup():
    import time as _t, uuid
    from converters.utils import BASE_TMP_DIR, sweep_stale_temp
    old = os.path.join(BASE_TMP_DIR, uuid.uuid4().hex)
    new = os.path.join(BASE_TMP_DIR, uuid.uuid4().hex)
    for p in (old, new):
        os.makedirs(p)
        open(os.path.join(p, "left.pdf"), "wb").write(b"x")
    past = _t.time() - 3600
    os.utime(old, (past, past))
    try:
        sweep_stale_temp(max_age_seconds=1800)
        assert not os.path.exists(old)     # left by an interrupted conversion -> cleaned up
        assert os.path.exists(new)         # a conversion still running is not touched
    finally:
        import shutil
        shutil.rmtree(new, ignore_errors=True)


def test_timed_background_cleanup_removes_abandoned_workspace():
    """R10 option 2: a timer thread runs clean-up every 5 minutes, with no request needed."""
    import time as _t, uuid, shutil
    from converters.utils import BASE_TMP_DIR
    assert kk._TEMP_SWEEP_TIMER_SECONDS == 300
    assert kk._temp_sweep_thread is not None and kk._temp_sweep_thread.is_alive()
    assert kk._temp_sweep_thread.daemon
    old = os.path.join(BASE_TMP_DIR, uuid.uuid4().hex)
    new = os.path.join(BASE_TMP_DIR, uuid.uuid4().hex)
    for p in (old, new):
        os.makedirs(p)
    past = _t.time() - 1801
    os.utime(old, (past, past))
    slept = []
    try:
        kk._temp_sweep_timer_loop(300, sleep=slept.append, max_runs=1)
        assert slept == [300]
        assert not os.path.exists(old)   # older than 30 minutes -> removed by the timer
        assert os.path.exists(new)       # newer folder left alone
    finally:
        shutil.rmtree(new, ignore_errors=True)


# ---- Privacy Notice changes 1-8 (adviser-approved 26 Nov 2026) ---------------------------
def test_privacy_notice_release10_wording():
    import config
    html = kk.app.test_client().get("/privacy").data.decode()
    assert "<title>Privacy Notice | KuickKonvert</title>" in html
    assert "automatically deletes the temporary workspace before sending the result" in html
    assert "not intentionally retained by our application after the transfer completes or is terminated" in html
    assert "as described in section 1." in html
    assert "As shown in the table in section 6;" in html
    assert "The Personal Data Protection Bill, 2023 remains a legislative proposal" in html
    assert "Article 14(1) of the Constitution of the Islamic Republic of Pakistan" in html
    assert f"Last updated: {config.PRIVACY_UPDATED_TEXT}" in html
    # 30-minute clean-up sentence, option 1 (approved 26 Nov 2026); option 2 timer makes it hold
    assert "deletes it at the next automatic clean-up after it is more than 30 minutes old" in html
    assert "[Release 10 deploy date]" not in html and "returned to you" not in html
    nums = [int(n) for n in re.findall(r"<h2>(\d+)\. ", html)]
    assert nums == list(range(1, 23))


# ---- Part 4 (26 Nov 2026): tool pages ---------------------------------------------------
def _tool_main_text(html):
    """First paragraph + section.tool-info, without the parts kept identical on purpose
    (at-a-glance table, Privacy line, guide links, Official sources, Related tools)."""
    import html as _h, re
    desc = re.search(r'<p class="tool-page-desc">(.*?)</p>', html, re.S).group(1)
    info = re.search(r'<section class="tool-info">(.*?)</section>', html, re.S).group(1)
    for pat in (r'<h2>[^<]* at a glance</h2>\s*<table.*?</table>', r'<ul class="related-guides-list">.*?</ul>',
                r'<h2>Privacy</h2>\s*<p>.*?</p>', r'<h2>Official sources</h2>\s*<ul.*?</ul>',
                r'<h2>Related tools</h2>\s*<ul.*?</ul>'):
        info = re.sub(pat, ' ', info, flags=re.S)
    t = re.sub(r'<(p|li|h2|h3|tr|summary|caption)\b', r'\n<\1', desc + '\n' + info)
    t = re.sub(r'<(td|th)\b', r' | <\1', t)
    return _h.unescape(re.sub(r'<[^>]+>', '', t))


def _sentences(t):
    import re
    out = []
    for line in t.split('\n'):
        for s in re.split(r'(?<=[.!?])\s+', line.strip()):
            s = re.sub(r'\s+', ' ', s).strip(' |')
            if len(s.split()) >= 3:
                out.append(s)
    return out


def test_tool_pages_repeated_text_at_most_25_percent():
    """Approved target (26 Nov 2026): repeated template text <= 25% of each tool page's
    main content. A sentence is 'repeated' if it appears on 2 or more tool pages."""
    import collections
    c = kk.app.test_client()
    pages = {t["slug"]: _sentences(_tool_main_text(c.get(f"/tools/{t['slug']}").data.decode()))
             for t in config.TOOLS}
    cnt = collections.Counter(s for ss in pages.values() for s in set(ss))
    for slug, ss in pages.items():
        total = sum(len(s.split()) for s in ss)
        rep = sum(len(s.split()) for s in ss if cnt[s] > 1)
        assert rep / total <= 0.25, (slug, round(100 * rep / total, 1))


def test_tool_pages_byline_figure_tests_step2_sources():
    import re
    c = kk.app.test_client()
    sm = c.get("/sitemap.xml").data.decode()
    step2s = set()
    for t in config.TOOLS:
        slug = t["slug"]
        html = c.get(f"/tools/{slug}").data.decode()
        # F10-07/F10-34: byline, date = sitemap lastmod = release day
        assert (f'Last checked <time datetime="{config.RELEASE10_DATE}">{config.R10_DATE_TEXT}</time> by '
                f'<a href="/about/shahid-iqbal">Shahid Iqbal</a>') in html, slug
        assert '<a href="/how-we-test">How we test</a>' in html, slug
        assert f"/tools/{slug}</loc><lastmod>{config.RELEASE10_DATE}</lastmod>" in sm, slug
        # F10-29/F10-36: a dated, measured figure in the first paragraph
        desc = re.search(r'<p class="tool-page-desc">(.*?)</p>', html, re.S).group(1)
        assert "26 November 2026" in desc and re.search(r"\d+(\.\d+)? (KB|seconds|pixels)", desc), slug
        # F10-30/F10-35: at least 3 dated results in a table
        table = re.search(r"<h2>What did our .*? tests show\?</h2>.*?<tbody>(.*?)</tbody>", html, re.S)
        assert table and table.group(1).count("<tr>") >= 3, slug
        assert any(w.startswith("Live site: ") for _, _, w in t["r10_tests"]), slug     # R4 speed figure
        # point 5: a tool-specific step 2 with the measured time
        assert t["r10_step2"] in _h.unescape(html) and "seconds" in t["r10_step2"], slug
        step2s.add(t["r10_step2"])
        assert "usually takes a few seconds" not in html, slug
        # F10-33: two official sources, https only
        assert len(t["sources"]) >= 2 and all(u.startswith("https://") for _, u in t["sources"]), slug
        for _, u in t["sources"]:
            assert f'href="{_h.escape(u)}"' in html or f'href="{u}"' in html, (slug, u)
    assert len(step2s) == len(config.TOOLS)


def test_part4_fact_fixes():
    t = config.TOOLS_BY_SLUG
    # F10-05: the bullet-list note appears once on PDF to Word (in "good to know")
    blob = " ".join(q + a for q, a in t["pdf-to-word"]["faq"]) + " ".join(p + f for p, f in t["pdf-to-word"]["troubleshooting"]["fixes"])
    assert "bullet" not in blob.lower() and "Bulleted" in t["pdf-to-word"]["good_to_know"]
    # F10-06: pdf2docx and LibreOffice linked on PDF to Word
    urls = [u for _, u in t["pdf-to-word"]["sources"]]
    assert "https://github.com/ArtifexSoftware/pdf2docx" in urls and "https://www.libreoffice.org/" in urls
    # P22: one set of fresh PNG to JPG figures (26 Nov 2026); the earlier run's numbers are gone
    fixes = " ".join(f for _, f in t["png-to-jpg"]["troubleshooting"]["fixes"])
    assert "2,930.0 KB to 459.8 KB" in fixes and "1,587 KB" not in fixes and "116 KB" not in fixes
    # F10-38: Rotate and Watermark grew by real facts (3 new FAQs each)
    assert len(t["rotate-pdf"]["faq"]) >= 6 and len(t["watermark-pdf"]["faq"]) >= 5
    # DOC to DOCX: shorter intro
    assert len(t["doc-to-docx"]["intro"].split()) < 40


def test_c2_videos_on_six_tool_pages():
    c = kk.app.test_client()
    for slug, (vid, sec, up, title) in config._R10_C2.items():
        html = c.get(f"/tools/{slug}", headers={"CF-IPCountry": "US"}).data.decode()
        assert f'data-yt="{vid}"' in html and 'data-wide="1"' in html, slug
        assert f'href="https://www.youtube.com/watch?v={vid}"' in html, slug
        assert f"/static/img/video/c2-{slug}.jpg" in html and 'width="320" height="180"' in html, slug
        assert "Read the transcript" not in html, slug
        de = c.get(f"/tools/{slug}", headers={"CF-IPCountry": "DE"}).data.decode()
        assert f'href="https://www.youtube.com/watch?v={vid}"' in de and "data-yt=" not in de, slug
    # Shorts keep the /shorts/ link
    html = c.get("/tools/merge-pdf", headers={"CF-IPCountry": "US"}).data.decode()
    assert "https://www.youtube.com/shorts/" in html and 'data-wide="1"' not in html


# ---- Part 5 (26 Nov 2026): guides ---------------------------------------------------------
def test_guides_r10_structure_and_dates():
    import json, re
    c = kk.app.test_client()
    sm = c.get("/sitemap.xml").data.decode()
    for g in config.GUIDES:
        slug = g["slug"]
        html = c.get(f"/guides/{slug}").data.decode()
        main = re.search(r"<main\b.*?</main>", html, re.S).group(0)
        # F10-50: the first <p> in <main> is the answer-first summary
        assert re.search(r"<p\b[^>]*>", main).group(0) == '<p class="tool-page-desc">', slug
        desc = re.search(r'<p class="tool-page-desc">(.*?)</p>', main, re.S).group(1)
        assert re.search(r"\d", re.sub(r"<[^>]+>", "", desc)), slug                      # F10-36
        heads = re.findall(r"<h2>(.*?)</h2>", main)
        assert sum(h.strip().endswith("?") for h in heads) >= 2, (slug, heads)           # F10-37
        assert "<table" in main, slug
        assert len(g["sources"]) >= 2, slug                                               # F10-33
        # F10-13: visible date = Article dateModified = sitemap lastmod
        art = [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
               if '"Article"' in b][0]
        assert art["dateModified"] == config.RELEASE10_DATE, slug
        assert f'Updated <time datetime="{config.RELEASE10_DATE}"' in main, slug
        assert f"/guides/{slug}</loc><lastmod>{config.RELEASE10_DATE}</lastmod>" in sm, slug
        assert "[[" not in main, slug
    assert f"/guides</loc><lastmod>{config.RELEASE10_DATE}</lastmod>" in sm


def test_guides_r10_links_paa_datasets_tests():
    c = kk.app.test_client()
    assert sorted(config.R10_LINKS_DONE) == list(range(1, 28))                            # F10-49
    for row, slug, anchor, target in config._R10_LINKS:
        html = _h.unescape(c.get(f"/guides/{slug}").data.decode())
        href = f'/guides/{target[6:]}' if target.startswith("guide:") else f"/tools/{target}"
        assert f'<a href="{href}">{anchor}</a>' in html or f'href="{href}"' in html, (row, slug)
    for slug, qs in (("xls-vs-xlsx", ("What does XLSX stand for?", "Can I open an XLS or XLSX file without Excel?")),
                     ("ppt-vs-pptx", ("What does PPTX stand for?", "Can I open a PPTX file without PowerPoint?"))):
        html = c.get(f"/guides/{slug}").data.decode()
        for q in qs:
            assert f"<h2>{q}</h2>" in html, (slug, q)                                    # F10-47
        assert "signifies an XML file that has no macros" in _h.unescape(html)
    for slug, doi in (("docx-vs-doc", "24199944"), ("pdf-compression-levels-explained", "24199944"),
                      ("jpg-vs-png", "24199944"), ("powerpoint-to-pdf-and-back", "24199944"),
                      ("reduce-pdf-size-for-email", "24324333")):
        html = c.get(f"/guides/{slug}").data.decode()
        assert f'href="https://doi.org/10.5281/zenodo.{doi}"' in html, slug              # F10-48
        assert "Suggested citation: Iqbal, S. (2026)." in html, slug
    for slug in ("merge-pdf-in-the-right-order", "pdf-password-protection-explained",
                 "pdf-to-excel-table-conversion-results", "powerpoint-to-pdf-and-back",
                 "split-and-rotate-pdf-pages", "what-happens-to-your-file", "how-to-split-pdf-files",
                 "heic-to-jpg-on-windows"):
        html = c.get(f"/guides/{slug}").data.decode()
        assert "Our tests on 26 November 2026" in html and html.count("<tr>") >= 4, slug  # F10-35
    # the clean-up sentence matches the code (5-minute timer, R10 option 2)
    html = c.get("/guides/what-happens-to-your-file").data.decode()
    assert "every 5 minutes while the server is running" in html and "at most every 30 minutes" not in html


# ---- Part 6 (26 Nov 2026): home, hubs, About, Contact, Link to us ----------------------------
def test_part6_hub_pages():
    import json, re
    c = kk.app.test_client()
    sm = c.get("/sitemap.xml").data.decode()
    for path, key, kind in (("/", None, "Last checked"), ("/tools", "tools", "Last checked"),
                            ("/guides", "guides", "Last checked"), ("/about", "about", "Last checked"),
                            ("/contact", "contact", "Last updated"), ("/link-to-us", "link-to-us", "Last updated")):
        html = c.get(path).data.decode()
        main = re.search(r"<main\b.*?</main>", html, re.S).group(0)
        assert f'{kind} <time datetime="{config.RELEASE10_DATE}">{config.R10_DATE_TEXT}</time> by <a href="/about/shahid-iqbal">Shahid Iqbal</a>' in main, path
        assert f"<loc>{config.SITE_URL}{path if path != '/' else '/'}</loc><lastmod>{config.RELEASE10_DATE}</lastmod>" in sm, path
        heads = re.findall(r"<h2[^>]*>(.*?)</h2>", main, re.S)
        assert sum(re.sub(r"<[^>]+>", "", h).strip().endswith("?") for h in heads) >= 2, (path, heads)   # F10-37
        assert "<table" in main, path
    # F10-36: a figure in the first paragraph of home, hubs and About
    for path, cls in (("/", "hero-sub"), ("/tools", "tool-page-desc"), ("/guides", "tool-page-desc")):
        html = c.get(path).data.decode()
        first = re.search(rf'<p class="{cls}">(.*?)</p>', html, re.S).group(1)
        assert re.search(r"\d+(\.\d+)? (seconds|KB|MB)", first), path
    about = c.get("/about").data.decode()
    first_p = re.search(r"<h1>About KuickKonvert</h1>.*?<p>(.*?)</p>", about, re.S).group(1)
    assert "0.4 and 4.7 seconds" in first_p
    # F10-39: limits and a live result for all 21 tools on /tools
    tools = c.get("/tools").data.decode()
    sec = tools.split('id="limits-and-tests"')[1].split("</table>")[0]
    assert sec.count("<tr>") == len(config.TOOLS) + 1
    # F10-17: pdf2docx on About; F10-18/F10-44: About lists match sameAs additions
    assert "https://github.com/ArtifexSoftware/pdf2docx" in about
    org = [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', about, re.S)
           if '"Organization"' in b][0]
    for _, url in config.R10_SAMEAS_ADD:
        assert url in org["sameAs"] and f'href="{url}"' in about, url
    assert len(org["sameAs"]) == 18
    # counsel-verbatim About sections unchanged
    assert "KuickKonvert's underlying application source code is published under the GNU Affero General Public License v3 (AGPL-3.0)." in about
    # F10-26: llms.txt
    llms = c.get("/llms.txt").data.decode()
    for part in ("/how-we-test)", "/about/shahid-iqbal)", "/guides)", "/link-to-us)", "https://blog.kuickkonvert.com"):
        assert part in llms, part


# ---- Score gate (F10-40) fixes, 26 Nov 2026 -------------------------------------------------
def test_score_gate_fixes():
    import re
    c = kk.app.test_client()
    for slug in ("what-is-a-heic-file", "what-is-a-webp-image", "pdf-compression-levels-explained"):
        dek = re.sub(r"\[\[[^|]+\|([^\]]+)\]\]", r"\1", config.GUIDES_BY_SLUG[slug]["dek"])
        assert len(dek.split()) <= 90, (slug, len(dek.split()))          # principle 2: answer first
    g = config.GUIDES_BY_SLUG["location-data-in-photos"]
    assert "2,774.9 KB HEIC photo" in g["dek"] and "1,848.1 KB JPG" in g["dek"]
    html = c.get("/tools/rotate-pdf").data.decode()
    assert "<h2>When should you use Rotate PDF?</h2>" in html
