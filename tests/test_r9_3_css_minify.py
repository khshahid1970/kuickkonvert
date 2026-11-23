"""R9.3 (23 Nov 2026): visitors get a minified style.css (comments and extra
spaces removed) while the file in the repository keeps its comments.
Also: long link text on .legal pages (the GitHub URL on /about) may wrap.
Run from the repo root:
    python -m pytest -q tests/test_r9_3_css_minify.py
"""
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app as kk  # noqa: E402

ROOT = Path(kk.__file__).resolve().parent
SOURCE = (ROOT / "static/css/style.css").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def client():
    was = kk.limiter.enabled
    kk.limiter.enabled = False
    yield kk.app.test_client()
    kk.limiter.enabled = was


def test_served_css_is_minified(client):
    r = client.get("/static/css/style.css")
    assert r.status_code == 200
    assert r.mimetype == "text/css"
    body = r.get_data(as_text=True)
    assert "/*" not in body and "\n" not in body
    assert len(body) < len(SOURCE) * 0.7


def test_quoted_text_kept(client):
    body = client.get("/static/css/style.css").get_data(as_text=True)
    for s in re.findall(r'"[^"\n]*"', re.sub(r"/\*.*?\*/", "", SOURCE, flags=re.S)):
        assert s in body


def test_same_rules_count(client):
    body = client.get("/static/css/style.css").get_data(as_text=True)
    no_comments = re.sub(r"/\*.*?\*/", "", SOURCE, flags=re.S)
    assert body.count("{") == no_comments.count("{")
    assert body.count("}") == no_comments.count("}")


def test_descendant_pseudo_space_kept():
    assert kk._minify_css(".a :focus { color: red; }") == ".a :focus{color:red}"
    assert kk._minify_css("a > b , c { x: calc(100% - 2rem) ; }") == "a>b,c{x:calc(100% - 2rem)}"
    assert kk._minify_css('p::before { content: "a  b /* c */"; }') == 'p::before{content:"a  b /* c */"}'


def test_versioned_css_cached_and_conditional(client):
    page = client.get("/").get_data(as_text=True)
    m = re.search(r'/static/css/style\.css\?v=([0-9a-f]+)', page)
    assert m
    r = client.get(m.group(0))
    assert "immutable" in r.headers.get("Cache-Control", "")
    etag = r.headers.get("ETag")
    assert etag
    r2 = client.get(m.group(0), headers={"If-None-Match": etag})
    assert r2.status_code == 304


def test_other_static_files_untouched(client):
    r = client.get("/static/js/video.js")
    assert r.status_code == 200
    assert r.get_data() == (ROOT / "static/js/video.js").read_bytes()


def test_legal_links_wrap():
    assert ".legal a { overflow-wrap: anywhere; }" in SOURCE
