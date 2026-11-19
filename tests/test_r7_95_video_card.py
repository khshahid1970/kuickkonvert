"""R7-95 (19 Nov 2026): one smaller, horizontal (16:9) video card on every page
with a video, placed after the tool content and directly above the footer.
The video name on the page, in the VideoObject markup and on YouTube is the same
text (the YouTube title without the " | KuickKonvert #..." suffix).
Run from the repo root:
    python -m pytest -q tests/test_r7_95_video_card.py
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

ROOT = Path(kk.__file__).resolve().parent
TOOL_SLUGS = [k for k in config.VIDEOS if k not in ("home", "all-tools")]
PAGES = [("/", "home"), ("/tools", "all-tools")] + [("/tools/" + s, s) for s in TOOL_SLUGS]


@pytest.fixture(scope="module")
def client():
    # Many page renders in one module; rate limits are not under test here.
    was = kk.limiter.enabled
    kk.limiter.enabled = False
    yield kk.app.test_client()
    kk.limiter.enabled = was
    kk.limiter.reset()


def _get(client, path, country):
    r = client.get(path, headers={"CF-IPCountry": country})
    assert r.status_code == 200, path
    return r.data.decode()


def _main(page):
    return re.search(r"<main\b.*?</main>", page, re.S).group(0)


def test_r7_95_every_video_has_a_title_for_all_23_pages():
    assert len(PAGES) == 23
    assert set(config.R7_95_VIDEO_TITLES) == set(config.VIDEOS)
    for key, video in config.VIDEOS.items():
        assert video["title"] == config.R7_95_VIDEO_TITLES[key]


def test_r7_95_titles_follow_the_copy_rules():
    banned = ["secure", "100%", "unlimited", "no limits", "no waiting", "no ads", "fastest",
              "best", "no catch", "every time", "guaranteed", "instant", "quick", "one click"]
    for key, title in config.R7_95_VIDEO_TITLES.items():
        low = title.lower()
        assert not [w for w in banned if w in low], (key, title)
        assert len(title) <= 100 - len(" | KuickKonvert"), (key, title)


@pytest.mark.parametrize("path,key", PAGES)
@pytest.mark.parametrize("country", ["PK", "DE"])
def test_r7_95_one_card_after_the_tool_and_last_in_main(client, path, key, country):
    page = _get(client, path, country)
    main = _main(page)
    assert main.count('class="kk-video-block"') == 1, path
    block_at = main.index('class="kk-video-block"')
    # the tool (upload form on tool pages, tool grid on home and /tools) comes first
    if path.startswith("/tools/"):
        assert main.index("<form") < block_at, path
    else:
        # every tool link of the grid comes before the card
        for slug in TOOL_SLUGS:
            assert main.index(f'href="/tools/{slug}"') < block_at, (path, slug)
    # nothing visible after the card inside <main>: only closing tags and scripts
    end = main.index("</section>", block_at) + len("</section>")
    rest = re.sub(r"<script\b.*?</script>", "", main[end:], flags=re.S)
    assert not re.sub(r"</?(div|section|main)\b[^>]*>", "", rest).strip(), (path, rest[:200])
    # the footer comes after </main>
    assert page.index("</main>") < page.index("<footer"), path
    # the video name is the heading of the card
    title = config.R7_95_VIDEO_TITLES[key]
    h2 = re.search(r'<h2 id="kk-video-heading">(.*?)</h2>', main, re.S).group(1)
    assert _html.unescape(h2).strip() == title, path
    # consent regions get the link version; others get click-to-play
    if country == "DE":
        assert 'class="kk-video kk-video--link"' in main and "data-yt=" not in main
    else:
        assert f'data-yt="{config.VIDEOS[key]["id"]}"' in main


@pytest.mark.parametrize("path,key", PAGES)
def test_r7_95_videoobject_name_equals_the_card_title(client, path, key):
    page = _get(client, path, "PK")
    names = []
    for raw in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', page, re.S):
        data = json.loads(raw)
        for item in data if isinstance(data, list) else [data]:
            if item.get("@type") == "VideoObject":
                names.append(item["name"])
                assert config.VIDEOS[key]["id"] in json.dumps(item) or item.get("thumbnailUrl")
    assert names == [config.R7_95_VIDEO_TITLES[key]], path


def test_r7_95_css_horizontal_16x9_box_and_player_size():
    css = (ROOT / "static/css/style.css").read_text()
    assert re.search(r"\.kk-video-block \.kk-video, \.kk-video-block \.kk-video\.kk-video--link\s*\{"
                     r"[^}]*width:\s*320px;[^}]*aspect-ratio:\s*16 / 9", css)
    assert re.search(r"\.kk-video-block \.kk-video img\s*\{[^}]*object-fit:\s*contain", css)
    assert re.search(r"\.kk-video-block \.kk-video:has\(iframe\)\s*\{[^}]*width:\s*270px", css)
    # the R7-95 rules come after the base .kk-video rules so they win the cascade
    assert css.index(".kk-video-block .kk-video img") > css.index(".kk-video img, .kk-video-frame")
    js = (ROOT / "static/js/video.js").read_text()
    assert 'f.width = "270";' in js and 'f.height = "480";' in js
