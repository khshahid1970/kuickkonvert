"""Release 10.4 (26 Nov 2026).

1. The author page /about/shahid-iqbal is dropped (Shahid, 26 Nov 2026): it
   redirects permanently to /about, it is out of the sitemap and llms.txt, and
   every byline and the Person @id point to /about#shahid-iqbal.
2. Lock-in check for the 27 approved guide links (F10-49, approved 25 Nov 2026,
   live since Release 10): each one is checked in the rendered HTML of its guide,
   not only in config.
"""
import html as _html
import re

import app as kk
import config

import pytest

SITE = "https://kuickkonvert.com"


@pytest.fixture(autouse=True)
def _reset_fair_use_limiter():
    # These tests fetch many pages from one test client; reset the fair-use
    # limiter before and after each one so later test modules are not throttled.
    kk.limiter.reset()
    yield
    kk.limiter.reset()


def _main(client, path):
    r = client.get(path)
    assert r.status_code == 200, path
    return re.search(r"<main\b.*?</main>", r.data.decode(), re.S).group(0)


def test_author_page_redirects_to_about():
    c = kk.app.test_client()
    r = c.get("/about/shahid-iqbal")
    assert r.status_code == 301
    assert r.headers["Location"] in ("/about", f"{SITE}/about", "http://localhost/about")


def test_author_page_gone_from_sitemap_llms_and_pages():
    c = kk.app.test_client()
    sm = c.get("/sitemap.xml").data.decode()
    assert "/about/shahid-iqbal" not in sm
    assert len(re.findall(r"<loc>", sm)) == 60
    assert "/about/shahid-iqbal" not in c.get("/llms.txt").data.decode()
    assert "about/shahid-iqbal" not in config.STATIC_LASTMOD


def test_bylines_and_person_id_point_to_about():
    c = kk.app.test_client()
    for path in ("/", "/tools", "/guides", "/about", "/contact", "/link-to-us",
                 "/tools/png-to-jpg", "/guides/docx-vs-doc", "/how-we-test"):
        main = _main(c, path)
        assert '<a href="/about#shahid-iqbal">Shahid Iqbal</a>' in main, path
    about = c.get("/about").data.decode()
    assert '"@id": "https://kuickkonvert.com/about#shahid-iqbal"' in about
    assert '<p id="shahid-iqbal">' in about
    home = c.get("/").data.decode()
    assert '"founder": {"@id": "https://kuickkonvert.com/about#shahid-iqbal"}' in home


def test_27_approved_guide_links_render():
    rows = config._R10_LINKS
    assert len(rows) == 27 and [r[0] for r in rows] == list(range(1, 28))
    c = kk.app.test_client()
    for row, slug, anchor, target in rows:
        main = _main(c, f"/guides/{slug}")
        href = f"/guides/{target[6:]}" if target.startswith("guide:") else f"/tools/{target}"
        texts = [_html.unescape(re.sub(r"<[^>]+>", "", t)).replace("’", "'")
                 for t in re.findall(rf'<a href="{re.escape(href)}">(.*?)</a>', main, re.S)]
        assert anchor.replace("’", "'") in texts, (row, slug, anchor, href, texts)
        assert href != f"/guides/{slug}", (row, "self-link")


# ---- R10.4 topic clusters: pillar and sub-pillar links, checked in rendered HTML ---------
def _guide_links(main):
    return set(re.findall(r'<a href="(/guides/[^"#]+)"', main))


def test_pillar_links_every_cluster_guide():
    c = kk.app.test_client()
    for name, cl in config.R104_CLUSTERS.items():
        members = list(cl["subpillars"]) + [m for ms in cl["subpillars"].values() for m in ms] + cl["guides"]
        links = _guide_links(_main(c, f"/guides/{cl['pillar']}"))
        missing = [m for m in members if f"/guides/{m}" not in links]
        assert not missing, (name, missing)


def test_every_cluster_guide_links_up_to_pillar_first():
    c = kk.app.test_client()
    for name, cl in config.R104_CLUSTERS.items():
        p = cl["pillar"]
        members = list(cl["subpillars"]) + [m for ms in cl["subpillars"].values() for m in ms] + cl["guides"]
        for m in members:
            main = _main(c, f"/guides/{m}")
            rel = re.search(r"<h2>Related guides</h2>\s*<ul[^>]*>(.*?)</ul>", main, re.S).group(1)
            hrefs = re.findall(r'<a href="(/guides/[^"#]+)"', rel)
            assert hrefs[0] == f"/guides/{p}", (name, m, hrefs[:2])
            sp = config.R104_MEMBER_OF[m][1]
            if sp:
                assert hrefs[1] == f"/guides/{sp}", (name, m, hrefs[:2])
            assert f"/guides/{m}" not in hrefs, (m, "self-link")
            assert len(hrefs) == len(set(hrefs)), (m, "duplicate")


def test_subpillars_list_their_group():
    c = kk.app.test_client()
    for name, cl in config.R104_CLUSTERS.items():
        for sp, members in cl["subpillars"].items():
            links = _guide_links(_main(c, f"/guides/{sp}"))
            assert f"/guides/{cl['pillar']}" in links, sp
            assert all(f"/guides/{m}" in links for m in members), (sp, members)


def test_tool_pages_list_their_hub_guide_first():
    c = kk.app.test_client()
    seen = set()
    for name, cl in config.R104_CLUSTERS.items():
        for tool, hub in cl["tools"].items():
            seen.add(tool)
            main = _main(c, f"/tools/{tool}")
            block = re.search(r"<h2>Guides for [^<]+</h2>\s*<ul[^>]*>(.*?)</ul>", main, re.S).group(1)
            hrefs = re.findall(r'<a href="(/guides/[^"#]+)"', block)
            assert hrefs[0] == f"/guides/{hub}", (tool, hrefs[:2])
            assert len(hrefs) == len(set(hrefs)), tool
            # the hub links up to the pillar, so the pillar is at most 2 clicks away
            if hub != cl["pillar"]:
                assert f"/guides/{cl['pillar']}" in _guide_links(_main(c, f"/guides/{hub}")), (tool, hub)
    assert seen == {t["slug"] for t in config.TOOLS}


def test_every_guide_is_in_one_cluster_or_trust():
    in_cluster = set(config.R104_MEMBER_OF) | {cl["pillar"] for cl in config.R104_CLUSTERS.values()}
    rest = {g["slug"] for g in config.GUIDES} - in_cluster
    assert rest == {"what-happens-to-your-file"}, rest


def test_contextual_links_per_page_stay_reasonable():
    c = kk.app.test_client()
    for g in config.GUIDES:
        main = _main(c, f"/guides/{g['slug']}")
        assert len(re.findall(r"<a href=", main)) <= 100, g["slug"]


def test_hub_guides_link_their_tools():
    c = kk.app.test_client()
    for name, cl in config.R104_CLUSTERS.items():
        hubs = {}
        for tool, hub in cl["tools"].items():
            hubs.setdefault(hub, []).append(tool)
        for hub, tools in hubs.items():
            main = _main(c, f"/guides/{hub}")
            missing = [t for t in tools if f'<a href="/tools/{t}"' not in main]
            assert not missing, (hub, missing)
