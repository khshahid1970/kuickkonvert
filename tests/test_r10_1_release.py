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


# ---- Release 10.2 (26 Nov 2026): remaining "works in any browser" wording ---------------
def test_r10_2_guides_say_conversion_runs_on_our_server():
    client = kk.app.test_client()
    split = _text(client.get("/guides/how-to-split-pdf-files", headers={"CF-IPCountry": "US"}).data.decode())
    hub = _text(client.get("/guides", headers={"CF-IPCountry": "US"}).data.decode())
    email = _text(client.get("/guides/reduce-pdf-size-for-email", headers={"CF-IPCountry": "US"}).data.decode())
    new_dek = ("You open it in any web browser, on a computer or a phone, and the splitting runs on our "
               "server, so there’s nothing to install.")
    assert new_dek in split and new_dek in hub
    assert "Split a PDF online, from any browser" in split
    assert "You can do this from any browser, on a computer or a phone; the compression runs on our server:" in email
    for t in (split, hub, email):
        assert "It works in any web browser, on a computer or a phone, with nothing to install." not in t
        assert "This works in any browser" not in t


# ---- Release 10.3 (26 Nov 2026): Gunicorn keep-alive behind Render's proxy --------------
def test_r10_3_dockerfile_sets_keep_alive_and_keeps_other_settings():
    import json as _json
    line = [l for l in (ROOT / "Dockerfile").read_text(encoding="utf-8").splitlines() if l.startswith("CMD ")]
    assert len(line) == 1
    cmd = _json.loads(line[0][4:])
    assert cmd[:2] == ["gunicorn", "app:app"]
    args = dict(zip(cmd[2::2], cmd[3::2]))
    assert args == {"--bind": "0.0.0.0:8080", "--workers": "2", "--threads": "4", "--timeout": "180",
                    "--keep-alive": "120", "--max-requests": "200", "--max-requests-jitter": "50"}
