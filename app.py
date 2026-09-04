"""KuickKonvert -- free file conversion tools.

Every upload is processed in an isolated temp directory that is deleted the
moment the response has been sent (see converters.utils.job_workspace).
Nothing uploaded here is stored permanently. See PRIVACY_NOTICE.md.
"""
import os
import secrets
import zipfile

from flask import (
    Flask, render_template, request, send_file, abort, jsonify, url_for, Response, g
)
from markupsafe import Markup
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import (
    TOOLS, TOOLS_BY_SLUG, CATEGORIES, MAX_CONTENT_LENGTH, ALLOWED_EXTENSIONS,
    FORMAT_BADGE_CLASS, SITE_URL,
)
from converters.utils import job_workspace, safe_name, change_ext
from converters.office import (
    ConversionError, convert_office_to_pdf, convert_pdf_to_word, convert_pdf_to_ppt,
)
from converters.tables import convert_pdf_to_excel
from converters.images import images_to_pdf, pdf_to_images
from converters.pdf_tools import (
    merge_pdfs, split_pdf, rotate_pdf, watermark_pdf, protect_pdf, compress_pdf,
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


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
_CSP_DIRECTIVES = (
    "default-src 'self'; "
    "script-src 'self' https://www.googletagmanager.com 'nonce-{nonce}'; "
    "style-src 'self'; "
    "img-src 'self' data: https://www.googletagmanager.com https://www.google-analytics.com; "
    "connect-src 'self' https://www.google-analytics.com https://www.googletagmanager.com https://region1.google-analytics.com; "
    "font-src 'self'; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "form-action 'self'; "
    "frame-ancestors 'self'; "
    "frame-src 'none'"
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
        name = safe_name(f.filename)
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
    srcs = _save_uploads(files, job_dir, {"jpg", "jpeg"})
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
        canonical_url=f"{SITE_URL}/",
    )


@app.route("/tools/<slug>")
def tool_page(slug):
    tool = TOOLS_BY_SLUG.get(slug)
    if not tool:
        abort(404)
    accepted_formats = [ext.strip(".").upper() for ext in tool["accept"].split(",")]
    related_tools = [TOOLS_BY_SLUG[s] for s in tool.get("related", []) if s in TOOLS_BY_SLUG]
    return render_template(
        "tool.html",
        tool=tool,
        canonical_url=f"{SITE_URL}/tools/{slug}",
        accepted_formats=accepted_formats,
        related_tools=related_tools,
    )


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

    try:
        with job_workspace() as job_dir:
            out_path, download_name, mimetype = handler(files, request.form, job_dir)
            # send_file streams while the file exists; read fully into memory
            # first so we can safely delete the temp workspace on exit.
            with open(out_path, "rb") as fh:
                data = fh.read()
    except ConversionError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        app.logger.exception("Unhandled conversion error on %s", slug)
        return jsonify({"error": "Something went wrong during conversion. Please try again."}), 500

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


@app.route("/sitemap.xml")
def sitemap_xml():
    # Static pages plus every tool page, generated from the same TOOLS list
    # that drives the homepage grid, so a new tool is picked up automatically.
    # No <lastmod> is included -- it's optional per the sitemap protocol, and
    # this app has no reliable per-page "last changed" date to report rather
    # than guess one.
    urls = [
        f"{SITE_URL}/", f"{SITE_URL}/privacy", f"{SITE_URL}/about",
        f"{SITE_URL}/contact", f"{SITE_URL}/terms",
    ]
    urls += [f"{SITE_URL}/tools/{t['slug']}" for t in TOOLS]

    body = ['<?xml version="1.0" encoding="UTF-8"?>']
    body.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for u in urls:
        body.append(f"  <url><loc>{u}</loc></url>")
    body.append("</urlset>")
    return Response("\n".join(body), mimetype="application/xml")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File is too large. Please upload a smaller file."}), 413


@app.errorhandler(429)
def rate_limited(e):
    return jsonify({"error": "Too many requests -- please wait a moment and try again."}), 429


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
