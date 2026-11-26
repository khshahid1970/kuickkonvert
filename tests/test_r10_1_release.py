"""Release 10.1 (26 Nov 2026): home-page wording says the conversion runs on our server
(Google's AI Overview had said the tools "run directly in your browser"), and the
"Choose file" label no longer carries role="button" (axe rule aria-allowed-role)."""
import re
import sys
from pathlib import Path
import html as _h

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import app as kk  # noqa: E402
import config  # noqa: E402


def _text(html):
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S)
    return re.sub(r"\s+", " ", _h.unescape(re.sub(r"<[^>]+>", " ", html)))


def test_home_says_conversion_runs_on_our_server():
    html = kk.app.test_client().get("/", headers={"CF-IPCountry": "US"}).data.decode()
    text = _text(html)
    assert ("No software, plugins or browser extensions — open the page in any modern browser "
            "and the conversion runs on our server.") in text
    assert "Nothing to install. Converted on our server." in text
    assert "it just works in any modern browser" not in text
    assert "Works in any browser" not in text


def test_choose_file_label_has_no_button_role_but_stays_focusable():
    client = kk.app.test_client()
    for slug in [t["slug"] for t in config.TOOLS]:
        html = client.get(f"/tools/{slug}", headers={"CF-IPCountry": "US"}).data.decode()
        label = re.search(r'<label[^>]*id="file-input-label"[^>]*>', html).group(0)
        assert 'role="button"' not in label, slug
        assert 'tabindex="0"' in label and 'for="file-input"' in label, slug


def test_keyboard_handler_for_choose_file_label_still_present():
    js = (ROOT / "static" / "js" / "main.js").read_text(encoding="utf-8")
    assert 'getElementById("file-input-label")' in js
    assert 'chooseLabel.addEventListener("keydown"' in js
