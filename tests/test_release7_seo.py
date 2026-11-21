"""Release 7 SEO acceptance checks for KuickKonvert (prepared 10 Nov 2026).

Copy to tests/test_release7_seo.py in the repo and run from the repo root:
    python -m pytest -q tests/test_release7_seo.py
It renders every sitemap URL with Flask's test client (no network, no
uploads) and checks the Release 7 acceptance rules. Against 4660635 some
checks fail on purpose: they describe the Release 7 end state.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app as kk  # noqa: E402

SITE = kk.SITE_URL
BANNED = ["secure", "security", "100%", "unlimited", "no limits", "no fixed limit",
          "no waiting", "no ads", "fastest", "best", "no catch", "every time",
          "guaranteed"]
NO_WATERMARK_META_OK = {"/", "/tools/word-to-pdf", "/tools/jpg-to-pdf",
                        "/tools/png-to-pdf", "/tools/merge-pdf",
                        "/tools/pdf-to-word"}  # 6th page added 11 Nov 2026
FORBIDDEN_TYPES = {"SoftwareApplication", "WebApplication", "FAQPage", "HowTo"}


def _unescape(s):
    import html
    return html.unescape(s or "").strip()


@pytest.fixture(scope="module")
def pages():
    client = kk.app.test_client()
    sm = client.get("/sitemap.xml").data.decode()
    out = {}
    for loc in re.findall(r"<loc>(.*?)</loc>", sm):
        path = loc.replace(SITE, "") or "/"
        r = client.get(path)
        html = r.data.decode()
        main = re.search(r"<main.*?</main>", html, re.S)
        out[path] = {
            "status": r.status_code,
            "html": html,
            "main": main.group(0) if main else html,
            "title": _unescape(re.search(r"<title>(.*?)</title>", html, re.S).group(1)),
            "desc": _unescape((re.search(r'name="description" content="(.*?)"', html, re.S) or [None, ""])[1]),
            "ld": re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S),
        }
    return out


def test_all_pages_200(pages):
    assert pages and all(p["status"] == 200 for p in pages.values())


def test_titles_and_descriptions_unique(pages):
    titles = [p["title"] for p in pages.values()]
    descs = [p["desc"] for p in pages.values()]
    assert len(set(titles)) == len(titles)
    assert len(set(descs)) == len(descs)


def test_title_length(pages):
    bad = {k: len(p["title"]) for k, p in pages.items() if len(p["title"]) > 60}
    assert not bad, bad


def test_description_length(pages):
    # /privacy is excluded: its wording changes only after owner approval
    # and regression tests (standing privacy rule).
    bad = {k: len(p["desc"]) for k, p in pages.items()
           if k != "/privacy" and not 120 <= len(p["desc"]) <= 160}
    assert not bad, bad


def test_no_banned_words_in_snippets(pages):
    bad = {}
    for k, p in pages.items():
        text = (p["title"] + " " + p["desc"]).lower()
        hits = [w for w in BANNED if re.search(r"\b" + re.escape(w) + r"\b", text)]
        if hits:
            bad[k] = hits
    assert not bad, bad


def test_no_watermark_only_where_allowed(pages):
    bad = [k for k, p in pages.items()
           if "no watermark" in p["desc"].lower() and k not in NO_WATERMARK_META_OK]
    assert not bad, bad
    assert "no watermark" not in pages["/tools/watermark-pdf"]["main"].lower()


def test_json_ld_valid_and_allowed(pages):
    for k, p in pages.items():
        for block in p["ld"]:
            data = json.loads(block)  # raises on invalid JSON
            assert data.get("@type") not in FORBIDDEN_TYPES, (k, data.get("@type"))


def test_entity_ids(pages):
    home = [json.loads(b) for b in pages["/"]["ld"]]
    site = next(d for d in home if d["@type"] == "WebSite")
    org = next(d for d in home if d["@type"] == "Organization")
    assert site.get("@id") == f"{SITE}/#website"
    assert org.get("@id") == f"{SITE}/#organization"
    assert "kuickkonvert.com" in site.get("alternateName", [])
    for k, p in pages.items():
        if k.startswith("/guides/"):
            art = next(json.loads(b) for b in p["ld"] if json.loads(b)["@type"] == "Article")
            assert art["publisher"].get("@id") == f"{SITE}/#organization", k


def test_tool_breadcrumb_points_to_tools_hub(pages):
    for k, p in pages.items():
        if k.startswith("/tools/"):
            bc = next(json.loads(b) for b in p["ld"] if json.loads(b)["@type"] == "BreadcrumbList")
            assert bc["itemListElement"][1]["item"] == f"{SITE}/tools", k
            assert "#" not in json.dumps(bc), k


def test_tools_hub_itemlist(pages):
    lists = [json.loads(b) for b in pages["/tools"]["ld"] if json.loads(b)["@type"] == "ItemList"]
    assert lists, "ItemList missing on /tools"
    items = lists[0]["itemListElement"]
    assert len(items) == len(kk.TOOLS)
    assert [i["position"] for i in items] == list(range(1, len(items) + 1))
    assert {i["url"] for i in items} == {f"{SITE}/tools/{t['slug']}" for t in kk.TOOLS}


def test_every_page_has_two_contextual_inlinks(pages):
    inlinks = defaultdict(set)
    for src, p in pages.items():
        for href in set(re.findall(r'href="([^"#?]+)', p["main"])):
            href = href.replace(SITE, "")
            if href.startswith("/") and not href.startswith("/static"):
                href = href.rstrip("/") or "/"
                if href != src:
                    inlinks[href].add(src)
    weak = {k: len(inlinks[k]) for k in pages if k != "/" and len(inlinks[k]) < 2}
    assert not weak, weak


def test_llms_txt_lists_every_page():
    body = kk.app.test_client().get("/llms.txt").data.decode()
    for t in kk.TOOLS:
        assert f"{SITE}/tools/{t['slug']}" in body
    for g in kk.GUIDES:
        assert f"{SITE}/guides/{g['slug']}" in body


# --- Scope update 10 Nov 2026: long-tail phrases word for word -------------
LONG_TAIL = {
    "/tools/split-pdf": ["how to split pdf files", "split pdf pages"],
    "/tools/merge-pdf": ["merge pdf files free"],
    "/tools/pdf-to-excel": ["convert pdf to excel free", "how to convert pdf to excel for free"],
    "/tools/png-to-pdf": ["png to pdf converter free"],
    "/tools/pdf-to-word": ["pdf to word document"],
    "/tools/png-to-jpg": ["change png to jpg"],
    "/tools/heic-to-jpg": ["how to convert heic to jpg"],
    # 11 Nov 2026 Ubersuggest: 40/month (US)
    "/tools/pdf-to-jpg": ["convert pdf to jpg without losing quality"],
}


def test_long_tail_phrases_present(pages):
    import html as _html
    missing = {}
    for path, phrases in LONG_TAIL.items():
        text = _html.unescape(re.sub(r"<[^>]+>", " ", pages[path]["html"])).lower()
        text = re.sub(r"\s+", " ", text + " " + pages[path]["desc"].lower())
        absent = [p for p in phrases if p not in text]
        if absent:
            missing[path] = absent
    assert not missing, missing


def test_favicon_sizes():
    from PIL import Image
    root = Path(__file__).resolve().parents[1] / "static" / "img"
    for size in (48, 96):
        im = Image.open(root / f"favicon-{size}.png")
        assert im.size == (size, size)
    html = kk.app.test_client().get("/").data.decode()
    assert 'sizes="48x48"' in html and "favicon-48.png" in html


def test_llms_txt_format():
    body = kk.app.test_client().get("/llms.txt").data.decode()
    lines = body.splitlines()
    assert lines[0] == "# KuickKonvert"
    assert not any(l.startswith("### ") for l in lines)
    in_section = False
    for l in lines:
        if l.startswith("## "):
            in_section = True
            continue
        if in_section and l.strip():
            assert re.match(r"^- \[[^\]]+\]\(https://[^)]+\)(: .+)?$", l), l
    assert "fair-use limits apply" in body and "per minute" not in body


# --- Shahid's answers of 11 Nov 2026 ---------------------------------------
def test_author_person_entity(pages):
    about = [json.loads(b) for b in pages["/about"]["ld"]]
    person = next(d for d in about if d["@type"] == "Person")
    assert person["@id"] == f"{SITE}/about#shahid-iqbal"
    assert person["worksFor"]["@id"] == f"{SITE}/#organization"
    for k, p in pages.items():
        if k.startswith("/guides/"):
            art = next(json.loads(b) for b in p["ld"] if json.loads(b)["@type"] == "Article")
            assert art["author"].get("@id") == f"{SITE}/about#shahid-iqbal", k


def test_blog_in_same_as(pages):
    org = next(json.loads(b) for b in pages["/"]["ld"] if json.loads(b)["@type"] == "Organization")
    assert "https://kuickkonvert.blogspot.com/" in org["sameAs"]


def test_release7_updated_dates(pages):
    # Exactly the guides whose text changed show the release day (rule N5):
    # the 12 of R7-28 (incl. docx-vs-doc and pdf-compression-levels-explained,
    # changed again by R7-92), plus pdf-to-excel-table-conversion-results
    # (R7-84 Q3), pdf-to-word-text-vs-scanned (R7-86) and
    # photos-to-one-pdf-jpg-to-pdf-tips (R7-89).
    import config
    changed = set(config.RELEASE7_UPDATED_GUIDES)
    assert len(changed) == 15
    # R8-02 (20 Nov 2026): two guides changed again in Release 8 and now show
    # R8_DATE instead (checked in test_r8_comparison_guides.py).
    redated = set(config._R8_DEK_ANSWERS)
    # Release 9 (21 Nov 2026): six guides got a step-by-step section and show
    # R9_DATE (checked in test_r9_release.py).
    redated |= set(config.R9_UPDATED_GUIDES)
    for k, p in pages.items():
        if k.startswith("/guides/") and k != "/guides":
            slug = k.split("/")[-1]
            if slug in redated:
                continue
            shows = f'Updated <time datetime="{config.RELEASE7_DATE}"' in p["html"]
            assert shows == (slug in changed), k


def test_consent_regions_r7_72():
    client = kk.app.test_client()
    for cc in ("RE", "GP", "MQ", "GF", "YT", "MF", "AX", "XX", "T1", "DE", "GB", "CH",
               "GI", "JE", "GG", "IM", "BL", "PM", "NC", "PF", "WF", "TF", "AD", "MC", "SM", "VA"):
        html = client.get("/tools/word-to-pdf", headers={"CF-IPCountry": cc}).data.decode()
        assert "js/consent.js" in html and "adsbygoogle.js" not in html, cc
    html = client.get("/tools/word-to-pdf").data.decode()  # no header at all
    assert "js/consent.js" in html and "adsbygoogle.js" not in html
    for cc in ("US", "PK"):
        html = client.get("/tools/word-to-pdf", headers={"CF-IPCountry": cc}).data.decode()
        # 12 Nov 2026: AdSense script withdrawn until approval (ADSENSE_SCRIPT_ENABLED)
        assert "js/consent.js" not in html and "adsbygoogle.js" not in html, cc
        assert 'name="google-adsense-account" content="ca-pub-2468332370767807"' in html, cc


# --- 12 Nov 2026 audit: banned words and absolute claims in VISIBLE copy ----
# The snippet test above covers titles and descriptions only; these phrases
# were found in page text. Advice wording such as "works best on" and the
# "no OCR" disclaimers are allowed.
FORBIDDEN_VISIBLE = ["100%", "best results", "best quality", "nothing is kept", "guaranteed, exact",
                     "fast, free, private", "private by design", "for security",
                     "deleted the moment"]


def test_no_forbidden_claims_in_visible_text(pages):
    import html as _h
    bad = {}
    for k, p in pages.items():
        body = re.search(r"<body.*?</body>", p["html"], re.S).group(0)
        body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", body, flags=re.S)
        text = re.sub(r"\s+", " ", _h.unescape(re.sub(r"<[^>]+>", " ", body))).lower()
        hits = [w for w in FORBIDDEN_VISIBLE if w in text]
        if hits:
            bad[k] = hits
    assert not bad, bad


# --- G13 transcripts (12 Nov 2026) -----------------------------------------
def test_video_transcripts(pages):
    import config
    with_t = {k for k, v in config.VIDEOS.items() if v.get("transcript")}
    # 12 Nov 2026: all 23 professional videos (8 re-uploaded after correction)
    assert len(with_t) == 23
    for slug in with_t:
        path = {"all-tools": "/tools", "home": "/"}.get(slug, f"/tools/{slug}")
        p = pages[path]
        assert "Read the transcript" in p["html"], path
        vo = next(json.loads(b) for b in p["ld"] if json.loads(b)["@type"] == "VideoObject")
        assert vo.get("transcript", "").startswith(config.VIDEOS[slug]["transcript"][:30]), path
        assert "quickconvert" not in vo["transcript"].lower(), path


def test_r7_83_new_voice_videos():
    """R7-83 (19 Nov 2026 fix): the 23 new-voice videos uploaded on 13 Nov 2026
    replace the earlier IDs; lengths match YouTube; the transcripts are the
    round-2 spoken text and end with the end-card line."""
    import config
    ids = {"home": "p8tYDhRRQHc", "word-to-pdf": "4Y2JCxaA9T8", "pdf-to-word": "UqK4o4H9yT8",
           "excel-to-pdf": "BwiQh7pkv6w", "pdf-to-excel": "r8VSFnV1rMs", "ppt-to-pdf": "08v4gGONweo",
           "pdf-to-ppt": "PZ9rf1UKdq8", "jpg-to-pdf": "1nxYETXA35Y", "png-to-pdf": "M6R_SikPg0c",
           "pdf-to-jpg": "KWbp5uIROk8", "pdf-to-png": "kFygV7CKyy0", "heic-to-jpg": "_6PwJwiU3Ic",
           "webp-to-jpg": "pSxJcICw1qY", "png-to-jpg": "e4lbRyCLLuA", "jpg-to-png": "IHPBh06crNk",
           "merge-pdf": "hzr82e6NkqY", "split-pdf": "I2xbhWO4xMI", "compress-pdf": "InIhMZl77y0",
           "rotate-pdf": "-dEMQIAoPuw", "watermark-pdf": "hvqWtyb8lq8", "protect-pdf": "BGB3Ae-KHh0",
           "doc-to-docx": "pljxa5C-ARk", "all-tools": "1E_AUIg4tZk"}
    assert set(ids) == set(config.VIDEOS)
    assert config.VIDEO_TRANSCRIPTS_AFTER_REUPLOAD == {}
    for slug, vid in ids.items():
        v = config.VIDEOS[slug]
        assert v["id"] == vid and v["uploaded"].startswith("2026-11-13T"), slug
        m, sec = divmod(v["seconds"], 60)
        assert v["duration"] == (f"PT{m}M{sec}S" if m else f"PT{sec}S"), slug
        low = v["transcript"].lower()
        if slug == "all-tools":
            continue   # V23 voice-over unchanged ("tap the bell" is its YouTube call to action)
        for bad in ("exactly", "perfectly", "in seconds", "tap ", "moment you", "far lighter", "pixel", "[conversion]"):
            assert bad not in low, (slug, bad)
        if "up to 20" in low:
            assert slug in kk.IMAGE_TO_IMAGE_SLUGS, slug   # true 20-image limit
        if slug == "home":
            assert v["transcript"].endswith("Files deleted after conversion. kuickkonvert.com.")
        elif slug != "all-tools":
            assert low.endswith(("no sign-up. files deleted after conversion.",
                                 "nothing to install. files deleted after conversion.",
                                 "up to 20 at once. files deleted after conversion.")), slug
    for old in ("pRmhhN1kfP0", "t4MdCZw2SaQ", "VLyY6sAZ5qg", "aouHgA5mJR4"):
        assert all(v["id"] != old for v in config.VIDEOS.values())


# --- Final legal opinion, 12 Nov 2026 ---------------------------------------
def test_gpc_blocks_adsense_and_denies_ad_storage():
    client = kk.app.test_client()
    html = client.get("/tools/word-to-pdf", headers={"CF-IPCountry": "US", "Sec-GPC": "1"}).data.decode()
    assert "adsbygoogle.js" not in html
    assert "navigator.globalPrivacyControl === true || true" in html
    html = client.get("/tools/word-to-pdf", headers={"CF-IPCountry": "US"}).data.decode()
    assert "adsbygoogle.js" not in html  # withdrawn until approval (12 Nov 2026)


def test_adsense_switch_restores_script_outside_consent_regions():
    """When ADSENSE_SCRIPT_ENABLED is set after approval, the old rules apply again."""
    import config
    old = kk.ADSENSE_SCRIPT_ENABLED
    try:
        kk.ADSENSE_SCRIPT_ENABLED = True
        client = kk.app.test_client()
        assert "adsbygoogle.js" in client.get("/tools/word-to-pdf", headers={"CF-IPCountry": "US"}).data.decode()
        assert "adsbygoogle.js" not in client.get("/tools/word-to-pdf", headers={"CF-IPCountry": "DE"}).data.decode()
        assert "adsbygoogle.js" not in client.get("/tools/word-to-pdf", headers={"CF-IPCountry": "US", "Sec-GPC": "1"}).data.decode()
    finally:
        kk.ADSENSE_SCRIPT_ENABLED = old


def test_privacy_notice_matches_code(pages):
    import app as _a, html as _h
    p = _h.unescape(pages["/privacy"]["html"])
    assert "Consent-Controlled Locations:</strong> For the purposes of our third-party advertising" in _h.unescape(pages["/privacy"]["html"]) or \
           "Consent-Controlled Locations: For the purposes of our third-party advertising" in re.sub(r"<[^>]+>", "", p)
    # Adviser review 12 Nov 2026: Version 1 (AdSense off) is the published wording.
    assert "KuickKonvert does not currently load Google AdSense advertising code" in p
    # Consent Mode paragraph: only after production verification (final opinion, stage 7)
    assert ("Google Consent Mode v2 advertising consent parameters are set to" in p) == _a.PRIVACY_CONSENT_MODE_DISCLOSURE
    # the two GPC sentences approved in the final legal opinion
    assert "If your browser sends a Global Privacy Control signal, the Google Ads tag is not activated" in p
    assert "If your browser sends a Global Privacy Control signal, the badge image is not loaded." in p
    assert "advertising code may be loaded" not in p
    # every territory code in the code is named in the notice
    names = {"GI": "Gibraltar", "JE": "Jersey", "GG": "Guernsey", "IM": "Isle of Man", "RE": "Réunion",
             "GP": "Guadeloupe", "MQ": "Martinique", "GF": "French Guiana", "YT": "Mayotte", "MF": "Saint-Martin",
             "BL": "Saint Barthélemy", "PM": "Saint Pierre and Miquelon", "NC": "New Caledonia",
             "PF": "French Polynesia", "WF": "Wallis and Futuna", "TF": "French Southern and Antarctic Lands",
             "AX": "Åland Islands", "AD": "Andorra", "MC": "Monaco", "SM": "San Marino", "VA": "Vatican City"}
    core = {"AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT", "LV",
            "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE", "IS", "LI", "NO", "GB", "CH"}
    assert set(_a._CONSENT_REGIONS) == core | set(names)
    for code, name in names.items():
        assert name in p, (code, name)
    assert "For visitors in the EEA, the UK and Switzerland we do not currently load" not in p
    # Adviser opinion 13 Nov 2026 (Part B amendments)
    assert "permanently deleted" not in p and "We do not review, copy, back up" not in p
    assert "We do not sell your uploaded files or disclose their contents to third parties for their independent commercial purposes" in p
    assert "Cloudflare (Cloudflare, Inc., United States)" in p and "Render (Render Services, Inc., United States)" in p
    assert "we normally hold no personal data" not in p
    for right in ("corrected", "restrict how it is used", "portable format", "withdraw your consent", "solely on automated processing"):
        assert right in p, right
    assert "How to make a privacy request" in p
    assert "Where available, our cookie settings interface" not in p
    # Final opinion 13 Nov 2026 (commit 8654c67 review)
    assert "to the extent required by applicable privacy law" in p
    assert "it does not by itself cover processing in other countries such as Singapore" in p
    assert "Why we use personal data and our legal bases" in p and "How long we keep personal data" in p
    assert "14 months under our current Google Analytics settings. The reset-on-new-activity option applies to user-level data, not event-level data." in p
    # Final opinion on a9dd916 (13 Nov 2026)
    assert "We remain responsible for ensuring that our arrangements with these providers provide an appropriate level of protection" in p
    assert "the relevant service providers are responsible for applying" not in p
    assert "Swiss Federal Act on Data Protection (FADP)" in p
    assert "depends on the law that applies to you and its conditions" in p
    assert "parental or guardian authorisation" in p


# --- Release 7 new guides (WP12, approved 12 Nov 2026 without photo figures) --
NEW_GUIDES = ("how-to-split-pdf-files", "heic-to-jpg-on-windows", "reduce-pdf-size-for-email")


def _sentences(text):
    text = re.sub(r"\[\[[a-z0-9-]+\|([^\]]+)\]\]", r"\1", text)
    return [s.strip().lower() for s in re.split(r"(?<=[.!?:])\s+", text) if len(s.strip()) >= 40]


def test_release7_new_guides_render_and_are_listed(pages):
    import config
    client = kk.app.test_client()
    llms = client.get("/llms.txt").data.decode()
    guides_index = client.get("/guides").data.decode()
    for slug in NEW_GUIDES:
        path = f"/guides/{slug}"
        assert path in pages, path                      # in the sitemap
        p = pages[path]
        assert p["status"] == 200
        assert len(p["title"]) <= 60 and 120 <= len(p["desc"]) <= 160, path
        assert f"{SITE}{path}" in llms, path
        assert path in guides_index, path
        assert '<ol class="guide-steps">' in p["html"], path
        assert "How we tested" in p["html"], path
        g = config.GUIDES_BY_SLUG[slug]
        assert g["published"] == config.RELEASE7_DATE
        assert all(t in config.TOOLS_BY_SLUG for t in g["related_tools"])
        types = {json.loads(b)["@type"] for b in p["ld"]}
        assert {"BreadcrumbList", "Article"} <= types and not types & FORBIDDEN_TYPES, (path, types)
        low = p["main"].lower()
        # the photo-size figures were dropped (no real iPhone/photo files)
        assert "needs" not in low or "real iphone" not in low
        assert "[needs" not in low and "no watermark" not in low, path


def test_release7_new_guides_do_not_repeat_text():
    """No sentence of a new guide appears in any other guide or tool page text."""
    import config
    def texts(g):
        yield g["dek"]
        for sec in g["sections"]:
            yield from sec.get("paragraphs", [])
            yield from sec.get("steps", [])
            if sec.get("table", {}).get("note"):
                yield sec["table"]["note"]
    others = set()
    for g in config.GUIDES:
        if g["slug"] not in NEW_GUIDES:
            for t in texts(g):
                others.update(_sentences(t))
    for t in config.TOOLS:
        for v in (t.get("intro", ""), t.get("description", ""), t.get("meta_description", "")):
            others.update(_sentences(v))
    seen = {}
    for slug in NEW_GUIDES:
        for t in texts(config.GUIDES_BY_SLUG[slug]):
            for s in _sentences(t):
                assert s not in others, (slug, s)
                assert seen.setdefault(s, slug) == slug, (slug, seen[s], s)


def test_release_gate_notice_matches_adsense_switch():
    """RELEASE GATE (12 Nov 2026). With the AdSense script switched off, the
    Privacy Notice must not say the code "may be loaded". This test fails on
    purpose until the adviser's re-approved Advertising wording is inserted
    into templates/privacy.html. Do not deploy while it fails."""
    import config
    html = kk.app.test_client().get("/privacy").data.decode()
    if not config.ADSENSE_SCRIPT_ENABLED:
        assert "advertising code may be loaded" not in html



def test_consent_mode_disclosure_switch():
    old = kk.PRIVACY_CONSENT_MODE_DISCLOSURE
    try:
        kk.PRIVACY_CONSENT_MODE_DISCLOSURE = True
        html = kk.app.test_client().get("/privacy").data.decode()
        assert "Google Consent Mode v2 advertising consent parameters are set to" in html
    finally:
        kk.PRIVACY_CONSENT_MODE_DISCLOSURE = old


def test_no_alternative_advertising_pathway(pages):
    """Final legal opinion 9.2 / 9.5: on every sitemap page, in every region, no
    AdSense script tag is rendered (global switch); with Sec-GPC no badge image
    and the GPC flag is set server-side before any tag is configured."""
    client = kk.app.test_client()
    kk.limiter.enabled = False   # many requests in one test; rate limits are not under test here
    for path in pages:
        for hdr in ({"CF-IPCountry": "US"}, {"CF-IPCountry": "US", "Sec-GPC": "1"}, {"CF-IPCountry": "DE", "Sec-GPC": "1"}):
            html = client.get(path, headers=hdr).data.decode()
            assert not re.search(r"<script[^>]*(adsbygoogle|googlesyndication|doubleclick)", html), (path, hdr)
            assert "<ins class=\"adsbygoogle\"" not in html, (path, hdr)
            if hdr.get("Sec-GPC"):
                assert "launchnest.io/badge" not in html, (path, hdr)
                if hdr["CF-IPCountry"] == "US":
                    assert "var KK_GPC = navigator.globalPrivacyControl === true || true;" in html, path
                    assert html.index("var KK_GPC") < html.index("gtag('config', 'G-K0VJLC113K')"), path


def test_god_mode_audit_copy_12nov(pages):
    # R7-76: PNG to JPG FAQ carries the real test results (12 Nov 2026 run of
    # convert_images on the PDF-to-PNG test pages and logo-512.png).
    png = pages["/tools/png-to-jpg"]["main"]
    for frag in ("4,165 KB as PNG to 660 KB as JPG", "710 KB to 1,706 KB", "129 KB to 247 KB", "18 KB to 17 KB"):
        assert frag in png, frag
    # R7-77: Merge PDF answers the "merge and convert" intent truthfully
    # (h_merge_pdf accepts PDFs only).
    merge = pages["/tools/merge-pdf"]["main"]
    assert "Can I merge Word files or images with my PDFs?" in merge
    assert "Merge PDF only accepts PDF files" in merge


def test_r7_78_official_sources_and_r7_79_links(pages):
    # R7-78: official sources on 10 guides, plus pdf-to-word-text-vs-scanned (R7-86) = 11;
    # https only, shown and in Article "citation".
    import config, json as _j
    guides = {g["slug"]: g for g in config.GUIDES} if isinstance(config.GUIDES, list) else config.GUIDES
    with_sources = [s for s, g in guides.items() if g.get("sources")]
    # R8-01 (20 Nov 2026): the five new comparison guides all cite official sources: 11 + 5 = 16.
    # Release 9 (21 Nov 2026): Microsoft/Google/Apple help pages added to the
    # Word-to-PDF and photos-to-one-PDF guides: 16 + 2 = 18.
    assert len(with_sources) == 18, with_sources
    for slug in with_sources:
        p = pages[f"/guides/{slug}"]
        assert "<h2>Official sources</h2>" in p["main"], slug
        for label, url in guides[slug]["sources"]:
            assert url.startswith("https://") and "kuickkonvert" not in url
            assert f'href="{url}"' in p["main"], (slug, url)
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', p["html"], re.S)
        art = [_j.loads(b) for b in blocks if '"Article"' in b][0]
        assert [c["url"] for c in art["citation"]] == [u for _, u in guides[slug]["sources"]]
    # HEIC accuracy fix: the Store page says HEVC Video Extensions are also needed
    assert "HEVC Video Extensions package must also be installed" in pages["/guides/what-is-a-heic-file"]["main"]
    # R7-79: "What happens to your file" gets contextual links to the Privacy notice and image tools
    m = pages["/guides/what-happens-to-your-file"]["main"]
    assert m.count('href="/privacy"') >= 2
    for slug in ("heic-to-jpg", "webp-to-jpg", "png-to-jpg", "jpg-to-png"):
        assert f'href="/tools/{slug}"' in m
    assert len(re.findall(r'<a[^>]+href="/', m)) >= 10


# ---- R7-82 internal linking (13 Nov 2026) ----------------------------------
def _contextual_inlinks(pages):
    inl = defaultdict(set)
    anchors = defaultdict(list)
    for src, p in pages.items():
        for href, text in re.findall(r'<a\b[^>]*href="([^"#?]+)[^"]*"[^>]*>(.*?)</a>', p["main"], re.S):
            href = href.replace(SITE, "")
            if not href.startswith("/") or href.startswith("/static"):
                continue
            href = href.rstrip("/") or "/"
            if href != src:
                inl[href].add(src)
                anchors[href].append(_unescape(re.sub(r"<[^>]+>", "", text)))
    return inl, anchors


def test_r7_82_every_tool_has_six_inlinks_and_one_from_a_guide(pages):
    inl, _ = _contextual_inlinks(pages)
    weak = {}
    for t in kk.TOOLS:
        path = f"/tools/{t['slug']}"
        srcs = inl[path]
        if len(srcs) < 6 or not any(s.startswith("/guides/") for s in srcs):
            weak[path] = sorted(srcs)
    assert not weak, weak


def test_r7_82_png_to_jpg_links_and_anchor_variety(pages):
    inl, anchors = _contextual_inlinks(pages)
    assert len(inl["/tools/png-to-jpg"]) >= 10, sorted(inl["/tools/png-to-jpg"])
    assert "Our PNG to JPG converter" in anchors["/tools/png-to-jpg"]
    for src in ("/tools/pdf-to-png", "/tools/png-to-pdf", "/guides/what-is-a-webp-image"):
        assert src in inl["/tools/png-to-jpg"], src


def test_r7_82_related_tools():
    import config
    rel = {t["slug"]: t["related"] for t in kk.TOOLS}
    # First two unchanged: main.js shows related[:2] after a conversion.
    first_two = {"pdf-to-png": ["pdf-to-jpg", "png-to-pdf"], "png-to-pdf": ["jpg-to-pdf", "pdf-to-png"],
                 "png-to-jpg": ["jpg-to-png", "png-to-pdf"], "pdf-to-jpg": ["pdf-to-png", "jpg-to-pdf"],
                 "compress-pdf": ["merge-pdf", "split-pdf"], "merge-pdf": ["split-pdf", "compress-pdf"]}
    for s, two in first_two.items():
        assert rel[s][:2] == two, (s, rel[s])
    must = {"pdf-to-png": ["png-to-jpg"], "png-to-pdf": ["png-to-jpg", "jpg-to-png"],
            "png-to-jpg": ["jpg-to-png", "png-to-pdf", "webp-to-jpg", "heic-to-jpg"],
            "merge-pdf": ["rotate-pdf", "watermark-pdf", "protect-pdf"], "pdf-to-jpg": ["rotate-pdf"],
            "compress-pdf": ["protect-pdf"], "split-pdf": ["rotate-pdf"], "protect-pdf": ["watermark-pdf"]}
    for s, targets in must.items():
        assert all(t in rel[s] for t in targets), (s, rel[s])
    assert all(len(r) <= 5 and len(set(r)) == len(r) for r in rel.values())
    assert all(t in config.TOOLS_BY_SLUG for r in rel.values() for t in r)


def test_r7_82_pillar_guide_first_on_tool_pages(pages):
    import config
    for slug, pillar in config.R7_82_PILLAR.items():
        main = pages[f"/tools/{slug}"]["main"]
        block = re.search(r"<h2>Guides for .*?</h2>\s*<ul[^>]*>(.*?)</ul>", main, re.S)
        assert block, slug
        first = re.search(r'href="([^"]+)"', block.group(1)).group(1)
        assert first.rstrip("/").endswith(f"/guides/{pillar}"), (slug, first)


def test_r7_82_contextual_links_per_page_reasonable(pages):
    too_many = {k: n for k, p in pages.items()
                if (n := len(re.findall(r"<a\b", p["main"]))) > 100}
    assert not too_many, too_many


# ---- R7-84 guide text gaps (13 Nov 2026) -----------------------------------
def test_r7_84_question_sections(pages):
    want = {
        "/guides/pdf-compression-levels-explained": ["What does compressing a PDF do?", "Is a PDF lossless?"],
        "/guides/excel-to-pdf-fit-on-one-page": ["Fitting a sheet on one A4 page"],
        "/guides/pdf-to-excel-table-conversion-results": ["Can you convert PDF to Excel without losing formatting?"],
        "/guides/ppt-vs-pptx": ["What is a PPTX file?"],
    }
    for path, heads in want.items():
        for h in heads:
            assert f">{h}</h2>" in pages[path]["main"], (path, h)
    # The direct answer comes straight after the first H2 (answer-first).
    main = pages["/guides/pdf-compression-levels-explained"]["main"]
    assert main.index("What does compressing a PDF do?") < main.index("What happens when you press Compress")


def test_r7_84_excel_keeps_a4_paper_size():
    from converters.office import _edit_sheet_fit_to_page
    out = _edit_sheet_fit_to_page(
        b'<worksheet><dimension ref="A1:L9"/><pageMargins left="0.7"/>'
        b'<pageSetup paperSize="9" orientation="portrait" r:id="rId1"/></worksheet>')
    assert b'paperSize="9"' in out and b'r:id="rId1"' in out
    assert b'fitToWidth="1"' in out and b'fitToHeight="0"' in out
    assert out.count(b"orientation=") == 1 and b'orientation="landscape"' in out


def test_r7_85_featured_on_listing_urls(pages):
    """R7-85 (14 Nov 2026): the footer "Featured on" links point at the live
    listing pages. nxgntools.com/tools/shahid-iqbal returned "The requested
    tool could not be found"; the live listing is /tools/kuickkonvert."""
    expected = [
        "https://www.producthunt.com/products/kuickkonvert",
        "https://peerpush.com/p/kuickkonvert",
        "https://www.saashub.com/kuickkonvert",
        "https://peerlist.io/kuickkonvert/project/kuickkonvert",
        "https://www.nxgntools.com/tools/kuickkonvert",
    ]
    for path, page in pages.items():
        html = page["html"]
        assert "nxgntools.com/tools/shahid-iqbal" not in html, path
        for url in expected:
            assert f'href="{url}"' in html, (path, url)


def test_r7_86_pdf_to_word_guide_sections(pages):
    """R7-86 (15 Nov 2026): three new sections in the PDF to Word guide, from the
    Ahrefs AI Content Helper review; the old "Getting the best result" section is
    replaced. No OCR claim, no competitor names, links to the right tools."""
    import config
    g = config.GUIDES_BY_SLUG["pdf-to-word-text-vs-scanned"]
    assert [s["heading"] for s in g["sections"]] == [
        "Two kinds of PDF that look the same",
        "How to tell which one you have",
        "How to open a PDF in Word, step by step",   # Release 9, C3 (21 Nov 2026)
        "What we measured",
        "Which method to use",
        "What to do with a scanned PDF",
        "Before you convert: prepare the PDF",
        "Keeping the formatting: what carries over to Word",
    ]
    p = pages["/guides/pdf-to-word-text-vs-scanned"]
    main = p["main"]
    assert "Getting the best result" not in main
    for h in ("Which method to use", "Before you convert: prepare the PDF",
              "Keeping the formatting: what carries over to Word"):
        assert f">{h}</h2>" in main, h
    for href in ('href="/tools/pdf-to-word"', 'href="/tools/split-pdf"', 'href="/tools/compress-pdf"'):
        assert href in main, href
    low = _unescape(main).lower()
    assert "our tool doesn't do ocr" in low
    for bad in ("smallpdf", "ilovepdf", "adobe acrobat", "pdfgear", "wps", "kimi",
                "guaranteed", "100%", "unlimited", "secure", " fast "):
        assert bad not in low, bad
    # Release 9 (21 Nov 2026) added a how-to section, so the guide now shows R9_DATE.
    assert f'Updated <time datetime="{config.R9_DATE}"' in p["html"]
