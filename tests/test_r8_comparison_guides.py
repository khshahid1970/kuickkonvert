"""Release 8, R8-01/R8-02 (20 Nov 2026): five comparison guides and two dek answers."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app as kk  # noqa: E402
import config  # noqa: E402

NEW = ["jpg-vs-jpeg", "jpg-vs-pdf", "png-vs-pdf", "excel-vs-pdf", "webp-vs-jpg-vs-png"]
BANNED_ANYWHERE = ["secure", "security", "100%", "unlimited", "no limits", "fastest", "best",
                   "guaranteed", "instantly", "private by design", "in your browser", "ocr"]


def _get(path):
    r = kk.app.test_client().get(path)
    assert r.status_code == 200, path
    return r.data.decode()


def test_new_guides_registered_and_linked():
    sm = _get("/sitemap.xml")
    index = _get("/guides")
    for slug in NEW:
        g = config.GUIDES_BY_SLUG[slug]
        assert g["published"] == config.R8_DATE
        assert f"/guides/{slug}</loc>" in sm, slug
        assert f'/guides/{slug}"' in index, slug
        assert "[[" in g["dek"], slug                      # direct answer ends with a tool link
        assert g["sources"] and all(u.startswith("https://") for _, u in g["sources"])
        assert 3 <= len(config.RELATED_GUIDES[slug]) <= 5   # R10.4: pillar (and sub-pillar) added first
        assert any(slug in v for k, v in config.RELATED_GUIDES.items() if k != slug), slug  # inbound link
        for t in g["related_tools"]:
            assert g in config.GUIDES_BY_TOOL[t], (slug, t)


def test_new_guides_copy_rules():
    for slug in NEW:
        g = config.GUIDES_BY_SLUG[slug]
        blob = " ".join([g["title"], g["seo_title"], g["meta_description"], g["dek"]] +
                        [" ".join(s.get("paragraphs", []) + s.get("steps", [])) for s in g["sections"]] +
                        [" ".join(" ".join(r) for r in s["table"]["rows"]) + " " + s["table"].get("note", "")
                         for s in g["sections"] if s.get("table")]).lower()
        hits = [w for w in BANNED_ANYWHERE if re.search(r"\b" + re.escape(w) + r"\b", blob)]
        assert not hits, (slug, hits)
        assert len(g["seo_title"]) <= 60 and 120 <= len(g["meta_description"]) <= 160, slug


def test_new_guides_numbers_match_test_results():
    # Spot checks against r8-test-results.json (20 Nov 2026).
    d = {s: config.GUIDES_BY_SLUG[s]["dek"] for s in NEW}
    assert "1,824 KB" in d["jpg-vs-pdf"] and "1,827 KB" in d["jpg-vs-pdf"]
    assert "113 KB to 114 KB" in d["png-vs-pdf"] and "28 KB" in d["png-vs-pdf"]
    assert "24 formulas" in d["excel-vs-pdf"] and "2-page PDF" in d["excel-vs-pdf"]
    assert "608 KB" in d["webp-vs-jpg-vs-png"] and "1,762 KB" in d["webp-vs-jpg-vs-png"]


def test_r8_dek_answers_and_dates():
    for slug, lead in config._R8_DEK_ANSWERS.items():
        html = _get(f"/guides/{slug}")
        assert lead.strip().split(":")[0] in html, slug
        assert f'Updated <time datetime="{config.RELEASE10_DATE}"' in html, slug   # R10 part 5
    # The six guides Microsoft Copilot cites keep their text and dates.
    for slug in ("docx-vs-doc", "jpg-vs-png", "why-pdf-layout-shifts",
                 "pdf-to-excel-table-conversion-results", "ppt-vs-pptx", "pdf-compression-levels-explained"):
        assert config.GUIDES_BY_SLUG[slug].get("updated") != config.R8_DATE, slug
