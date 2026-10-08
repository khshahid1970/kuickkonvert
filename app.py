"""KuickKonvert -- free file conversion tools.

Every upload is processed in an isolated temp directory that is deleted the
moment the response has been sent (see converters.utils.job_workspace).
Nothing uploaded here is stored permanently. See PRIVACY_NOTICE.md.
"""
import os

# Added 2026-10-07: keep the number-crunching libraries (numpy's OpenBLAS,
# OpenCV used by pdf2docx) to ONE thread each. By default they start one
# thread per CPU they can see -- on Render that can be the whole host
# machine's CPU count, not our 1 CPU -- and every extra thread reserves
# memory. That reserved memory counts against the per-conversion memory cap
# (converters/isolate.py) and is the likely reason PDF to Word failed on
# Render on 7 Oct 2026 even for a 3-page file. Must run BEFORE numpy/OpenCV
# are imported (i.e. right here).
for _var in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
             "OPENCV_FOR_THREADS_NUM"):
    os.environ.setdefault(_var, "1")

import hashlib
import re
import secrets
import zipfile

from flask import (
    Flask, render_template, request, send_file, abort, jsonify, url_for, Response, g,
    redirect, send_from_directory,
)
from markupsafe import Markup, escape
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import (
    TOOLS, TOOLS_BY_SLUG, CATEGORIES, MAX_CONTENT_LENGTH, ALLOWED_EXTENSIONS,
    FORMAT_BADGE_CLASS, SITE_URL, GUIDES, GUIDES_BY_SLUG, GUIDES_BY_TOOL,
    HOME_LASTMOD, TOOLS_LASTMOD, GUIDES_LINKS_LASTMOD, STATIC_LASTMOD,
)
from converters.utils import job_workspace, safe_name, change_ext
from converters.isolate import run_isolated, JobFailed
from converters.office import (
    ConversionError, convert_office_to_pdf, convert_pdf_to_word, convert_pdf_to_ppt,
)
from converters.tables import convert_pdf_to_excel
from converters.images import images_to_pdf, pdf_to_images
from converters.pdf_tools import (
    merge_pdfs, split_pdf, rotate_pdf, watermark_pdf, protect_pdf, compress_pdf,
    ensure_pdf_unlocked,
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


# --- Static files: one-year browser cache with automatic version tags -----
# Added 2026-10-08 (phone-speed fix). Every url_for('static', ...) link gets
# "?v=<first 10 characters of the file's SHA-256>". Those versioned URLs are
# sent with a one-year cache (see _cache_versioned_static below), so a
# visitor's phone keeps style.css, the JS files and the icons instead of
# re-checking them with the server on every page view (that check took
# ~230 ms per page on 8 Oct 2026). When a file changes, its hash -- and so
# its URL -- changes too, so visitors get the new file straight away.
# Requests WITHOUT ?v (old links, hard-coded paths) keep Flask's default
# "no-cache" revalidation. Conversion downloads are not static files and
# are never affected.
_STATIC_VERSIONS = {}


def _static_version(filename):
    if filename not in _STATIC_VERSIONS:
        try:
            with open(os.path.join(app.static_folder, filename), "rb") as fh:
                _STATIC_VERSIONS[filename] = hashlib.sha256(fh.read()).hexdigest()[:10]
        except OSError:
            _STATIC_VERSIONS[filename] = ""
    return _STATIC_VERSIONS[filename]


@app.url_defaults
def _add_static_version(endpoint, values):
    if endpoint == "static" and "filename" in values and "v" not in values:
        version = _static_version(values["filename"])
        if version:
            values["v"] = version


@app.after_request
def _cache_versioned_static(response):
    if (request.endpoint == "static" and request.args.get("v")
            and response.status_code in (200, 304)):
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    return response


# --- Per-request CSP nonce -------------------------------------------------
# One random, unguessable value generated fresh for every request and used to
# allow exactly one specific inline <script> block (the Google Analytics
# gtag() init snippet in base.html) through the Content-Security-Policy below,
# without resorting to the much weaker 'unsafe-inline' (which would let ANY
# inline script run, including one injected by an attacker via a bug
# elsewhere on the page). A nonce is preferred here over a CSP hash of the
# script's exact text because a hash silently breaks (fails closed -- the
# script just stops running, no error shown to visitors) the moment anyone
# edits so much as a character of that inline block and forgets to
# regenerate the hash; a nonce keeps working no matter what the script says,
# since only base.html and this header need to agree on the nonce value, not
# on the script's content.
@app.before_request
def _set_csp_nonce():
    g.csp_nonce = secrets.token_urlsafe(16)


# --- Trailing-slash addresses -> 301 to the real page ----------------------
# Added 2026-10-08. Pages live at addresses WITHOUT a trailing slash
# (/tools/word-to-pdf). A link that adds one (/tools/word-to-pdf/) used to
# get "not found"; now it is sent permanently (301) to the real page, so the
# visitor lands on it and search engines treat both as one address.
# Only GET/HEAD (uploads and forms are never redirected), only when the
# address without the slash is a real route, the query string is kept,
# and never to "//..." (a browser would read that as another website).
@app.before_request
def _redirect_trailing_slash():
    path = request.path
    if request.method not in ("GET", "HEAD") or len(path) < 2 or not path.endswith("/"):
        return None
    target = path.rstrip("/")
    if not target or target.startswith("//") or "\\" in target:
        return None
    try:
        app.create_url_adapter(request).match(target, method="GET")
    except Exception:
        return None
    query = request.query_string.decode("utf-8", "replace")
    return redirect(target + ("?" + query if query else ""), code=301)


# --- Security headers -------------------------------------------------------
# Adds the standard baseline of browser-enforced hardening headers that were
# missing as of the 2026-09-04 external audit (securityheaders.com: grade D;
# Mozilla/MDN HTTP Observatory: 45/100, grade C-) -- only
# Strict-Transport-Security was previously set. TLS/certificate configuration
# itself was already excellent (SSL Labs: A+) and is untouched by this
# change; these headers hardens what the BROWSER does with content this app
# already serves, they do not change how the app serves it.
#
# Content-Security-Policy is scoped to exactly what this site actually loads
# (verified directly against every template, 2026-09-04): its own
# same-origin CSS/JS/images, Google Tag Manager's gtag.js loader plus the one
# inline init snippet (allowed via the per-request nonce above), and
# Google Analytics' own beacon/collection endpoints. There is currently no
# other third-party script, font, iframe, or CDN asset anywhere in the
# templates. The AdSense JS connector is intentionally still commented out
# (see the long comment above the AdSense meta tag in base.html -- it was
# swapped for a script-free verification meta tag to fix a severe CLS
# regression while the account is under review) -- so no AdSense domains are
# allowed yet. When that script is restored after AdSense approval, add
# https://pagead2.googlesyndication.com and https://googleads.g.doubleclick.net
# (and any other domain Google's own AdSense integration instructions name at
# that time -- these do shift over time, so don't assume this list is still
# current) to script-src, frame-src, and connect-src below, and give the
# real <ins class="adsbygoogle"> tag a nonce or move it to a CSP-exempt path,
# the same way the analytics inline script is handled here. Re-run a header
# scan after any CSP change -- a wrong CSP fails closed (breaks the feature
# it was blocking), it does not fail open.
# 2026-09-28: Google Ads conversion tracking (AW-18473004328) added. The
# extra domains below are the ones Google's "Use a Content Security Policy"
# guide lists for Google Ads conversions and for Google Analytics 4
# (developers.google.com/tag-platform/security/guides/csp). CSP does not allow
# wildcards for top-level domains, so each country Google domain must be
# listed on its own: google.com plus the main target markets' domains
# (Pakistan, India, UK) are included. A missing TLD only drops that one
# measurement ping silently; it never breaks the site.
# 2026-10-08: subdomain wildcards (*.google.com etc.), as that guide lists for
# Google Analytics: GA4 also sends hits to analytics.google.com, which the
# www-only list blocked (console error on every page view).
_GOOGLE_TLDS = "https://*.google.com https://*.google.com.pk https://*.google.co.in https://*.google.co.uk"
_CSP_DIRECTIVES = (
    "default-src 'self'; "
    "script-src 'self' https://www.googletagmanager.com https://www.googleadservices.com https://www.google.com 'nonce-{nonce}'; "
    "style-src 'self'; "
    "img-src 'self' data: https://www.googletagmanager.com https://*.google-analytics.com https://www.googleadservices.com "
    "https://googleads.g.doubleclick.net https://*.g.doubleclick.net https://pagead2.googlesyndication.com " + _GOOGLE_TLDS + " https://launchnest.io; "
    "connect-src 'self' https://www.googletagmanager.com https://*.google-analytics.com https://www.googleadservices.com "
    "https://googleads.g.doubleclick.net https://*.g.doubleclick.net https://pagead2.googlesyndication.com https://ad.doubleclick.net " + _GOOGLE_TLDS + "; "
    "font-src 'self'; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "form-action 'self'; "
    "frame-ancestors 'self'; "
    "frame-src https://www.googletagmanager.com"
)


@app.after_request
def _set_security_headers(response):
    is_https = request.is_secure or request.headers.get("X-Forwarded-Proto", "") == "https"
    if is_https:
        # max-age is 6 months (15768000s). includeSubDomains and preload are
        # intentionally still left off, per the original reasoning: preload
        # is effectively permanent once submitted (removal takes months
        # across browser vendors) and is a deliberate later decision, and
        # includeSubDomains would also force HTTPS on any future subdomain
        # (e.g. mail.kuickkonvert.com) whether or not it's ready for it.
        # Revisit once there's a firm reason to lock either in.
        response.headers.setdefault("Strict-Transport-Security", "max-age=15768000")

    response.headers.setdefault(
        "Content-Security-Policy",
        _CSP_DIRECTIVES.format(nonce=g.get("csp_nonce", "")),
    )
    # Legacy header kept alongside frame-ancestors above: frame-ancestors is
    # the modern replacement and is what current browsers actually honor,
    # but X-Frame-Options is still what a number of external scanners and
    # older tooling check for specifically, so both are set to the same
    # same-origin-only policy rather than relying on just one.
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    # Explicitly denies browser features this site has no use for. Extend
    # this list (rather than deleting entries) if a real feature is ever
    # added that genuinely needs one of them.
    response.headers.setdefault(
        "Permissions-Policy",
        "camera=(), microphone=(), geolocation=(), payment=(), usb=(), "
        "magnetometer=(), gyroscope=(), interest-cohort=()",
    )
    return response

# --- Rate limiting / abuse protection -------------------------------------
# Anonymous, no-login uploads are an obvious target for scripted abuse (mass
# automated conversions driving up compute cost, or someone hammering the
# endpoint to degrade the service for real visitors). Flask-Limiter throttles
# by client IP.
#
# PRODUCTION-GRADE CAVEAT (read before relying on this for capacity planning):
# storage defaults to in-memory, which is per-process, not shared. gunicorn
# runs 2 worker processes (see Procfile/Dockerfile), and each worker keeps
# its own counters -- so the *effective* ceiling per IP can run up to ~2x the
# configured number in the worst case (a client that gets routed roughly
# evenly across both workers). In-memory storage also resets on every
# deploy/restart and cannot coordinate across more than one dyno/instance if
# this app is ever scaled horizontally. This is a real limitation, not a
# hidden one -- it is an accepted Phase 1 trade-off (it still stops
# unthrottled scripted abuse today, and needs no new paid service), not a
# claim that this is exact, production-grade global rate limiting.
#
# To upgrade to a shared, worker-safe, restart-safe limit once Redis (or
# another supported backend -- see the Flask-Limiter docs for the current
# list) is available, set the RATE_LIMIT_STORAGE_URI environment variable,
# e.g. RATE_LIMIT_STORAGE_URI=redis://<host>:6379 -- no code change needed.
# Render offers a managed Redis add-on (a new, separate resource/cost on
# your Render account, not something this code can provision on its own).
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["120 per minute", "2000 per day"],
    storage_uri=os.environ.get("RATE_LIMIT_STORAGE_URI", "memory://"),
)


@app.template_global()
def obfuscated_mailto(email, label=None):
    """Renders a ready-to-use `<a href="mailto:...">label</a>` tag with both
    the href and the visible text written out as numeric HTML character
    entities (e.g. "a" -> "&#97;"). Browsers and screen readers decode these
    transparently, so the link looks and behaves exactly like a normal
    mailto link to a real visitor -- but the address never appears in the
    page's HTML source as consecutive plain-text characters, which is what
    the simple regex-based address harvesters that scrape plaintext mailto
    links look for. This is a standard, low-effort mitigation, not a claim
    of protection against a scraper that executes real JavaScript against
    the rendered DOM.
    """
    label = label or email

    def _entities(s):
        return "".join(f"&#{ord(ch)};" for ch in s)

    return Markup(f'<a href="mailto:{_entities(email)}">{_entities(label)}</a>')


# Guide text can link to a tool page with [[tool-slug|link text]] (added
# 8 Oct 2026, keyword plan Phase 2), e.g. "[[compress-pdf|PDF size
# reducer]]". Everything else in the text is HTML-escaped exactly as before,
# and an unknown slug falls back to plain text, so a typo can never produce
# a broken link or stray markup.
_TOOL_LINK_RE = re.compile(r"\[\[([a-z0-9-]+)\|([^\]|]+)\]\]")


@app.template_filter("tool_links")
def tool_links(text):
    parts = []
    pos = 0
    for m in _TOOL_LINK_RE.finditer(text or ""):
        parts.append(escape(text[pos:m.start()]))
        slug, label = m.group(1), m.group(2)
        if slug in TOOLS_BY_SLUG:
            parts.append(Markup('<a href="{}">{}</a>').format(
                url_for("tool_page", slug=slug), label))
        else:
            parts.append(escape(label))
        pos = m.end()
    parts.append(escape((text or "")[pos:]))
    return Markup("").join(parts)


@app.context_processor
def inject_site_url():
    """Makes {{ site_url }} available in every template without passing it
    from each view -- base.html uses it to build a canonical/OG URL fallback
    for any page (e.g. the 404 handler) that doesn't explicitly pass one."""
    return {"site_url": SITE_URL}


@app.context_processor
def inject_csp_nonce():
    """Makes {{ csp_nonce }} available in every template -- base.html applies
    it to the one inline <script> the Content-Security-Policy header (see
    _set_security_headers above) is configured to allow by nonce."""
    return {"csp_nonce": g.get("csp_nonce", "")}


def _ext_ok(filename, allowed):
    ext = os.path.splitext(filename or "")[1].lower().lstrip(".")
    return ext in allowed


# ---- File names -------------------------------------------------------
# Two different names are used for every upload:
#   * _storage_name(): a safe ASCII name for the TEMPORARY copy on our server
#     (protects against path tricks like "../../"). It always keeps the file
#     extension, so a file named entirely in Urdu/Arabic/Hindi letters is
#     stored as "file.pdf" instead of an extension-less "pdf".
#   * _display_stem(): the user's ORIGINAL name, used for the download, so
#     "My Report (Final).pdf" comes back as "My Report (Final).pdf" (or
#     ".docx" etc. for conversions) -- not "My_Report_Final.pdf". Only
#     characters Windows/macOS forbid in file names are replaced.
_FORBIDDEN_IN_FILENAMES = set('\\/:*?"<>|')


def _storage_name(filename):
    ext = os.path.splitext(filename or "")[1].lower()
    if not re.fullmatch(r"\.[a-z0-9]{1,5}", ext):
        ext = ""
    stem = os.path.splitext(safe_name(filename))[0]
    if not stem or stem.lower() == ext.lstrip("."):
        stem = "file"
    return stem + ext


def _display_stem(filename):
    base = (filename or "").replace("\\", "/").rsplit("/", 1)[-1]
    stem = os.path.splitext(base)[0]
    stem = "".join(
        "_" if (c in _FORBIDDEN_IN_FILENAMES or ord(c) < 32) else c for c in stem
    ).strip().strip(".")
    return stem[:150] or "file"


def _save_uploads(files, job_dir, allowed_exts):
    """Validate and save every uploaded file into job_dir. Returns saved paths in order."""
    if not files:
        raise ConversionError("Please choose at least one file to upload.")
    saved = []
    for f in files:
        if not f or not f.filename:
            continue
        if not _ext_ok(f.filename, allowed_exts):
            raise ConversionError(
                f"'{f.filename}' has an unsupported file type for this tool."
            )
        name = _storage_name(f.filename)
        path = os.path.join(job_dir, name)
        # avoid collisions when two uploads share a sanitized name
        i = 1
        base, ext = os.path.splitext(path)
        while os.path.exists(path):
            path = f"{base}({i}){ext}"
            i += 1
        f.save(path)
        if os.path.getsize(path) == 0:
            raise ConversionError(f"'{f.filename}' is empty.")
        if path.lower().endswith(".pdf"):
            ensure_pdf_unlocked(path, f"'{f.filename}'")
        saved.append(path)
    if not saved:
        raise ConversionError("Please choose at least one file to upload.")
    return saved


def _zip_files(paths, zip_path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in paths:
            zf.write(p, arcname=os.path.basename(p))
    return zip_path


# ---- Per-tool handlers ------------------------------------------------
# Each handler: (files, form, job_dir) -> (output_path, download_name, mimetype)

def h_word_to_pdf(files, form, job_dir):
    [src] = _save_uploads(files, job_dir, {"doc", "docx"})
    out = convert_office_to_pdf(src, job_dir)
    return out, change_ext(os.path.basename(src), "pdf"), "application/pdf"


def h_excel_to_pdf(files, form, job_dir):
    [src] = _save_uploads(files, job_dir, {"xls", "xlsx"})
    out = convert_office_to_pdf(src, job_dir)
    return out, change_ext(os.path.basename(src), "pdf"), "application/pdf"


def h_ppt_to_pdf(files, form, job_dir):
    [src] = _save_uploads(files, job_dir, {"ppt", "pptx"})
    out = convert_office_to_pdf(src, job_dir)
    return out, change_ext(os.path.basename(src), "pdf"), "application/pdf"


def h_pdf_to_word(files, form, job_dir):
    [src] = _save_uploads(files, job_dir, {"pdf"})
    out = convert_pdf_to_word(src, job_dir)
    return out, change_ext(os.path.basename(src), "docx"), (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


def h_pdf_to_excel(files, form, job_dir):
    [src] = _save_uploads(files, job_dir, {"pdf"})
    out = convert_pdf_to_excel(src, job_dir)
    return out, change_ext(os.path.basename(src), "xlsx"), (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


def h_pdf_to_ppt(files, form, job_dir):
    [src] = _save_uploads(files, job_dir, {"pdf"})
    out = convert_pdf_to_ppt(src, job_dir)
    return out, change_ext(os.path.basename(src), "pptx"), (
        "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )


def h_jpg_to_pdf(files, form, job_dir):
    # Also accepts PNG (since 8 Oct 2026), so this page can serve "image to
    # PDF" searches; images_to_pdf() already handles JPG and PNG together.
    srcs = _save_uploads(files, job_dir, {"jpg", "jpeg", "png"})
    out = os.path.join(job_dir, "converted.pdf")
    images_to_pdf(srcs, out)
    name = "images.pdf" if len(srcs) > 1 else change_ext(os.path.basename(srcs[0]), "pdf")
    return out, name, "application/pdf"


def h_png_to_pdf(files, form, job_dir):
    srcs = _save_uploads(files, job_dir, {"png"})
    out = os.path.join(job_dir, "converted.pdf")
    images_to_pdf(srcs, out)
    name = "images.pdf" if len(srcs) > 1 else change_ext(os.path.basename(srcs[0]), "pdf")
    return out, name, "application/pdf"


def h_pdf_to_jpg(files, form, job_dir):
    [src] = _save_uploads(files, job_dir, {"pdf"})
    pages = pdf_to_images(src, job_dir, fmt="jpg")
    if len(pages) == 1:
        return pages[0], change_ext(os.path.basename(src), "jpg"), "image/jpeg"
    zpath = os.path.join(job_dir, "pages.zip")
    _zip_files(pages, zpath)
    return zpath, change_ext(os.path.basename(src), "zip"), "application/zip"


def h_pdf_to_png(files, form, job_dir):
    [src] = _save_uploads(files, job_dir, {"pdf"})
    pages = pdf_to_images(src, job_dir, fmt="png")
    if len(pages) == 1:
        return pages[0], change_ext(os.path.basename(src), "png"), "image/png"
    zpath = os.path.join(job_dir, "pages.zip")
    _zip_files(pages, zpath)
    return zpath, change_ext(os.path.basename(src), "zip"), "application/zip"


def h_merge_pdf(files, form, job_dir):
    srcs = _save_uploads(files, job_dir, {"pdf"})
    if len(srcs) < 2:
        raise ConversionError("Add at least two PDFs to merge.")
    out = os.path.join(job_dir, "merged.pdf")
    merge_pdfs(srcs, out)
    return out, "merged.pdf", "application/pdf"


def h_split_pdf(files, form, job_dir):
    [src] = _save_uploads(files, job_dir, {"pdf"})
    pages = split_pdf(src, job_dir)
    if len(pages) == 1:
        return pages[0], change_ext(os.path.basename(src), "pdf"), "application/pdf"
    zpath = os.path.join(job_dir, "split-pages.zip")
    _zip_files(pages, zpath)
    return zpath, change_ext(os.path.basename(src), "zip"), "application/zip"


def h_compress_pdf(files, form, job_dir):
    [src] = _save_uploads(files, job_dir, {"pdf"})
    level = form.get("level", "ebook")
    out = os.path.join(job_dir, "compressed.pdf")
    compress_pdf(src, out, level=level)
    return out, change_ext(os.path.basename(src), "pdf"), "application/pdf"


def h_rotate_pdf(files, form, job_dir):
    [src] = _save_uploads(files, job_dir, {"pdf"})
    degrees = form.get("degrees", "90")
    try:
        degrees = int(degrees)
    except ValueError:
        raise ConversionError("Rotation must be 90, 180, or 270 degrees.")
    out = os.path.join(job_dir, "rotated.pdf")
    rotate_pdf(src, out, degrees)
    return out, change_ext(os.path.basename(src), "pdf"), "application/pdf"


def h_watermark_pdf(files, form, job_dir):
    [src] = _save_uploads(files, job_dir, {"pdf"})
    text = (form.get("text") or "").strip()
    if not text:
        raise ConversionError("Enter the text you want watermarked onto every page.")
    out = os.path.join(job_dir, "watermarked.pdf")
    watermark_pdf(src, out, text)
    return out, change_ext(os.path.basename(src), "pdf"), "application/pdf"


def h_protect_pdf(files, form, job_dir):
    [src] = _save_uploads(files, job_dir, {"pdf"})
    password = form.get("password") or ""
    out = os.path.join(job_dir, "protected.pdf")
    protect_pdf(src, out, password)
    return out, change_ext(os.path.basename(src), "pdf"), "application/pdf"


HANDLERS = {
    "word-to-pdf": h_word_to_pdf,
    "excel-to-pdf": h_excel_to_pdf,
    "ppt-to-pdf": h_ppt_to_pdf,
    "pdf-to-word": h_pdf_to_word,
    "pdf-to-excel": h_pdf_to_excel,
    "pdf-to-ppt": h_pdf_to_ppt,
    "jpg-to-pdf": h_jpg_to_pdf,
    "png-to-pdf": h_png_to_pdf,
    "pdf-to-jpg": h_pdf_to_jpg,
    "pdf-to-png": h_pdf_to_png,
    "merge-pdf": h_merge_pdf,
    "split-pdf": h_split_pdf,
    "compress-pdf": h_compress_pdf,
    "rotate-pdf": h_rotate_pdf,
    "watermark-pdf": h_watermark_pdf,
    "protect-pdf": h_protect_pdf,
}


# ---- Routes -------------------------------------------------------------

@app.route("/")
def index():
    by_category = {c: [t for t in TOOLS if t["category"] == c] for c in CATEGORIES}
    return render_template(
        "index.html",
        categories=CATEGORIES,
        by_category=by_category,
        badge_class=FORMAT_BADGE_CLASS,
        guides=GUIDES,
        canonical_url=f"{SITE_URL}/",
    )


@app.route("/tools/<slug>")
def tool_page(slug):
    tool = TOOLS_BY_SLUG.get(slug)
    if not tool:
        abort(404)
    accepted_formats = [ext.strip(".").upper() for ext in tool["accept"].split(",")]
    related_tools = [TOOLS_BY_SLUG[s] for s in tool.get("related", []) if s in TOOLS_BY_SLUG]
    related_guides = GUIDES_BY_TOOL.get(slug, [])
    return render_template(
        "tool.html",
        tool=tool,
        canonical_url=f"{SITE_URL}/tools/{slug}",
        accepted_formats=accepted_formats,
        related_tools=related_tools,
        related_guides=related_guides,
    )


@app.route("/guides")
def guides_index():
    return render_template(
        "guides_index.html",
        guides=GUIDES,
        canonical_url=f"{SITE_URL}/guides",
    )


@app.route("/guides/<slug>")
def guide_page(slug):
    guide = GUIDES_BY_SLUG.get(slug)
    if not guide:
        abort(404)
    related_tools = [
        TOOLS_BY_SLUG[s] for s in guide.get("related_tools", []) if s in TOOLS_BY_SLUG
    ]
    return render_template(
        "guide.html",
        guide=guide,
        canonical_url=f"{SITE_URL}/guides/{slug}",
        related_tools=related_tools,
    )


# At most this many conversions run at the same time in each gunicorn worker
# (2 workers -> 2 in total with the default of 1). Other requests wait their
# turn instead of all running at once. Added 2026-10-05 after three
# out-of-memory restarts on the 2 GB instance; default lowered from 2 to 1 on
# 2026-10-07 after two more. If the wait is too long the visitor gets a clear
# "busy" message. Can be changed with the CONVERT_SLOTS setting on Render.
# Each conversion also runs in its own memory-capped child process
# (converters/isolate.py), so one oversized file fails on its own instead of
# restarting the whole server.
import threading as _threading
_CONVERT_SLOTS = _threading.BoundedSemaphore(int(os.environ.get("CONVERT_SLOTS", "1")))


@app.route("/convert/<slug>", methods=["POST"])
@limiter.limit("10 per minute; 100 per hour")
def convert(slug):
    tool = TOOLS_BY_SLUG.get(slug)
    handler = HANDLERS.get(slug)
    if not tool or not handler:
        abort(404)

    files = request.files.getlist("file")
    if not tool.get("multi") and len(files) > 1:
        files = files[:1]

    if not _CONVERT_SLOTS.acquire(timeout=90):
        return jsonify({"error": "The converter is busy right now. Please try again in a minute."}), 503
    try:
        with job_workspace() as job_dir:
            out_path, download_name, mimetype = run_isolated(
                handler, (files, request.form, job_dir), ConversionError
            )
            # Give the download the user's original file name. Handlers build
            # download_name from the safe storage name of the first upload;
            # when that's the case, swap in the original name (keeping the
            # new extension). Fixed names like "merged.pdf" are left alone.
            first = next((f.filename for f in files if f and f.filename), None)
            if first:
                base, ext = os.path.splitext(download_name)
                if base == os.path.splitext(_storage_name(first))[0]:
                    download_name = _display_stem(first) + ext
            # send_file streams while the file exists; read fully into memory
            # first so we can safely delete the temp workspace on exit.
            with open(out_path, "rb") as fh:
                data = fh.read()
    except ConversionError as exc:
        return jsonify({"error": str(exc)}), 400
    except JobFailed as exc:
        # Memory cap or time limit hit in the child process. Logged without
        # the file name (privacy); the visitor gets a clear message.
        app.logger.warning("Conversion stopped on %s (%s)", slug, exc.detail)
        return jsonify({"error": str(exc)}), 413
    except Exception as exc:
        app.logger.exception("Unhandled conversion error on %s", slug)
        return jsonify({"error": "Something went wrong during conversion. Please try again."}), 500
    finally:
        _CONVERT_SLOTS.release()

    import io
    return send_file(
        io.BytesIO(data),
        mimetype=mimetype,
        as_attachment=True,
        download_name=download_name,
    )


@app.route("/privacy")
def privacy():
    return render_template("privacy.html", canonical_url=f"{SITE_URL}/privacy")


@app.route("/about")
def about():
    return render_template("about.html", canonical_url=f"{SITE_URL}/about")


@app.route("/contact")
def contact():
    return render_template("contact.html", canonical_url=f"{SITE_URL}/contact")


@app.route("/terms")
def terms():
    return render_template("terms.html", canonical_url=f"{SITE_URL}/terms")


# Added 2026-10-08: some browsers and crawlers ask for /favicon.ico directly
# (it used to return "not found"). Serve the same icon the pages declare.
@app.route("/favicon.ico")
@limiter.exempt
def favicon():
    response = send_from_directory(
        os.path.join(app.static_folder, "img"), "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )
    response.headers["Cache-Control"] = "public, max-age=604800"
    return response


@app.route("/robots.txt")
def robots_txt():
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /convert/\n"
        f"\nSitemap: {SITE_URL}/sitemap.xml\n"
    )
    return Response(body, mimetype="text/plain")


@app.route("/ads.txt")
def ads_txt():
    # Required by Google AdSense so ad exchanges can confirm KuickKonvert is
    # an authorized seller of its own ad inventory. Format and the trailing
    # certification ID (f08c47fec0942fa0) are Google's fixed standard for
    # every AdSense publisher -- verified against Google's own AdSense Help
    # documentation on 2026-08-29, not something specific to this site.
    body = "google.com, pub-2468332370767807, DIRECT, f08c47fec0942fa0\n"
    return Response(body, mimetype="text/plain")


# IndexNow (https://www.indexnow.org) lets Bing, Yandex, Seznam and Naver
# learn about new or changed pages straight away. The protocol requires a key
# file at the site root: /<key>.txt whose only content is the key itself.
# This key is PUBLIC by design (search engines fetch it to confirm the site
# owner) -- it is not a password. Google does not use IndexNow.
INDEXNOW_KEY = "2408c240ba6c3916f8e395b4fdafec43"


@app.route(f"/{INDEXNOW_KEY}.txt")
def indexnow_key():
    return Response(INDEXNOW_KEY, mimetype="text/plain")


# Yandex Webmaster site-ownership check. Yandex asks for this exact file at
# the site root (HTML-file verification method). Keep it live so the site
# stays verified in Yandex Webmaster -- do not delete this route.
YANDEX_VERIFICATION_FILE = "yandex_1756538b996a2a41.html"
YANDEX_VERIFICATION_BODY = (
    "<html>\n"
    "    <head>\n"
    '        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n'
    "    </head>\n"
    "    <body>Verification: 1756538b996a2a41</body>\n"
    "</html>\n"
)


@app.route(f"/{YANDEX_VERIFICATION_FILE}")
def yandex_verification():
    return Response(YANDEX_VERIFICATION_BODY, mimetype="text/html")


@app.route("/sitemap.xml")
def sitemap_xml():
    # Static pages plus every tool page, generated from the same TOOLS list
    # that drives the homepage grid, so a new tool is picked up automatically.
    # <lastmod> is only included where there is a genuinely accurate date.
    # Google uses <lastmod> only when it is "consistently and verifiably
    # accurate", so a page with no known date is listed without one rather
    # than guessed.
    #   * privacy, about, contact, terms and the guides list: STATIC_LASTMOD
    #     in config.py (since 8 Oct 2026);
    #   * home page and tool pages: HOME_LASTMOD / TOOLS_LASTMOD in config.py
    #     (since 8 Oct 2026), or a tool's own "lastmod" key;
    #   * guides: the latest of the guide's own "updated"/"published" date
    #     and GUIDES_LINKS_LASTMOD (the last time links were added to every
    #     guide -- Google counts new links as a significant change, but they
    #     don't warrant a visible "Updated" date on the page).
    # When a page changes significantly, bump the matching date in config.py
    # (for a guide's own text, add/refresh its "updated": "YYYY-MM-DD").
    entries = [
        (f"{SITE_URL}/", HOME_LASTMOD),
        (f"{SITE_URL}/privacy", STATIC_LASTMOD.get("privacy")),
        (f"{SITE_URL}/about", STATIC_LASTMOD.get("about")),
        (f"{SITE_URL}/contact", STATIC_LASTMOD.get("contact")),
        (f"{SITE_URL}/terms", STATIC_LASTMOD.get("terms")),
        (f"{SITE_URL}/guides", STATIC_LASTMOD.get("guides")),
    ]
    entries += [
        (f"{SITE_URL}/tools/{t['slug']}", t.get("lastmod") or TOOLS_LASTMOD)
        for t in TOOLS
    ]
    entries += [
        (f"{SITE_URL}/guides/{g['slug']}",
         max(d for d in (g.get("updated"), g.get("published"), GUIDES_LINKS_LASTMOD) if d))
        for g in GUIDES
    ]

    body = ['<?xml version="1.0" encoding="UTF-8"?>']
    body.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for loc, lastmod in entries:
        if lastmod:
            body.append(f"  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod></url>")
        else:
            body.append(f"  <url><loc>{loc}</loc></url>")
    body.append("</urlset>")
    return Response("\n".join(body), mimetype="application/xml")


@app.errorhandler(404)
def not_found(e):
    # is_error_page: base.html then leaves out the canonical/og:url tags.
    return render_template("404.html", is_error_page=True), 404


@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File is too large. Please upload a smaller file."}), 413


@app.errorhandler(429)
def rate_limited(e):
    return jsonify({"error": "Too many requests -- please wait a moment and try again."}), 429


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html", is_error_page=True), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
