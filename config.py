import os
from datetime import date as _date

# Canonical site origin (no trailing slash). Used to build absolute canonical
# URLs, Open Graph/Twitter URLs, and the sitemap -- always the primary custom
# domain, even when a visitor is browsing via the onrender.com URL, so search
# engines consolidate both origins onto one canonical address instead of
# treating them as duplicate content.
SITE_URL = "https://kuickkonvert.com"

# <lastmod> dates for sitemap.xml -- the date of the last SIGNIFICANT change
# to each group of pages. Google counts changes to the main content, the
# structured data or the links on a page as significant (a footer year is
# not), and only trusts <lastmod> while it stays accurate, so bump the
# matching date whenever those pages change. A single tool can override
# TOOLS_LASTMOD with its own "lastmod" key in TOOL_CONTENT below.
# 8 Oct 2026: new titles/H1s/headings/FAQs on the home page and all 16 tool
# pages (keyword plan Phase 1), and new links to the tools inside every
# guide (Phase 2).
# 9 Oct 2026: home page only -- "file converter" wording added to the hero
# line and the Why KuickKonvert intro (title and H1 unchanged). Tool pages
# did not change, so TOOLS_LASTMOD stays on 8 Oct.
# RELEASE_DATE = the day the "forensic audit fixes + image tools" release goes
# live. It dates every page whose own content changes in that release:
#   * home page (4 new tool cards, FAQ wording), all tool pages (new "How to"
#     steps; 4 new tools; corrected FAQs), the JPG vs PNG guide (new links),
#   * About, Privacy and Terms (corrected/finalised text; the Privacy "Last
#     updated" and Terms "Effective date" lines show RELEASE_DATE_TEXT).
# Other pages only gain the 4 new links in the site menu, which isn't a change
# to their own content, so they keep their dates.
# Change this ONE date if the release moves to another day.
RELEASE_DATE = "2026-10-10"
RELEASE_DATE_TEXT = _date.fromisoformat(RELEASE_DATE).strftime("%-d %B %Y")
# FIX_RELEASE_DATE = the day the follow-up fix release goes live (consent
# banner v2 + "Cookie settings", test results in 4 guides, JPG to PDF
# orientation fix + wording, JSON-LD and meta fixes, /healthz). The Privacy
# notice is deliberately NOT part of it (wording on hold), so its "Last
# updated" line and sitemap date stay on RELEASE_DATE.
# >>> OWNER: set this to the ACTUAL deploy day (YYYY-MM-DD) before you
# commit, if it is not 11 Oct 2026. <<<
# It dates ONLY the pages whose own content changes in that release:
#   * the 4 guides given test results (what-is-a-heic-file,
#     location-data-in-photos, what-is-a-webp-image,
#     submitting-coursework-as-a-pdf) and the 2 guides whose JPG to PDF
#     wording was corrected (jpg-vs-png, photos-to-one-pdf-jpg-to-pdf-tips):
#     their "Updated" line, Article dateModified and sitemap <lastmod>;
#   * the JPG to PDF tool page (its own "lastmod" key): wording corrected and
#     sideways phone photos kept upright again.
# RELEASE_DATE above is deliberately NOT moved: it also dates the Terms
# "Effective date" and every tool page, which this release doesn't change.
FIX_RELEASE_DATE = "2026-10-11"
# SEO_FIX_RELEASE_DATE = the day the 12 Oct 2026 SEO fixes go live: Article
# markup on every guide gains "image" and author "url", and the Organization
# logo (read by Google from the home page) points to the square logo. Google
# counts structured-data changes as significant, so ONLY the sitemap <lastmod>
# of the home page and the 18 guides moves to this date. Nothing visible
# changes: a guide's "Updated" line and Article dateModified stay as they are.
# >>> OWNER: set this to the ACTUAL deploy day (YYYY-MM-DD) before you
# commit, if it is not 12 Oct 2026. <<<
SEO_FIX_RELEASE_DATE = "2026-10-12"
# HOME_LASTMOD: set below with DOC_DOCX_RELEASE_DATE (19 Oct 2026); was SEO_FIX_RELEASE_DATE.
TOOLS_LASTMOD = RELEASE_DATE
# 15 Oct 2026: every guide gains a "Related guides" block (RELATED_GUIDES,
# below), so every guide's sitemap <lastmod> moves to this date. The same
# value is also used for the DOC vs DOCX guide's visible "Updated" date and
# for the new /link-to-us page's <lastmod>, so there is ONE date to set.
# >>> OWNER: set this to the ACTUAL deploy day (YYYY-MM-DD) before you
# commit, if it is not 15 Oct 2026. This is the only date to change. <<<
GUIDES_LINKS_LASTMOD = "2026-10-15"
GUIDES_MARKUP_LASTMOD = SEO_FIX_RELEASE_DATE
# 16 Oct 2026: three internal-link gaps closed -- Merge PDF now lists the
# PDF compression guide, PDF to Excel lists the scanned-PDF guide (both via
# the guides' related_tools, shown under "Further reading"), and About links
# the guides hub. Used as the sitemap <lastmod> of /tools/merge-pdf,
# /tools/pdf-to-excel and /about only.
# >>> OWNER: set this to the ACTUAL deploy day (YYYY-MM-DD) if not 16 Oct. <<<
LINK_GAPS_LASTMOD = "2026-10-16"
# 19 Oct 2026 release ("DOC vs DOCX" package): new DOC to DOCX tool
# (/tools/doc-to-docx), the DOC vs DOCX guide's new title, opening and
# "How to convert" section, and the corrected "files are not stored" wording
# (now "deleted automatically after conversion", matching the Organization
# data). Dates ONLY the pages whose own content changes: the home page (new
# tool card, tool count, WebSite description), /about (tool count and
# description), the new tool, Word to PDF and PDF to Word (new related-tool
# link) and the DOC vs DOCX guide (visible "Updated" line too).
# >>> OWNER: set this to the ACTUAL deploy day (YYYY-MM-DD) if not 19 Oct. <<<
DOC_DOCX_RELEASE_DATE = "2026-10-19"
# 24 Oct 2026 (AI-visibility plan, Google steps 2 and 5): three new guides
# (xls-vs-xlsx, ppt-vs-pptx, pdf-or-word-which-to-send) and answer-first
# openings for the PDF compression and Excel fit-to-page guides.
# Combined release (Package 2 + 3): uses PACKAGE2_RELEASE_DATE below, so there is ONE date to set.
HOME_LASTMOD = DOC_DOCX_RELEASE_DATE
# Package 2 ("trust content", built 24 Oct 2026): About gains the open-source
# sections (wording approved by counsel, 16 Oct 2026, used verbatim) and a
# "How we test" note; Terms gains section 15 "Software Licensing vs. Hosted
# Infrastructure Access" and a "Last updated" line; new guide "What happens
# to your file"; font-substitution table in the Word to PDF guide; the guides
# list gains the new guide. Dates ONLY those pages (sitemap <lastmod>, the
# Terms "Last updated" line and the two guides' visible dates). The footer
# link text change on every page is not a change to their own content.
# >>> OWNER: set this to the ACTUAL deploy day (YYYY-MM-DD) if not 24 Oct. <<<
PACKAGE2_RELEASE_DATE = "2026-10-24"
NEW_GUIDES_RELEASE_DATE = PACKAGE2_RELEASE_DATE  # Package 3 guides and openings (combined release)
TERMS_UPDATED_TEXT = _date.fromisoformat(PACKAGE2_RELEASE_DATE).strftime("%-d %B %Y")
# Package 2 also carries the two queued fixes (claude/next-release-pending.md):
# the shorter /about meta description (173 -> 147 characters, Bing flag) and
# TikTok in the Organization sameAs + footer. The home page carries the
# Organization data Google reads and gains the new guide in its guides list,
# so its <lastmod> moves too.
HOME_LASTMOD = PACKAGE2_RELEASE_DATE   # was DOC_DOCX_RELEASE_DATE
# Release 5 (26 Oct 2026, SEO-tools review): /tools hub page (new), shorter
# privacy line + 4 de-duplicated FAQ questions on tool pages, home heading
# "Private by design", larger tap targets on phones (CSS only).
# Dates: every tool page, the home page and /tools.
# >>> OWNER: set this to the ACTUAL deploy day (YYYY-MM-DD) if not 26 Oct. <<<
RELEASE5_DATE = "2026-10-26"
HOME_LASTMOD = RELEASE5_DATE   # Release 5: heading + link to /tools (was PACKAGE2_RELEASE_DATE)
# Static pages (key = URL path without the "/"). 8 Oct 2026 (evening): new
# titles on the guides list, About, Contact, Privacy and Terms, plus
# breadcrumb data on the guides list, About and Contact.
STATIC_LASTMOD = {
    "guides": PACKAGE2_RELEASE_DATE,   # Package 2: new guide listed (was DOC_DOCX_RELEASE_DATE)
    "about": PACKAGE2_RELEASE_DATE,   # Package 2: open-source sections + How we test (was DOC_DOCX_RELEASE_DATE)
    "contact": DOC_DOCX_RELEASE_DATE,   # 19 Oct 2026: help sections added (low word count, Ubersuggest)
    "privacy": DOC_DOCX_RELEASE_DATE,   # 19 Oct 2026: <title> lengthened + meta wording (notice text unchanged; counsel-approved 11 Oct 2026)
    "terms": PACKAGE2_RELEASE_DATE,   # Package 2: new section 15 + "Last updated" line (was RELEASE_DATE)
    "link-to-us": GUIDES_LINKS_LASTMOD,   # new page, 15 Oct 2026 package
    "tools": RELEASE5_DATE,   # Release 5: new /tools hub page
}

# ---- Consent (EEA / UK / Switzerland visitors only) ------------------------
# Used by templates/base.html and static/js/consent.js for visitors whose
# Cloudflare CF-IPCountry is in app.py's _CONSENT_REGIONS. Visitors elsewhere
# get exactly the same pages as before this was added.
#
# CONSENT_VERSION: stored in each visitor's consent record (localStorage key
# "kk_consent"). Change it (e.g. "2026-11-02.1") whenever the banner text,
# the purposes or the list of tools covered changes materially: every
# visitor whose record has a different version is asked again.
CONSENT_VERSION = "2026-10-11.1"
# CONSENT_MAX_AGE_DAYS: a stored choice older than this is ignored and the
# banner is shown again. 365 is a common choice, NOT a legal requirement --
# ADVISER DECISION (some regulators suggest re-asking sooner, e.g. after
# 6-13 months).
CONSENT_MAX_AGE_DAYS = 365
# CONSENT_MODE_TYPE:
#   "basic" (SHIPPED DEFAULT for the 11 Oct 2026 release -- owner rule: no
#      published claim about limited/cookieless data transmission until it
#      has been verified with the real Google tag). Strict PER CATEGORY:
#      the Analytics tag (G-K0VJLC113K) is configured only with Analytics
#      consent, the Google Ads tag (AW-18473004328) only with Advertising
#      consent, and static/js/main.js sends GA4 events only with Analytics
#      consent and the Ads conversion only with Advertising consent. With
#      both refused, nothing at all is requested from Google.
#   "advanced": after ANY choice both tags are configured and the library
#      loads; refused categories stay 'denied' and Google Consent Mode
#      governs what is still sent (cookieless pings). Kept for later; its
#      banner sentence makes a claim that must first be verified with the
#      real tag (evidence/REAL-TAG-TEST-PLAN.md, optional section).
# Before any choice the tag is never loaded, in either mode.
CONSENT_MODE_TYPE = "basic"
# ADS_DATA_REDACTION: gtag('set', 'ads_data_redaction', true) on consent-region
# pages. Per Google's documentation, when ad_storage is 'denied' ad click
# identifiers in Google Ads / Floodlight network requests are redacted and
# requests go through a cookieless domain; it has no effect when ad_storage
# is 'granted'. url_passthrough is deliberately NOT enabled.
ADS_DATA_REDACTION = True
# LAUNCHNEST_CONSENT_REGIONS: what consent-region visitors see in place of the
# LaunchNest badge image (an image from launchnest.io, which receives the
# visitor's IP address when it loads):
#   "text_link"   (default): a plain text link "Listed on LaunchNest" with the
#                 same href -- no request to launchnest.io, whatever the choice;
#   "advertising": the badge image, loaded only with Advertising consent.
# Visitors outside the consent regions always get the image, as before.
LAUNCHNEST_CONSENT_REGIONS = "text_link"

# Fail safe: an unknown value falls back to the more private option.
if CONSENT_MODE_TYPE not in ("advanced", "basic"):
    CONSENT_MODE_TYPE = "basic"
if LAUNCHNEST_CONSENT_REGIONS not in ("text_link", "advertising"):
    LAUNCHNEST_CONSENT_REGIONS = "text_link"
if not isinstance(CONSENT_MAX_AGE_DAYS, int) or CONSENT_MAX_AGE_DAYS < 1:
    CONSENT_MAX_AGE_DAYS = 365

# ---- Tool catalogue -------------------------------------------------------
# Single source of truth for the homepage grid, each tool's page, and the
# /convert dispatcher in app.py. Add a new converter by adding an entry here
# plus a handler function in app.py's HANDLERS dict with the same slug.
#
# from_fmt / to_fmt are short display labels used to render the colored
# format badges on each homepage tool card (see FORMAT_BADGE_CLASS below
# and .badge-* rules in static/css/style.css). They are purely cosmetic --
# they do not affect conversion logic.

TOOLS = [
    # -- Document conversions --
    {
        "slug": "word-to-pdf",
        "name": "Word to PDF",
        "category": "Documents",
        "description": "Convert Word to PDF -- DOC to PDF and DOCX to PDF.",
        "accept": ".doc,.docx",
        "multi": False,
        "from_fmt": "DOC",
        "to_fmt": "PDF",
    },
    {
        "slug": "pdf-to-word",
        "name": "PDF to Word",
        "category": "Documents",
        "description": "Convert PDF to Word: an editable DOCX file. Text-based PDFs give the cleanest result.",
        "accept": ".pdf",
        "multi": False,
        "from_fmt": "PDF",
        "to_fmt": "DOC",
    },
    {
        # 19 Oct 2026: new tool. Direction follows the uploaded file:
        # .doc -> .docx, .docx -> .doc (converters/office.py convert_word_format).
        "slug": "doc-to-docx",
        "name": "DOC to DOCX",
        "category": "Documents",
        "description": "Convert old Word DOC files to DOCX -- or DOCX back to DOC for older Word.",
        "accept": ".doc,.docx",
        "multi": False,
        "from_fmt": "DOC",
        "to_fmt": "DOCX",
    },
    {
        "slug": "excel-to-pdf",
        "name": "Excel to PDF",
        "category": "Documents",
        "description": "Convert Excel to PDF -- XLS and XLSX spreadsheets.",
        "accept": ".xls,.xlsx",
        "multi": False,
        "from_fmt": "XLS",
        "to_fmt": "PDF",
    },
    {
        "slug": "pdf-to-excel",
        "name": "PDF to Excel",
        "category": "Documents",
        "description": "Convert PDF to Excel: pull tables into an editable XLSX file.",
        "accept": ".pdf",
        "multi": False,
        "from_fmt": "PDF",
        "to_fmt": "XLS",
    },
    {
        "slug": "ppt-to-pdf",
        "name": "PPT to PDF",
        "category": "Documents",
        "description": "Convert PPT to PDF -- PPT and PPTX presentations.",
        "accept": ".ppt,.pptx",
        "multi": False,
        "from_fmt": "PPT",
        "to_fmt": "PDF",
    },
    {
        "slug": "pdf-to-ppt",
        "name": "PDF to PPT",
        "category": "Documents",
        "description": "Convert PDF to PPT: each page becomes a slide in a PPTX file.",
        "accept": ".pdf",
        "multi": False,
        "from_fmt": "PDF",
        "to_fmt": "PPT",
    },
    # -- Image conversions --
    {
        "slug": "jpg-to-pdf",
        "name": "JPG to PDF",
        "category": "Images",
        "description": "Image to PDF converter: combine JPG or PNG photos into one PDF.",
        "accept": ".jpg,.jpeg,.png",
        "multi": True,
        "from_fmt": "JPG",
        "to_fmt": "PDF",
    },
    {
        "slug": "png-to-pdf",
        "name": "PNG to PDF",
        "category": "Images",
        "description": "Convert PNG to PDF: combine one or more PNG images into a single PDF.",
        "accept": ".png",
        "multi": True,
        "from_fmt": "PNG",
        "to_fmt": "PDF",
    },
    {
        "slug": "pdf-to-jpg",
        "zip_output": True,
        "name": "PDF to JPG",
        "category": "Images",
        "description": "PDF to image: turn each page into a JPG (a ZIP for multi-page files).",
        "accept": ".pdf",
        "multi": False,
        "from_fmt": "PDF",
        "to_fmt": "JPG",
    },
    {
        "slug": "pdf-to-png",
        "zip_output": True,
        "name": "PDF to PNG",
        "category": "Images",
        "description": "Convert PDF to PNG: each page as a sharp PNG image (a ZIP for multi-page files).",
        "accept": ".pdf",
        "multi": False,
        "from_fmt": "PDF",
        "to_fmt": "PNG",
    },
    # Image to image (added 9 Oct 2026) -- converters/images.py convert_images()
    {
        "slug": "heic-to-jpg",
        "zip_output": True,
        "name": "HEIC to JPG",
        "category": "Images",
        "description": "Convert iPhone HEIC photos to JPG so they open on any device.",
        "accept": ".heic,.heif",
        "multi": True,
        "from_fmt": "HEIC",
        "to_fmt": "JPG",
    },
    {
        "slug": "webp-to-jpg",
        "zip_output": True,
        "name": "WEBP to JPG",
        "category": "Images",
        "description": "Convert WEBP images saved from websites into standard JPG files.",
        "accept": ".webp",
        "multi": True,
        "from_fmt": "WEBP",
        "to_fmt": "JPG",
    },
    {
        "slug": "png-to-jpg",
        "zip_output": True,
        "name": "PNG to JPG",
        "category": "Images",
        "description": "Change PNG images to JPG -- transparent areas turn white.",
        "accept": ".png",
        "multi": True,
        "from_fmt": "PNG",
        "to_fmt": "JPG",
    },
    {
        "slug": "jpg-to-png",
        "zip_output": True,
        "name": "JPG to PNG",
        "category": "Images",
        "description": "Convert JPG photos to PNG for sites and apps that ask for PNG.",
        "accept": ".jpg,.jpeg",
        "multi": True,
        "from_fmt": "JPG",
        "to_fmt": "PNG",
    },
    # -- PDF tools --
    {
        "slug": "merge-pdf",
        "name": "Merge PDF",
        "category": "PDF Tools",
        "description": "Combine PDF files into one, in the order you add them.",
        "accept": ".pdf",
        "multi": True,
        "from_fmt": "PDF",
        "to_fmt": "PDF",
    },
    {
        "slug": "split-pdf",
        "zip_output": True,
        "name": "Split PDF",
        "category": "PDF Tools",
        "description": "PDF splitter: save every page as its own PDF (downloaded as a ZIP).",
        "accept": ".pdf",
        "multi": False,
        "from_fmt": "PDF",
        "to_fmt": "PDF",
    },
    {
        "slug": "compress-pdf",
        "name": "Compress PDF",
        "category": "PDF Tools",
        "description": "PDF size reducer: shrink a PDF's file size while keeping it readable.",
        "accept": ".pdf",
        "multi": False,
        "from_fmt": "PDF",
        "to_fmt": "PDF",
        "fields": [
            {
                "name": "level",
                "label": "Compression level",
                "type": "select",
                "options": [
                    ("screen", "Smallest file (screen quality)"),
                    ("ebook", "Balanced (recommended)"),
                    ("printer", "Highest quality, larger file"),
                ],
                "default": "ebook",
            }
        ],
    },
    {
        "slug": "rotate-pdf",
        "name": "Rotate PDF",
        "category": "PDF Tools",
        "description": "Rotate PDF pages: turn every page by 90, 180 or 270 degrees.",
        "accept": ".pdf",
        "multi": False,
        "from_fmt": "PDF",
        "to_fmt": "PDF",
        "fields": [
            {
                "name": "degrees",
                "label": "Rotate by",
                "type": "select",
                "options": [("90", "90°"), ("180", "180°"), ("270", "270°")],
                "default": "90",
            }
        ],
    },
    {
        "slug": "watermark-pdf",
        "name": "Watermark PDF",
        "category": "PDF Tools",
        "description": "Add a watermark to a PDF: diagonal text on every page.",
        "accept": ".pdf",
        "multi": False,
        "from_fmt": "PDF",
        "to_fmt": "PDF",
        "fields": [
            {"name": "text", "label": "Watermark text", "type": "text", "default": "CONFIDENTIAL"}
        ],
    },
    {
        "slug": "protect-pdf",
        "name": "Protect PDF",
        "category": "PDF Tools",
        "description": "Password protect a PDF so only people with the password can open it.",
        "accept": ".pdf",
        "multi": False,
        "from_fmt": "PDF",
        "to_fmt": "PDF",
        "fields": [
            {"name": "password", "label": "Password", "type": "password", "default": ""}
        ],
    },
]

TOOLS_BY_SLUG = {t["slug"]: t for t in TOOLS}

# ---- Per-tool page content -------------------------------------------------
# Extends each TOOLS entry (via .update() below) with the fields tool.html
# needs to render a full page: an intro, an honest "good to know" note about
# how that specific conversion behaves, a couple of realistic use cases, a
# short tool-specific FAQ (kept separate from the sitewide FAQ on the
# homepage so pages don't duplicate each other), related tools to link to,
# and dedicated SEO title/meta description text. Every technical claim here
# describes how the actual converter in converters/*.py behaves -- nothing
# here is invented or aspirational.
#
# Optional keys (added 8 Oct 2026, keyword-gap plan): "h1" replaces the
# page's H1 (the short "name" is still used in the menu, cards and
# breadcrumb), and "how_to_heading" replaces the default "How to convert
# <name>" heading -- used by the PDF tools, where "convert" doesn't fit.
TOOL_CONTENT = {
    "word-to-pdf": {
        "intro": "Word to PDF is a free online converter that turns MS Word files into PDF -- DOC to PDF or DOCX to PDF -- so your document looks the same on every device. It's the simplest way to share a Word document with someone you can't be sure has Microsoft Word installed, or to lock in a finished document's layout before sending it.",
        "good_to_know": "Converting to PDF preserves your document's current layout, so it won't shift when opened elsewhere. If your file uses a font we don't have installed, we substitute another one. Calibri, Cambria, Arial, Times New Roman and Courier New are replaced by metric-compatible fonts (for example Carlito in place of Calibri), so line breaks stay the same; other fonts -- including Aptos, Word's newer default -- are replaced by fonts with different letter widths, so text can rewrap and the page count can change.",
        "use_cases": [
            "Sending a document to someone you're not sure has Word installed.",
            "Submitting a CV, invoice, or contract in a format the recipient can't accidentally edit.",
            "Archiving a finished document in a format that won't change if you update Word later.",
        ],
        "faq": [
            ("Will my formatting change?", "Page layout, fonts, and images are preserved as closely as possible. The main exception is font substitution (see \"Good to know\" above): fonts other than Calibri, Cambria, Arial, Times New Roman and Courier New can make text rewrap."),
            ("Can I convert a password-protected Word file?", "No -- remove the password in Word first (File → Info → Protect Document), then convert."),
        ],
        "related": ["pdf-to-word", "doc-to-docx", "excel-to-pdf", "ppt-to-pdf"],
        "seo_title": "Word to PDF Converter - DOC & DOCX to PDF | KuickKonvert",
        "meta_description": "Free online DOC to PDF converter: convert Word files (DOC and DOCX) to PDF with no sign-up, no installation and no watermark. Files are deleted automatically.",
        # 19 Oct 2026: new related-tool link to DOC to DOCX.
        "lastmod": DOC_DOCX_RELEASE_DATE,
    },
    "pdf-to-word": {
        "intro": "This free tool converts PDF to Word online: it turns a PDF's pages into an editable DOCX file (PDF to DOCX), so you can update text you'd otherwise have to retype. It works best on PDFs that already contain real text, rather than a scan of a printed page.",
        "good_to_know": "We use pdf2docx first, with a LibreOffice-based fallback if that doesn't produce a usable result. Bulleted and numbered lists currently convert to plain text lines rather than a live Word list -- you may need to reapply bullet formatting afterward. Complex layouts, tables, and heavily designed pages may need manual adjustment once opened in Word.",
        "use_cases": [
            "Editing text from a PDF you only have as a final, uneditable file.",
            "Updating an old contract or letter you no longer have the original Word file for.",
            "Pulling text out of a report to reuse in a new document.",
        ],
        "faq": [
            ("Will bullet points and numbering be preserved?", "They convert to plain text lines rather than a live bulleted list -- you may need to reapply list formatting in Word."),
            ("Does this work on a scanned PDF?", "This tool extracts text that's already embedded in the PDF; it doesn't perform OCR, so a scanned image-only PDF won't produce editable text."),
            ("Can I convert PDF to Word without sign-up?", "Yes -- there's no account, email or payment. Upload your PDF, convert it, and download the DOCX file. Your upload and the result are deleted from our server as soon as your download is ready."),
            ("Can I convert PDF to DOC instead of DOCX?", "Our PDF to Word converter creates a DOCX file -- the standard Word format since Word 2007, which opens in Microsoft Word, Google Docs and LibreOffice. If you specifically need the older .doc format, upload the DOCX to our DOC to DOCX converter, which also converts DOCX to DOC -- or open it in Word and choose File → Save As → Word 97-2003 Document (*.doc)."),
        ],
        "related": ["word-to-pdf", "doc-to-docx", "pdf-to-excel", "pdf-to-ppt", "compress-pdf"],
        "seo_title": "PDF to Word Converter Online Free (DOCX) | KuickKonvert",
        "how_to_heading": "How to convert a PDF to Word document format",
        "meta_description": "Free online PDF to Word converter: turn a PDF into an editable Word (DOCX) document with no sign-up and no watermark. Text-based PDFs give the cleanest result.",
        # 19 Oct 2026: new related-tool link and FAQ mention of DOC to DOCX.
        "lastmod": DOC_DOCX_RELEASE_DATE,
    },
    "doc-to-docx": {
        "intro": "DOC to DOCX converts old Word 97-2003 documents (.doc) into DOCX, the format every version of Word since 2007 uses by default and the one Google Docs and LibreOffice handle best. It also works the other way: upload a .docx and you get a .doc back, for someone who still uses Word 2003 or earlier.",
        "good_to_know": "The direction is set by the file you upload: a .doc comes back as a .docx, and a .docx comes back as a .doc. The conversion runs through LibreOffice on our server; text, headings, tables and pictures carry over, but a document with a complex layout can come out slightly differently, so give the result a quick look before you send it. Pictures linked from other websites (rather than stored in the file) are removed from a DOCX before conversion, so the server never fetches anything from another website. Password-protected files can't be converted.",
        "use_cases": [
            "Uploading an old .doc to a form or portal that only accepts .docx.",
            "Opening an old Word 97-2003 file in Google Docs or a current program without Compatibility Mode.",
            "Sending a document to someone who still uses Word 2003 or earlier (DOCX to DOC).",
        ],
        "faq": [
            ("What is the difference between DOC and DOCX?", "DOC is the binary format used by Word 97 to 2003; DOCX is the modern format used since Word 2007, a ZIP archive of XML files. Our DOC vs DOCX guide explains what that changes for you."),
            ("Can I convert DOCX to DOC as well?", "Yes -- upload a .docx file and you get a .doc back. You only need this if the person you are sending it to uses Word 2003 or earlier; every newer version of Word opens DOCX."),
            ("Will my document look the same?", "Text, headings, tables and pictures carry over. Complex layouts can shift slightly, and fonts we don't have installed are replaced, so check the converted file before you send it."),
            ("Can I convert DOC to DOCX in Microsoft Word instead?", "Yes. Open the .doc in Word and choose File → Save As → Word Document (*.docx). Our converter is useful when you don't have Word installed."),
            ("Is it free, and are my files kept?", "It is free, with no sign-up. Your upload and the converted file are deleted from our server as soon as your download is ready."),
        ],
        "related": ["word-to-pdf", "pdf-to-word"],
        "seo_title": "DOC to DOCX Converter Online Free | KuickKonvert",
        "meta_description": "Convert DOC to DOCX online for free: turn old Word 97-2003 files into modern .docx, or DOCX back to DOC. No sign-up; files are deleted automatically.",
        "h1": "DOC to DOCX Converter (and DOCX to DOC)",
        # Label used in the "How to" steps: the result can be either format.
        "out_label": "DOCX (or DOC)",
        "lastmod": DOC_DOCX_RELEASE_DATE,
    },
    "excel-to-pdf": {
        "intro": "Excel to PDF turns an XLS or XLSX spreadsheet into a fixed-layout PDF -- useful whenever you want to share numbers without letting the recipient edit formulas, or print a clean copy of a sheet.",
        "good_to_know": "Columns are automatically widened to fit their content, and for a very wide sheet the page automatically switches to landscape orientation so more columns fit on the page. Extremely wide sheets may still show slightly smaller text even in landscape.",
        "use_cases": [
            "Sharing a read-only copy of a spreadsheet with a client or manager.",
            "Printing an invoice or price list for someone without Excel.",
            "Archiving a finished spreadsheet in a format that won't change if formulas are later edited.",
        ],
        "faq": [
            ("Will my columns get cut off?", "Columns are automatically resized to fit, and very wide sheets switch to landscape orientation automatically to keep everything on the page."),
            ("Are my formulas or macros preserved?", "The PDF shows your sheet's values as recalculated by our converter -- formulas and macros themselves aren't carried into the PDF, since PDF is a fixed, non-editable format. Very new Excel functions (such as XLOOKUP) may not be recognised by the converter and can show an error, so check the PDF if your sheet uses them."),
            ("Can I convert Excel to PDF without Excel installed?", "Yes -- you upload the file from your browser and the conversion runs on our server, so you can convert an XLS or XLSX file to PDF even on a device that doesn't have Excel installed."),
            ("Is this free, and is there a file size limit?", "It's free with no sign-up. Uploads can be up to 50MB, which covers the vast majority of spreadsheets, and fair-use limits apply to how many conversions can run per minute."),
        ],
        "related": ["pdf-to-excel", "word-to-pdf", "compress-pdf"],
        "seo_title": "Excel to PDF Converter - XLS & XLSX to PDF | KuickKonvert",
        "meta_description": "Convert Excel to PDF online free: turn XLS and XLSX spreadsheets into PDF files without Excel installed. No sign-up; files are deleted automatically.",
    },
    "pdf-to-excel": {
        "intro": "PDF to Excel extracts tables from a PDF and rebuilds them as an editable XLSX file, so you can sort, filter, or recalculate data that arrived as a static document.",
        "good_to_know": "Tables are detected by their visible layout on the page, along with the text immediately around them. Cell values and column structure carry over, but formatting like colors, borders, and merged cells doesn't -- this works best on PDFs with genuinely tabular data rather than free-flowing text.",
        "use_cases": [
            "Pulling a table from a bank statement or invoice into a spreadsheet for review.",
            "Getting data out of a report PDF to analyze or chart in Excel.",
            "Rebuilding an old price list you only have as a PDF.",
        ],
        "faq": [
            ("Will colors and cell formatting carry over?", "No -- only the data and its column layout are extracted; visual styling isn't preserved."),
            ("What if my PDF isn't a clear table?", "The tool works best on genuinely tabular content. Text outside a detected table is still included alongside it, but results are less structured for free-form pages."),
            ("Is this PDF to Excel converter really free?", "Yes -- no sign-up, subscription, or watermark on the output file. Uploads can be up to 50MB, and fair-use limits apply to how many conversions can run per minute."),
        ],
        "related": ["excel-to-pdf", "pdf-to-word", "merge-pdf"],
        "seo_title": "PDF to Excel Converter Online Free | KuickKonvert",
        "how_to_heading": "How to convert PDF to Excel for free",
        "meta_description": "Convert PDF to Excel free: turn tables in a PDF into an editable XLSX spreadsheet online, with no sign-up or software. Files are deleted automatically.",
        # 16 Oct 2026: new "Further reading" guide link (see LINK_GAPS_LASTMOD).
        "lastmod": LINK_GAPS_LASTMOD,
    },
    "ppt-to-pdf": {
        "intro": "PPT to PDF converts PowerPoint presentations to PDF online for free -- PPT and PPTX to PDF -- so slides display exactly as designed on any device, without needing PowerPoint installed.",
        "good_to_know": "Slide layout, images, and text positioning are preserved. As with other Office conversions, a font we don't have installed is substituted: Calibri, Cambria, Arial, Times New Roman and Courier New get metric-compatible replacements, while other fonts (such as Aptos) are replaced by fonts with different letter widths, which can make text rewrap on text-heavy slides.",
        "use_cases": [
            "Sending a deck to someone without PowerPoint.",
            "Sharing slides that can't be accidentally edited before a meeting.",
            "Printing handouts from a presentation.",
        ],
        "faq": [
            ("Will animations or transitions be included?", "No -- PDF is a static format, so each slide converts to a single fixed page; animations and transitions don't carry over."),
            ("Will my fonts look exactly the same?", "Not always. If your presentation uses a font we don't have, a substitute is used: for Calibri, Cambria, Arial, Times New Roman and Courier New it has the same letter widths, so the layout stays intact; other fonts can make text rewrap or look different."),
        ],
        "related": ["pdf-to-ppt", "word-to-pdf", "compress-pdf"],
        "seo_title": "PPT to PDF Converter - PowerPoint to PDF Free | KuickKonvert",
        "meta_description": "Convert PowerPoint to PDF online free: turn PPT and PPTX slides into a PDF with one slide per page. No sign-up or software; files deleted automatically.",
    },
    "pdf-to-ppt": {
        "intro": "PDF to PPT turns each page of a PDF into a slide in a PowerPoint file, keeping each page exactly as it looks in the PDF.",
        "good_to_know": "Each PDF page becomes a full-slide image on its own slide, so its layout is reproduced exactly -- but the text on those slides isn't editable, since it's an image rather than live PowerPoint text. The slides take the size of the PDF's first page; a page with a different size or orientation is scaled to fit, keeping its proportions. Up to 50 pages can be converted at a time; for a longer PDF, split it with Split PDF and convert it in parts.",
        "use_cases": [
            "Turning a PDF report into slides for a presentation without redesigning it.",
            "Getting PDF content into a format you can present directly from PowerPoint.",
            "Combining PDF pages with other slides in an existing deck.",
        ],
        "faq": [
            ("Can I edit the text after converting?", "No -- each PDF page becomes a static image on its own slide, so layout is preserved exactly but the text itself isn't editable."),
            ("Will the slide size match my PDF's page size?", "The slides take the size of the PDF's first page. If other pages have a different size or orientation, each is scaled to fit its slide and centred, keeping its proportions."),
        ],
        "related": ["ppt-to-pdf", "pdf-to-word", "pdf-to-jpg"],
        "seo_title": "PDF to PPT Converter - PDF to PowerPoint Free | KuickKonvert",
        "meta_description": "Convert PDF to PowerPoint online for free: each PDF page becomes a slide in a PPTX file, with the layout kept exactly. No sign-up.",
    },
    "jpg-to-pdf": {
        "h1": "JPG to PDF Converter - Photo to PDF",
        "intro": "Convert images to PDF online for free: turn a single JPG photo into a PDF, or merge JPG to PDF to combine several photos into one file. It's a quick way to turn pictures of documents, receipts, or whiteboards into one shareable PDF -- and PNG images work too.",
        "good_to_know": "Images are combined into the PDF in the order you add them. You can remove a file from the list before converting if you added the wrong one, but there's no reorder option -- if you need a different order, remove all the files and re-add them in the order you want. The photo data in your JPG files goes into the PDF without being re-compressed, so there's no extra quality loss; only hidden details such as the location a photo was taken are removed. PNG files are embedded losslessly, and any transparent areas are placed on a white background.",
        "use_cases": [
            "Combining several photographed pages of a document into one PDF to email.",
            "Turning receipt photos into a single PDF for an expense claim.",
            "Creating a simple PDF portfolio from a set of images.",
        ],
        "faq": [
            ("Can I reorder the images after adding them?", "Not directly -- images are combined in the order you add them. Remove the files and re-add them in your preferred order if needed."),
            ("Is there a limit to how many images I can combine?", "There's no fixed count limit, but the combined upload must stay under the 50MB file size limit."),
            ("Is converting JPG to PDF online free?", "Yes -- there's no charge, sign-up, or watermark. You upload from your browser, the PDF is built on our server, and your files are deleted as soon as your download is ready."),
            ("Can I mix JPG and PNG files in one PDF?", "Yes -- add JPG and PNG images together and they're combined into one PDF, in the order you add them."),
            ("Can I convert a picture to PDF on my phone?", "Yes -- open this page in your phone's browser, tap \"Choose files\" and pick one or more photos (JPG or PNG). They're combined into one PDF that downloads straight to your phone, with no app to install."),
        ],
        "related": ["png-to-pdf", "pdf-to-jpg", "merge-pdf"],
        "seo_title": "JPG to PDF - Image to PDF Converter Free | KuickKonvert",
        "meta_description": "Free image to PDF converter: convert JPG or PNG photos to PDF online, or combine several images into one PDF. No sign-up and no watermark on the result.",
        # Own date (fix release): "Good to know" wording corrected and sideways
        # phone photos now kept upright. Only this tool page changes, so
        # TOOLS_LASTMOD (shared by every tool page) is left alone.
        "lastmod": FIX_RELEASE_DATE,
    },
    "png-to-pdf": {
        "intro": "PNG to PDF combines one or more PNG images into a single PDF file, keeping the sharp edges and transparency-free areas PNG is known for.",
        "good_to_know": "Images are combined into the PDF in the order you add them, the same as JPG to PDF. PNG images are embedded losslessly, so text and sharp edges stay exactly as crisp as in your file. Transparent areas are placed on a white background, like a sheet of paper.",
        "use_cases": [
            "Combining screenshots into a single PDF for a bug report or walkthrough.",
            "Turning a set of scanned PNG pages into one document.",
            "Creating a simple PDF handout from PNG graphics.",
        ],
        "faq": [
            ("What happens to transparent backgrounds?", "Transparent areas are placed on a white background, so a logo or graphic with a transparent background appears on white in the PDF, just as it would on a printed page."),
            ("Can I combine PNG and JPG images in one PDF?", "Yes -- use JPG to PDF, which accepts JPG and PNG images together and combines them in the order you add them. This page accepts PNG files only."),
            ("Can I convert PNG to PDF online for free?", "Yes -- this tool is completely free, with no account or software installation needed. You upload from your browser and the PDF is built on our server."),
        ],
        "related": ["jpg-to-pdf", "pdf-to-png", "merge-pdf"],
        "seo_title": "PNG to PDF Converter Online Free | KuickKonvert",
        "meta_description": "Free PNG to PDF converter: turn one PNG, or several at once, into a single PDF online. No sign-up and no watermark; files are deleted automatically.",
    },
    "pdf-to-jpg": {
        "h1": "PDF to JPG - PDF to Image Converter",
        "intro": "PDF to JPG turns every page of a PDF into its own JPG image, useful when you need to drop a page into a slide, a website, or a chat message rather than share the whole PDF.",
        "good_to_know": "Pages are rendered at 300 DPI, sharp enough for most printing and on-screen use. A single-page PDF downloads as one JPG; a multi-page PDF downloads as a ZIP file containing one JPG per page. Up to 50 pages can be converted at a time; for a longer PDF, split it with Split PDF and convert it in parts.",
        "use_cases": [
            "Dropping one page of a PDF into a presentation or webpage as an image.",
            "Sharing a document preview somewhere that only accepts images, not PDFs.",
            "Turning a scanned form into an image for further editing in an image editor.",
        ],
        "faq": [
            ("What resolution are the images?", "Pages are rendered at 300 DPI, which is sharp enough for most printing and screen use."),
            ("What do I get for a multi-page PDF?", "A ZIP file containing one JPG image per page."),
            ("How do I convert PDF to JPG without losing quality?", "JPG always drops a little detail, because it uses lossy compression, but KuickKonvert keeps that small: each page is rendered at 300 DPI before it is saved. In our test of three A4 pages, the JPGs stayed very close to lossless PNG copies (37 to 48 dB PSNR), and fine text showed the most change. For text, forms and diagrams that must stay sharp, use PDF to PNG, which saves the page without lossy compression. For photo pages JPG is far smaller: 413 KB against 4,165 KB in the same test."),
            ("Is converting PDF to JPG online free?", "Yes -- there's no charge or sign-up, and nothing to install: you upload from your browser and the images are created on our server. The limits are the 50MB upload cap, 50 pages per conversion, and fair-use limits on how many conversions can run per minute."),
        ],
        "related": ["pdf-to-png", "jpg-to-pdf", "compress-pdf"],
        "seo_title": "PDF to JPG Converter - PDF to Image Free | KuickKonvert",
        "meta_description": "Convert PDF to JPG online free: every page becomes a 300 DPI JPG image, with multi-page PDFs delivered as one ZIP. No sign-up; files deleted automatically.",
    },
    "pdf-to-png": {
        "intro": "PDF to PNG turns every page of a PDF into its own PNG image -- a good choice when you need a crisp image of a page with sharp text or line art, such as a diagram or a form.",
        "good_to_know": "Pages are rendered at 300 DPI. A single-page PDF downloads as one PNG; a multi-page PDF downloads as a ZIP file containing one PNG per page. Up to 50 pages can be converted at a time; for a longer PDF, split it with Split PDF and convert it in parts.",
        "use_cases": [
            "Extracting a diagram or chart from a PDF as a clean image.",
            "Getting a sharp image of a form or certificate to insert elsewhere.",
            "Preparing PDF pages for use in a design or editing tool.",
        ],
        "faq": [
            ("Why PNG instead of JPG?", "PNG uses lossless compression, so sharp text and line art stay crisp -- JPG can be a better choice for photo-heavy pages where a smaller file size matters more."),
            ("What will I get if my PDF has several pages?", "A ZIP file containing one PNG image per page."),
        ],
        "related": ["pdf-to-jpg", "png-to-pdf", "compress-pdf"],
        "seo_title": "PDF to PNG Converter Online Free | KuickKonvert",
        "meta_description": "Convert PDF to PNG online free: each page becomes a lossless 300 DPI PNG, sharp for text, forms and diagrams. No sign-up; files are deleted automatically.",
    },
    # ---- Image to image (added 9 Oct 2026). Claims match convert_images() in
    # converters/images.py: quality 90 JPG / lossless PNG, full size, turned
    # upright, transparency on white, first frame / main image only, colour
    # profile kept, ONLY date taken + camera make/model kept (GPS removed),
    # up to 20 images and 65 MP each, 150 MB of output per conversion.
    "heic-to-jpg": {
        "h1": "HEIC to JPG Converter - iPhone Photos to JPG",
        "intro": "HEIC to JPG converts the HEIC photos taken by iPhones and iPads into ordinary JPG files that open on any computer, phone or website. Convert one photo or up to 20 at a time -- several photos come back together in one ZIP file.",
        "good_to_know": "Each photo is saved as a high-quality JPG (quality 90) at full size, turned the right way up, with its colour profile kept so colours look the same. The JPG is usually larger than the HEIC file -- HEIC stores photos more compactly, which is why iPhones use it. Location (GPS) details are removed from the JPG; the date and time taken and the camera make and model are kept. If a HEIC file holds several images, such as a burst, the main image is converted, and a Live Photo becomes a still photo. Photos up to 65 megapixels are supported.",
        "use_cases": [
            "Opening iPhone photos on a Windows PC or an older computer that can't display HEIC files.",
            "Uploading photos to a website, online form or job portal that only accepts JPG.",
            "Sending pictures to friends, family or colleagues whose devices don't open HEIC.",
        ],
        "faq": [
            ("What is a HEIC file?", "HEIC is the photo format iPhones and iPads use by default (since iOS 11). It's a type of HEIF image that stores photos in less space than JPG, but many Windows PCs, older phones and websites can't open it -- converting to JPG solves that."),
            ("Can I convert HEIC to JPG on Windows without installing anything?", "Yes -- open this page in your browser, add your HEIC photos and download the JPGs. Nothing is installed on your PC and there's no sign-up."),
            ("How many photos can I convert at once?", "Up to 20 photos at a time, with a combined upload of up to 50 MB. One photo downloads as a JPG; several download together in one ZIP file."),
            ("Is the photo's location removed?", "Yes. GPS location details are removed from the JPG, so you can share it without revealing where it was taken. The date and time taken and the camera make and model are kept."),
            ("Will the JPG look the same as the HEIC photo?", "Yes on screen: it's saved at quality 90 and full size, with the photo's colour profile kept. Two differences: the JPG file is usually larger, and the extra HDR brightness some newer iPhone photos have isn't carried into the JPG."),
        ],
        "related": ["jpg-to-pdf", "webp-to-jpg", "png-to-jpg"],
        "seo_title": "HEIC to JPG Converter - iPhone Photos to JPG | KuickKonvert",
        "meta_description": "Convert HEIC to JPG online for free: turn iPhone photos into JPG files that open anywhere. Up to 20 at once, location data removed. No sign-up.",
        "lastmod": RELEASE_DATE,
    },
    "webp-to-jpg": {
        "h1": "WEBP to JPG Converter - Web Images to JPG",
        "intro": "WEBP to JPG turns WEBP images -- the format many websites now use for their pictures -- into ordinary JPG files that open in any photo viewer or editor and upload anywhere. Convert one image or up to 20 at a time.",
        "good_to_know": "Images are saved as high-quality JPGs (quality 90) at full size. JPG has no transparency, so transparent areas become white, and an animated WEBP is saved as a still JPG of its first frame. The JPG can be larger than the WEBP, because WEBP compresses images more tightly. Location (GPS) details are removed if the image has any; the date taken and the camera make and model are kept.",
        "use_cases": [
            "Opening or editing a picture saved from a website as .webp in software that doesn't support WEBP.",
            "Uploading an image to a form, marketplace or print service that only accepts JPG.",
            "Putting a web image into a document or presentation made with an older version of Office.",
        ],
        "faq": [
            ("What is a WEBP file?", "WEBP is an image format created by Google for the web. It makes pictures smaller so pages load faster, which is why images saved from many websites arrive as .webp -- but some programs, upload forms and older devices still can't open it."),
            ("What happens to animated WEBP files?", "Only the first frame is converted, as a still JPG -- the JPG format can't hold animation."),
            ("What happens to transparent areas?", "They become white, because JPG doesn't support transparency."),
            ("How many WEBP files can I convert in one go?", "Up to 20 WEBP images per batch, with a combined upload of up to 50 MB. When you convert several, the JPGs download together in one ZIP file."),
            ("Do I need special software to open WEBP files as JPG?", "No -- it works in your browser on Windows, Mac, Android or iPhone. Upload your WEBP images, convert them and download the JPGs. There's no sign-up."),
        ],
        "related": ["png-to-jpg", "jpg-to-pdf", "heic-to-jpg"],
        "seo_title": "WEBP to JPG Converter Online Free | KuickKonvert",
        "meta_description": "Convert WEBP to JPG online for free: turn images saved from websites into standard JPG files. Up to 20 at once, no sign-up or install.",
        "lastmod": RELEASE_DATE,
    },
    "png-to-jpg": {
        "h1": "PNG to JPG - Change PNG Images to JPG",
        "intro": "PNG to JPG changes PNG images into JPG files -- the most widely accepted image format, and usually a much smaller file when the picture is a photo. Convert one PNG or up to 20 at a time.",
        "good_to_know": "Each image is saved as a high-quality JPG (quality 90) at full size. JPG has no transparency, so transparent areas -- for example around a logo -- become white. Photos usually shrink a lot as JPG, but screenshots, logos and pages of text can come out larger and slightly less sharp, because JPG is designed for photos. 16-bit PNGs are converted to standard 8-bit JPGs. Location (GPS) details are removed if the PNG has any.",
        "use_cases": [
            "Making a photo saved as PNG small enough to email or upload.",
            "Uploading an image to a form or website that only accepts JPG.",
            "Turning PNG photos or screenshots into JPGs for an online album or print order that asks for JPG.",
        ],
        "faq": [
            ("Will my PNG get smaller as a JPG?", "Usually, if it's a photo -- JPG is built for photos and can make them several times smaller. Screenshots, logos and text pages may not shrink and can even grow, because JPG struggles with sharp edges. In our test (November 2026, A4 pages at 300 DPI), a photo page went from 4,165 KB as PNG to 660 KB as JPG, while a page of text grew from 710 KB to 1,706 KB and a simple diagram from 129 KB to 247 KB. A 512 x 512 logo with a transparent background stayed about the same size (18 KB to 17 KB) and its transparent areas became white. We don't promise a particular file size."),
            ("What happens to a transparent background?", "It becomes white, because JPG doesn't support transparency. Keep the PNG if you need the see-through background."),
            ("Is there any quality loss?", "Very little on photos: images are saved at quality 90, where the difference is hard to see. Sharp text and thin lines can look slightly softer, as with any JPG."),
            ("How many PNG files can I convert at once?", "Up to 20 at a time, with a combined upload of up to 50 MB. Several images download together in one ZIP file."),
            ("Can I change PNG to JPG on my phone?", "Yes -- open this page in your phone's browser, choose your PNG images and download the JPGs. There's no app to install and no sign-up."),
        ],
        "related": ["jpg-to-png", "png-to-pdf", "webp-to-jpg"],
        "seo_title": "PNG to JPG Converter Online Free | KuickKonvert",
        "how_to_heading": "How to change PNG to JPG",
        "meta_description": "Change PNG to JPG online for free, up to 20 images at once. Photos usually get much smaller; transparent areas turn white. No sign-up.",
        "lastmod": RELEASE_DATE,
    },
    "jpg-to-png": {
        "h1": "JPG to PNG Converter - Save JPG as PNG",
        "intro": "JPG to PNG converts JPG (JPEG) photos into PNG files -- for when a website, app or form asks for PNG, or when you plan to edit an image several times. Convert one JPG or up to 20 at a time.",
        "good_to_know": "The PNG is saved losslessly, so it won't lose more detail when you edit and save it again. Converting can't bring back detail the JPG already lost, and it doesn't make the background transparent -- the image looks exactly as before. Expect a bigger file: a photo saved as PNG is often several times larger than the JPG, so a very large batch may need to be converted in smaller groups. Photos are turned the right way up, and location (GPS) details are removed; the date taken and the camera make and model are kept.",
        "use_cases": [
            "Uploading an image to a website, app or form that only accepts PNG.",
            "Editing a picture several times without the extra loss JPG adds every time it's saved.",
            "Adding a photo to a design project or tool that works with PNG files.",
        ],
        "faq": [
            ("Does converting JPG to PNG improve quality?", "No. The PNG keeps exactly what's in your JPG, but it can't restore detail the JPG compression already removed. The benefit is that the image won't lose any more quality when you edit and save it again."),
            ("Will the background become transparent?", "No -- a JPG has no transparency, so the PNG keeps the same solid background. Removing a background needs a separate editing tool."),
            ("Why is the PNG so much bigger?", "PNG is lossless, and photos are full of fine detail that lossless compression can't shrink much -- so a PNG of a photo is often several times the size of the JPG. Screenshots and simple graphics grow far less."),
            ("How many images can I convert at once?", "Up to 20 at a time, with a combined upload of up to 50 MB. Because PNG copies of photos are large, a big batch can go over the 150 MB download limit -- if that happens, convert fewer images at a time."),
        ],
        "related": ["png-to-jpg", "png-to-pdf", "pdf-to-png"],
        "seo_title": "JPG to PNG Converter Online Free | KuickKonvert",
        "meta_description": "Convert JPG to PNG online for free, up to 20 images at once. Lossless PNG copies for sites and apps that require PNG. No sign-up or install.",
        "lastmod": RELEASE_DATE,
    },
    "merge-pdf": {
        "h1": "Merge PDF Files - PDF Combiner",
        "how_to_heading": "How to merge PDF files for free",
        "intro": "Merge PDF combines multiple PDF files into a single document, in the order you add them. It's a free online PDF merger (some call it a PDF joiner) -- handy for putting together a report from separate sections or combining scanned pages into one file.",
        "good_to_know": "Files are combined in the order you add them. You can remove a file from the list before merging if you added the wrong one; there's no drag-to-reorder option, so remove and re-add files in your preferred order if needed.",
        "use_cases": [
            "Combining a cover letter, CV, and references into one PDF for a job application.",
            "Putting separate scanned pages together into a single document.",
            "Assembling several reports into one file before sending.",
        ],
        "faq": [
            ("Can I change the order after adding files?", "Not directly -- files merge in the order you add them. Remove the files and re-add them in your preferred order if needed."),
            ("Is there a limit on how many files I can merge?", "There's no fixed file-count limit, but the combined upload must stay under the 50MB size limit."),
            ("Can I merge PDF files without sign-up?", "Yes -- Merge PDF is free with no account or email needed, and no watermark is added. Add your files, merge them, and download the combined PDF."),
            ("Can I merge Word files or images with my PDFs?", "Not in one step -- Merge PDF only accepts PDF files. Convert the other files first: Word documents with Word to PDF, and JPG or PNG images with JPG to PDF, which can combine several images into one PDF. Then add all the PDFs here and merge them."),
        ],
        "related": ["split-pdf", "compress-pdf", "pdf-to-word"],
        "seo_title": "Merge PDF Online Free - Combine PDF Files | KuickKonvert",
        "meta_description": "Merge PDF files free online: combine PDF documents into one file, in the order you add them. No sign-up, no installation and no watermark on the merged PDF.",
        # 16 Oct 2026: new "Further reading" guide link (see LINK_GAPS_LASTMOD).
        "lastmod": LINK_GAPS_LASTMOD,
    },
    "split-pdf": {
        "how_to_heading": "How to split PDF files into single pages",
        "intro": "Split PDF is a free online PDF splitter: it breaks every page of a PDF into its own single-page PDF file, delivered as a ZIP -- useful when you only need to send someone one page out of a longer document.",
        "good_to_know": "This splits every page of the PDF into a separate file -- there's currently no option to choose a specific page range. If you only need a few pages, split the whole file and keep just the ones you want.",
        "use_cases": [
            "Pulling a single page out of a long PDF to send on its own.",
            "Breaking a scanned multi-page document into individual page files.",
            "Preparing individual pages for a page-by-page workflow.",
        ],
        "faq": [
            ("Can I choose which pages to split out?", "This splits every page into its own file; if you only need a range, split the whole file and discard the pages you don't need."),
            ("What format do I get the pages in?", "A ZIP file containing one single-page PDF for every page in your original file."),
            ("Can I extract pages from PDF files?", "Yes -- Split PDF saves every page of your PDF as its own single-page PDF, delivered in one ZIP file. Keep the pages you need; to put several of them back into one document, combine them with Merge PDF. There's no option to pick a page range in one step."),
        ],
        "related": ["merge-pdf", "rotate-pdf", "compress-pdf"],
        "seo_title": "Split PDF Online Free - PDF Splitter | KuickKonvert",
        "meta_description": "Split PDF pages online free: separate every page of a PDF into its own single-page PDF file, delivered together in one ZIP. No sign-up or software needed.",
    },
    "compress-pdf": {
        "h1": "Compress PDF - Reduce PDF Size",
        "how_to_heading": "How to reduce PDF file size",
        "intro": "Compress PDF is a free online PDF compressor: it reduces a PDF's file size while keeping it readable -- useful when you need to resize PDF files for an email or upload limit, or just want a smaller version to store.",
        "good_to_know": "Three compression levels are available: Screen (smallest file -- images reduced to about 72 dpi), Ebook (the balanced default -- about 150 dpi), and Printer (keeps image resolution, so it usually shrinks the file very little). Compression works on embedded images, so a text-only PDF can't get much smaller. If the result wouldn't be smaller than your original, you get your original file back unchanged instead of a bigger one.",
        "use_cases": [
            "Shrinking a scanned document so it fits under an email attachment limit.",
            "Reducing a large PDF before uploading it to a form or portal with a size cap.",
            "Making an image-heavy report smaller to store or archive.",
        ],
        "faq": [
            ("Which compression level should I choose?", "Ebook is a good default balance. Choose Screen for the smallest possible file if quality matters less, or Printer if quality matters most."),
            ("Will text quality be affected?", "Text stays sharp at every level -- compression mainly targets embedded images, so an image-heavy PDF will shrink more than a text-only one."),
            ("Can I compress a PDF without losing quality?", "Partly. Text and vector graphics stay sharp at every level, because compression only works on images. To keep images as close to the original as possible, choose \"Highest quality, larger file\" (the Printer preset): it keeps image resolution and uses a gentler JPEG setting, but it usually shrinks the file only a little. A noticeably smaller file always means some loss of image detail -- our PDF compression guide shows real test results."),
            ("Can I reduce a PDF's file size online for free?", "Yes -- use Compress PDF without sign-up or payment. Upload your PDF, choose a compression level, and our server returns the smaller file."),
            ("Can I compress a PDF to 1MB or a few hundred KB?", "There's no exact-size setting, so we can't promise a specific size. For the biggest reduction, choose \"Smallest file (screen quality)\": image-heavy and scanned PDFs usually shrink a lot, while a text-only PDF may already be close to its smallest size. Check the result's size before uploading it to a form with a limit."),
            ("Is this a PDF resize tool?", "It resizes the file, not the pages. Compress PDF makes the file smaller (fewer KB or MB) by reducing embedded images; the page dimensions -- for example A4 or Letter -- stay exactly the same."),
        ],
        "related": ["merge-pdf", "split-pdf", "pdf-to-jpg"],
        "seo_title": "Compress PDF Online Free - PDF Size Reducer | KuickKonvert",
        "meta_description": "Free PDF size reducer online: compress PDF files and reduce PDF size while keeping them readable. Choose a compression level — no sign-up.",
    },
    "rotate-pdf": {
        "how_to_heading": "How to rotate PDF pages",
        "intro": "Rotate PDF turns every page of a PDF by 90, 180, or 270 degrees -- a quick fix for a document that was scanned sideways or upside down.",
        "good_to_know": "The same rotation is applied to every page in the file. If only some pages of your PDF are rotated the wrong way, split the file first, rotate just the affected pages, then merge them back together.",
        "use_cases": [
            "Fixing a document that was scanned in landscape by mistake.",
            "Correcting a PDF that opens sideways on your screen.",
            "Preparing a scanned file for printing in the right orientation.",
        ],
        "faq": [
            ("Can I rotate individual pages differently?", "No -- the same rotation is applied to every page. Use Split PDF first if only some pages need rotating, then merge them back afterward."),
            ("Does rotating affect the file's quality?", "No -- rotation only changes page orientation; it doesn't re-encode or degrade the page content."),
            ("Can I rotate a PDF online without installing software?", "Yes -- upload the file from your browser, choose a rotation angle, and download the corrected PDF. The rotation runs on our server; nothing is installed on your device."),
        ],
        "related": ["split-pdf", "merge-pdf", "compress-pdf"],
        "seo_title": "Rotate PDF Pages Online Free | KuickKonvert",
        "meta_description": "Rotate PDF pages online free by 90, 180 or 270 degrees and download the turned file with no loss of quality. No sign-up; files are deleted automatically.",
    },
    "watermark-pdf": {
        "how_to_heading": "How to add a watermark to a PDF",
        "intro": "Watermark PDF stamps your own text diagonally across every page of a PDF -- a simple way to mark a document as a draft, confidential, or belonging to you before sharing it.",
        "good_to_know": "The watermark is applied as semi-transparent gray text, rotated diagonally across each page, using the text you enter. Its size, color, and position aren't currently configurable -- only the text itself is. The watermark font covers Latin letters, numbers and common symbols; letters from scripts such as Urdu, Arabic or Hindi aren't supported yet.",
        "use_cases": [
            "Marking a document \"CONFIDENTIAL\" or \"DRAFT\" before sending it for review.",
            "Adding your name or company across a document to discourage unauthorized reuse.",
            "Labeling a sample document so it's clearly not the final version.",
        ],
        "faq": [
            ("Can I change the watermark's color or position?", "Not currently -- it's applied as a standard semi-transparent gray diagonal stamp; only the watermark text itself is configurable."),
            ("Will the watermark cover important content?", "It's semi-transparent by design so the underlying page stays fully readable underneath it."),
        ],
        "related": ["protect-pdf", "compress-pdf", "merge-pdf"],
        "seo_title": "Add Watermark to PDF Online | KuickKonvert",
        "meta_description": "Add a text watermark to a PDF online free: stamp your own words, such as DRAFT or CONFIDENTIAL, across every page. No sign-up; files deleted automatically.",
    },
    "protect-pdf": {
        "how_to_heading": "How to password protect a PDF",
        "intro": "Protect PDF adds a password to a PDF file, so only someone who has the password can open it -- useful before emailing a document with sensitive information.",
        "good_to_know": "The file is encrypted with a password you choose (at least 4 characters) using 256-bit AES encryption, the standard set by PDF 2.0. Keep the password somewhere safe -- if it's lost, the file can't be opened or recovered by KuickKonvert, since we don't keep a copy of your file or password.",
        "use_cases": [
            "Password-protecting a document with personal or financial details before emailing it.",
            "Restricting who can open a contract before it's signed.",
            "Adding a basic layer of protection to a file shared over an unsecured channel.",
        ],
        "faq": [
            ("What encryption does this use?", "256-bit AES encryption, applied with the password you choose. This is the method the current PDF standard (PDF 2.0) specifies for password-protected PDFs, and Adobe Acrobat and Reader have supported it since version 9."),
            ("What if I forget the password?", "There's no way to recover it -- we don't keep a copy of your file or password after the conversion finishes, so choose a password you'll remember or keep it somewhere safe."),
            ("Is password-protecting a PDF online really free here?", "Yes -- Protect PDF, like every tool on KuickKonvert, is completely free with no sign-up or subscription. The limits are a 50MB upload cap and fair-use limits on how many conversions can run per minute."),
            ("Do I need to install anything to password-protect a PDF?", "No -- upload your PDF from your browser, choose a password, and download the protected file. The encryption runs on our server; nothing is installed on your device."),
        ],
        "related": ["watermark-pdf", "compress-pdf", "merge-pdf"],
        "seo_title": "Protect PDF with Password Online | KuickKonvert",
        "meta_description": "Password protect a PDF online free: add an open password with 256-bit AES encryption so only people who know it can open the file. No sign-up or install.",
    },
}

for _t in TOOLS:
    _t.update(TOOL_CONTENT.get(_t["slug"], {}))

CATEGORIES = ["Documents", "Images", "PDF Tools"]

# Maps a format label to the CSS badge class used on homepage tool cards.
FORMAT_BADGE_CLASS = {
    "DOC": "badge-doc",
    "DOCX": "badge-doc",   # 19 Oct 2026: DOC to DOCX tool card (same Word blue)
    "XLS": "badge-xls",
    "PPT": "badge-ppt",
    "PDF": "badge-pdf",
    "JPG": "badge-jpg",
    "PNG": "badge-png",
    "HEIC": "badge-heic",
    "WEBP": "badge-webp",
}

MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH_MB", "50")) * 1024 * 1024
ALLOWED_EXTENSIONS = {
    "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "jpg", "jpeg", "png",
    "heic", "heif", "webp",
}

# ---- Guides -----------------------------------------------------------
# Original, long-form editorial content -- deliberately separate from the
# 16 tool pages above. Those pages necessarily share a lot of structure
# (upload box, "How to convert", supported formats, FAQ), which is fine on
# its own but means the SITE as a whole leaned heavily on one repeated
# template. This list is the permanent fix for that: a second, independent
# content type that isn't tied to the tool-page skeleton at all, plus a
# route (/guides, /guides/<slug>), a sitemap entry, and a "Further reading"
# link from every related tool page -- all wired up automatically below.
#
# To add a new guide: append a dict with slug / title / seo_title /
# meta_description / dek / published / related_tools / sections, and
# nothing else needs to change -- it appears on /guides, gets its own page,
# joins the sitemap, and shows up as "Further reading" on every tool page
# listed in related_tools.
#
# Ground rule, same as TOOL_CONTENT above: every factual/technical claim in
# a guide must be true of what this site's own converters do (cross-check
# converters/*.py) or be an independently verifiable fact about the file
# format itself. Nothing here is invented or aspirational -- an inaccurate
# "helpful" guide is worse than no guide at all, both for readers and for
# how Google evaluates the site's content quality.
GUIDES = [
    {
        "slug": "docx-vs-doc",
        # Release 7, R7-78: official sources (each URL checked 13 Nov 2026).
        "sources": [('Microsoft Support: Open XML Formats and file name extensions', 'https://support.microsoft.com/en-us/office/open-xml-formats-and-file-name-extensions-5200d93c-3449-4380-8e11-31ef14555b18')],
        # 19 Oct 2026: title, SEO title, meta description and opening rewritten
        # "DOC vs DOCX" first and answer-first (SEO report 19 Oct 2026); new
        # "How to convert DOC to DOCX (and back)" section; DOC to DOCX tool
        # added to related_tools. The slug stays the same.
        "title": "DOC vs DOCX: What's Actually Different (and When It Matters)",
        "seo_title": "DOC vs DOCX: What's the Difference? (Tested) | KuickKonvert",
        "meta_description": "What's the difference between DOC and DOCX? A side-by-side table, a real file-size test and a simple answer: use DOCX unless an old Word needs DOC.",
        "dek": "DOCX is Word's modern format (Word 2007 onwards): a ZIP archive of XML files. DOC is the older binary format used by Word 97 to 2003. Use DOCX for almost everything, and DOC only when someone has a very old version of Word. Below: what that changes for you, and one common claim our own test didn't bear out. To switch a file, use our [[doc-to-docx|DOC to DOCX converter]].",
        "published": "2026-09-14",
        # 15 Oct 2026: quick-comparison table and three short question
        # sections added (the doc/docx query group is this site's largest
        # source of search impressions in GSC). Every statement in them
        # repeats a fact already stated and sourced further down this guide,
        # or is about our own PDF to Word converter (always writes .docx --
        # converters/office.py). OWNER: set to the actual deploy day.
        "updated": DOC_DOCX_RELEASE_DATE,   # 19 Oct 2026 (was GUIDES_LINKS_LASTMOD)
        "related_tools": ["doc-to-docx", "word-to-pdf", "pdf-to-word"],
        "sections": [
            {
                "heading": "DOC vs DOCX at a glance",
                "paragraphs": [
                    "The short version: DOCX is the modern Word format and the right choice for almost everything. DOC is the older format, still worth knowing about if someone uses a very old version of Word.",
                ],
                "table": {
                    "caption": "DOC and DOCX compared",
                    "headers": ["", "DOC", "DOCX"],
                    "rows": [
                        ["Word's default format", "Word 97 to Word 2003", "Word 2007 onwards"],
                        ["What the file is inside", "One binary file", "A ZIP archive of XML files (Office Open XML)"],
                        ["Can contain macros?", "Yes", "No - macro documents use .docm"],
                        ["Opens in Word 2003 and earlier?", "Yes", "Only with Microsoft's compatibility pack"],
                        ["File size", "About the same in our test", "About the same in our test"],
                        ["Converts to PDF with our tool?", "Yes", "Yes"],
                    ],
                    "note": "Details and sources for each row are in the sections below.",
                },
            },
            {
                "heading": "Two different formats, one program",
                "paragraphs": [
                    "DOC was Microsoft Word's format from Word 97 through Word 2003: a single binary file that only Word itself, or software specifically built to parse that binary structure, could reliably read.",
                    "DOCX replaced it as Word's default starting with Word 2007. It isn't a new version of the same format -- it's a completely different approach: a DOCX file is actually a ZIP archive containing a set of XML files (the \"Office Open XML\", or OOXML, standard). Rename any .docx file to .zip and a normal file archiver will open it and show you the XML inside.",
                ],
            },
            {
                "heading": "What we found inside each file",
                "paragraphs": [
                    "We created a four-page test document in DOCX and saved a copy as DOC with LibreOffice (October 2026), then looked at the raw files.",
                    "The DOCX file starts with the letters PK -- the signature of every ZIP file -- and unzips into separate parts: the text in word/document.xml, the formatting in word/styles.xml, the theme in word/theme/theme1.xml, document properties in docProps, and, when the document has them, a separate part for comments and a folder for images. The DOC file starts with a different signature (D0 CF 11 E0), the marker of Microsoft's older compound binary file format, and can't be opened with a file archiver.",
                ],
            },
            {
                "heading": "Is DOCX really smaller? Our test says: not always",
                "paragraphs": [
                    "Microsoft's own support page says Open XML files are automatically compressed and \"can be up to 75 percent smaller in some cases\". That is true for some documents, but it isn't a rule.",
                    "In our test the two formats came out almost the same size. The four-page text document was 37.3 KB as DOCX and 36.5 KB as DOC. With one large photo added, it was 5,510 KB as DOCX and 5,565 KB as DOC -- the photo, already compressed as a JPG, was most of the file in both formats, and zipping it again saves almost nothing.",
                    "So if you need a smaller Word file, switching between DOC and DOCX is rarely the answer. Compressing or resizing the pictures inside it makes far more difference.",
                ],
                "table": {
                    "caption": "The same document saved both ways (our test, October 2026)",
                    "headers": ["Test document", "DOCX", "DOC", "Converted to PDF with our tool"],
                    "rows": [
                        ["Four pages of text", "37.3 KB", "36.5 KB", "4 pages from either format"],
                        ["Same document plus one 4000 x 3000 photo", "5,510 KB", "5,565 KB", "-"],
                    ],
                    "note": "The DOC copy was saved with LibreOffice, not Microsoft Word; sizes from Word itself can differ.",
                },
            },
            {
                "heading": "Why Microsoft made the switch",
                "paragraphs": [
                    "XML-based formats are openly documented, so other software -- Google Docs, LibreOffice, Apple Pages, and the conversion tools on this site included -- can read and write them without reverse-engineering a proprietary binary layout.",
                    "Microsoft also points to resilience: because the parts of a DOCX file are stored separately, it says a file can still be opened even if one component, such as a chart or table, is damaged.",
                ],
            },
            {
                "heading": "When the difference actually matters to you",
                "paragraphs": [
                    "Compatibility with older software. Word 2003 and earlier can't open a .docx file without Microsoft's separate compatibility pack -- the most common real-world reason someone still asks for a plain .doc.",
                    "Macros. A normal .docx file can't contain macros; Word uses the separate .docm extension for macro-enabled documents. That makes a .docx a little safer to open from an unknown sender, while an old .doc may contain macros.",
                    "Converting to PDF. In our test, both formats converted to the same four-page PDF with our Word to PDF tool, so either one is fine to upload.",
                    "For everyday writing, editing and sharing with someone on a current version of Word or Google Docs, the difference is invisible.",
                ],
            },
            {
                "heading": "Which one should you use?",
                "paragraphs": [
                    "Use DOCX unless someone specifically needs DOC for an old program. It is Word's default, it is the format other software supports best, and it keeps macros out unless you deliberately choose .docm.",
                    "If a form or portal asks for \"a Word document\" without saying which, DOCX is the safe choice. If it must not be edited at all, send a PDF instead -- our [[word-to-pdf|DOC to PDF converter]] accepts both .doc and .docx. Your upload and the PDF are deleted from our server as soon as your download is ready.",
                    "Going the other way, our [[pdf-to-word|PDF to Word converter]] always gives you a .docx file, so it opens in any current version of Word, Google Docs or LibreOffice.",
                ],
            },
            {
                "heading": "Switching a file between DOC and DOCX",
                "paragraphs": [
                    "In Microsoft Word: open the .doc file, choose File → Save As, and pick Word Document (*.docx). To go the other way, pick Word 97-2003 Document (*.doc) instead.",
                    "Without Word: upload the file to our [[doc-to-docx|DOC to DOCX converter]]. A .doc comes back as a .docx, and a .docx comes back as a .doc. It is free, needs no sign-up, and your upload and the converted file are deleted from our server as soon as your download is ready.",
                    "Either way, open the converted file once before you send it. Text, headings, tables and pictures carry over, but a complex layout can shift slightly.",
                ],
            },
            {
                "heading": "Is DOC the same as DOCX?",
                "paragraphs": [
                    "No. Both are Word documents and both open in current versions of Word, but they are different file formats: DOC is a single binary file, while DOCX is a ZIP archive of XML files. Word 2003 and earlier cannot open a DOCX without Microsoft's compatibility pack.",
                ],
            },
            {
                "heading": "Is a DOCX file a Word document?",
                "paragraphs": [
                    "Yes. DOCX has been Microsoft Word's default format since Word 2007, so a .docx file is a normal Word document. Google Docs, LibreOffice and Apple Pages can open and edit it too.",
                ],
            },
            {
                "heading": "What does DOCX stand for?",
                "paragraphs": [
                    "The \"x\" refers to XML: a DOCX file stores the document as XML files (the Office Open XML standard) packed into a ZIP archive. DOC, the older format, is short for \"document\".",
                ],
            },
        ],
    },
    {
        "slug": "why-pdf-layout-shifts",
        # Release 7, R7-78: official sources (each URL checked 13 Nov 2026).
        "sources": [('Microsoft Learn: Aptos font family', 'https://learn.microsoft.com/en-us/typography/font-list/aptos')],
        "title": "Why a PDF's Layout Sometimes Shifts After Conversion (and How to Avoid It)",
        "seo_title": "Why PDF Layout Shifts After Conversion | KuickKonvert",
        "meta_description": "Converted a Word document to PDF and the fonts or page count changed? Our test shows exactly why — and why Word's newer default font, Aptos, is affected.",
        "dek": "It's almost never a bug. In the overwhelming majority of cases it comes down to one specific, well-understood cause: font substitution. Our test shows how much difference it can make. To check your own file, try our [[word-to-pdf|Word to PDF converter]].",
        "published": "2026-09-14",
        "updated": "2026-10-05",
        "related_tools": ["word-to-pdf", "excel-to-pdf", "ppt-to-pdf"],
        "sections": [
            {
                "heading": "Why does the layout change when converting Word to PDF?",
                "paragraphs": [
                    "Because the layout isn't stored as fixed positions -- it's calculated from the font.",
                    "A Word or PowerPoint file doesn't store where every letter sits on the page. It stores the text and which font it's set in, and the software calculates line breaks and spacing at the moment it displays the document, based on that font's actual letter widths.",
                    "PDF, by contrast, is a fixed-layout format -- once converted, every letter's position is locked in. That conversion step is exactly where a font mismatch becomes visible.",
                ],
            },
            {
                "heading": "What happens when the exact font isn't available",
                "paragraphs": [
                    "Commercial fonts such as Calibri, Cambria, Arial and Times New Roman are licensed by Microsoft and aren't necessarily installed on the server that performs the conversion. Our Office-to-PDF conversions -- [[word-to-pdf|Word to PDF]], [[excel-to-pdf|Excel to PDF]] and [[ppt-to-pdf|PPT to PDF]] -- run through LibreOffice, and our server has free, metric-compatible replacements installed for the most common ones: Carlito for Calibri, Caladea for Cambria, and the Liberation fonts for Arial, Times New Roman and Courier New.",
                    "\"Metric-compatible\" means each letter is exactly as wide as in the original font, so line breaks and page counts stay the same. What can still differ slightly is the shape of the letters themselves.",
                    "Any font without such a replacement falls back to a general-purpose font with different letter widths -- and that is when lines rewrap and pages move.",
                ],
            },
            {
                "heading": "What we measured",
                "paragraphs": [
                    "We wrote the same document -- headings, about 1,600 words of text, a link and a header -- three times, changing only the body font, and converted each one with the same code and the same set of fonts our server uses (LibreOffice 24.2, October 2026). We then checked which font actually ended up in each PDF.",
                    "Calibri and Arial were replaced by their metric-compatible twins, and both documents stayed at four pages. Aptos was replaced by DejaVu Sans, a font with wider letters, and the same text grew to five pages.",
                ],
                "table": {
                    "caption": "The same document in three fonts, converted with our Word to PDF tool (October 2026)",
                    "headers": ["Font chosen in Word", "Font used in the PDF", "Pages", "Layout kept?"],
                    "rows": [
                        ["Calibri", "Carlito (metric-compatible)", "4", "Yes"],
                        ["Arial", "Liberation Sans (metric-compatible)", "4", "Yes"],
                        ["Aptos", "DejaVu Sans (fallback, wider letters)", "5", "No - text rewrapped onto an extra page"],
                    ],
                    "note": "Headings in all three tests used Word's heading style and came out in Carlito Bold. Exact results can vary with the LibreOffice version.",
                },
            },
            {
                "heading": "Why Aptos matters: Word's newer default font",
                "paragraphs": [
                    "Microsoft has replaced Calibri with Aptos as the default font in Microsoft 365, so many new documents are now written in Aptos without anyone choosing it. Aptos has no free metric-compatible replacement installed on our server, so as our test shows, a document in Aptos can change its line breaks and page count when converted here.",
                    "If your document was created recently in Microsoft 365 and its exact layout matters, check which font it uses before converting.",
                ],
            },
            {
                "heading": "How to check which font your document uses",
                "paragraphs": [
                    "In Word, click inside the text: the font box on the Home tab shows the font. If it shows Aptos, or a font you don't recognise, that is the text most likely to move.",
                    "In the finished PDF, most readers can list the fonts actually used. In Adobe Acrobat Reader, open File > Properties and choose the Fonts tab; a name such as DejaVu Sans where you expected your own font means a substitution took place.",
                ],
            },
            {
                "heading": "How to avoid it",
                "paragraphs": [
                    "Choose a font with a metric-compatible replacement if layout precision matters. Calibri and Arial kept their layout exactly in our test, and Cambria, Times New Roman and Courier New also have metric-compatible replacements on our server.",
                    "To change a whole document quickly in Word, select all the text (Ctrl+A) and pick the new font, or change the font of the Normal style so every paragraph using it follows.",
                    "If you must keep a font with no replacement, such as Aptos or a decorative brand font, and need an exact match, save the PDF from Word itself (File > Save As > PDF) on a computer that has that font installed.",
                    "Always open the PDF and compare the page count and the last line of each page with your original before sending it. Your upload and the PDF are deleted from our server as soon as your download is ready.",
                ],
            },
        ],
    },
    {
        "slug": "pdf-compression-levels-explained",
        # Release 7, R7-78: official sources (each URL checked 13 Nov 2026).
        "sources": [('Ghostscript documentation: High Level Devices (PDF output presets)', 'https://ghostscript.readthedocs.io/en/latest/VectorDevices.html')],
        "title": "PDF Compression Explained: Screen vs eBook vs Printer (With Real Test Results)",
        "seo_title": "PDF Compression Levels Explained (Tested) | KuickKonvert",
        "meta_description": "What Screen, eBook and Printer PDF compression really change, why some PDFs barely shrink, and our own test results on photos, scans and text-only files.",
        "dek": "Compressing a PDF makes it smaller mainly by shrinking the pictures inside it: lowering their resolution and storing them with stronger JPEG compression. Text stays sharp at every level. Screen shrinks photos the most, eBook is the balanced choice, and Printer keeps the most detail -- while a text-only PDF may hardly shrink at all. Below: what each level does, and our own test results. To shrink a file now, use our [[compress-pdf|Compress PDF tool]].",
        "published": "2026-09-14",
        "updated": NEW_GUIDES_RELEASE_DATE,  # 24 Oct 2026: answer-first opening (was: "2026-10-02")
        "related_tools": ["compress-pdf", "merge-pdf"],
        "sections": [
            {
                "heading": "What actually makes a PDF big",
                "paragraphs": [
                    "Typed text takes up very little space in a PDF: each letter is stored as a character code plus a reference to a font, not as a picture. Lines, charts and other vector graphics are similarly compact. A 20-page report of plain text is often well under a megabyte.",
                    "Images are different. A single photo taken on a phone can be several megabytes, and a scanned document is nothing but images -- every page is one picture of paper. In practice, when a PDF is too big to email or upload, embedded images are almost always the reason. That's why every compression level works on images and leaves the text alone.",
                ],
            },
            {
                "heading": "What happens when you press Compress",
                "paragraphs": [
                    "Our Compress PDF tool -- a free [[compress-pdf|PDF size reducer]] -- rewrites your file with Ghostscript, a long-established open-source PDF engine, using one of its three standard presets: /screen, /ebook or /printer. Each preset combines two techniques.",
                    "Downsampling lowers the resolution of images that are sharper than the preset needs. Resolution is measured in dots per inch (dpi) -- how many pixels the image uses for each inch of the printed page. Halving the resolution leaves roughly a quarter of the pixels, which is where most of the saving comes from.",
                    "Re-encoding saves photographic images with JPEG compression, which discards fine detail the eye is unlikely to notice in exchange for a much smaller file.",
                    "Text stays as real text at every level, so it remains sharp at any zoom and can still be selected and searched.",
                ],
            },
            {
                "heading": "The three levels, in numbers",
                "paragraphs": [
                    "The figures below come from Ghostscript's own documentation for the three presets our tool uses.",
                    "Screen: colour and greyscale images are reduced to 72 dpi, and black-and-white images to 300 dpi. It also uses the stronger of the two JPEG settings. 72 dpi is fine on a screen but looks soft or blocky when printed.",
                    "eBook (our default): colour and greyscale images are reduced to 150 dpi, black-and-white images to 300 dpi, with the same JPEG setting as Screen. A 150 dpi image generally still prints acceptably at normal size, so this is the sensible balance for most documents.",
                    "Printer: the preset lists 300 dpi (1,200 dpi for black-and-white), but it has downsampling switched off, so images keep their original resolution. It also uses a gentler, higher-quality JPEG setting. The result looks almost identical to the original -- and is usually only slightly smaller, if at all.",
                ],
                "table": {
                    "caption": "The three presets at a glance",
                    "headers": ["Level", "Colour and greyscale images", "Black-and-white images", "Colour images reduced only if above", "JPEG setting", "Best for"],
                    "rows": [
                        ["Screen", "72 dpi", "300 dpi", "108 dpi", "Stronger", "Reading on screen only"],
                        ["eBook (default)", "150 dpi", "300 dpi", "225 dpi", "Stronger (same as Screen)", "Email and most documents"],
                        ["Printer", "Not reduced (keeps original)", "Not reduced", "No downsampling", "Gentler, higher quality", "Professional printing"],
                    ],
                    "note": "Source: Ghostscript's documentation for the /screen, /ebook and /printer presets used by our Compress PDF tool.",
                },
            },
            {
                "heading": "The 1.5x rule: why some images aren't touched at all",
                "paragraphs": [
                    "Ghostscript only downsamples an image when its resolution is more than 1.5 times the target. With the eBook target of 150 dpi, that means only images above 225 dpi are reduced; with Screen's 72 dpi, anything above 108 dpi is reduced.",
                    "This explains a common surprise. Suppose your scanner saves pages at 200 dpi. That's below eBook's 225 dpi threshold, so eBook leaves those images as they are and the file hardly changes. Only Screen shrinks it. A 300 dpi scan, on the other hand, is reduced by both Screen and eBook.",
                ],
            },
            {
                "heading": "What we measured",
                "paragraphs": [
                    "We ran three typical files through the same Ghostscript presets our tool uses (Ghostscript 10.02, September 2026). Your own results will depend on what's inside your PDF, but the pattern is consistent.",
                    "A PDF containing one 3000 x 2000 pixel photo at 300 dpi (3.2 MB): Screen produced 50 KB (1.6% of the original, photo now 72 dpi); eBook produced 127 KB (3.9%, photo now 150 dpi); Printer made no meaningful difference -- the photo kept its full 300 dpi.",
                    "A one-page greyscale scan at 200 dpi (93 KB): Screen produced 24 KB (25%). eBook and Printer didn't reduce it at all, because 200 dpi is below their downsampling threshold -- Ghostscript's output was actually 6-9% larger.",
                    "A five-page, text-only PDF (4.5 KB): every level produced a larger file -- about 25% larger on Screen and eBook, and 170% larger on Printer, which copied the font into the file. The text itself stayed as real, selectable text at every level.",
                ],
                "table": {
                    "caption": "Our test results (Ghostscript 10.02, September 2026)",
                    "headers": ["Test file", "Original", "Screen", "eBook", "Printer"],
                    "rows": [
                        ["One photo, 3000 x 2000 px at 300 dpi", "3.2 MB", "50 KB (1.6%)", "127 KB (3.9%)", "No meaningful change"],
                        ["One-page greyscale scan at 200 dpi", "93 KB", "24 KB (25%)", "Not reduced (6-9% larger)", "Not reduced (6-9% larger)"],
                        ["Five-page, text-only PDF", "4.5 KB", "About 25% larger", "About 25% larger", "About 170% larger"],
                    ],
                    "note": "When the result isn't smaller than your upload, our tool gives you back your original file instead.",
                },
            },
            {
                "heading": "Why a \"compressed\" file can come out bigger -- and what we do about it",
                "paragraphs": [
                    "Ghostscript's developers state plainly that rewriting a PDF is not guaranteed to make it smaller, and can make it larger. There's no image data to shrink in a text-only file, and rewriting the file can add overhead -- for example by copying fonts into it, as Printer did in our test.",
                    "So our tool compares the result with your upload. If the compressed version isn't smaller, you get your original file back unchanged instead of a bigger one. If that happens, your PDF is already about as small as these presets can make it.",
                ],
            },
            {
                "heading": "Can you compress a PDF without losing quality?",
                "paragraphs": [
                    "It depends on what is in the file. Text and vector graphics never lose quality: they stay as real text at every level. What can lose quality is images, because making a PDF smaller mostly means storing its images with fewer pixels or stronger JPEG compression.",
                    "If you want to compress a PDF without losing quality you can see, choose Printer (\"Highest quality, larger file\" in our tool). It keeps every image at its original resolution and uses the gentler JPEG setting. The trade-off, as our test showed, is that the file usually gets only slightly smaller, if at all.",
                    "To reduce a PDF's file size without losing quality that matters on screen, eBook is the practical middle ground: photos are reduced to 150 dpi, which still looks sharp on a phone or laptop and generally prints acceptably at normal size, while the text is untouched.",
                    "Whichever level you choose, open the compressed file, zoom in on the smallest text and on any photos, and keep your original until you're happy with the result.",
                ],
            },
            {
                "heading": "Which level to choose",
                "paragraphs": [
                    "Documents with photos that you'll email or read on screen: start with eBook. Try Screen only if you still need a smaller file and nobody will print it.",
                    "Scanned documents: eBook works well on 300 dpi scans. For 200 dpi scans only Screen reduces the size -- but a scanned page is a picture of text, so at 72 dpi small print can become hard to read. Open the result and zoom in before you send it.",
                    "Anything that will be printed professionally: use Printer, and expect only a small reduction.",
                    "Text-only PDFs such as contracts or letters: these are usually small already. Compression won't help much -- you'll most likely get your original back.",
                ],
            },
            {
                "heading": "A quick checklist before you send the file",
                "paragraphs": [
                    "Check the new file size against the limit you're trying to meet, open the compressed PDF and zoom in on the smallest text and on any photos, and keep your original file until you're happy with the compressed copy. Your uploaded file and the result are deleted from our server as soon as your download is ready, so we don't keep a copy for you.",
                ],
            },
        ],
    },
    {
        "slug": "jpg-vs-png",
        # Release 7, R7-78: official sources (each URL checked 13 Nov 2026).
        "sources": [('W3C: Portable Network Graphics (PNG) Specification', 'https://www.w3.org/TR/png/')],
        "title": "JPG vs PNG for Documents: Which Format to Use (With Real Test Results)",
        "seo_title": "JPG vs PNG for Documents and Scans | KuickKonvert",
        "meta_description": "JPG or PNG for scans, screenshots and document pages? What each format does to text and photos, our own size tests, and how our converters handle both.",
        "dek": "JPG is built for photos, PNG for sharp edges. For pages full of text, our own test found PNG was both sharper and smaller -- here's why, and when JPG is still the right call. To turn PDF pages into images, use [[pdf-to-png|PDF to PNG]] or [[pdf-to-jpg|PDF to JPG]].",
        "published": "2026-09-14",
        "updated": FIX_RELEASE_DATE,  # JPG to PDF wording: no re-compression, metadata removed (was RELEASE_DATE: links to PNG to JPG / JPG to PNG added)
        "related_tools": ["jpg-to-pdf", "png-to-pdf", "pdf-to-jpg", "pdf-to-png", "png-to-jpg", "jpg-to-png"],
        "sections": [
            {
                "heading": "The one difference that matters: lossy vs lossless",
                "paragraphs": [
                    "JPG (also written JPEG) uses lossy compression. It splits the picture into small blocks and throws away fine detail the eye is least likely to miss. On a photograph -- smooth skin tones, sky, foliage -- the loss is very hard to see, and the file becomes far smaller.",
                    "PNG uses lossless compression -- its W3C specification describes it as a format for lossless storage of images. Nothing is thrown away, so what you save is exactly what you get back.",
                    "The difference shows on sharp edges. The boundary between black text and white paper is exactly the kind of detail JPG simplifies, which leaves faint smudges and speckles (called artifacts) around letters. PNG keeps those edges perfectly clean.",
                ],
            },
            {
                "heading": "Transparency: only PNG has it",
                "paragraphs": [
                    "PNG can store an alpha channel -- a transparency value for every pixel -- which is why logos, icons and signatures with see-through backgrounds are usually PNGs. JPG has no transparency at all: every pixel is a solid colour.",
                ],
            },
            {
                "heading": "What we measured on a real document page",
                "paragraphs": [
                    "We created a one-page A4 letter -- a heading and six paragraphs of ordinary 11-point text -- and turned it into images with our own [[pdf-to-png|PDF to PNG]] and [[pdf-to-jpg|PDF to JPG]] tools, which render at 300 dpi (2481 x 3508 pixels).",
                    "The PNG was 645 KB. The JPG was 1.1 MB -- about 70% larger -- and it had lost detail: around 65,000 pixels around the letters changed noticeably compared with the exact PNG. Saved as a greyscale PNG, the same page was just 347 KB.",
                    "The reason is simple. A text page is mostly large areas of plain white with sharp black edges. Lossless PNG compression handles plain areas extremely efficiently, while JPG spends a lot of data trying to approximate every sharp edge -- and still doesn't get them exactly right.",
                ],
                "table": {
                    "caption": "The same A4 text page, rendered at 300 dpi (2481 x 3508 pixels)",
                    "headers": ["Saved as", "File size", "Exact copy of the page?"],
                    "rows": [
                        ["PNG (colour)", "645 KB", "Yes - lossless"],
                        ["JPG (quality 75)", "1.1 MB (about 70% larger)", "No - around 65,000 pixels around the letters changed noticeably"],
                        ["PNG (greyscale)", "347 KB", "Yes - lossless"],
                    ],
                },
            },
            {
                "heading": "Photos are the opposite",
                "paragraphs": [
                    "A photograph has almost no plain areas: every pixel differs slightly from its neighbours. Lossless PNG can't compress that kind of detail well, so a PNG of a camera photo is typically several times larger than a good-quality JPG of the same picture, and the extra detail PNG preserves is usually invisible. For photos, JPG is the right choice.",
                ],
            },
            {
                "heading": "JPG vs PNG quality for printing",
                "paragraphs": [
                    "For printing, resolution matters more than format. 300 dpi is a common standard for sharp prints at normal size, which is why our PDF to JPG and PDF to PNG tools render every page at 300 dpi.",
                    "Text, forms, line drawings and logos: print from PNG. Because PNG is lossless, letter edges stay clean, while the smudges JPG leaves around text can show up on paper.",
                    "Photographs: a good-quality JPG prints well and keeps the file small. If a print shop asks for a particular format, follow their instructions.",
                    "In short, the PNG vs JPG quality difference is easiest to see on text and hardest to see on photos.",
                ],
            },
            {
                "heading": "Which one to use",
                "paragraphs": [
                    "PNG for scanned text documents, screenshots, forms, charts, diagrams, and anything you'll need to read or zoom into later.",
                    "PNG for logos and graphics that need a transparent background.",
                    "JPG for photographs -- including a photo of a receipt or a whiteboard, where the camera image itself is already full of fine texture.",
                    "Already have a JPG? Converting it to PNG won't bring back the detail JPG discarded; it only makes the file bigger. Keep JPGs as JPGs -- unless a website or app insists on PNG, in which case [[jpg-to-png|JPG to PNG]] makes a lossless copy without adding any further loss.",
                    "Editing an image several times? Work in PNG. Every time a JPG is edited and saved again, it is compressed again and loses a little more detail.",
                ],
                "table": {
                    "caption": "JPG vs PNG at a glance",
                    "headers": ["", "JPG", "PNG"],
                    "rows": [
                        ["Compression", "Lossy - discards fine detail", "Lossless - keeps every pixel"],
                        ["Transparent background", "No", "Yes"],
                        ["Text and sharp edges", "Faint smudges (artifacts) around letters", "Perfectly clean"],
                        ["File size for photos", "Small", "Several times larger"],
                        ["File size for text pages", "Larger in our test", "Smaller in our test"],
                        ["Editing and re-saving", "Loses a little more detail each save", "No loss"],
                        ["Printing", "Good for photos", "Best for text, forms, line art and logos"],
                        ["Best for", "Photographs", "Scans of text, screenshots, forms, charts, logos"],
                    ],
                },
            },
            {
                "heading": "How our converters handle JPG and PNG",
                "paragraphs": [
                    "PDF to PNG renders every page at 300 dpi and saves it losslessly -- the best choice for pages with text, tables or line drawings.",
                    "PDF to JPG renders every page at 300 dpi and saves it as a standard-quality JPG (quality 75). That keeps photo-heavy pages compact, but as our test shows, text-heavy pages are often smaller and sharper as PNG.",
                    "[[jpg-to-pdf|JPG to PDF]] copies the compressed photo data from your JPG files into the PDF without re-compressing it, so there's no second round of compression and no extra quality loss -- only hidden metadata such as the location is removed. It also accepts PNG images, so photos and screenshots can go into one PDF.",
                    "PNG to PDF embeds your images without any lossy compression and keeps greyscale images in greyscale. Transparent areas are placed on a white background, the same as a logo printed on paper.",
                    "[[png-to-jpg|Our PNG to JPG converter]] saves each image as a quality-90 JPG -- the right move for photos stored as PNG. Transparent areas become white, and screenshots or text pages may not get any smaller.",
                    "JPG to PNG saves a lossless copy of each JPG for sites and apps that require PNG. It can't restore detail the JPG already lost, and the file gets bigger.",
                    "Every uploaded image and every result is deleted from our server as soon as your download is ready.",
                ],
            },
        ],
    },
    {
        "slug": "merge-pdf-in-the-right-order",
        "title": "How to Get the Page Order Right When Merging PDFs (and Fix It If It's Wrong)",
        "seo_title": "How to Get the Page Order Right When Merging | KuickKonvert",
        "meta_description": "How our Merge PDF tool decides page order, what survives a merge in our own tests, and how to fix a merged PDF whose pages came out in the wrong order.",
        "dek": "A merged PDF follows one simple rule: files are joined in the order they appear in your list. Here's how to get that list right first time, what a merge keeps and drops, and how to repair a file that came out wrong.",
        "published": "2026-10-05",
        "related_tools": ["merge-pdf", "split-pdf", "rotate-pdf"],
        "sections": [
            {
                "heading": "The one rule: list order is page order",
                "paragraphs": [
                    "Our Merge PDF tool, which lets you [[merge-pdf|combine PDF files]] for free, takes your files from top to bottom of the list shown under the upload box and copies every page of each file, in that order, into one new PDF. Nothing is sorted by name, date or size. If the list reads Cover, Report, Appendix, the merged file starts with every page of Cover, then every page of Report, then every page of Appendix.",
                    "Each time you choose or drop more files, they are added to the end of the list. That gives you a simple way to control the order: add your files one at a time, in the order you want them in the finished document.",
                    "If you select several files in one go, they appear in whatever order your browser passes them to the page, which is not always the order you clicked them. Always read the list before you press the button.",
                    "Each file in the list has a Remove button. There is no drag-to-reorder, so if a file is in the wrong place, remove it and the files after it, then add them again in the right order.",
                ],
            },
            {
                "heading": "Prepare your files before you upload",
                "paragraphs": [
                    "Number the file names. Renaming files to 01-cover.pdf, 02-report.pdf, 03-appendix.pdf makes the intended order obvious in the list, and in your file picker, which usually sorts by name.",
                    "Fix sideways pages first. Our Rotate PDF tool turns every page of a file by 90, 180 or 270 degrees, so rotate a sideways file on its own before merging rather than after.",
                    "Remove passwords. Merge cannot open a password-protected PDF, so the merge will stop with an error. Open the file with its password in your PDF reader, save or print an unprotected copy, and merge that copy.",
                    "Check the combined size. All uploads together must stay under our 50 MB limit. If a scanned file is very large, run it through Compress PDF first.",
                ],
            },
            {
                "heading": "What a merge keeps and what it drops: our test",
                "paragraphs": [
                    "We merged three test files with the same code our tool runs (October 2026): a one-page A4 cover, a three-page US Letter report containing three bookmarks and a web link, and a two-page landscape A4 appendix.",
                    "The result had all six pages in the correct order. Each page kept its own size and orientation -- the A4, Letter and landscape pages were not forced to one size -- and the web link was kept.",
                    "Two things did not carry over. The report's three bookmarks (the clickable outline some PDF readers show in a side panel) were gone, and the document title stored in the first file's properties was not copied into the merged file. If you need bookmarks, add them again in a PDF editor after merging.",
                ],
                "table": {
                    "caption": "Merging three test files with our Merge PDF tool (October 2026)",
                    "headers": ["What we checked", "Result"],
                    "rows": [
                        ["Page order", "Kept - all 6 pages in list order"],
                        ["Page sizes (A4, US Letter, landscape A4)", "Kept - each page keeps its own size and orientation"],
                        ["Web link inside the report", "Kept"],
                        ["Bookmarks (3 in the report)", "Not kept - the merged file had none"],
                        ["Document title in file properties", "Not kept"],
                        ["Password-protected input file", "Not accepted - the merge stops with an error"],
                    ],
                },
            },
            {
                "heading": "How to fix a merged PDF with the pages in the wrong order",
                "paragraphs": [
                    "If whole files are in the wrong order, the quickest fix is to merge again from your original files. Add them one at a time, check the list, then merge.",
                    "If you no longer have the originals, or need to move individual pages, use [[split-pdf|Split PDF]] and then Merge PDF. Split PDF breaks a file into one PDF per page and gives you a ZIP of files named page-001.pdf, page-002.pdf and so on. Unzip it, then merge the pages back together in the order you want, adding them one at a time.",
                    "If just one page is sideways, the same method works. Split the file, run that single page through Rotate PDF, then merge all the pages again. Rotate PDF turns every page of the file you give it, which is why the page has to be on its own first.",
                    "The same split-and-merge method also removes pages: simply leave out the ones you don't need when you merge the pages back together.",
                ],
            },
            {
                "heading": "Final checks before you send it",
                "paragraphs": [
                    "Scroll through the whole merged file once. Check the first and last page of each original file, since the joins between files are where order mistakes show up.",
                    "Check the page count. It should equal the page counts of your original files added together.",
                    "If the recipient relies on bookmarks or a document title, add them back in a PDF editor -- a merge doesn't keep them.",
                    "Keep your original files until you're happy with the result. Your uploads and the merged file are deleted from our server as soon as your download is ready, so we can't recover them for you.",
                ],
            },
        ],
    },
    {
        "slug": "pdf-password-protection-explained",
        # Release 7, R7-78: official sources (each URL checked 13 Nov 2026).
        "sources": [('PDF Association: ISO 32000-2 (PDF 2.0)', 'https://pdfa.org/resource/iso-32000-2/')],
        "title": "Password-Protecting a PDF: What AES-256 Encryption Protects (and What It Doesn't)",
        "seo_title": "PDF Password Protection Explained (AES-256) | KuickKonvert",
        "meta_description": "What our Protect PDF tool's AES-256 encryption hides, what stays visible, why your password still matters most, and our own test results.",
        "dek": "A password-protected PDF hides its contents from anyone without the password. But some details stay visible, and in practice the strength of your password decides how safe the file is.",
        "published": "2026-10-05",
        "related_tools": ["protect-pdf", "watermark-pdf"],
        "sections": [
            {
                "heading": "What our Protect PDF tool actually does",
                "paragraphs": [
                    "Protect PDF lets you [[protect-pdf|password protect a PDF]] online: it encrypts your file with a password you choose (at least 4 characters), using 256-bit AES encryption -- the method the current PDF standard, PDF 2.0 (ISO 32000-2), specifies for password-protected PDFs. Adobe Acrobat and Reader have supported 256-bit AES since version 9, so the recipient only needs the password and an up-to-date PDF reader.",
                    "Some very old PDF software can't open this type of file. For example, the developers of the iText PDF library note that iText 5 and earlier versions can't read it. If someone can't open your protected file, ask them to update their PDF reader.",
                    "When we checked a protected file with three independent PDF programs (October 2026), opening it without the password failed, and opening it with the password worked normally.",
                    "The password you set is used to open the file. Our tool does not add separate restrictions on printing, copying or editing, so anyone who has the password can do everything with the document that they could with the original.",
                    "Until 5 October 2026 our tool used an older method, 128-bit RC4 encryption, which Adobe Acrobat and Reader have supported since version 7. Files protected before that date keep that older method.",
                ],
            },
            {
                "heading": "What is hidden, and what isn't",
                "paragraphs": [
                    "We protected a three-page test report and then searched the raw bytes of the protected file for anything readable without the password (October 2026).",
                    "The page text could not be found, and neither could the document's title. Encryption scrambles the text, images and other content of every page, and the document's properties -- such as its title and author -- are kept in the file but encrypted too, so they only appear once the file is opened with the password.",
                    "Some structural details are not encrypted, because PDF encryption is designed to protect content, not the file's layout. The page count and each page's size could still be read directly from the file. And, as with any file, its name and size are visible to anyone who can see the file -- so don't put sensitive information in the file name.",
                ],
                "table": {
                    "caption": "Reading a protected test file without the password (October 2026)",
                    "headers": ["Part of the file", "Readable without the password?"],
                    "rows": [
                        ["Text on the pages", "No"],
                        ["Images on the pages", "No - all page content is encrypted"],
                        ["Title, author and other document properties", "No - kept in the file, but encrypted"],
                        ["Number of pages", "Yes"],
                        ["Size of each page", "Yes"],
                        ["File name and file size", "Yes - like any file"],
                    ],
                },
            },
            {
                "heading": "Why your password matters more than the encryption",
                "paragraphs": [
                    "Guessing a 256-bit encryption key directly isn't practical, but the key is protected by your password -- and a password can be guessed. Anyone with a copy of the file can try passwords on it as many times as they like, with no lockout. So the real question is how long it would take to try every possible password of yours.",
                    "To give a feel for it, we timed a simple password-guessing script on a single processor core. Against a file protected by our tool it managed about 130 guesses per second. Against the same file protected with the older 128-bit RC4 method, the same script managed roughly 2,100 to 2,700 guesses per second -- the newer method takes far more computing work to check each password. The table shows the worst case at 130 guesses per second: the time to try every combination of a given length.",
                    "Dedicated password-recovery software running on graphics cards is many times faster than our simple script, and real attackers try common words and patterns first. Treat these times as the most optimistic case, not a guarantee.",
                ],
                "table": {
                    "caption": "Time to try every possible password at about 130 guesses per second (our single-core test on an AES-256 file, October 2026)",
                    "headers": ["Password", "Possible combinations", "Time to try them all"],
                    "rows": [
                        ["4 lowercase letters", "456,976", "About 1 hour"],
                        ["6 lowercase letters", "About 309 million", "About 4 weeks"],
                        ["8 lowercase letters", "About 209 billion", "About 51 years"],
                        ["8 characters: upper, lower and digits", "About 218 trillion", "About 53,000 years"],
                        ["10 characters: upper, lower and digits", "About 839 quadrillion", "About 205 million years"],
                    ],
                    "note": "Faster tools reduce these times a great deal. A password that is a word or name can be found far sooner than the table suggests.",
                },
            },
            {
                "heading": "A note on encryption standards",
                "paragraphs": [
                    "PDF 2.0 deprecates every use of RC4 encryption and promotes AES-256 instead, as summarised by the PDF Association. That is why our tool now uses AES-256.",
                    "If you protected a file with our tool before 5 October 2026, it uses 128-bit RC4. To move it to AES-256, open it with its password in your PDF reader, save or print a copy without a password, and run that copy through Protect PDF again.",
                    "Whatever the method, for everyday privacy -- sending a payslip, a bank statement or a signed form so that it can't be opened by someone who intercepts it or finds it later -- the deciding factor is still the password.",
                ],
            },
            {
                "heading": "Good practice for protecting a PDF",
                "paragraphs": [
                    "Use at least 10 characters mixing upper-case letters, lower-case letters and digits, and avoid names, dates and dictionary words.",
                    "Send the password separately: for example, email the PDF and send the password by text message or tell it to the recipient by phone. A password in the same email as the file protects nothing.",
                    "Keep an unprotected original somewhere safe. A forgotten password cannot be recovered or reset -- not by us, and not by anyone else without guessing it -- and we don't keep a copy of your file or your password. Your upload and the protected file are deleted from our server as soon as your download is ready.",
                    "Don't put sensitive details in the file name, since the name stays visible.",
                ],
            },
        ],
    },
    {
        "slug": "excel-to-pdf-fit-on-one-page",
        "title": "How to Make a Spreadsheet Fit on One Page When You Save It as a PDF",
        "seo_title": "How to Fit a Spreadsheet on One PDF Page | KuickKonvert",
        "meta_description": "Why spreadsheets split across pages in a PDF, what our Excel to PDF tool does automatically, our measured results, and how to keep the text readable.",
        "dek": "To fit a whole sheet on one PDF page in Excel, open Page Layout > Page Setup, choose Fit to 1 page wide by 1 tall, then save as PDF. Our Excel to PDF tool does the width part automatically: every column is fitted across the page, and long sheets continue onto further pages. The real question is how small the text becomes -- and that is something you can control before you upload. To convert a sheet, use our [[excel-to-pdf|Excel to PDF converter]].",
        "published": "2026-10-05",
        "updated": NEW_GUIDES_RELEASE_DATE,  # 24 Oct 2026: answer-first opening (was: "2026-10-10")
        "related_tools": ["excel-to-pdf"],
        "sections": [
            {
                "heading": "Why spreadsheets split across pages",
                "paragraphs": [
                    "A spreadsheet has no page size; a PDF does. Converting one to the other means fitting a grid that can be any width onto pages of a fixed size. Unless the file says otherwise, a spreadsheet program prints columns that don't fit onto extra pages, so a wide sheet can turn into a PDF where the right-hand columns are on page 2 -- separated from the rows they belong to.",
                ],
            },
            {
                "heading": "What our tool does automatically",
                "paragraphs": [
                    "Before converting, our [[excel-to-pdf|Excel to PDF converter]] adjusts the page setup of every sheet in your workbook.",
                    "Every column is fitted across the page width. The tool sets each sheet to fit one page wide, so no column is ever cut off or pushed onto a separate page. Long sheets are not squeezed vertically; they simply continue onto further pages, top to bottom.",
                    "Column widths are set from your content. Each column is widened to fit its longest entry (with a minimum of 8 characters and a maximum of 60), so entries aren't cut off in the PDF.",
                    "Wide sheets are turned to landscape. If a sheet's columns add up to more than about 80 characters across, the page is set to landscape, which gives noticeably more width and lets the text stay larger.",
                    "Your own print area, print titles and hidden columns are respected, as our tests below show. Hidden sheets are not included in the PDF.",
                ],
            },
            {
                "heading": "What we measured",
                "paragraphs": [
                    "We converted several test workbooks with the same code our tool runs and measured the result (LibreOffice 24.2, October 2026). The text size is the size the cell text came out at in the PDF; 11 pt is the size it was typed in.",
                    "The pattern is clear: the tool always keeps every column, but the more total width a sheet has, the smaller the text. A 12-month budget fitted comfortably at full size. Twenty columns with long headings shrank the text to 3.6 pt, which is very hard to read on paper. Forty columns still fitted, but at 1.8 pt.",
                ],
                "table": {
                    "caption": "Our Excel to PDF tests (LibreOffice 24.2, October 2026)",
                    "headers": ["Test sheet", "PDF pages", "Text size in the PDF"],
                    "rows": [
                        ["Budget: 14 short columns (Jan-Dec and Total), 25 rows", "1", "11 pt - full size"],
                        ["20 columns with long headings, 30 rows", "1", "3.6 pt - hard to read"],
                        ["40 columns, 30 rows", "1", "1.8 pt - all columns present, but unreadable on paper"],
                        ["5 columns, 300 rows", "10", "11 pt - headings on page 1 only"],
                        ["Same sheet with row 1 set as a print title", "10", "11 pt - headings repeated on every page"],
                        ["20-column sheet with print area A1:H31", "1", "9.3 pt - only columns A to H"],
                        ["20-column sheet with columns I to T hidden", "1", "9.3 pt - hidden columns left out"],
                    ],
                    "note": "Exact text sizes can vary slightly between LibreOffice versions and fonts; the pattern does not.",
                },
            },
            {
                "heading": "How to keep the text readable",
                "paragraphs": [
                    "Set a print area. If only part of the sheet needs to be in the PDF, select that range in Excel and choose Page Layout > Print Area > Set Print Area, then save. In our test, limiting a 20-column sheet to columns A to H raised the text from 3.6 pt to 9.3 pt.",
                    "Hide or delete columns the reader doesn't need. Helper columns, IDs and working calculations take up width. Hidden columns are left out of the PDF, with the same effect as a print area in our test.",
                    "Shorten long headings and long text. Because each column is sized to its longest entry, one long heading or comment widens the whole column. Wrap or abbreviate long headings, or move long notes to a separate sheet.",
                    "Split one very wide sheet into two. A sheet of 40 columns will never be comfortable on one page. Two sheets of 20 columns each, or one summary sheet plus a detail sheet, are far easier to read.",
                ],
            },
            {
                "heading": "Long sheets: repeat the headings on every page",
                "paragraphs": [
                    "Fitting the width never squeezes rows onto one page, so a long list still runs to several pages. In our 300-row test the column headings only appeared on page 1, which makes pages 2 to 10 hard to follow.",
                    "The fix is a print title. In Excel, choose Page Layout > Print Titles and set Rows to repeat at top to your heading row (for example $1:$1), then save. With that set, our tool repeated the headings at the top of every one of the 10 pages.",
                ],
            },
            {
                "heading": "Formulas in the PDF",
                "paragraphs": [
                    "A PDF shows values, not formulas. When we convert, your spreadsheet's formulas are recalculated and the PDF shows the resulting numbers -- not the =SUM() or =VLOOKUP() behind them -- exactly as a printout would.",
                    "One thing worth a check: a very new spreadsheet function (for example XLOOKUP or the newer dynamic-array functions) can occasionally come through as an error in the PDF, because the conversion engine recalculates the sheet and may not support the very latest functions. If your sheet relies on recent functions, open the PDF and confirm the totals match your spreadsheet. If a cell shows an error, either paste those results as values before converting, or save the sheet as a PDF from Excel itself and upload that.",
                ],
            },
            {
                "heading": "Quick checklist before converting",
                "paragraphs": [
                    "Hide or delete columns the reader doesn't need, set a print area if only part of the sheet matters, shorten very long headings, set a print title on long sheets, and unhide any sheet you want included. Then convert and zoom in on the PDF to check the smallest text. Your upload and the PDF are deleted from our server as soon as your download is ready.",
                ],
            },
        ],
    },
    {
        "slug": "pdf-to-excel-table-conversion-results",
        "title": "Why Some PDF Tables Don't Convert Cleanly to Excel (With Test Results)",
        "seo_title": "Why PDF Tables Don't Convert Cleanly to Excel | KuickKonvert",
        "meta_description": "Why some PDF tables convert to Excel cleanly and others don't: our tests on ruled, borderless, merged and multi-page tables, and how to fix each one.",
        "dek": "A PDF doesn't actually contain a table -- just text and lines placed on a page. How well a table converts to Excel depends on how clearly those lines mark out the cells. Here's what we found.",
        "published": "2026-10-05",
        "related_tools": ["pdf-to-excel"],
        "sections": [
            {
                "heading": "Why tables are hard to get out of a PDF",
                "paragraphs": [
                    "A spreadsheet knows which cell every value is in. A PDF doesn't: it records each piece of text and each line as a drawing instruction at a position on the page. When you look at a PDF table you see rows and columns, but the file only knows that some text sits near some lines.",
                    "So a [[pdf-to-excel|PDF to Excel converter]] has to rebuild the table. Our tool uses an open-source library called pdfplumber to find table structures on each page, mainly from the ruling lines drawn around and between cells, and then writes each table into a worksheet, with the text found above and below it.",
                ],
            },
            {
                "heading": "How our tool lays out the Excel file",
                "paragraphs": [
                    "Each page of the PDF that has content becomes its own worksheet, named Page 1, Page 2 and so on.",
                    "Text around a table is kept. A heading above a table and a total below it are written into the same sheet, one line per row, so nothing on the page is silently dropped.",
                    "A page where no table is detected still contributes its text, one line per row in column A.",
                    "Every value is written as text. The tool does not guess whether 1,000.50 is a number, a code or a date, so it leaves that decision to you. The next sections show how to turn those values into real numbers.",
                ],
            },
            {
                "heading": "What we measured",
                "paragraphs": [
                    "We built five test PDFs of a typical invoice table -- Date, Description, Qty, Unit price and Amount -- and converted each with the same code our tool runs (October 2026).",
                ],
                "table": {
                    "caption": "Our PDF to Excel tests (October 2026)",
                    "headers": ["Test PDF", "Result in Excel", "What to do"],
                    "rows": [
                        ["Table with ruled lines around every cell", "All 5 columns correct; heading and Total line kept", "Convert number columns from text to numbers"],
                        ["Same table with no lines (borderless)", "Each whole row placed as one line in column A", "Use Data > Text to Columns, then check every row"],
                        ["Table with a merged title cell across the top", "Title placed in the first column only; table below correct", "Merge or re-centre the title in Excel if needed"],
                        ["Ruled table running across 2 pages", "Two sheets (Page 1 and Page 2); header row repeated on sheet 2", "Copy the rows into one sheet and delete the repeated header"],
                        ["Scanned PDF (a picture of the same table)", "Not converted - message that no text or tables could be found", "Needs OCR first - see below"],
                    ],
                },
            },
            {
                "heading": "Fix 1: numbers stored as text",
                "paragraphs": [
                    "In our test, values like 1,000.50 and PKR 1,000 arrived in Excel as text. You'll often see a small green triangle in the cell's corner, and SUM formulas will ignore those cells.",
                    "For plain numbers, select the column, click the warning icon that appears next to the selection and choose Convert to Number.",
                    "For values with a currency label or other text, remove the text first. Select the column, press Ctrl+H, type the label exactly as it appears -- for example PKR followed by a space -- in Find what, leave Replace with empty, and choose Replace All. Then use Convert to Number.",
                ],
            },
            {
                "heading": "Fix 2: borderless tables land in column A",
                "paragraphs": [
                    "Without ruling lines there is nothing reliable to show where one column ends and the next begins, so in our test each row came through as a single line of text in column A.",
                    "Excel can split those lines for you. Select column A, choose Data > Text to Columns, pick Delimited and tick Space. Check the result carefully: a value that itself contains spaces, such as a description like \"Office chair\", will be split across two columns and needs to be joined back together. If you can get the original file the PDF was made from, such as the Excel or Word file, use that instead.",
                ],
            },
            {
                "heading": "Fix 3: one table spread over several sheets",
                "paragraphs": [
                    "Because each PDF page becomes its own sheet, a long table is split into pieces -- and if the PDF repeats the header row on every page, each piece starts with that header. Copy the rows from Page 2 onwards onto the end of the Page 1 sheet, then delete the extra header rows. Sorting or filtering by the first column can help you spot the repeats.",
                ],
            },
            {
                "heading": "Scanned PDFs need OCR first",
                "paragraphs": [
                    "A scanned PDF is a picture of a page. There is no text in it for a converter to read, so our tool stops with a message that no text or tables could be found. Our site does not currently offer OCR (optical character recognition, which turns a picture of text into real text).",
                    "To check whether a PDF is scanned, open it and try to select a word, or search for a word with Ctrl+F. If you can't, it's a picture. The best option is usually to ask the sender for the original file, or for a PDF exported directly from the software that created it.",
                ],
            },
            {
                "heading": "Getting the best result",
                "paragraphs": [
                    "PDFs exported from accounting or banking software, with lines around every cell, convert best. Check totals in Excel against the PDF after converting, convert number columns from text, and keep the original PDF for reference. Your upload and the Excel file are deleted from our server as soon as your download is ready.",
                ],
            },
        ],
    },
    {
        "slug": "photos-to-one-pdf-jpg-to-pdf-tips",
        "title": "How to Turn Photos into One PDF for Applications and Forms",
        "seo_title": "How to Put Photos into One PDF for Forms | KuickKonvert",
        "meta_description": "Combine phone photos into one PDF for an application or form: why photo PDFs get huge, why compression may not help, and our tested fix.",
        "dek": "Combining photos into one PDF is easy. Getting a PDF small enough for an upload portal, with sensibly sized pages, takes one extra step before you upload -- here's what our tests showed.",
        "published": "2026-10-05",
        "updated": FIX_RELEASE_DATE,  # JPG to PDF wording + measured sizes (was 2026-10-10)
        "related_tools": ["jpg-to-pdf", "compress-pdf", "merge-pdf"],
        "sections": [
            {
                "heading": "How our JPG to PDF tool builds the PDF",
                "paragraphs": [
                    "Our [[jpg-to-pdf|photo to PDF converter]] puts each photo on its own page, in the order of the file list. Files are added to the end of the list each time you choose more, and each one has a Remove button, so the easiest way to get the order right is to add the photos one at a time.",
                    "Your JPGs go into the PDF without being re-compressed: the compressed photo data is copied across as it is, and only hidden metadata such as the location is removed (more on that below). There is no second round of compression, so no quality is lost -- but it also means the PDF ends up about the same size as all your photos added together. In our test, three images totalling 9,693 KB produced a 9,694 KB PDF.",
                    "Photos taken with the phone held upright are shown upright. Phones often store such photos sideways with a tag telling viewers how to turn them, and our tool follows that tag: our sideways-stored test photo was set to display upright in the PDF.",
                ],
            },
            {
                "heading": "iPhone and web photos, and a note on location data",
                "paragraphs": [
                    "The JPG to PDF tool takes JPG and PNG images. iPhone photos are often saved as HEIC, and pictures saved from a website are often WEBP; neither goes straight in. Convert them to JPG first with our [[heic-to-jpg|HEIC to JPG converter]] or [[webp-to-jpg|WEBP to JPG converter]] (up to 20 at a time), then combine the JPGs into one PDF.",
                    "A note on location data. As it builds the PDF, our JPG to PDF tool now removes the hidden EXIF data -- including any GPS location -- from each JPEG, without changing the picture itself, so the place a photo was taken is not carried into the PDF. If you start from a HEIC or WEBP photo, our image converters also keep only the date taken and the camera make and model and drop GPS, so either route keeps your location private.",
                ],
            },
            {
                "heading": "Why the pages can come out enormous",
                "paragraphs": [
                    "The page size of each PDF page is worked out from the photo's pixel count and its dpi label (dots per inch) -- the setting that says how big the picture should be when printed. Photos from cameras and phones are often labelled 72 dpi, or have no dpi label at all.",
                    "In our test, a 12-megapixel photo (4032 x 3024 pixels) labelled 72 dpi became a page of 56 x 42 inches -- about 142 x 107 cm, far larger than A4. The same photo with no dpi label -- or with its dpi label stored only in the photo's hidden EXIF data, which our converter removes along with the location -- became a 42 x 31.5 inch page. A scan saved at 300 dpi by contrast came out at its true size, 8.3 x 11.7 inches (A4).",
                    "Most people won't notice, because PDF readers zoom to fit the screen. But a reviewer who prints the file, or a portal that checks page size, may.",
                ],
            },
            {
                "heading": "Why Compress PDF may not shrink a photo PDF",
                "paragraphs": [
                    "This surprised us. We combined two realistic phone photos (about 2.7 MB each) into a 5,456 KB PDF and ran it through [[compress-pdf|Compress PDF]] at all three levels. The file stayed at 5,456 KB every time.",
                    "The reason is the page size. Compression reduces image resolution in dots per inch, and on a 56-inch-wide page a 4032-pixel photo is only 72 dpi -- already below every threshold, so there is nothing for the compressor to reduce. Our Compress PDF tool gives you the original back when it can't make the file smaller.",
                    "When we labelled one of the same photos 300 dpi, compression worked as expected: the 2,726 KB one-photo PDF shrank to 319 KB on eBook and 116 KB on Screen.",
                ],
            },
            {
                "heading": "The reliable fix: resize the photos first",
                "paragraphs": [
                    "For applications and forms, a photo doesn't need 12 megapixels. Resizing each photo before converting makes the PDF smaller and the pages more sensible at the same time.",
                    "In our test, resizing a 12-megapixel photo to 1600 x 1200 pixels at JPEG quality 85 cut it to 359 KB, and a PDF of two such photos was 720 KB -- down from 5,456 KB. At 2000 x 1500 pixels each photo was 526 KB, which still keeps small print on a document readable.",
                    "On Windows, open the photo in Paint, choose Resize, select Pixels and enter a width, then save a copy. On a Mac, open it in Preview and use Tools > Adjust Size. Many phone gallery and sharing apps also offer a smaller size option.",
                ],
                "table": {
                    "caption": "Two phone photos combined into one PDF (our tests, October 2026)",
                    "headers": ["What we did", "PDF size"],
                    "rows": [
                        ["Original 12-megapixel photos (about 2.7 MB each)", "5,456 KB"],
                        ["Same PDF through Compress PDF (any level)", "5,456 KB - not reduced"],
                        ["Photos resized to 2000 x 1500 first", "About 1,050 KB (526 KB per photo)"],
                        ["Photos resized to 1600 x 1200, quality 85, first", "720 KB"],
                    ],
                    "note": "The 2000 x 1500 PDF size is estimated from the measured photo sizes, since JPG to PDF keeps each JPG unchanged.",
                },
            },
            {
                "heading": "Tips for application and form uploads",
                "paragraphs": [
                    "Read the portal's rules first: maximum file size, whether it wants one PDF or separate files, and whether it asks for a particular page size.",
                    "Photograph documents flat, in good light, with the whole page in frame, and crop away the background before converting.",
                    "Add pages in the order the form asks for -- for example ID front, ID back, then certificates -- adding one photo at a time.",
                    "Our JPG to PDF tool accepts JPG and PNG files, so phone photos and PNG screenshots can go into one PDF in a single step.",
                    "Open the finished PDF and check every page is upright, readable and in order before you submit. Your photos and the PDF are deleted from our server as soon as your download is ready.",
                ],
            },
        ],
    },
    {
        "slug": "pdf-to-word-text-vs-scanned",
        "title": "Text-Based vs Scanned PDFs: Converting to Word, and What to Do With a Scan",
        "seo_title": "Text vs Scanned PDFs: Converting to Word | KuickKonvert",
        "meta_description": "Why some PDFs convert to editable Word text and others become a picture: how to spot a scan, our own test results, and a free way to handle scans.",
        "dek": "Whether a PDF converts into editable Word text depends on one thing: whether the PDF contains real text or a picture of text. Here's how to tell in five seconds, and what to do when it's a scan.",
        "published": "2026-10-05",
        "related_tools": ["pdf-to-word", "pdf-to-excel"],
        "sections": [
            {
                "heading": "Two kinds of PDF that look the same",
                "paragraphs": [
                    "A text-based PDF is created by software -- Word, Excel, an accounting system, a website's Save as PDF button. Each letter is stored as a real character in a font, so it can be selected, searched and copied.",
                    "A scanned PDF is created by a scanner or a phone camera. Each page is a single photograph of paper. It looks identical on screen, but to a computer there are no letters in it, only pixels.",
                    "PDF to Word conversion rebuilds a Word document from the text, tables and images in the PDF. With a text-based PDF there is plenty to work with. With a scan, the only thing on the page is a picture.",
                ],
            },
            {
                "heading": "How to tell which one you have",
                "paragraphs": [
                    "Open the PDF and try to highlight a sentence with your mouse. If individual words highlight, the PDF has real text. If a whole rectangle is selected, or nothing is, it's a picture.",
                    "Or press Ctrl+F (Cmd+F on a Mac) and search for a word you can see on the page. If the reader can't find it, the page is an image.",
                    "Our test files showed the difference plainly: the text-based version of our test document contained 801 selectable characters; the scanned version contained none.",
                ],
            },
            {
                "heading": "What we measured",
                "paragraphs": [
                    "We made a one-page test document -- a heading, four short clauses and a small rent table -- and converted three versions of it with the same code our tool runs (October 2026). Our [[pdf-to-word|PDF to Word converter]] is built on pdf2docx, an open-source library, with LibreOffice as a fallback.",
                    "The text-based PDF converted into an editable Word document: 140 words of text and a real Word table, with \"Monthly rent\" and \"PKR 45,000\" in editable cells.",
                    "The scanned PDF became a Word document containing one picture of the page and no text.",
                    "The third version is the one that catches people out. We ran the scan through Tesseract, a free OCR program, which adds an invisible text layer behind the picture so the PDF becomes searchable. That PDF had 818 selectable characters -- yet our tool still produced one picture and no text. The converter did not use the invisible OCR text at all.",
                ],
                "table": {
                    "caption": "Converting three versions of the same page with our PDF to Word tool (October 2026)",
                    "headers": ["PDF version", "Selectable characters in the PDF", "Word result"],
                    "rows": [
                        ["Text-based (exported from software)", "801", "Editable: 140 words and 1 Word table"],
                        ["Scanned (picture only)", "0", "1 picture, no editable text"],
                        ["Scanned, then made searchable with OCR", "818 (invisible layer)", "1 picture, no editable text"],
                    ],
                },
            },
            {
                "heading": "What to do with a scanned PDF",
                "paragraphs": [
                    "Ask for the original. If the document came from an office or a company, the Word file or a PDF exported directly from their software will convert far better than any scan.",
                    "Use OCR to turn the picture into text. Google Drive offers this for free. According to Google's help page, open drive.google.com on a computer, upload the PDF, right-click it and choose Open with > Google Docs. Google converts the file and opens the result as a Google Doc, which you can download as a Word file with File > Download > Microsoft Word (.docx).",
                    "Google lists some requirements for good results: the file should be 2 MB or smaller, text should be at least 10 pixels high, pages must be the right way up, and common fonts such as Arial or Times New Roman work best. Google also notes that bold, italics, font size, font type and line breaks are likely to be kept, but lists, tables, columns, footnotes and endnotes are not likely to be detected -- so expect to rebuild tables by hand.",
                    "If a scanned page is sideways or upside down, fix it with our Rotate PDF tool before uploading it to Drive. If the file is over 2 MB, our Compress PDF tool may bring it under the limit, but zoom in afterwards to make sure small text is still sharp, because OCR needs clear letters.",
                    "Tesseract is also free and open source if you prefer software on your own computer, but as our test shows, its searchable PDF output still converts to a picture in our tool. Use it for copying text, not as a step before our PDF to Word tool.",
                ],
            },
            {
                "heading": "Getting the best result from a text-based PDF",
                "paragraphs": [
                    "Text-based PDFs with a simple layout -- letters, contracts, reports -- convert best. Complex layouts, such as multi-column brochures or text over images, can need tidying in Word afterwards.",
                    "Our tool cannot open password-protected PDFs, so remove the password first. Your upload and the Word file are deleted from our server as soon as your download is ready.",
                ],
            },
        ],
    },
    {
        "slug": "powerpoint-to-pdf-and-back",
        "title": "PowerPoint and PDF, Both Ways: What Carries Over (With Test Results)",
        "seo_title": "PowerPoint and PDF: What Carries Over | KuickKonvert",
        "meta_description": "What happens to hidden slides, speaker notes, links and fonts when you convert PowerPoint to PDF — and why PDF to PowerPoint gives picture slides. Our tests.",
        "dek": "Converting a presentation to PDF keeps what the audience sees and drops what only the presenter sees. Converting back gives you slides you can show, but not edit. Here's exactly what our tests found. To convert a deck now, use our [[ppt-to-pdf|PowerPoint to PDF converter]].",
        "published": "2026-10-05",
        "updated": "2026-10-10",
        "related_tools": ["ppt-to-pdf", "pdf-to-ppt"],
        "sections": [
            {
                "heading": "What carries over into the PDF",
                "paragraphs": [
                    "Our [[ppt-to-pdf|PPT to PDF converter]] turns .ppt and .pptx files into PDF with LibreOffice, one PDF page per slide. The page has the same shape as your slides, so a widescreen 16:9 deck gives widescreen 13.33 x 7.5 inch pages, not A4 or Letter.",
                    "The result is a fixed copy of the deck: it looks the same on any device, and nobody needs PowerPoint to open it -- which is why PDF is the usual way to send slides to a client or attach them to an application.",
                ],
            },
            {
                "heading": "What we measured",
                "paragraphs": [
                    "We built a five-slide widescreen test deck with a title and two bullet points on each slide, speaker notes on every slide, a web link on slide 2, and slide 4 set to hidden. We converted it with the same code and fonts our server uses (LibreOffice 24.2, October 2026).",
                    "The PDF had four pages, because the hidden slide was left out. None of the speaker notes appeared. The link on slide 2 stayed clickable, and all the slide text could be selected and searched. The 39.7 KB presentation became a 20.5 KB PDF.",
                ],
                "table": {
                    "caption": "Converting a five-slide test deck with our PPT to PDF tool (October 2026)",
                    "headers": ["What we checked", "Result in the PDF"],
                    "rows": [
                        ["Number of pages", "4 - one per visible slide"],
                        ["Hidden slide", "Left out"],
                        ["Speaker notes", "Not included"],
                        ["Web link on a slide", "Kept and clickable"],
                        ["Slide text", "Real text - selectable and searchable"],
                        ["Page size", "13.33 x 7.5 inches, the same as the 16:9 slides"],
                        ["Calibri text", "Shown in Carlito, its metric-compatible replacement"],
                    ],
                },
            },
            {
                "heading": "Before you convert a presentation",
                "paragraphs": [
                    "Unhide any slide you want in the PDF. Hidden slides are skipped, which is useful for backup slides you don't want to send -- and a surprise if you forgot one was hidden. In PowerPoint's Slide Sorter view, hidden slides are easy to spot because their slide numbers are crossed out.",
                    "Don't rely on speaker notes. If the reader needs them, move the key points onto the slides, or create notes pages in PowerPoint itself (its Notes Pages print layout) and print those to PDF.",
                    "Check your fonts. The same font substitution that can shift Word documents applies to slides, including Aptos, the newer Microsoft 365 default -- see our guide on why a PDF's layout sometimes shifts. Text that just fits a box in PowerPoint can wrap differently in another font.",
                    "Keep the file under our 50 MB upload limit.",
                ],
            },
            {
                "heading": "PDF to PowerPoint: why you get picture slides",
                "paragraphs": [
                    "Our [[pdf-to-ppt|PDF to PPT converter]] makes one slide per PDF page (up to 50 pages at a time), and each slide holds a single picture of that page, rendered at 200 dpi. When we converted our four-page test PDF back, we got four slides of the same 13.33 x 7.5 inch size, each containing one picture -- with no text boxes and no speaker notes.",
                    "The slide size follows your PDF's first page as it appears on screen -- its crop box and any rotation -- so the slides match what you see in a PDF reader. If later pages are a different size, each is fitted onto the slide with its proportions kept, so nothing is stretched (improved 10 October 2026).",
                    "That is a deliberate choice. When we built the tool, LibreOffice's own PDF-to-PowerPoint route reported success but produced presentations with no slides at all for every test file we tried. A picture of each page is an exact copy of how the page looks, which is more useful than an \"editable\" file that is silently empty.",
                    "Pictures take more space than text, so expect a bigger file: our 20.5 KB PDF became a 170.5 KB presentation.",
                ],
            },
            {
                "heading": "When PDF to PowerPoint is the right tool -- and when it isn't",
                "paragraphs": [
                    "It works well when you need to present a PDF in PowerPoint or Google Slides, add your own slides before or after it, or draw and write on top of the pages during a talk.",
                    "It is the wrong tool if you need to edit the words. The text on each slide is part of a picture, so it can't be changed. Ask the sender for the original .pptx, or, if you only need the wording, use our PDF to Word tool on a text-based PDF and copy the text from there.",
                ],
            },
            {
                "heading": "Quick checklist",
                "paragraphs": [
                    "Unhide the slides you need, move essential notes onto the slides, use common fonts, and open the PDF to check every slide before sending it. For PDF to PowerPoint, expect picture slides and a larger file. Your upload and the result are deleted from our server as soon as your download is ready.",
                ],
            },
        ],
    },
    {
        "slug": "watermark-pdf-what-it-protects",
        "title": "What a Text Watermark on a PDF Does and Doesn't Protect",
        "seo_title": "What a Text Watermark on a PDF Protects | KuickKonvert",
        "meta_description": "What our Watermark PDF tool adds to each page, how much text fits, what a watermark can't stop, and how to combine it with a password. Our own test results.",
        "dek": "A watermark labels every page -- CONFIDENTIAL, DRAFT, COPY -- so nobody can mistake what the document is. It doesn't lock anything. Here's what our tests showed, and how to use one well.",
        "published": "2026-10-05",
        "related_tools": ["watermark-pdf", "protect-pdf"],
        "sections": [
            {
                "heading": "What our Watermark PDF tool adds",
                "paragraphs": [
                    "The tool lets you [[watermark-pdf|add a watermark to a PDF]] for free: it stamps the text you type diagonally across the centre of every page, at a 45-degree angle, in bold grey letters that are 35% opaque, so the page underneath stays readable. The letters are sized to the page's shorter side: 49 points on an A4 page and 51 points on US Letter, whether the page is portrait or landscape.",
                    "The watermark is placed on top of the page content, not behind it, so it also shows over photos and scanned pages, where a watermark behind the content would be hidden.",
                    "You can type up to 120 characters. Anything longer is cut off at 120.",
                ],
            },
            {
                "heading": "How much text fits",
                "paragraphs": [
                    "The diagonal of an A4 page is about 1,031 points long, and the watermark text is not made smaller to fit. So the length of your text decides whether it is all visible.",
                    "In our tests (October 2026), CONFIDENTIAL used about 365 points -- roughly a third of the diagonal -- and sat neatly in the middle. A 58-character sentence was about 1,644 points wide, so only around 30 of its 58 characters landed on the page; the beginning and end ran off the edges. In practice, keep watermark text to about 25 characters for an A4 page.",
                ],
                "table": {
                    "caption": "Watermark text on an A4 page with our tool (October 2026)",
                    "headers": ["Watermark text", "Length", "Width at 49 pt", "Fits on the page?"],
                    "rows": [
                        ["DRAFT", "5 characters", "About 166 pt", "Yes"],
                        ["CONFIDENTIAL", "12 characters", "About 365 pt", "Yes"],
                        ["COPY - NOT VALID", "16 characters", "About 446 pt", "Yes"],
                        ["A 58-character sentence", "58 characters", "About 1,644 pt", "No - about 30 characters visible"],
                        ["150 characters typed", "Cut to 120", "Far wider than the page", "No"],
                    ],
                    "note": "Widths are for capital letters in Helvetica Bold, the font the tool uses. Lower-case text is narrower.",
                },
            },
            {
                "heading": "Scans, mixed page sizes and every page",
                "paragraphs": [
                    "Because the watermark sits on top of the page, it stays visible on scanned documents, where each page is a single photo. On a scan the watermark is the only real text on the page, so searching a scanned, watermarked file finds the watermark but not the words in the scan.",
                    "Every page is watermarked; there is no option to skip the cover or choose pages. If a file mixes page sizes -- say A4 pages and a landscape table -- the tool sizes the watermark separately for each page size, so it stays centred on every page.",
                ],
            },
            {
                "heading": "What a watermark does -- and what it doesn't",
                "paragraphs": [
                    "It labels the document. Every page, including printouts and screenshots of it, carries the word you chose, which makes a draft hard to pass off as final and makes the purpose of a copy clear.",
                    "It doesn't stop anyone opening, reading, copying or printing the file. In our test, the original page text was still fully selectable after watermarking, and the watermark itself was ordinary text too -- searching the page found it, and copying text from the page picked it up.",
                    "Because it is ordinary content added to each page, it can be edited or removed by someone with PDF editing software. Treat a watermark as a clear label and a deterrent, not as protection.",
                    "Watermarking added very little to the file size: our two-page test PDF grew from 2.5 KB to 9.2 KB.",
                ],
            },
            {
                "heading": "Watermark and password together: do it in the right order",
                "paragraphs": [
                    "If a document needs both a label and protection, watermark it first, then run the watermarked file through [[protect-pdf|Protect PDF]]. Our tools can't open a password-protected PDF, so if you protect it first, the watermark step will stop with a message that the file is password-protected.",
                    "A password stops people without it from opening the file; the watermark stays on every page for the people who do open it.",
                ],
            },
            {
                "heading": "Tips for an effective watermark",
                "paragraphs": [
                    "Keep it short and specific: DRAFT, CONFIDENTIAL, SAMPLE, or COPY - NOT VALID read instantly.",
                    "To show who a copy was for, a short label such as \"Copy for ABC Ltd\" fits comfortably; a full sentence will run off the page.",
                    "Keep an unwatermarked original. The tool doesn't remove watermarks, so you'll need the original to make a clean final version.",
                    "Open the result and check a page before sending it. Your upload and the watermarked file are deleted from our server as soon as your download is ready.",
                ],
            },
        ],
    },
    {
        "slug": "split-and-rotate-pdf-pages",
        "title": "What Splitting and Rotating Pages Do Inside a PDF File (With Test Results)",
        "seo_title": "What Splitting and Rotating Do to a PDF | KuickKonvert",
        "meta_description": "Why split PDF pages can add up to far more than the original, why rotating a PDF loses no quality, and how to rotate or extract just some pages. Our tests.",
        "dek": "Splitting and rotating look like the simplest PDF jobs, but our tests turned up two things worth knowing: split pages can take up many times the space of the original, and rotation never touches your content.",
        "published": "2026-10-05",
        "related_tools": ["split-pdf", "rotate-pdf", "merge-pdf"],
        "sections": [
            {
                "heading": "What Split PDF gives you",
                "paragraphs": [
                    "Split PDF, our free [[split-pdf|PDF splitter]], turns every page of your file into its own one-page PDF. For a multi-page file you download a ZIP containing page-001.pdf, page-002.pdf and so on, in page order; a one-page PDF simply comes back as a PDF. There is no option to choose a page range -- every page is split.",
                    "Each page file is a complete, normal PDF: in our test the text on it was still real, selectable text. Like Merge, Split does not copy the document's title from the original's properties into the new files.",
                ],
            },
            {
                "heading": "Why the split pages can add up to far more than the original",
                "paragraphs": [
                    "This is the result that surprised us. We split a 10-page text report of 50.3 KB, which used an embedded font. The ten page files added up to 421.3 KB -- more than eight times the original -- and each single page was about 42 KB on its own.",
                    "The reason is fonts. A PDF that embeds a font stores it once and shares it between all its pages. When the pages are separated, every page file needs its own copy of the font, so the same font is stored ten times.",
                    "A scanned document behaves differently. We split a five-page scan of 3,214 KB, and the five page files added up to 3,214 KB -- almost exactly the same -- because each page's picture belongs to that page alone and nothing is shared.",
                ],
                "table": {
                    "caption": "Splitting two test files with our Split PDF tool (October 2026)",
                    "headers": ["Test file", "Original", "All page files together", "One page file"],
                    "rows": [
                        ["10-page text report with an embedded font", "50.3 KB", "421.3 KB (8.4x)", "About 42 KB"],
                        ["5-page scanned document (200 dpi)", "3,214 KB", "3,214 KB (1.0x)", "About 640 KB"],
                    ],
                },
            },
            {
                "heading": "What that means in practice",
                "paragraphs": [
                    "Sending one page is still efficient: a single 42 KB page file is smaller than the whole 50.3 KB report.",
                    "But don't split a document to make it smaller overall, and don't send all the separate pages when the whole file would do -- with text documents the pages together can be several times bigger. To shrink a file, use Compress PDF instead.",
                    "To keep only some pages, split the file, then put the pages you want back together with Merge PDF, adding them one at a time in the order you want. The merged file shares its fonts again.",
                ],
            },
            {
                "heading": "What Rotate PDF does -- and why it loses no quality",
                "paragraphs": [
                    "[[rotate-pdf|Rotate PDF]] turns every page by 90, 180 or 270 degrees. In the PDF format, page rotation is a setting stored with each page that tells the reader how to display it; the PDF standard defines it as a clockwise turn. So 90 degrees turns pages a quarter turn clockwise, 270 degrees a quarter turn anticlockwise, and 180 degrees turns them upside down.",
                    "We checked what changes inside the file. After rotating, the content of each page -- the text and drawing instructions -- was byte-for-byte identical to the original; only the rotation setting changed. The text stayed selectable and searchable, and the file size barely moved: 50.3 KB became 49.7 KB, and a 3,214 KB scan stayed at 3,213 KB.",
                    "Rotations add up. Rotating a file by 90 degrees and then rotating the result by 90 degrees again gave a total rotation of 180 degrees, so you can always rotate again if the first choice was wrong.",
                ],
                "table": {
                    "caption": "Rotating test files with our Rotate PDF tool (October 2026)",
                    "headers": ["What we checked", "Result"],
                    "rows": [
                        ["Page content (text and drawing instructions)", "Unchanged, byte for byte"],
                        ["Text", "Still selectable and searchable"],
                        ["File size, 10-page text report", "50.3 KB to 49.7 KB"],
                        ["File size, 5-page scan", "3,214 KB to 3,213 KB"],
                        ["Rotating by 90 degrees twice", "Total rotation 180 degrees"],
                        ["Which pages are rotated", "All pages"],
                    ],
                },
            },
            {
                "heading": "Rotating just one page",
                "paragraphs": [
                    "Rotate PDF always turns every page. If only one page of a scan is sideways, split the file, rotate that single page file, then merge all the pages back together in order with Merge PDF. Our guide to merging PDFs in the right order walks through the merge step.",
                    "Your uploads and results are deleted from our server as soon as your download is ready, so keep your original until you've checked the result.",
                ],
            },
        ],
    },
    {
        "slug": "word-to-pdf-what-carries-over",
        "title": "What Carries Over from Word to a PDF: Links, Headings, Comments and Photos (With Test Results)",
        "seo_title": "What Carries Over from Word to a PDF (Tested) | KuickKonvert",
        "meta_description": "Do links, headings, headers, comments and photos survive Word to PDF conversion? Our test results, including how photos are resized, and what to check first.",
        "dek": "A Word document holds more than the words on the page: links, heading structure, comments, full-size photos. We tested which of these make it into the PDF our tool creates. To convert a document, use our [[word-to-pdf|Word to PDF converter]].",
        "published": "2026-10-05",
        "updated": PACKAGE2_RELEASE_DATE,   # Package 2: font-substitution table added
        "related_tools": ["word-to-pdf"],
        "sections": [
            {
                "heading": "What we tested",
                "paragraphs": [
                    "We created a four-page Word document with two main headings and one sub-heading, a page header, a web link, a comment in the margin, and a 4000 x 3000 pixel photo placed 6 inches wide. We converted it with the same code and fonts our server uses (LibreOffice 24.2, October 2026) and examined the PDF.",
                ],
                "table": {
                    "caption": "A four-page test document converted with our Word to PDF tool (October 2026)",
                    "headers": ["Part of the document", "In the PDF?"],
                    "rows": [
                        ["Text", "Yes - real, selectable and searchable text"],
                        ["Web link", "Yes - still clickable"],
                        ["Page header", "Yes - on the pages"],
                        ["Headings (Heading styles)", "Yes - also turned into PDF bookmarks"],
                        ["Comment in the margin", "No - comments are not included"],
                        ["Photo", "Yes - resized to 300 dpi for its printed size and saved as JPEG"],
                    ],
                },
            },
            {
                "heading": "Links and headings",
                "paragraphs": [
                    "The web link stayed clickable in the PDF, so readers can still follow it.",
                    "Our headings, formatted with Word's built-in Heading styles, also appeared as bookmarks: the clickable outline most PDF readers show in a side panel, with each sub-heading nested under its main heading. This makes long documents much easier to navigate. In a second test, a line we had simply made large and bold did not become a bookmark -- so use Word's Heading 1 and Heading 2 styles if you want them.",
                ],
            },
            {
                "heading": "Page numbers and tables",
                "paragraphs": [
                    "In a second test we put an automatic page number in the footer (Word's PAGE field) and added a table. The six-page PDF showed the correct number on every page -- Page 1 to Page 6 -- and the table came through as a table, with its cell text still selectable.",
                    "Automatic fields like this are calculated during conversion, so they match the PDF's pages. If a page number or date was typed in by hand, it stays exactly as typed.",
                ],
            },
            {
                "heading": "Comments are left out",
                "paragraphs": [
                    "The comment we added in the margin did not appear anywhere in the PDF. For most people that's what they want: a PDF sent to a client shouldn't carry internal review notes.",
                    "If you do need the comments, for example to share a review, keep sending the Word file, or print the document from Word with its markup shown and choose a PDF printer.",
                    "Leaving comments out of the PDF doesn't remove them from your Word file, so don't send the .docx itself if the comments are private.",
                ],
            },
            {
                "heading": "Photos are resized -- usually a good thing",
                "paragraphs": [
                    "Our 4000 x 3000 photo was placed 6 inches wide on the page. In the PDF it was stored at 1800 x 1350 pixels -- exactly 300 pixels for every inch it occupies on the page -- and saved as a JPEG. The JPG photo file itself was 5.4 MB; in the PDF it took up 518 KB.",
                    "300 dpi is a common standard for sharp printing, so the photo still looks sharp on paper and on screen at normal zoom. The benefit is size: the whole four-page document was 5,510 KB as a Word file and only 544 KB as a PDF.",
                    "If you need the original full-resolution photo -- for example for a print shop -- send the image file separately instead of relying on the copy inside the PDF.",
                ],
            },
            {
                "heading": "Fonts: the one thing to check",
                "paragraphs": [
                    "Text is converted as real text, but in the fonts available on our server. Calibri and Arial are replaced by metric-compatible twins, so the layout stays the same. Aptos, the newer Microsoft 365 default, is not, and in our test the same document grew from four pages to five. Our guide on why a PDF's layout sometimes shifts explains this in detail.",
                ],
                # Package 2 (24 Oct 2026): facts from the Dockerfile notes (the
                # font packages installed on the server) and checked with
                # fc-match on the test machine.
                "table": {
                    "caption": "Fonts our server uses in place of common Microsoft fonts",
                    "headers": ["Font in your document", "Font used in the PDF"],
                    "rows": [
                        ["Calibri", "Carlito"],
                        ["Cambria", "Caladea"],
                        ["Arial", "Liberation Sans"],
                        ["Times New Roman", "Liberation Serif"],
                        ["Courier New", "Liberation Mono"],
                    ],
                    "note": "Each replacement has the same character widths as the original, so line breaks and page counts match. The letters look similar but not identical, because the Microsoft fonts themselves can't be redistributed. Fonts not in this table, such as Aptos, may be replaced by a font with different widths, so check the page count.",
                },
            },
            {
                "heading": "Checklist before converting",
                "paragraphs": [
                    "Use Word's Heading styles if you want bookmarks, use a common font such as Calibri or Arial, remember that comments won't appear, and keep the original photos if anyone needs them at full size. Then open the PDF, check the page count and click a link or two. Our [[word-to-pdf|Word to PDF converter]] accepts both .doc and .docx, and your upload and the PDF are deleted from our server as soon as your download is ready.",
                ],
            },
        ],
    },
    {
        "slug": "what-is-a-heic-file",
        # Release 7, R7-78: official sources (each URL checked 13 Nov 2026).
        "sources": [('Apple Support: Using HEIF or HEVC media on Apple devices', 'https://support.apple.com/en-us/116944'), ('Microsoft Store: HEIF Image Extension', 'https://apps.microsoft.com/detail/9pmmsr1cgpwg')],
        "title": "What Is a HEIC File, and How Do You Open iPhone Photos Everywhere?",
        "seo_title": "What Is a HEIC File? Open iPhone Photos | KuickKonvert",
        "meta_description": "HEIC is the format iPhones use for photos. Why it won't open on some PCs, forms and Android phones, how to switch it off, and how to convert HEIC to JPG.",
        "dek": "If your iPhone photos arrive as .HEIC and won't open on a Windows PC, an Android phone or an upload form, here is what the format is, why Apple uses it, and the simplest ways to view or convert it. To convert photos you already have, use our [[heic-to-jpg|HEIC to JPG converter]].",
        "published": "2026-10-10",
        "updated": FIX_RELEASE_DATE,  # test results tables + "How we tested" added
        "related_tools": ["heic-to-jpg", "jpg-to-pdf"],
        "sections": [
            {
                "heading": "What a HEIC file actually is",
                "paragraphs": [
                    "HEIC is the file name Apple uses for HEIF, a modern image container, with the picture inside compressed using HEVC (also called H.265). Apple made it the iPhone's default photo format in 2017 with iOS 11. Its main advantage is size: it stores a photo in roughly half the space of a JPEG at a similar quality, which is why your phone's storage lasts longer.",
                    "A HEIC file can also hold more than a plain photo -- a depth map for portrait shots, the extra frames of a Live Photo, or several images in one file. That flexibility is useful on the phone but is part of why other devices struggle with it.",
                ],
            },
            {
                "heading": "Why it won't open everywhere",
                "paragraphs": [
                    "HEIC is efficient but not as widely supported as JPEG, which almost everything has understood for decades. Older versions of Windows and Android, many website upload forms, and some older photo apps simply don't read .heic files.",
                    "On Windows 10 and 11 you can add support by installing Microsoft's HEIF Image Extension from the Microsoft Store; its Store page says the HEVC Video Extensions package must also be installed to view .heic files. But an upload form that only accepts JPG or PNG will still reject a .heic file no matter what your own PC can open -- which is when you need to convert.",
                ],
            },
            {
                "heading": "Switch it off on the iPhone, or convert on transfer",
                "paragraphs": [
                    "If you would rather your iPhone take JPEGs from now on, open Settings, tap Camera, then Formats, and choose Most Compatible (the High Efficiency option is the one that saves HEIC). New photos will be JPEG; photos you already took stay HEIC.",
                    "Apple can also convert automatically when you move photos off the phone: under Settings > Photos, the Transfer to Mac or PC setting offers Automatic, which hands over JPEGs to a Windows PC instead of HEIC. These are Apple's own settings and may move slightly between iOS versions.",
                ],
            },
            {
                "heading": "Converting the HEIC photos you already have",
                "paragraphs": [
                    "For photos already saved as HEIC, our [[heic-to-jpg|HEIC to JPG converter]] turns them into ordinary JPGs, up to 20 at a time and up to 65 megapixels each. Several photos come back together in one ZIP file, each JPG keeping its own file name.",
                    "We tested what the converter keeps and removes, using the same code the tool runs (October 2026; see How we tested below). The JPG keeps the date taken, the camera make and model and the colour profile, and drops the GPS location and other hidden details. A photo stored sideways came out upright, and for a HEIC holding several images the tool converted the main (primary) image the file marks, not simply the first one stored.",
                ],
                "table": {
                    "caption": "What our HEIC to JPG converter did with our test files (October 2026)",
                    "headers": ["What we tested", "Result"],
                    "rows": [
                        ["GPS location", "Removed"],
                        ["Owner name, serial number, software version", "Removed"],
                        ["Date and time taken, camera make and model", "Kept"],
                        ["Colour profile", "Kept"],
                        ["Photo stored sideways (4032 x 3024 plus a rotation instruction)", "Upright JPG, 3024 x 4032"],
                        ["One HEIC holding three images, the second marked as main", "The second (main) image was converted"],
                        ["Three HEIC files at once", "One ZIP with three JPGs, original names kept"],
                    ],
                },
            },
            {
                "heading": "Will the JPG be bigger than the HEIC?",
                "paragraphs": [
                    "Usually, yes. Because HEVC compression is newer and more efficient than JPEG, the same picture saved as JPEG takes more space. Every single-image HEIC we tested produced a larger JPG: 12% and 26% larger for two 12-megapixel photo-like images, and almost three times larger for a flat-colour, screenshot-style image, which HEIC compresses especially well.",
                    "The one JPG that came out smaller was from the HEIC holding three images -- simply because the JPG contains only one of them. The converter saves at quality 90 and full size, so the picture is kept; the extra size reflects the older format. If file size matters for an upload, resize the photo before converting.",
                ],
                "table": {
                    "caption": "The same test images as HEIC and as JPG (our tests, October 2026)",
                    "headers": ["Test image", "Pixels", "HEIC", "JPG from our tool", "Difference"],
                    "rows": [
                        ["Photo-like image 1", "4032 x 3024", "1,715 KB", "1,925 KB", "12% larger"],
                        ["Photo-like image 2", "3024 x 4032", "1,587 KB", "1,994 KB", "26% larger"],
                        ["Screenshot-style graphic", "1290 x 2796", "33 KB", "98 KB", "About 2.9 times larger"],
                        ["HEIC holding three images", "1200 x 900 each", "64 KB (all three)", "62 KB (main image only)", "Smaller - only one image kept"],
                    ],
                    "note": "Computer-generated test images, not photos taken on an iPhone, so your own photos will give different sizes.",
                },
            },
            {
                "heading": "Putting converted photos into one PDF",
                "paragraphs": [
                    "If you need those photos as a single document -- for a form or an application -- convert them to JPG and then use our [[jpg-to-pdf|JPG to PDF converter]].",
                    "Expect large pages. The converted JPG carries no print-size (dpi) setting, so JPG to PDF sizes each page as if the photo were printed at 96 dpi: in our test, a 3024 x 4032 photo converted this way became a 31.5 x 42 inch page (80 x 107 cm). PDF readers zoom to fit, so it looks normal on screen; if page size or file size matters, see our guide on turning photos into one PDF.",
                ],
            },
            {
                "heading": "How we tested",
                "paragraphs": [
                    "We made the test files ourselves rather than on an iPhone: computer-generated pictures with fine, photo-like detail, encoded as HEIC with the open-source libheif library (through pillow-heif 1.8, using its x265 encoder at default quality). We wrote test location, date, camera, owner-name and serial-number details into them, stored one sideways with a HEIF rotation instruction, and packed three different images into one file with the second marked as main.",
                    "Each file was converted by the same code our HEIC to JPG tool runs, in a test copy of the site with Python 3.11, Pillow 12.3.0 and pi-heif 1.4.0 -- the versions the live site uses -- and the results were read back with Pillow. The tests ran on our own test machine, not on the live server.",
                ],
            },
        ],
    },
    {
        "slug": "location-data-in-photos",
        "title": "Can a Photo Show Where It Was Taken? Location Data, and How to Remove It",
        "seo_title": "Location Data in Photos: How to Remove It | KuickKonvert",
        "meta_description": "Phone photos can carry the GPS spot where they were taken. How to check, stop your phone adding it, and which of our tools strip it — tested October 2026.",
        "dek": "Many phone photos quietly record the exact place they were taken. Here is what that hidden data is, how to see it, and how to remove it before you share a picture or upload it to a form.",
        "published": "2026-10-10",
        "updated": FIX_RELEASE_DATE,  # test results table + PDF tools + "How we tested" added
        "related_tools": ["heic-to-jpg", "webp-to-jpg", "png-to-jpg", "jpg-to-pdf"],
        "sections": [
            {
                "heading": "The hidden data inside a photo",
                "paragraphs": [
                    "Most cameras and phones write extra information into every photo, called EXIF metadata. It can include the date and time, the camera or phone make and model, the settings used, and -- if location is switched on -- the GPS coordinates of exactly where the photo was taken, often accurate to a few metres.",
                    "Not every image has it. A screenshot, or a picture you saved from a website, usually carries no location. But a photo straight from a phone camera very often does, and it travels with the file when you send or upload it.",
                ],
            },
            {
                "heading": "How to see what a photo is carrying",
                "paragraphs": [
                    "On Windows, right-click the photo, choose Properties, and open the Details tab -- any GPS latitude and longitude appear there. On a Mac, open it in Preview and choose Tools > Show Inspector, then the information tab. On the phone itself, the photo's info or details view will show a map if the photo is geotagged.",
                ],
            },
            {
                "heading": "Stop your phone adding location in the first place",
                "paragraphs": [
                    "On an iPhone, open Settings > Privacy & Security > Location Services, tap Camera, and set it to Never. On most Android phones, open the Camera app's settings and turn off the location or geotagging option. New photos then carry no GPS; photos you already took are unchanged.",
                ],
            },
            {
                "heading": "How our image tools remove it (tested October 2026)",
                "paragraphs": [
                    "Our image converters -- [[heic-to-jpg|HEIC to JPG]], [[webp-to-jpg|WEBP to JPG]], [[png-to-jpg|PNG to JPG]] and [[jpg-to-png|JPG to PNG]] -- keep only the date taken and the camera make and model, and drop GPS location and other hidden data. We tested each one with a file carrying test GPS coordinates, an owner name, a serial number and a software version: every time, only the date and the camera make and model were left.",
                    "Our [[jpg-to-pdf|JPG to PDF converter]] goes further as it builds the PDF: it removes the hidden EXIF data from each JPEG entirely -- the GPS location, and the date and camera details too -- without re-compressing the picture. In our tests the location was also gone when a JPG carried it a second way, in an XMP block, and when a PNG with location data was turned into a PDF with either JPG to PDF or PNG to PDF. (One aside: taking a screenshot of a photo also drops the original location data, which is why screenshots are safe to share.)",
                ],
                "table": {
                    "caption": "Location data after each of our tools (our tests, October 2026)",
                    "headers": ["Tool", "Test file", "Location in the result?", "What else was left"],
                    "rows": [
                        ["HEIC to JPG", "HEIC photo with GPS", "No - removed", "Date taken, camera make and model"],
                        ["WEBP to JPG", "WEBP image with GPS", "No - removed", "Date taken, camera make and model"],
                        ["PNG to JPG", "PNG image with GPS", "No - removed", "Date taken, camera make and model"],
                        ["JPG to PNG", "JPG with GPS (in EXIF and XMP)", "No - removed", "Date taken, camera make and model"],
                        ["JPG to PDF", "The same JPG", "No - removed", "No photo details at all"],
                        ["JPG to PDF and PNG to PDF", "PNG image with GPS", "No - removed", "No photo details at all"],
                        ["Merge PDF and Rotate PDF", "PDF made elsewhere, photo inside still carrying GPS", "Yes - kept", "Everything, unchanged"],
                        ["Compress PDF, Screen or eBook", "The same kind of PDF, photo at 300 dpi", "No - photo was re-saved", "-"],
                        ["Compress PDF, Printer", "The same PDF", "Yes - kept", "Original returned, as it couldn't be made smaller"],
                    ],
                },
            },
            {
                "heading": "PDFs made somewhere else",
                "paragraphs": [
                    "Our PDF tools work differently from the image tools. Merge PDF and Rotate PDF copy the pictures on each page across without re-saving them, so if a PDF was made by another app that left a photo's location inside it, the location is still there afterwards -- our test PDF kept it through both.",
                    "Compress PDF isn't a reliable way to remove it either. It removed the location from our 300-dpi test photo on Screen and eBook, because those levels re-save the photo at a lower resolution. But when a file can't be made smaller -- on Printer, and on every level when we placed the same photo at 72 dpi -- the tool hands back your original file, location included. If you're not sure where a PDF's photos came from, rebuild it from the original pictures with JPG to PDF.",
                ],
            },
            {
                "heading": "A simple routine before sharing",
                "paragraphs": [
                    "If you are about to post a photo publicly or send it to someone you don't know well, run it through one of our image converters first (or, if you are making a document, let JPG to PDF strip it), then check the file's Properties to confirm no GPS remains. Don't rely on Merge, Rotate or Compress to remove it. Your upload and the converted file are deleted from our server as soon as your download is ready.",
                ],
            },
            {
                "heading": "How we tested",
                "paragraphs": [
                    "We created the test images ourselves -- computer-generated pictures, not real photos -- and wrote the same test details into each: GPS coordinates for an arbitrary point, a date, a camera make and model, an owner name, a serial number and a software version (one JPG also carried the location in an XMP block). For the PDF tools we used a PDF built with a general-purpose PDF library that keeps photo metadata, standing in for a PDF from another app.",
                    "Every file went through the same code our tools run, in a test copy of the site (Python 3.11, Pillow 12.3.0 and pi-heif 1.4.0, as on the live site; Ghostscript 10.02 for Compress PDF). We read the results back with Pillow and pikepdf, checking every picture inside each PDF for EXIF and XMP data. The tests ran on our own test machine, not on the live server.",
                ],
            },
        ],
    },
    {
        "slug": "what-is-a-webp-image",
        # Release 7, R7-78: official sources (each URL checked 13 Nov 2026).
        "sources": [('Google for Developers: WebP, an image format for the Web', 'https://developers.google.com/speed/webp')],
        "title": "What Is a WEBP Image, and Why Won't It Open Everywhere?",
        "seo_title": "What Is a WEBP Image? Why It Won't Open | KuickKonvert",
        "meta_description": "WEBP is Google's web image format. Why pictures saved from websites are often .webp, what it does well, and how to convert WEBP to JPG — tested October 2026.",
        "dek": "Saved a picture from a website and got a .webp file that won't open in your photo app or upload to a form? Here is what WEBP is, why sites use it, and how to convert it. To get a JPG copy, use our [[webp-to-jpg|WEBP to JPG converter]].",
        "published": "2026-10-10",
        "updated": FIX_RELEASE_DATE,  # test results tables + "How we tested" added
        "related_tools": ["webp-to-jpg", "jpg-to-pdf"],
        "sections": [
            {
                "heading": "What WEBP is",
                "paragraphs": [
                    "WEBP (pronounced 'weppy', file extension .webp) is an image format developed by Google specifically for the web, first released in 2010. It can compress pictures either with some quality loss (like JPEG) or losslessly (like PNG), and it also supports transparency and animation. At a similar quality it is usually smaller than JPEG or PNG, which saves bandwidth -- the reason so many websites now serve their images as WEBP.",
                    "Both kinds use the same .webp extension, so you can't tell from the file name whether a WEBP is lossy or lossless. As our tests below show, that matters when you convert it.",
                ],
            },
            {
                "heading": "Why you keep running into it, and why it won't open",
                "paragraphs": [
                    "When a modern browser visits a site, it is often served WEBP to make the page load faster. If you then right-click and Save image as, you get a .webp file. That is fine for the web, but older photo viewers, some office and design apps, and many upload forms don't accept WEBP, so the file you saved won't open or won't upload.",
                    "Converting it to JPG solves this: JPG is understood by essentially every program and every upload form.",
                ],
            },
            {
                "heading": "Getting a JPG copy of a WEBP picture",
                "paragraphs": [
                    "Our [[webp-to-jpg|WEBP to JPG converter]] turns WEBP files into standard JPGs, up to 20 at a time, at full size and quality 90. From our tests in October 2026: a still WEBP becomes an ordinary JPG with the same width and height; if the WEBP had transparent areas (JPG has no transparency) they are placed on a white background; and an animated WEBP is turned into a single still picture of its first frame.",
                    "Hidden photo details are handled the same way as in our other image converters. A test WEBP carrying GPS location came out without it, while the date taken and the camera make and model were kept.",
                ],
                "table": {
                    "caption": "What happened to our test WEBP files (October 2026)",
                    "headers": ["Test file", "Result"],
                    "rows": [
                        ["Logo on a transparent background (600 x 600)", "Background became white; the logo's own colours were unchanged"],
                        ["Animated WEBP, three frames (red, green, blue)", "One still JPG of the first (red) frame"],
                        ["Photo-like image with GPS, date and camera details", "GPS removed; date taken and camera make and model kept"],
                        ["Every test file", "JPG had the same width and height as the WEBP"],
                    ],
                },
            },
            {
                "heading": "Will the JPG be larger?",
                "paragraphs": [
                    "It depends on how hard the WEBP was compressed. Lossy WEBPs saved at an ordinary quality setting (we used 80, the default in Pillow, the imaging library our converter uses) got bigger as quality-90 JPGs in our tests: a photo-like image doubled in size, and a flat-colour banner with text grew about 2.4 times. Flat graphics stored losslessly grew even more -- about 7 to 8 times for our banner and logo -- because lossless WEBP compresses large plain areas extremely well.",
                    "A WEBP saved at very high quality, or losslessly, can go the other way: the same photo-like picture saved as a quality-95 WEBP got 42% smaller as a JPG, and from a lossless WEBP the JPG was about a ninth of the size. Either way the JPG is saved at full size and quality 90, where differences are hard to see; the change in file size mostly reflects how tightly the WEBP had been compressed.",
                ],
                "table": {
                    "caption": "File sizes: WEBP and the JPG our tool made from it (October 2026)",
                    "headers": ["Test image", "WEBP", "JPG", "Change"],
                    "rows": [
                        ["Photo-like, 1600 x 1200, lossy quality 80", "133 KB", "264 KB", "About 2 times larger"],
                        ["Same picture, lossy quality 95", "632 KB", "370 KB", "42% smaller"],
                        ["Same picture, lossless", "3,221 KB", "366 KB", "About a ninth of the size"],
                        ["Banner with text, 1200 x 630, lossy quality 80", "34 KB", "83 KB", "About 2.4 times larger"],
                        ["Same banner, lossless", "11 KB", "82 KB", "About 7.7 times larger"],
                        ["Logo with transparency, 600 x 600, lossless", "3 KB", "22 KB", "About 7 times larger"],
                    ],
                    "note": "Computer-generated test images; your own images will give different numbers.",
                },
            },
            {
                "heading": "After converting",
                "paragraphs": [
                    "If a site or form has a file-size limit and the JPG is too big, resize the image first. If you then need the images as one document, use our [[jpg-to-pdf|JPG to PDF converter]]. Your upload and the JPG are deleted from our server as soon as your download is ready.",
                ],
            },
            {
                "heading": "How we tested",
                "paragraphs": [
                    "We generated the test images ourselves with Pillow, the imaging library our converter uses: a photo-like picture with fine detail saved as lossy WEBP at quality 80 and 95 and as lossless WEBP, a flat-colour banner with text, a logo on a transparent background, a three-frame animation, and a photo-like image carrying test GPS, date and camera details.",
                    "Each went through the same code as our WEBP to JPG tool, in a test copy of the site using Python 3.11 and Pillow 12.3.0 -- the version the live site uses -- and we measured the results with Pillow. The tests ran on our own test machine, not on the live server.",
                ],
            },
        ],
    },
    {
        "slug": "submitting-coursework-as-a-pdf",
        "title": "Submitting Coursework as a PDF: A Checklist That Portals Accept",
        "seo_title": "Submit Coursework as One PDF: A Checklist | KuickKonvert",
        "meta_description": "Turn an assignment into one PDF a submission portal will accept: convert Word, add scanned or photographed pages, combine them in order and keep it small.",
        "dek": "Most university and college portals want a single PDF, under a size limit, that opens cleanly. Here is a tested, step-by-step way to get there from a Word file, scanned pages, or phone photos.",
        "published": "2026-10-10",
        "updated": FIX_RELEASE_DATE,  # test results tables + "How we tested" added
        "related_tools": ["word-to-pdf", "merge-pdf", "compress-pdf", "jpg-to-pdf", "heic-to-jpg"],
        "sections": [
            {
                "heading": "Start from the right source file",
                "paragraphs": [
                    "If your work is in Word, convert it with our [[word-to-pdf|Word to PDF converter]] (it takes both .doc and .docx). The PDF keeps your text as real, selectable text, and Heading styles become bookmarks. In our test, a five-page essay with four headings in Word's Heading 1 style became a 26 KB PDF with selectable text on every page and four bookmarks.",
                    "One thing to watch is fonts: common fonts such as Calibri and Arial keep your layout and page breaks, while some newer fonts -- including Aptos, Microsoft 365's newer default -- can make text rewrap. If the layout matters, see our guide on why a PDF's layout sometimes shifts, and check the PDF before you submit.",
                ],
            },
            {
                "heading": "Handwritten or photographed pages",
                "paragraphs": [
                    "For handwritten answers or a page you can only photograph, take a clear, well-lit picture of each page. If the photos are iPhone HEIC files or web WEBP files, convert them to JPG first (our [[heic-to-jpg|HEIC to JPG]] tool handles iPhone photos), then combine them with our [[jpg-to-pdf|JPG to PDF converter]], adding them one at a time so the page order is right.",
                    "Expect very large pages. JPG to PDF sizes each page from the photo's resolution (dpi) label, or assumes 96 dpi when it finds none. In our tests a 3024 x 4032 phone-style photo of a page became a 42 x 56 inch page (about 107 x 142 cm) when labelled 72 dpi, or 31.5 x 42 inches when its label was stored only in the hidden EXIF data our tool removes; a page scanned at 300 dpi came out at true A4 size. PDF readers zoom to fit, so this looks normal on screen, but it can matter if someone prints the file or a portal checks page size.",
                    "Photo PDFs can also come out very large in file size, because each page is a full-resolution picture. If yours is too big, resize the photos before converting -- our guide on turning photos into one PDF shows how and why Compress PDF alone often can't shrink them.",
                ],
            },
            {
                "heading": "Combine everything into one PDF",
                "paragraphs": [
                    "If your submission is in pieces -- a cover sheet, the main document, an appendix of photos -- put them in the required order and join them with our [[merge-pdf|Merge PDF tool]]. Adding files one at a time is the simplest way to control the order.",
                    "We checked the order both ways, and the merged file always followed the order the files were added. Each page keeps its own size, so our merged file mixed US Letter text pages, 42 x 56 inch photo pages and an A4 scan, and the essay's four bookmarks were not carried over -- a merge doesn't keep them.",
                ],
                "table": {
                    "caption": "Our test submission, piece by piece (October 2026)",
                    "headers": ["Part", "Made with", "Pages", "Page size in the PDF"],
                    "rows": [
                        ["Essay in Word, with Heading styles", "Word to PDF", "5", "8.5 x 11 in (US Letter, as set in the document)"],
                        ["Two phone photos of handwritten pages", "JPG to PDF", "2", "42 x 56 in each (photos labelled 72 dpi)"],
                        ["One page scanned at 300 dpi", "JPG to PDF (same file)", "1", "21.0 x 29.7 cm (A4)"],
                        ["Everything joined", "Merge PDF", "8", "Each page kept its own size; bookmarks not kept"],
                    ],
                },
            },
            {
                "heading": "Get under the size limit",
                "paragraphs": [
                    "If the portal has a maximum file size, try our [[compress-pdf|Compress PDF tool]]. How much it helps depends on what is in the file, as our four test PDFs show.",
                    "Scanned pages shrank dramatically: three pages scanned at 300 dpi went from 7,657 KB to 685 KB on eBook and 276 KB on Screen. Pages scanned at 200 dpi only shrank on Screen, because eBook reduces only images above 225 dpi and Printer doesn't reduce resolution at all. Our text-only essay was already small at 26 KB and lost only a few kilobytes.",
                    "Photographed pages are the trap. In our combined PDF, compression shrank only the scanned page; the two phone photos were not reduced at all, because on a 42-inch-wide page a 3024-pixel photo is only 72 dpi -- below every level's threshold. For a photo-heavy PDF, resizing the photos before you build the PDF is the more reliable fix. We can't promise a final size, and if Compress PDF can't make a file smaller, you get your original back unchanged.",
                    "Check readability after compressing. On Screen, our 300-dpi scan was reduced to 72 dpi: still readable on screen, but visibly blockier when zoomed in. eBook reduced it to 150 dpi and looked clean, so try eBook first.",
                ],
                "table": {
                    "caption": "Compress PDF on four test PDFs (our tests, October 2026)",
                    "headers": ["Test PDF", "Original", "Screen", "eBook", "Printer"],
                    "rows": [
                        ["Five-page essay from Word (text only)", "25.7 KB", "22.2 KB (86%)", "22.2 KB (86%)", "25.2 KB (98%)"],
                        ["Three pages scanned at 300 dpi", "7,657 KB", "276 KB (3.6%)", "685 KB (8.9%)", "Not reduced - original returned"],
                        ["Three pages scanned at 200 dpi", "3,523 KB", "247 KB (7.0%)", "Not reduced - original returned", "Not reduced - original returned"],
                        ["Two phone photos of pages plus one 300-dpi scan", "9,694 KB", "7,222 KB (74%)", "7,363 KB (76%)", "Not reduced - original returned"],
                    ],
                    "note": "In the last PDF, only the scanned page shrank; the two photo pages were not reduced at any level.",
                },
            },
            {
                "heading": "Final checks before you submit",
                "paragraphs": [
                    "Make sure it is one PDF, that it opens cleanly, that the pages are upright, in the right order and readable, and that it is under the portal's size limit. Open the finished file and scroll through it once. Everything you upload and every file we return is deleted from our server as soon as your download is ready.",
                ],
            },
            {
                "heading": "How we tested",
                "paragraphs": [
                    "We built a test submission from computer-generated material: a five-page essay written with the python-docx library (Calibri as the font, with Heading styles), two 3024 x 4032 'phone photos' of text pages labelled 72 dpi, and A4 text pages made to look scanned at 300 and 200 dpi. LibreOffice used the metric-compatible Carlito font in place of Calibri; Carlito is also installed on our live server.",
                    "Each step used the same code as our Word to PDF, JPG to PDF, Merge PDF and Compress PDF tools, run in a test copy of the site on our own test machine (LibreOffice 24.2 and Ghostscript 10.02 there; the live server's versions may differ slightly). We measured page sizes, page order, bookmarks and file sizes with pikepdf and pypdf.",
                ],
            },
        ],
    },
    {
        # Package 2 (24 Oct 2026). Every statement here is checked against the
        # code at the time of writing -- change it if the code changes:
        #   converters/utils.py job_workspace() (own folder, deleted in a
        #   finally block), subprocess_env() (helper temp files inside it) and
        #   sweep_stale_temp() (30-minute age); app.py convert() (output read
        #   into memory, folder deleted, then sent), _maybe_sweep_temp() and
        #   the start-up sweep (TEMP_SWEEP_SECONDS, default 1800);
        #   config.MAX_CONTENT_LENGTH (50 MB default) and
        #   app.MAX_IMAGES_PER_CONVERSION (20, image-to-image tools only);
        #   converters/isolate.py (separate process, 700 MB / 170 s defaults);
        #   logging as in the Privacy notice. Region: Render Settings show
        #   "Singapore (Southeast Asia)" (checked 10 Oct 2026).
        "slug": "what-happens-to-your-file",
        "title": "What Happens to Your File When You Use KuickKonvert",
        "seo_title": "What Happens to Your File After Upload | KuickKonvert",
        "meta_description": "Where your upload goes, how long it exists and when it is deleted: each conversion runs in its own temporary folder on our server and is then deleted.",
        "dek": "KuickKonvert converts files on our server, not in your browser. Here is, step by step, where your file goes, how long it exists there, and how it is deleted.",
        "published": PACKAGE2_RELEASE_DATE,
        "related_tools": ["jpg-to-pdf", "pdf-to-word", "word-to-pdf", "compress-pdf"],
        "sections": [
            {
                "heading": "Where your file is converted",
                "paragraphs": [
                    "When you press Convert, your file is uploaded to our server and converted there. The server is run by our hosting provider, Render, in its Singapore (Southeast Asia) region, and traffic reaches it through Cloudflare's network. If you are outside Singapore, this means your file is briefly processed in another country.",
                ],
            },
            {
                "heading": "Each conversion gets its own temporary folder",
                "paragraphs": [
                    "Every conversion starts with a new, empty folder with a random name. Your uploaded file, any working files the converter creates and the converted result are all written into that folder. The helper programs we use, such as LibreOffice and Ghostscript, are pointed at the same folder for their own temporary files.",
                    "Each conversion also runs in a separate process with its own memory allowance and a time limit, so one very large file can't hold up the whole server.",
                ],
            },
            {
                "heading": "When your file is deleted",
                "paragraphs": [
                    "When the conversion finishes, the converted file is read into memory, the whole folder is deleted, and only then is the result sent to your browser. If the conversion fails, the folder is deleted in the same way. The code that deletes it runs whatever the outcome, success or error.",
                    "If a server process stops unexpectedly in the middle of a conversion, its folder can be left behind. A clean-up removes any such folder once it is more than 30 minutes old. It runs whenever a server process starts, and at most every 30 minutes when a new conversion begins.",
                ],
            },
            {
                "heading": "Size limits",
                "paragraphs": [
                    "Each upload can be up to 50 MB, counting all the files in it together. The image converters ([[heic-to-jpg|HEIC to JPG]], [[webp-to-jpg|WEBP to JPG]], [[png-to-jpg|PNG to JPG]] and [[jpg-to-png|JPG to PNG]]) take up to 20 images at a time.",
                ],
            },
            {
                "heading": "What our logs record",
                "paragraphs": [
                    "Our own application logs record which tool was used and technical error details when a conversion fails. They never contain file contents, and they are designed to leave out file names, although a report of an unexpected error may occasionally include one. Our hosting providers also see basic request details, such as the page or tool requested, as described in our [[page:privacy|Privacy notice]].",
                ],
            },
            {
                "heading": "What this means for you",
                "paragraphs": [
                    "Keep your original file: we don't keep a copy, so once the folder is deleted there is nothing we can send you again. Download the result when it is ready, and open it to check it before you rely on it. If a file contains information you are not allowed to share, don't upload it. Our [[page:privacy|Privacy notice]] has the full details.",
                ],
            },
        ],
    },
    {
        "slug": "xls-vs-xlsx",
        # Release 7, R7-78: official sources (each URL checked 13 Nov 2026).
        "sources": [('Microsoft Support: Use Excel with earlier versions of Excel', 'https://support.microsoft.com/en-us/office/use-excel-with-earlier-versions-of-excel-2fd9ffcb-6fce-485b-85af-fecfd651a5ac'), ('Microsoft Support: Open XML Formats and file name extensions', 'https://support.microsoft.com/en-us/office/open-xml-formats-and-file-name-extensions-5200d93c-3449-4380-8e11-31ef14555b18')],
        # 24 Oct 2026 (AI-visibility plan, Google step 5): mirrors the DOC vs
        # DOCX guide, the site's largest source of search impressions. Facts:
        # Microsoft support "Use Excel with earlier versions of Excel" (row and
        # column limits, data beyond them "will not be saved") and "Open XML
        # Formats and file name extensions" (.xlsm, 75 percent). Test figures:
        # measure_office.py, 24 Oct 2026, LibreOffice 24.2, converters/office.py.
        "title": "XLS vs XLSX: What's the Difference? (With Test Results)",
        "seo_title": "XLS vs XLSX: What's the Difference? (Tested) | KuickKonvert",
        "meta_description": "XLS vs XLSX explained: row limits, file size and macros, plus our own test. Use XLSX unless an old Excel needs XLS -- and why rows can go missing.",
        "dek": "XLSX is Excel's modern format (Excel 2007 onwards): a ZIP archive of XML files that holds up to 1,048,576 rows. XLS is the older binary format of Excel 97 to 2003, limited to 65,536 rows and 256 columns. Use XLSX for almost everything -- saving a big sheet as XLS drops whatever doesn't fit, as our test shows. To make a PDF of either format, use our [[excel-to-pdf|Excel to PDF converter]].",
        "published": NEW_GUIDES_RELEASE_DATE,
        "related_tools": ["excel-to-pdf", "pdf-to-excel"],
        "sections": [
            {
                "heading": "XLS vs XLSX at a glance",
                "paragraphs": [
                    "The short version: XLSX is the modern Excel format and the right choice for almost everything. XLS is the older format, still worth knowing about if someone uses a very old version of Excel.",
                ],
                "table": {
                    "caption": "XLS and XLSX compared",
                    "headers": ["", "XLS", "XLSX"],
                    "rows": [
                        ["Excel's default format", "Excel 97 to Excel 2003", "Excel 2007 onwards"],
                        ["What the file is inside", "One binary file", "A ZIP archive of XML files (Office Open XML)"],
                        ["Rows and columns per sheet", "65,536 rows x 256 columns", "1,048,576 rows x 16,384 columns"],
                        ["Can contain macros?", "Yes", "No - macro workbooks use .xlsm"],
                        ["File size in our test", "About 1.6 to 3.3 times larger", "Smaller"],
                        ["Converts to PDF with our tool?", "Yes", "Yes"],
                    ],
                    "note": "Details and sources for each row are in the sections below.",
                },
            },
            {
                "heading": "Two different formats",
                "paragraphs": [
                    "XLS was Excel's format from Excel 97 through Excel 2003: a single binary file. XLSX replaced it as the default from Excel 2007. Like DOCX for Word, an XLSX file is really a ZIP archive of XML files, part of the Office Open XML standard.",
                    "You can see the difference in the first bytes of each file. In our test, the XLSX file started with the letters PK, the signature of a ZIP archive, and the XLS file started with D0 CF 11 E0, the marker of Microsoft's older compound binary format.",
                ],
            },
            {
                "heading": "The row limit: what happens to data that doesn't fit",
                "paragraphs": [
                    "Microsoft's support page on using Excel with earlier versions puts it plainly: an Excel 97-2003 worksheet is only 65,536 rows tall by 256 columns wide, data beyond that \"will not be saved\", and formulas that refer to it return a #REF! error. Excel's Compatibility Checker warns you when you save as XLS; other programs may not.",
                    "We tested it. A sheet with 70,000 numbered rows, saved as XLS and opened again, ended at row 65,536 -- the last 4,464 rows were gone. A sheet 300 columns wide came back with 256 columns. Nothing in the reopened file shows that anything is missing, so the loss is easy to overlook if someone else saved it.",
                ],
                "table": {
                    "caption": "Saving beyond the XLS limits (our test, October 2026)",
                    "headers": ["Test sheet", "Saved as XLS and reopened"],
                    "rows": [
                        ["70,000 rows x 4 columns", "65,536 rows kept; 4,464 rows lost"],
                        ["10 rows x 300 columns", "256 columns kept; 44 columns lost"],
                    ],
                    "note": "The XLS copies were saved with LibreOffice; Microsoft documents the same limits for Excel itself.",
                },
            },
            {
                "heading": "Is XLSX smaller? In our tests, yes",
                "paragraphs": [
                    "Microsoft says Open XML files are compressed automatically and \"can be up to 75 percent smaller in some cases\". Unlike our DOC vs DOCX test, where the two Word formats came out almost the same, the spreadsheet difference was large: our XLS copies were 1.6 to 3.3 times the size of the XLSX originals.",
                ],
                "table": {
                    "caption": "The same workbook saved both ways (our test, October 2026)",
                    "headers": ["Test workbook", "XLSX", "XLS"],
                    "rows": [
                        ["One sheet, 50 rows x 6 columns", "6.6 KB", "10.5 KB"],
                        ["Three sheets, 5,000 rows x 8 columns each", "632 KB", "1,702 KB"],
                        ["One sheet, 70,000 rows x 4 columns", "1,619 KB", "5,287 KB (and only 65,536 rows kept)"],
                    ],
                    "note": "Numbers, text and dates generated for the test. The XLS copies were saved with LibreOffice, not Microsoft Excel; sizes from Excel itself can differ.",
                },
            },
            {
                "heading": "When the difference actually matters",
                "paragraphs": [
                    "Old software. Excel 2003 and earlier can't open an .xlsx without Microsoft's compatibility pack -- the usual reason anyone still asks for .xls.",
                    "Large sheets. Anything over 65,536 rows or 256 columns has to stay XLSX.",
                    "Macros. A normal .xlsx can't contain macros; Excel uses .xlsm for macro-enabled workbooks. An .xls from an unknown sender may contain macros.",
                    "Converting to PDF. Our [[excel-to-pdf|Excel to PDF converter]] accepts both .xls and .xlsx. An .xls is first converted to .xlsx on our server, then every column is fitted across the page width. Your upload and the PDF are deleted from our server as soon as your download is ready.",
                ],
            },
            {
                "heading": "Which one should you use?",
                "paragraphs": [
                    "Use XLSX unless someone specifically needs XLS for an old program. It is Excel's default, it holds far more data, and in our tests it was the smaller file. If you must send an XLS, check first that the sheet fits within 65,536 rows and 256 columns.",
                    "If the reader only needs to see the figures, not edit them, a PDF is often better than either. Going the other way, our [[pdf-to-excel|PDF to Excel converter]] always gives you an .xlsx file.",
                ],
            },
            {
                "heading": "Is XLS the same as XLSX?",
                "paragraphs": [
                    "No. Both are Excel workbooks and both open in current versions of Excel, but they are different file formats with different limits: XLS is a single binary file with at most 65,536 rows and 256 columns per sheet, while XLSX is a ZIP archive of XML files with up to 1,048,576 rows and 16,384 columns.",
                ],
            },
            {
                "heading": "How we tested",
                "paragraphs": [
                    "We generated test workbooks with openpyxl (numbers, text and dates), saved copies as XLS with LibreOffice 24.2, then reopened them to count rows and columns. File sizes were measured on disk. The tests ran in a test copy of this site on our own machine, using the same converter code as our Excel to PDF tool; the live server's software versions may differ slightly.",
                ],
            },
        ],
    },
    {
        "slug": "ppt-vs-pptx",
        # Release 7, R7-78: official sources (each URL checked 13 Nov 2026).
        "sources": [('Library of Congress: PowerPoint 97-2003 Binary File Format (.ppt)', 'https://www.loc.gov/preservation/digital/formats/fdd/fdd000511.shtml'), ('Microsoft Support: Open XML Formats and file name extensions', 'https://support.microsoft.com/en-us/office/open-xml-formats-and-file-name-extensions-5200d93c-3449-4380-8e11-31ef14555b18')],
        # 24 Oct 2026 (AI-visibility plan, Google step 5). Facts: Library of
        # Congress format description fdd000511 (PPTX the default from
        # PowerPoint 2007; ISO/IEC 29500) and Microsoft "Open XML Formats and
        # file name extensions" (.pptm). Test figures: measure_office.py,
        # 24 Oct 2026, LibreOffice 24.2, converters/office.py.
        "title": "PPT vs PPTX: What's the Difference? (With Test Results)",
        "seo_title": "PPT vs PPTX: What's the Difference? (Tested) | KuickKonvert",
        "meta_description": "PPT vs PPTX explained: what changed, file size, macros and PDF conversion, with our own test results. Use PPTX unless an old PowerPoint needs PPT.",
        "dek": "PPTX is PowerPoint's modern format (PowerPoint 2007 onwards): a ZIP archive of XML files. PPT is the older binary format of PowerPoint 97 to 2003. Use PPTX for almost everything; in our tests it was the smaller file, and both formats gave the same PDF. To make a PDF of either format, use our [[ppt-to-pdf|PowerPoint to PDF converter]].",
        "published": NEW_GUIDES_RELEASE_DATE,
        "related_tools": ["ppt-to-pdf", "pdf-to-ppt"],
        "sections": [
            {
                "heading": "PPT vs PPTX at a glance",
                "paragraphs": [
                    "The short version: PPTX is the modern PowerPoint format and the right choice for almost everything. PPT is the older format, still worth knowing about if someone uses a very old version of PowerPoint.",
                ],
                "table": {
                    "caption": "PPT and PPTX compared",
                    "headers": ["", "PPT", "PPTX"],
                    "rows": [
                        ["PowerPoint's default format", "PowerPoint 97 to 2003", "PowerPoint 2007 onwards"],
                        ["What the file is inside", "One binary file", "A ZIP archive of XML files (Office Open XML)"],
                        ["Can contain macros?", "Yes", "No - macro presentations use .pptm"],
                        ["File size in our test", "Larger", "Smaller"],
                        ["Same PDF from our tool?", "Yes", "Yes"],
                    ],
                    "note": "Details and sources for each row are in the sections below.",
                },
            },
            {
                "heading": "Two different formats",
                "paragraphs": [
                    "PPT was PowerPoint's format from PowerPoint 97 through 2003. According to the US Library of Congress's format records, PPTX replaced it as the default from PowerPoint 2007, and it is standardised as ISO/IEC 29500 (Office Open XML). PowerPoint can still save in the old format, as \"PowerPoint 97-2003 Presentation\".",
                    "In our test files, the PPTX started with PK, the signature of a ZIP archive, and the PPT with D0 CF 11 E0, the marker of Microsoft's older compound binary format -- the same split as DOC and DOCX for Word.",
                ],
            },
            {
                "heading": "File size: what we measured",
                "paragraphs": [
                    "We built a ten-slide text presentation and a copy with one extra full-slide photo, then saved each as PPTX and as PPT. For the text-only deck the difference was dramatic: 36 KB as PPTX against 659 KB as PPT. With the photo, most of the file was the photo itself, already compressed as a JPG, so the gap shrank: 3,108 KB against 3,756 KB.",
                    "Both formats then went through our PowerPoint to PDF converter and gave the same result: the same number of pages and almost exactly the same PDF size.",
                ],
                "table": {
                    "caption": "The same presentation saved both ways (our test, October 2026)",
                    "headers": ["Test presentation", "PPTX", "PPT", "PDF from our tool (either format)"],
                    "rows": [
                        ["10 text slides", "36 KB", "659 KB", "10 pages, about 45 KB"],
                        ["Same 10 slides plus one 4000 x 3000 photo (3,072 KB JPG)", "3,108 KB", "3,756 KB", "11 pages, about 1,832 KB"],
                    ],
                    "note": "The PPT copies were saved with LibreOffice, not Microsoft PowerPoint; sizes from PowerPoint itself can differ.",
                },
            },
            {
                "heading": "When the difference actually matters",
                "paragraphs": [
                    "Old software. PowerPoint 2003 and earlier can't open a .pptx without Microsoft's compatibility pack -- the usual reason someone still asks for .ppt.",
                    "Macros. A normal .pptx can't contain macros; PowerPoint uses .pptm for macro-enabled presentations. A .ppt from an unknown sender may contain macros.",
                    "Email and upload limits. In our test the old format was the bigger file, so if a presentation is too large to send, saving it as PPT won't help -- compressing the pictures inside it, or sending a PDF, usually will.",
                ],
            },
            {
                "heading": "Which one should you use?",
                "paragraphs": [
                    "Use PPTX unless someone specifically needs PPT for an old program. If the audience only needs to view the slides, send a PDF: it looks the same on every device. Our [[ppt-to-pdf|PowerPoint to PDF converter]] accepts both .ppt and .pptx, and your upload and the PDF are deleted from our server as soon as your download is ready.",
                    "Going the other way, our [[pdf-to-ppt|PDF to PowerPoint converter]] gives you a .pptx file with each PDF page as a picture slide.",
                ],
            },
            {
                "heading": "Is PPT the same as PPTX?",
                "paragraphs": [
                    "No. Both are PowerPoint presentations and both open in current versions of PowerPoint, but they are different file formats: PPT is a single binary file, while PPTX is a ZIP archive of XML files. PowerPoint 2003 and earlier cannot open a PPTX without Microsoft's compatibility pack.",
                ],
            },
            {
                "heading": "How we tested",
                "paragraphs": [
                    "We generated the presentations with python-pptx (ten title-and-text slides, plus a copy with one computer-generated 4000 x 3000 photo), saved copies as PPT with LibreOffice 24.2, and converted both versions to PDF with the same code our PowerPoint to PDF tool runs. The tests ran in a test copy of this site on our own machine; the live server's software versions may differ slightly.",
                ],
            },
        ],
    },
    {
        "slug": "pdf-or-word-which-to-send",
        # 24 Oct 2026 (AI-visibility plan, Google step 5): a decision guide
        # that links out to the detailed Word-to-PDF guides. Test figures:
        # measure_word_pdf.py, 24 Oct 2026, LibreOffice 24.2,
        # converters/office.py convert_office_to_pdf (fonts checked with pypdf).
        "title": "PDF or Word: Which Should You Send? (With Test Results)",
        "seo_title": "PDF or Word: Which Should You Send? (Tested) | KuickKonvert",
        "meta_description": "Should you send a PDF or a Word file? When each is right, what changes when you convert, and our test: a 6 MB Word file became a 1.8 MB PDF.",
        "dek": "Send a PDF when the document is finished and must look the same for everyone -- a CV, an invoice, a form or a report. Send Word (DOCX) when the other person needs to edit it, or when they ask for Word. Here is why, with what we measured when converting. To convert, use [[word-to-pdf|Word to PDF]] or [[pdf-to-word|PDF to Word]].",
        "published": NEW_GUIDES_RELEASE_DATE,
        "related_tools": ["word-to-pdf", "pdf-to-word", "watermark-pdf"],
        "sections": [
            {
                "heading": "The quick answer",
                "paragraphs": [
                    "PDF is for reading; Word is for editing. If someone has asked for a specific format, use that. Otherwise:",
                ],
                "table": {
                    "caption": "PDF or Word: which to send",
                    "headers": ["You are sending...", "Send", "Why"],
                    "rows": [
                        ["A finished CV, letter, invoice or report", "PDF", "Looks the same on every device and is harder to change by accident"],
                        ["A draft someone will edit or comment on", "Word (DOCX)", "Easy to edit, track changes and comment"],
                        ["A form to print or sign", "PDF", "Keeps the exact page layout for printing"],
                        ["A file to a portal that asks for Word", "Word (DOCX)", "Follow the instructions -- some systems read Word files"],
                        ["Something with large photos, by email", "PDF", "In our test it was less than a third of the Word file's size"],
                    ],
                },
            },
            {
                "heading": "Why a PDF looks the same everywhere",
                "paragraphs": [
                    "A Word file is laid out by whichever program opens it, using the fonts installed on that computer. If a font is missing, the program substitutes another one and lines can re-wrap. A PDF stores the finished pages, and normally the fonts as well.",
                    "In our test, the PDF made by our Word to PDF tool had its fonts embedded and its text was still real text: it could be searched and copied. On our server, Calibri is replaced by Carlito, a font with identical letter widths, so the layout is kept. Newer fonts such as Aptos are a known exception, explained in our guide on why a PDF's layout sometimes shifts.",
                ],
            },
            {
                "heading": "File size: what we measured",
                "paragraphs": [
                    "We wrote a two-page CV-style document in Word format and converted it with the same code our Word to PDF tool runs. The text-only version went from 36 KB as DOCX to 21 KB as PDF. A version with two 4000 x 3000 photos added went from 6,179 KB to 1,808 KB, because photos are stored in the PDF at 300 pixels for every inch they take up on the page, which is still sharp for printing.",
                ],
                "table": {
                    "caption": "The same document as Word and as PDF (our test, October 2026)",
                    "headers": ["Test document", "Word (DOCX)", "PDF from our tool", "PDF text searchable?"],
                    "rows": [
                        ["2 pages of text", "36 KB", "21 KB", "Yes"],
                        ["Same text plus two 4000 x 3000 photos (4 pages)", "6,179 KB", "1,808 KB", "Yes"],
                    ],
                    "note": "Computer-generated test document; your own files will give different numbers.",
                },
            },
            {
                "heading": "Is a PDF safe from editing?",
                "paragraphs": [
                    "Not completely. A PDF is harder to change by accident, but PDF editors and converters -- including our own [[pdf-to-word|PDF to Word converter]] -- can turn a text-based PDF back into an editable document. If you need to stop casual copying or opening, add a password with our [[protect-pdf|Protect PDF tool]]; for proof of origin, a visible watermark helps more than a file format.",
                ],
            },
            {
                "heading": "How to convert",
                "paragraphs": [
                    "Word to PDF: in Word, choose File > Save As and pick PDF, or upload the .doc or .docx to our [[word-to-pdf|Word to PDF converter]]. PDF to Word: upload the PDF to our [[pdf-to-word|PDF to Word converter]] and you get a .docx. Both are free with no sign-up, and your upload and the converted file are deleted from our server as soon as your download is ready.",
                    "Always open the converted file once before you send it, and check the fonts and page breaks.",
                ],
            },
            {
                "heading": "How we tested",
                "paragraphs": [
                    "We generated the test document with python-docx (Calibri 11 pt, headings, about two pages of text) and a copy with two computer-generated 4000 x 3000 photos placed 6 inches wide. Both went through the same code our Word to PDF tool runs (LibreOffice 24.2) in a test copy of this site on our own machine; we checked the page count, embedded fonts and searchable text with pypdf. The live server's software versions may differ slightly.",
                ],
            },
        ],
    },
]

GUIDES_BY_SLUG = {g["slug"]: g for g in GUIDES}

# ---- Related guides (added 15 Oct 2026) ----------------------------------
# A crawl of the live site on 15 Oct 2026 found no guide linking to any
# other guide, and seven guides reachable from only three pages each. Each
# guide below links to 2-3 guides on a closely related topic, shown as a
# "Related guides" list under "Related tools" (templates/guide.html).
# Edit freely; a misspelt slug stops the app at start-up (check below), so
# a broken link can never reach the live site.
RELATED_GUIDES = {
    "docx-vs-doc": ["word-to-pdf-what-carries-over", "why-pdf-layout-shifts", "pdf-to-word-text-vs-scanned", "ppt-vs-pptx"],
    "why-pdf-layout-shifts": ["word-to-pdf-what-carries-over", "docx-vs-doc", "powerpoint-to-pdf-and-back"],
    "pdf-compression-levels-explained": ["photos-to-one-pdf-jpg-to-pdf-tips", "submitting-coursework-as-a-pdf", "jpg-vs-png"],
    "jpg-vs-png": ["photos-to-one-pdf-jpg-to-pdf-tips", "what-is-a-heic-file", "pdf-compression-levels-explained"],
    "merge-pdf-in-the-right-order": ["split-and-rotate-pdf-pages", "submitting-coursework-as-a-pdf", "photos-to-one-pdf-jpg-to-pdf-tips"],
    "pdf-password-protection-explained": ["watermark-pdf-what-it-protects", "location-data-in-photos"],
    "excel-to-pdf-fit-on-one-page": ["pdf-to-excel-table-conversion-results", "why-pdf-layout-shifts", "xls-vs-xlsx"],
    "pdf-to-excel-table-conversion-results": ["pdf-to-word-text-vs-scanned", "excel-to-pdf-fit-on-one-page"],
    "photos-to-one-pdf-jpg-to-pdf-tips": ["what-is-a-heic-file", "pdf-compression-levels-explained", "submitting-coursework-as-a-pdf"],
    "pdf-to-word-text-vs-scanned": ["pdf-to-excel-table-conversion-results", "docx-vs-doc", "pdf-or-word-which-to-send"],
    "powerpoint-to-pdf-and-back": ["why-pdf-layout-shifts", "word-to-pdf-what-carries-over", "ppt-vs-pptx"],
    "watermark-pdf-what-it-protects": ["pdf-password-protection-explained", "split-and-rotate-pdf-pages"],
    "split-and-rotate-pdf-pages": ["merge-pdf-in-the-right-order", "pdf-compression-levels-explained"],
    "word-to-pdf-what-carries-over": ["why-pdf-layout-shifts", "docx-vs-doc", "submitting-coursework-as-a-pdf"],
    "what-is-a-heic-file": ["location-data-in-photos", "what-is-a-webp-image", "photos-to-one-pdf-jpg-to-pdf-tips"],
    "location-data-in-photos": ["what-is-a-heic-file", "what-is-a-webp-image", "pdf-password-protection-explained"],
    "what-is-a-webp-image": ["what-is-a-heic-file", "jpg-vs-png", "location-data-in-photos"],
    "submitting-coursework-as-a-pdf": ["photos-to-one-pdf-jpg-to-pdf-tips", "pdf-compression-levels-explained", "merge-pdf-in-the-right-order"],
    "xls-vs-xlsx": ["docx-vs-doc", "excel-to-pdf-fit-on-one-page", "pdf-to-excel-table-conversion-results"],
    "ppt-vs-pptx": ["docx-vs-doc", "powerpoint-to-pdf-and-back", "xls-vs-xlsx"],
    "pdf-or-word-which-to-send": ["word-to-pdf-what-carries-over", "why-pdf-layout-shifts", "docx-vs-doc"],
}
for _src, _targets in RELATED_GUIDES.items():
    if _src not in GUIDES_BY_SLUG:
        raise ValueError(f"RELATED_GUIDES: unknown guide slug {_src!r}")
    for _t in _targets:
        if _t not in GUIDES_BY_SLUG or _t == _src:
            raise ValueError(f"RELATED_GUIDES[{_src!r}]: bad target {_t!r}")

# Reverse index: tool slug -> the guides that reference it, so tool.html can
# render a "Further reading" block without every TOOL_CONTENT entry having
# to separately know which guides exist.
from collections import defaultdict as _defaultdict

GUIDES_BY_TOOL = _defaultdict(list)
for _g in GUIDES:
    for _slug in _g.get("related_tools", []):
        GUIDES_BY_TOOL[_slug].append(_g)


# Release 7 (2026-11-19): structured data (@id, breadcrumbs), tool-page
# facts table and headings, descriptions, guide links. Every tool page, every
# guide's markup and /tools, /about, /link-to-us changed significantly, so
# their sitemap <lastmod> moves to the release day (this also feeds IndexNow).
RELEASE7_DATE = "2026-11-19"
TOOLS_LASTMOD = RELEASE7_DATE
HOME_LASTMOD = RELEASE7_DATE
GUIDES_MARKUP_LASTMOD = RELEASE7_DATE
for _t in TOOLS:
    _t["lastmod"] = RELEASE7_DATE
for _k in ("tools", "about", "link-to-us"):
    STATIC_LASTMOD[_k] = RELEASE7_DATE
# R7-93: the Privacy Notice text changed in Release 7 ("Last updated" =
# RELEASE7_DATE), so its sitemap <lastmod> moves to the same day.
STATIC_LASTMOD["privacy"] = RELEASE7_DATE
# R7-28 (Shahid, 11 Nov 2026: yes): the 12 guides whose visible text changed
# in Release 7 (dek links R7-26; H2 renames R7-27 are in three of them) show
# "Updated" with the release day. Only these 12: a date moves only with a
# real change (compliance rule N5).
RELEASE7_UPDATED_GUIDES = (
    "docx-vs-doc", "why-pdf-layout-shifts", "pdf-compression-levels-explained",
    "jpg-vs-png", "excel-to-pdf-fit-on-one-page", "powerpoint-to-pdf-and-back",
    "what-is-a-heic-file", "what-is-a-webp-image", "word-to-pdf-what-carries-over",
    "xls-vs-xlsx", "ppt-vs-pptx", "pdf-or-word-which-to-send",
)
for _g in GUIDES:
    if _g["slug"] in RELEASE7_UPDATED_GUIDES:
        _g["updated"] = RELEASE7_DATE

# ---- Release 7: three new guides (WP12 / R7-48, R7-49, R7-50) -------------
# Drafted 12 Nov 2026 (G12) and approved by Shahid the same day "without the
# photo figures": the size results that needed real iPhone HEIC photos and a
# real photo PDF are left out. Every number below comes from KuickKonvert's
# own converter code run on computer-made test files (results.json, G12), or
# from the providers' help pages checked on 12 Nov 2026. Each guide owns one
# query family and links to the older guide that explains the detail, so no
# explanation is repeated (checked by test_release7_new_guides).
RELEASE7_NEW_GUIDES = [
    {
        "slug": "how-to-split-pdf-files",
        "title": "How to Split a PDF on Windows, Mac, iPhone or Android",
        "seo_title": "How to Split PDF Files on Any Device (Tested) | KuickKonvert",
        "meta_description": "Split a PDF into one file per page on Windows, Mac, iPhone or Android, open the ZIP on each device, and see what our split test did to file size.",
        "dek": "Splitting a PDF gives you every page as a separate PDF file. It works in any web browser, on a computer or a phone, with nothing to install. Here are the steps, how to open the result on each kind of device, and what we found when we split a file of text and photos. Our [[split-pdf|Split PDF tool]] is free, with no sign-up.",
        "published": RELEASE7_DATE,
        "related_tools": ["split-pdf", "merge-pdf", "compress-pdf"],
        "sections": [
            {
                "heading": "Split a PDF in your browser",
                "paragraphs": [
                    "The steps are the same in Chrome, Edge, Safari and Firefox, on a computer or a phone:",
                ],
                "steps": [
                    "Open [[split-pdf|Split PDF]] on kuickkonvert.com.",
                    "Choose your PDF (up to 50 MB). On a phone, tap Choose file and pick the PDF from Files or Downloads.",
                    "Press Convert. A PDF with several pages comes back as one ZIP file holding a one-page PDF for each page, numbered in page order.",
                ],
            },
            {
                "heading": "Opening the ZIP on each device",
                "paragraphs": [
                    "Windows: in File Explorer, double-click the ZIP to look inside it, or right-click it and choose Extract All to copy the page files into an ordinary folder.",
                    "Mac: double-click the ZIP in Finder and macOS unpacks it into a folder beside it.",
                    "iPhone and iPad: in the Files app, tap the ZIP and Files unpacks it into a folder in the same place.",
                    "Android: on many phones, open the Files app, tap the ZIP and choose Extract. Menus differ between phone makers.",
                ],
            },
            {
                "heading": "What splitting did to file size in our test",
                "paragraphs": [
                    "We split a 10-page, 1,250 KB test PDF with six pages of text and four pages that each held one photo. Every photo page came out at 309 to 314 KB, carrying its picture at full size, while each text page was about 1 KB. Together the ten files came to 1,253 KB, slightly more than the original, because each new file has its own small header and page structure.",
                    "Splitting never makes a picture smaller. If a single page is still too large to send, put that page through [[compress-pdf|Compress PDF]].",
                    "The text in this test used a standard font that was not stored inside the file. When a PDF embeds its font, each split page needs its own copy, and the pages can add up to several times the original. Our guide to what splitting and rotating do inside a PDF shows that test.",
                ],
                "table": {
                    "caption": "Splitting a 10-page text-and-photo test PDF with our Split PDF code (November 2026)",
                    "headers": ["Pages", "Size of each page file"],
                    "rows": [
                        ["6 text pages", "About 1 KB"],
                        ["4 pages with a photo", "309 to 314 KB"],
                        ["All 10 page files together", "1,253 KB (original 1,250 KB)"],
                    ],
                    "note": "A test file made on a computer, not a real document; sizes from your own PDFs will differ.",
                },
            },
            {
                "heading": "Keeping only the pages you want",
                "paragraphs": [
                    "Split PDF always gives you every page; there is no page-range setting. Delete the page files you don't need. If you want a few of the remaining pages back in a single document, add them in order to [[merge-pdf|Merge PDF]].",
                    "A PDF that asks for a password when you open it can't be split until you have saved a copy without the password.",
                ],
            },
            {
                "heading": "How we tested",
                "paragraphs": [
                    "November 2026. We made a 10-page A4 test PDF of 1,250 KB: six pages of text in a standard font that was not embedded, and four pages each with one 1800 x 1200 JPEG photo. It was split by the same code our Split PDF tool runs, in a test copy of the site, and the sizes were read from the output files.",
                ],
            },
        ],
    },
    {
        "slug": "heic-to-jpg-on-windows",
        # Release 7, R7-78: official sources (each URL checked 13 Nov 2026).
        "sources": [('Apple Support: Transfer photos and videos from your iPhone or iPad to your Mac or PC', 'https://support.apple.com/en-us/120267')],
        "title": "How to Convert iPhone HEIC Photos to JPG on Windows",
        "seo_title": "How to Convert HEIC to JPG on Windows | KuickKonvert",
        "meta_description": "Three ways to handle iPhone HEIC photos on a Windows PC: view them with Microsoft's extensions, switch the iPhone to JPG, or convert online for free.",
        "dek": "Photos copied from an iPhone often reach a Windows PC as .heic files that some apps and most upload forms won't take. You can get Windows to show them, stop the iPhone saving new photos as HEIC, or turn the ones you have into JPGs with our [[heic-to-jpg|HEIC to JPG converter]].",
        "published": RELEASE7_DATE,
        "related_tools": ["heic-to-jpg", "jpg-to-pdf", "webp-to-jpg"],
        "sections": [
            {
                "heading": "Getting the photos onto your PC",
                "paragraphs": [
                    "Apple's support page on transferring photos to a Mac or PC (checked 12 November 2026) gives these steps for Windows:",
                ],
                "steps": [
                    "Install the Apple Devices app from the Microsoft Store.",
                    "Connect the iPhone to the PC with a USB cable and unlock it if asked.",
                    "If the iPhone asks whether to trust this computer, tap Trust or Allow.",
                    "Import the photos with the Microsoft Photos app.",
                ],
            },
            {
                "heading": "If iCloud Photos is turned on",
                "paragraphs": [
                    "Apple notes that with iCloud Photos on, you must first download the original, full-resolution photos to the iPhone before importing them to a PC.",
                ],
            },
            {
                "heading": "Way 1: let Windows show HEIC photos",
                "paragraphs": [
                    "Microsoft's Store listing for the HEIF Image Extension says it lets Windows read HEIF files, and that the separate HEVC Video Extensions package is also needed to view .heic photos. With both installed, the Photos app can display them.",
                    "This only helps on that PC. The files are still .heic, so a website or form that asks for JPG will still refuse them.",
                ],
            },
            {
                "heading": "Way 2: switch the iPhone to JPG for new photos",
                "paragraphs": [
                    "To make photos work well with Windows, Apple suggests Settings > Camera > Formats > Most Compatible. From then on the camera saves photos as JPEG; photos already on the phone are not changed.",
                ],
            },
            {
                "heading": "Way 3: convert the HEIC photos you already have",
                "paragraphs": [
                    "This is the route for photos you need to upload or send now:",
                ],
                "steps": [
                    "Find the imported .heic photos in File Explorer.",
                    "Open [[heic-to-jpg|HEIC to JPG]] and add up to 20 photos at a time: up to 65 megapixels each and 50 MB per upload in total.",
                    "Press Convert. One photo downloads as a JPG; several come back together in a ZIP. To unpack it, right-click the ZIP in File Explorer and choose Extract All.",
                ],
            },
            {
                "heading": "What our batch test showed",
                "paragraphs": [
                    "We ran a batch of five test HEIC photos through the converter's code. Each JPG kept its file name, its full 4032 x 3024 size, the date taken and the camera name, and none kept the GPS location that every HEIC contained. What else the converter keeps or drops, and why the JPG usually comes out larger than the HEIC, is in our guide to HEIC files.",
                ],
                "table": {
                    "caption": "Converting 5 HEIC test photos with our HEIC to JPG code (November 2026)",
                    "headers": ["What we checked", "Result"],
                    "rows": [
                        ["File names", "Kept: test-photo-1.heic became test-photo-1.jpg"],
                        ["Picture size", "Kept: 4032 x 3024 pixels"],
                        ["Date taken and camera name", "Kept in all 5"],
                        ["GPS location (in all 5 HEIC files)", "Removed from all 5 JPGs"],
                    ],
                    "note": "Test photos made on a computer, not taken on an iPhone.",
                },
            },
            {
                "heading": "Which way to choose",
                "paragraphs": [
                    "If you only want to look at the photos on your own PC, Way 1 is enough. If you want future photos to work everywhere without converting, use Way 2. If you need to upload or send photos you already have, use Way 3; the JPGs you get back carry no GPS location.",
                ],
            },
            {
                "heading": "How we tested",
                "paragraphs": [
                    "November 2026. Five 4032 x 3024 HEIC files were made on a computer, each with a date, a camera name and GPS coordinates, and converted together by the same code our HEIC to JPG tool runs, in a test copy of the site. The EXIF data in each JPG was read back with Pillow. The Windows and iPhone steps come from Apple's and Microsoft's own support and Store pages, checked on 12 November 2026.",
                ],
            },
        ],
    },
    {
        "slug": "reduce-pdf-size-for-email",
        "title": "How to Reduce a PDF's Size for Email (With Our Test Results)",
        "seo_title": "How to Reduce PDF Size for Email (Tested) | KuickKonvert",
        "meta_description": "Email attachment limits for Gmail and Outlook, which compression level suits scans, photos or text, and what to do when a PDF is still too big to send.",
        "dek": "Gmail and Outlook.com stop at 25 MB of attachments, and the Outlook app can stop at 20 MB. A PDF made of scans or photos can usually be made much smaller; a PDF of typed text is normally small already. Our [[compress-pdf|Compress PDF tool]] is free, with no sign-up.",
        "published": RELEASE7_DATE,
        "related_tools": ["compress-pdf", "split-pdf", "jpg-to-pdf"],
        "sections": [
            {
                "heading": "Attachment limits (checked 12 November 2026)",
                "paragraphs": [
                    "Aim for a file comfortably under the limit. Email carries attachments as text using Base64 encoding, which turns every 3 bytes into 4 characters, so the message is about a third bigger than the file on your disk.",
                ],
                "table": {
                    "caption": "Limits stated on each provider's own help page",
                    "headers": ["Service", "Limit"],
                    "rows": [
                        ["Gmail (personal accounts)", "25 MB of attachments (Google: Send attachments with your Gmail message)"],
                        ["Outlook.com", "25 MB for file attachments (Microsoft: Sending limits in Outlook.com)"],
                        ["Outlook app with an internet account such as Outlook.com or Gmail", "20 MB per email (Microsoft: Reduce attachment size to send large files with Outlook)"],
                    ],
                },
            },
            {
                "heading": "Compress a PDF before you attach it",
                "paragraphs": [
                    "This works in any browser, on a computer or a phone:",
                ],
                "steps": [
                    "Open [[compress-pdf|Compress PDF]] on kuickkonvert.com and choose your PDF (up to 50 MB).",
                    "Choose a level using the table below, then press Convert.",
                    "Look at the size of the downloaded file before you attach it, and open it to check it still reads well.",
                ],
            },
            {
                "heading": "Pick the level by what is in your PDF",
                "paragraphs": [
                    "On our scan, Balanced (4,286 KB) and Highest quality (4,288 KB) hardly helped, because the pages were scanned at 200 dpi, below the resolution at which those levels start reducing pictures. Smallest file cut it to under a tenth of its size. Why the levels behave like this is explained in our guide to PDF compression levels.",
                    "Before you send a scan compressed at screen quality, zoom in on the smallest print: small text on a scanned page can blur at that setting.",
                ],
                "table": {
                    "caption": "Compressing two test PDFs with our Compress PDF code (November 2026)",
                    "headers": ["What is in your PDF", "Level to try", "Our test"],
                    "rows": [
                        ["Scanned pages", "Smallest file (screen quality)", "3-page scan: 5,355 KB became 501 KB"],
                        ["Photos", "Balanced (recommended) first, then Smallest file if it is still too big", "Depends on the photos' resolution; see our compression levels guide"],
                        ["Typed text only", "Usually no need to compress", "5-page report: stayed at 5 KB at every level"],
                    ],
                    "note": "When the result isn't smaller, the tool gives you back your original file.",
                },
            },
            {
                "heading": "If it is still too big",
                "paragraphs": [
                    "Split it: [[split-pdf|Split PDF]] gives every page as its own file, so you can send the pages over two or more emails. Check the total size of the files you attach to each one.",
                    "Or send a link: Google's and Microsoft's help pages both point to Google Drive or OneDrive for files over their limits. Upload the PDF there and email the link instead.",
                ],
            },
            {
                "heading": "How we tested",
                "paragraphs": [
                    "November 2026. We made two test PDFs on a computer: a 3-page scan of 5,355 KB (each page a 200-dpi greyscale picture of text, with no text layer) and a 5-page typed report of 5 KB. Each was compressed at all three levels by the same code our Compress PDF tool runs (Ghostscript 10.02.1), in a test copy of the site; the live server's version may differ. The attachment limits come from Google's and Microsoft's own help pages, checked on 12 November 2026.",
                ],
            },
        ],
    },
]
GUIDES.extend(RELEASE7_NEW_GUIDES)
for _g in RELEASE7_NEW_GUIDES:
    GUIDES_BY_SLUG[_g["slug"]] = _g
    for _slug in _g["related_tools"]:
        GUIDES_BY_TOOL[_slug].append(_g)
RELATED_GUIDES.update({
    "how-to-split-pdf-files": ["split-and-rotate-pdf-pages", "merge-pdf-in-the-right-order", "reduce-pdf-size-for-email"],
    "heic-to-jpg-on-windows": ["what-is-a-heic-file", "location-data-in-photos", "photos-to-one-pdf-jpg-to-pdf-tips"],
    "reduce-pdf-size-for-email": ["pdf-compression-levels-explained", "how-to-split-pdf-files", "submitting-coursework-as-a-pdf"],
})
RELATED_GUIDES["split-and-rotate-pdf-pages"] = RELATED_GUIDES["split-and-rotate-pdf-pages"] + ["how-to-split-pdf-files"]
for _src, _targets in RELATED_GUIDES.items():
    for _t in _targets:
        if _t not in GUIDES_BY_SLUG or _t == _src:
            raise ValueError(f"RELATED_GUIDES[{_src!r}]: bad target {_t!r}")
TOOLS_BY_SLUG["word-to-pdf"]["faq"] = list(TOOLS_BY_SLUG["word-to-pdf"]["faq"]) + [
    ("Is Word to PDF free, and does it add a watermark?",
     "It's free with no sign-up, and no watermark is added: the PDF contains only your document. "
     "Uploads can be up to 50MB, and fair-use limits apply to how many conversions can run per minute. "
     "Your file is deleted automatically after conversion."),
]
# Release 7, WP14 R7-62 (Package 2, 11 Nov 2026): shown in the upload box,
# before anything is sent, on the tools whose refusals were most common
# (pdf_locked, pdf_scanned, pdf_too_complex in the 30 Oct-8 Nov review).
# Plain statements of what the tool can't take; no numbers that may change.
UPLOAD_NOTES = {
    "pdf-to-word": "Can't be converted: password-protected PDFs, scanned PDFs whose pages are pictures of text (KuickKonvert doesn't do OCR), and PDFs with very detailed pages.",
    "pdf-to-excel": "Can't be converted: password-protected PDFs, and scanned PDFs whose pages are pictures of text, with no tables to extract (KuickKonvert doesn't do OCR).",
    "pdf-to-ppt": "Can't be converted: password-protected PDFs. Open the file with its password and save a copy without one first.",
}
TOOLS_BY_SLUG["png-to-pdf"]["faq"] = list(TOOLS_BY_SLUG["png-to-pdf"]["faq"]) + [
    ("Is this PNG to PDF converter free?",
     "Yes. It is free with no sign-up, and KuickKonvert adds no watermark to your PDF. Fair-use limits apply."),
]


# ---------------------------------------------------------------------------
# Release 7, WP8: professional videos on the website (lawyer's advice, 10 Nov
# 2026). IDs, lengths and upload times were read from YouTube and the master
# MP4s on 10 Nov 2026. Professional versions only; never the Gen-Z cuts.
# Thumbnails are frames from the master files, stored in static/img/video/.
# ---------------------------------------------------------------------------
VIDEO_PLAY_LABEL = ("Play Video \u2014 Loads player from YouTube (Google). "
                    "Connects to external servers and processes device details.")


def _video(vid, seconds, iso, uploaded, thumb):
    return {"id": vid, "seconds": seconds, "duration": iso,
            "uploaded": uploaded, "thumb": thumb}


VIDEOS = {
    "home": _video("pRmhhN1kfP0", 29, "PT29S", "2026-11-12T04:16:58-08:00", "home.jpg"),
    "all-tools": _video("aouHgA5mJR4", 129, "PT2M9S", "2026-11-10T03:30:33-08:00", "all-tools.jpg"),
    "word-to-pdf": _video("t4MdCZw2SaQ", 13, "PT13S", "2026-11-12T04:22:13-08:00", "word-to-pdf.jpg"),
    "pdf-to-word": _video("VLyY6sAZ5qg", 14, "PT14S", "2026-11-04T08:19:52-08:00", "pdf-to-word.jpg"),
    "excel-to-pdf": _video("pwrFytJwBd8", 16, "PT16S", "2026-11-04T08:21:04-08:00", "excel-to-pdf.jpg"),
    "pdf-to-excel": _video("wjHNfb-S99Q", 16, "PT16S", "2026-11-04T08:21:59-08:00", "pdf-to-excel.jpg"),
    "ppt-to-pdf": _video("JG--gxZvDq8", 14, "PT14S", "2026-11-12T04:24:09-08:00", "ppt-to-pdf.jpg"),
    "pdf-to-ppt": _video("n__r7wUNHhg", 10, "PT10S", "2026-11-04T08:23:41-08:00", "pdf-to-ppt.jpg"),
    "jpg-to-pdf": _video("wCl7aVKRXF8", 13, "PT13S", "2026-11-04T08:24:49-08:00", "jpg-to-pdf.jpg"),
    "png-to-pdf": _video("XzBztET4xug", 12, "PT12S", "2026-11-12T04:31:28-08:00", "png-to-pdf.jpg"),
    "pdf-to-jpg": _video("DpSO6gciYNA", 14, "PT14S", "2026-11-04T08:26:11-08:00", "pdf-to-jpg.jpg"),
    "pdf-to-png": _video("YA3Nv2bdhdc", 13, "PT13S", "2026-11-04T09:48:14-08:00", "pdf-to-png.jpg"),
    "heic-to-jpg": _video("YPpm3srHRZw", 19, "PT19S", "2026-11-04T09:48:32-08:00", "heic-to-jpg.jpg"),
    "webp-to-jpg": _video("_p23V4wmO08", 14, "PT14S", "2026-11-04T09:48:38-08:00", "webp-to-jpg.jpg"),
    "png-to-jpg": _video("VHItHcqkhkc", 9, "PT9S", "2026-11-12T04:33:55-08:00", "png-to-jpg.jpg"),
    "jpg-to-png": _video("eeRqcbrzmgc", 13, "PT13S", "2026-11-12T04:36:30-08:00", "jpg-to-png.jpg"),
    "merge-pdf": _video("F0snv-p1_is", 13, "PT13S", "2026-11-12T04:39:37-08:00", "merge-pdf.jpg"),
    "split-pdf": _video("mFyvkxM1hL8", 14, "PT14S", "2026-11-04T09:49:02-08:00", "split-pdf.jpg"),
    "compress-pdf": _video("DZFSWepaqlI", 14, "PT14S", "2026-11-04T09:49:09-08:00", "compress-pdf.jpg"),
    "rotate-pdf": _video("Tfi_y3-JTHg", 10, "PT10S", "2026-11-12T04:44:00-08:00", "rotate-pdf.jpg"),
    "watermark-pdf": _video("VYEUpopBP6k", 14, "PT14S", "2026-11-04T09:49:21-08:00", "watermark-pdf.jpg"),
    "protect-pdf": _video("GVHzA9hSlZM", 16, "PT16S", "2026-11-04T09:49:27-08:00", "protect-pdf.jpg"),
    "doc-to-docx": _video("ruRe-nX3WWs", 19, "PT19S", "2026-11-04T09:49:33-08:00", "doc-to-docx.jpg"),
}

# G13 (12 Nov 2026): transcripts of the professional voice-overs, from the
# YouTube auto-captions (V03-V22, read 12 Nov 2026) corrected for recognition
# errors ("quickconvert.com" -> kuickkonvert.com, "H EIC" -> HEIC ...), and
# for V23 from the v3 FINAL script (Cut Y). Shahid to vet against the audio.
# Square brackets mark words added for clarity that are not spoken (standard
# transcription practice): the voice-over says "deleted after"; the end card
# of the corrected videos reads "Files deleted after conversion".
#
# V01, V02, V06, V09, V14, V15, V16 and V19: the published videos' audio
# contains claims the site copy rules don't allow. Corrected cuts were made on
# 12 Nov 2026 (files *_R7fix.mp4). Their transcripts are below in
# VIDEO_TRANSCRIPTS_AFTER_REUPLOAD and are NOT applied: only after a corrected
# video is uploaded and its new YouTube ID (and thumbnail) is set in VIDEOS,
# move its entry into VIDEO_TRANSCRIPTS, so the page never shows a transcript
# that differs from the video it embeds.
VIDEO_TRANSCRIPTS = {
    'pdf-to-word': "Got a PDF you need to edit, but no original file? Turn it back into an editable Word document. Fix the text, change a number, and you're done. Free at kuickkonvert.com. Your file's deleted right after [conversion].",
    'excel-to-pdf': 'Sending an Excel sheet that spills onto six messy pages? Convert it to a clean PDF that holds its layout. Easy to read, easy to share, opens for everyone. Free at kuickkonvert.com. No sign-up, file deleted after [conversion].',
    'pdf-to-excel': 'Someone sent the report as a PDF, and now you need those numbers in Excel. Convert the PDF to Excel and get your tables back as rows and columns you can actually work with. Free at kuickkonvert.com. File deleted after converting.',
    'pdf-to-ppt': 'Only have the slides as a PDF? Convert the PDF back into PowerPoint slides, free at kuickkonvert.com. File deleted after [conversion].',
    'jpg-to-pdf': "Upload form wants one PDF, but you've got a pile of photos? Drop your JPGs in, put them in order, and get one neat PDF, free at kuickkonvert.com. Files deleted after [conversion].",
    'pdf-to-jpg': 'Want to grab an image or a page out of a PDF? Convert the PDF to JPG and get each page as an image you can post, send or save, free at kuickkonvert.com. File deleted after [conversion].',
    'pdf-to-png': 'Need sharp, high-quality images out of a PDF? Convert it to PNG. Crisp edges, perfect for pages with text or logos. Free at kuickkonvert.com. [Files] deleted after [conversion].',
    'heic-to-jpg': "Sent an iPhone photo and it just won't open on their computer? That's HEIC. Convert it to JPG and it opens anywhere. And we strip the hidden GPS location from your photo while we're at it. Free at kuickkonvert.com. Up to 20 at once. [Files] deleted after [conversion].",
    'webp-to-jpg': "Saved a picture from a website and now nothing will open it? It's a WEBP. Convert it to JPG, the normal format every app and device understands. Free at kuickkonvert.com. [Files] deleted after [conversion].",
    'split-pdf': 'Only need one page out of a big PDF? Split it, and every page becomes its own PDF. Keep the one you need, leave the rest behind. Free at kuickkonvert.com. [Files] deleted after [conversion].',
    'compress-pdf': 'That annoying "file too large" message again? Compress your PDF down to a size that actually uploads, without turning it into mush. Free at kuickkonvert.com. [Files] deleted after [conversion].',
    'watermark-pdf': "Sending out a draft you don't want passed off as final? Stamp a watermark on it: DRAFT, CONFIDENTIAL or your name, on every page. Free at kuickkonvert.com. [Files] deleted after [conversion].",
    'protect-pdf': 'About to email a sensitive PDF with no protection? Add a password first. Locked with strong AES-256 encryption, so only the right person can open it. Free at kuickkonvert.com. File deleted after [conversion].',
    'doc-to-docx': 'Got an old Word file that ends in .doc? Upload portals and Google Docs often want DOCX instead. Convert DOC to DOCX free at kuickkonvert.com. Text, headings, tables and pictures carry over. Free, no sign-up. Your file is deleted after [conversion].',
    'all-tools': "You've got the right file, just in the wrong format. Let's fix that. Meet KuickKonvert: twenty-one free tools for Word, Excel, PowerPoint, images and PDF, all in one place. Follow us for practical file tips. Under Documents, turn Word, Excel and PowerPoint files into PDFs that are ready to share or print. Old and new Office formats both work. Need to make changes? Convert a PDF into an editable Word file, pull its tables into Excel, or turn every page into a PowerPoint slide. You can even switch Word files between DOC and DOCX. Under Images, combine photos and scans into one PDF, or save PDF pages as JPG or PNG. Open iPhone HEIC photos as JPG, convert WEBP images saved from websites, and switch between PNG and JPG whenever a form asks for a specific type. PDF Tools handle the everyday jobs. Merge files into one, in the order you add them. Split a PDF so every page becomes its own file. Compress a PDF that's too big to send. Rotate pages that come out sideways. Add a text watermark across every page. And lock a PDF with a password. Prefer to browse? The All Conversion Tools page shows all twenty-one on one screen. How it works is simple: choose a tool, upload your file, and your result downloads straight away. It's free, with no sign-up, no watermark and nothing to install. Your file is processed in a temporary workspace and deleted automatically after conversion. Questions about file size or formats? The FAQ has quick answers. Uploads can be up to fifty megabytes. And the Guides explain, in plain English, what really changes when you convert a file, based on our own tests. Want to know more, or have a suggestion? Visit About, or reach us through Contact. Try it today at kuickkonvert.com. If this helped, hit like, subscribe to KuickKonvert, and tap the bell so you're the first to see every new tip.",
}
VIDEO_TRANSCRIPTS_AFTER_REUPLOAD = {
    'home': "Still paying or signing up just to convert one file? Watch this. KuickKonvert does it all. Word, Excel and PowerPoint to and from PDF. Turn iPhone HEIC and web WEBP photos into JPG. Merge, split, compress, rotate, watermark or password-protect your PDFs. Twenty-one tools, right in your browser. All free, no sign-up, and every file is deleted. kuickkonvert.com.",
    'word-to-pdf': "Ever sent a Word file and the layout fell apart on their screen? Convert it to PDF first. Do it free at kuickkonvert.com. Nothing to install, and your file's deleted after [conversion].",
    'ppt-to-pdf': "Need to share a slide deck with someone who doesn't have PowerPoint? Turn it into a PDF. Your slides open on any phone or laptop, no app needed. Free at kuickkonvert.com. Your file's deleted after [conversion].",
    'png-to-pdf': "Got a bunch of PNG screenshots you need to send as one file? Turn your PNGs into a single clean PDF. Free at kuickkonvert.com. [Files] deleted after [conversion].",
    'png-to-jpg': "Your PNG too heavy to email or upload? Convert it to JPG. Free at kuickkonvert.com. [Files] deleted after [conversion].",
    'jpg-to-png': "App or website only accepting PNG files? Convert your JPG to a clean, lossless PNG, ready to upload. Free at kuickkonvert.com. [Files] deleted after [conversion].",
    'merge-pdf': "Trying to send five separate PDFs in one email? Merge them into one file. Add them in the order you want. Free at kuickkonvert.com. Files deleted after [conversion].",
    'rotate-pdf': "Scanned a document and it came out sideways? Rotate it the right way up. Free at kuickkonvert.com. [Files] deleted after [conversion].",
}

# 12 Nov 2026: the 8 corrected videos were uploaded (new IDs above), so their
# transcripts now match the embedded videos and are switched on. Drafts from
# offline recognition: Shahid is vetting them by ear (vetting sheet in
# Downloads\KuickKonvert video vetting 12112026).
VIDEO_TRANSCRIPTS.update(VIDEO_TRANSCRIPTS_AFTER_REUPLOAD)
VIDEO_TRANSCRIPTS_AFTER_REUPLOAD = {}

for _k, _t in VIDEO_TRANSCRIPTS.items():
    VIDEOS[_k]["transcript"] = _t



# ---- AdSense script (R7-66) withdrawn, 12 Nov 2026 -------------------------
# Shahid's decision (12 Nov 2026), after the adviser called loading AdSense
# with no ad inventory "NOT RECOMMENDED": do not load the AdSense script until
# the site is approved. The site stays connected to AdSense through the
# <meta name="google-adsense-account"> tag and /ads.txt, which Google's help
# page "Connect your site to AdSense" lists as alternatives to the code
# snippet (checked 12 Nov 2026). Neither contacts Google from the visitor's
# browser. After approval: set True, update the Privacy Notice first (adviser
# wording), add a certified CMP for the Consent-Controlled Locations if ads
# are to be shown there, and re-run the network test.
ADSENSE_SCRIPT_ENABLED = False


# Final legal opinion, 12 Nov 2026 (deployment stages 3-7): Release 7 deploys the
# GPC / Consent Mode controls first; the Consent Mode paragraph of the Privacy
# Notice ("Advertising on this site") is published only after the production
# tests pass (GPC browser, Google Tag Assistant, HAR files). Then set True and
# redeploy. If a live test fails, leave False and keep advertising disabled.
PRIVACY_CONSENT_MODE_DISCLOSURE = False


# ---- R7-82: internal linking for topical authority (Shahid, 13 Nov 2026: yes) ----
# Source: internal linking plan, 13 Nov 2026 (P1). Lists and one anchor only,
# no new URLs and no new sentences. Rules applied:
#   * Every tool keeps the first two items of its "related" list, because
#     main.js shows related[:2] as "You might also need" after a conversion.
#     New links are appended (at most 5 related tools per page).
#   * A pillar guide is added to a tool page only where it is about that
#     tool's task. Excel and PowerPoint tools already show their own format
#     guides (xls-vs-xlsx, ppt-vs-pptx). Rotate, Watermark and Protect show
#     guides on exactly their task, so the compression guide is not forced
#     onto them.
# The anchor change (L1) is in the JPG vs PNG guide text above: "Our PNG to
# JPG converter" (was "PNG to JPG"). L2 (location-data-in-photos) is left
# as it is: its PNG to JPG link sits in a list of four tool names, and
# changing one name would read badly.
R7_82_RELATED_ADD = {
    "pdf-to-png": ["png-to-jpg"],                # L3
    "png-to-pdf": ["png-to-jpg", "jpg-to-png"],  # L4, L10
    "png-to-jpg": ["heic-to-jpg"],               # L5 (jpg-to-png, png-to-pdf, webp-to-jpg already, in that order)
    "pdf-to-jpg": ["rotate-pdf"],                # L7
    "compress-pdf": ["protect-pdf"],             # L9
}
for _slug, _add in R7_82_RELATED_ADD.items():
    _rel = TOOLS_BY_SLUG[_slug]["related"]
    TOOLS_BY_SLUG[_slug]["related"] = _rel + [s for s in _add if s not in _rel]
# L7, L8, L9 on Merge PDF: rotate, protect and watermark are the usual
# "finish the document" steps after merging. They replace PDF to Word,
# which is not a merging task (the Merge FAQ still names Word to PDF).
TOOLS_BY_SLUG["merge-pdf"]["related"] = [
    "split-pdf", "compress-pdf", "rotate-pdf", "protect-pdf", "watermark-pdf"]

# Pillar guides link their cluster tools (shown in the guide's "Related tools")
# and so appear under "Guides for {Tool}" on those tool pages.
R7_82_GUIDE_TOOLS_ADD = {
    "jpg-vs-png": ["heic-to-jpg", "webp-to-jpg"],          # L13 + pillar on 2 tools
    "pdf-compression-levels-explained": ["split-pdf"],     # L14: split a large file before emailing
    "what-is-a-webp-image": ["png-to-jpg"],                # L5: guides on the PNG to JPG page
    # L11: the same "old Office format" problem; DOC to DOCX had only 5 in-links.
    "xls-vs-xlsx": ["doc-to-docx"],
    "ppt-vs-pptx": ["doc-to-docx"],
}
for _gslug, _add in R7_82_GUIDE_TOOLS_ADD.items():
    _g = GUIDES_BY_SLUG[_gslug]
    _g["related_tools"] = _g["related_tools"] + [s for s in _add if s not in _g["related_tools"]]

# Rebuild the tool -> guides index in place (app.py holds a reference to this
# dict) with the cluster pillar guide listed first.
R7_82_PILLAR = {}
for _s in ("png-to-jpg", "jpg-to-png", "heic-to-jpg", "webp-to-jpg",
           "jpg-to-pdf", "png-to-pdf", "pdf-to-jpg", "pdf-to-png"):
    R7_82_PILLAR[_s] = "jpg-vs-png"
for _s in ("doc-to-docx", "word-to-pdf", "pdf-to-word"):
    R7_82_PILLAR[_s] = "docx-vs-doc"
for _s in ("compress-pdf", "merge-pdf", "split-pdf"):
    R7_82_PILLAR[_s] = "pdf-compression-levels-explained"
GUIDES_BY_TOOL.clear()
for _g in GUIDES:
    for _slug in _g.get("related_tools", []):
        GUIDES_BY_TOOL[_slug].append(_g)
for _slug, _pillar in R7_82_PILLAR.items():
    _lst = GUIDES_BY_TOOL[_slug]
    _lst.sort(key=lambda g, p=_pillar: g["slug"] != p)  # stable: pillar first, rest unchanged


# ---- R7-84: guide text gaps from the GSC regex exports (Shahid, 13 Nov 2026: Release 7) ----
# Source: claude/gsc-regex-summary-and-analysis-13112026.md, actions Q1-Q4.
# Each new section answers a question that Search Console shows people
# asking, in words that match our own tests and code. No new numbers except
# the A4 test (Q2), which was run on 13 Nov 2026 with the converter code
# in this build.
def _r7_84_insert(slug, after_heading, section):
    secs = GUIDES_BY_SLUG[slug]["sections"]
    if any(s.get("heading") == section["heading"] for s in secs):
        return
    idx = next(i for i, s in enumerate(secs) if s.get("heading") == after_heading)
    secs.insert(idx + 1, section)


# Q1: "what does compressing a PDF do" (5 query variants) and "is PDF lossless".
_r7_84_insert("pdf-compression-levels-explained", "What actually makes a PDF big", {
    "heading": "What does compressing a PDF do?",
    "paragraphs": [
        "Compressing a PDF makes the file smaller by shrinking the pictures inside it. Our tool lowers the resolution of images that are sharper than the chosen level needs and re-saves photos with JPEG compression. Typed text and vector graphics stay as real, sharp text, and no pages, words or layout are removed.",
        "Because a text-only PDF has no images to shrink, compressing it may not make it smaller. In that case our tool gives you your original file back instead of a bigger one.",
    ],
})
_r7_84_insert("pdf-compression-levels-explained", "Can you compress a PDF without losing quality?", {
    "heading": "Is a PDF lossless?",
    "paragraphs": [
        "A PDF is a container, so it depends on what is inside. Text and vector graphics are stored exactly and never lose quality. Images can be stored losslessly, with Flate compression (the same method PNG uses), or with lossy JPEG compression, depending on how the file was made.",
        "Compressing with our tool re-saves photographic images as JPEG, which is lossy: fine detail is discarded to save space, more at Screen than at Printer. If you need an image-perfect copy, keep the original PDF.",
    ],
})

# Q2: "how to fit excel sheet in a4 size pdf". Verified 13 Nov 2026: the
# converter keeps the paper size saved in the workbook (A4 in, A4 out), with
# and without pictures in the sheet (office.py fix, also R7-84).
_r7_84_insert("excel-to-pdf-fit-on-one-page", "What our tool does automatically", {
    "heading": "Fitting a sheet on one A4 page",
    "paragraphs": [
        "Our tool keeps the paper size saved in your workbook. To get A4 pages, choose Page Layout > Size > A4 in Excel and save before converting. The columns are then fitted to the width of an A4 page, turned to landscape if the sheet is wide.",
        "In our test (November 2026), a 12-column workbook saved as A4 came out on A4 pages, both with and without a picture in the sheet. A workbook with no paper size saved came out as US Letter, so set A4 yourself if you need it.",
        "Fitting works on the width. A long sheet still continues onto further A4 pages; to keep it to a single page, reduce the rows, for example with a print area.",
    ],
})

# Q3: "pdf to excel without losing formatting" -- answered honestly
# (converters/tables.py writes values as text and copies no styles).
_r7_84_insert("pdf-to-excel-table-conversion-results", "Scanned PDFs need OCR first", {
    "heading": "Can you convert PDF to Excel without losing formatting?",
    "paragraphs": [
        "Not fully. Our tool brings across the content: the text and numbers of each table in their rows and columns, with the text found around the table. It does not copy the look. Fonts, bold, colours, cell borders and merged cells are not carried over, every value arrives as text, and the tool sets the column widths.",
        "Plan to reapply number formats, styling and any formulas in Excel after converting. If you need the original formatting, ask for the spreadsheet the PDF was made from.",
    ],
})
GUIDES_BY_SLUG["pdf-to-excel-table-conversion-results"]["updated"] = RELEASE7_DATE
RELEASE7_UPDATED_GUIDES = RELEASE7_UPDATED_GUIDES + ("pdf-to-excel-table-conversion-results",)

# Q4: "what is a pptx file" (low priority).
_r7_84_insert("ppt-vs-pptx", "Is PPT the same as PPTX?", {
    "heading": "What is a PPTX file?",
    "paragraphs": [
        "A PPTX file is a PowerPoint presentation saved in the Office Open XML format, PowerPoint's default since PowerPoint 2007. Inside, it is a ZIP archive of XML files plus the pictures and other media used on the slides, which is one reason it was the smaller file in our test. It opens in current PowerPoint and in most other presentation programs.",
    ],
})

# ---- R7-86: PDF to Word guide, three new sections (Shahid, 15 Nov 2026: Release 7) ----
# From the Ahrefs AI Content Helper review of this guide (document 258083,
# keyword "how to convert PDF to Word without losing formatting"; content
# score 53 -> 78 with this text). Weak topics were choosing a method, source
# file preparation and preserving formatting. Every statement comes from this
# guide's own October 2026 test, the PDF to Word tool page, the converter's
# messages (converters/pdf_tools.py: password, split hint) or the two help
# pages listed in "sources" (both checked 15 Nov 2026). No competitor names,
# no OCR claim, no promise that formatting is always kept.
# The old last section "Getting the best result from a text-based PDF" is
# replaced: its two points (simple layouts; password; deletion) are carried
# into the new sections, and "best" leaves the heading.
_r7_86_g = GUIDES_BY_SLUG["pdf-to-word-text-vs-scanned"]
_r7_86_g["sections"] = [s for s in _r7_86_g["sections"]
                        if s.get("heading") != "Getting the best result from a text-based PDF"]
_r7_84_insert("pdf-to-word-text-vs-scanned", "What we measured", {
    "heading": "Which method to use",
    "paragraphs": [
        "There are three common ways to turn a PDF into a Word document. Which one suits you depends on what kind of PDF you have and where you're happy for the file to go.",
        "An online converter, such as our [[pdf-to-word|PDF to Word tool]], needs no software and no account, and works in a phone or computer browser. It suits text-based PDFs up to 50 MB. Your upload and the Word file are deleted from our server as soon as your download is ready.",
        "Microsoft Word can also open a PDF itself. According to Microsoft's help page, go to File > Open and choose the PDF: Word makes a copy and converts it, and the original PDF isn't changed. Microsoft says this suits PDFs that are mostly text, and warns that lines and pages may break in different places from the original. Because the file stays on your computer, it's a sensible choice for confidential documents if you have Word installed.",
        "For a scanned PDF you need OCR, which turns the picture of the text back into letters. Our tool doesn't do OCR, so a scan comes out as a picture (see our test above). Google Docs can do it for free, as described in the next section.",
    ],
})
_r7_84_insert("pdf-to-word-text-vs-scanned", "What to do with a scanned PDF", {
    "heading": "Before you convert: prepare the PDF",
    "paragraphs": [
        "Check that it has real text. Use the highlight or Ctrl+F test above. If it's a scan, our tool will give you a picture, not editable text.",
        "Remove the password. Our tool can't open a password-protected PDF. Open it in your PDF reader with its password, save or print a copy without one, and upload that copy.",
        "Use the original export where you can. A PDF saved directly from Word or another program converts much more cleanly than one that has been printed and scanned. If someone sent you the PDF, ask whether they still have the Word file.",
        "Split very long files. Long PDFs, and pages packed with ruled table cells such as bank statements, take much longer to convert. If our tool says a file is too long, split it with [[split-pdf|Split PDF]] and convert it in parts.",
        "Keep it under 50 MB. If it's larger, [[compress-pdf|Compress PDF]] may bring it down. Text stays text when a PDF is compressed, but zoom in afterwards to check that small print in any images is still readable.",
    ],
})
_r7_84_insert("pdf-to-word-text-vs-scanned", "Before you convert: prepare the PDF", {
    "heading": "Keeping the formatting: what carries over to Word",
    "paragraphs": [
        "No converter can promise to turn every PDF into Word without losing formatting, because a PDF stores where things sit on the page, not how the document was built. The converter has to rebuild paragraphs, tables and lists from those positions.",
        "Simple layouts such as letters, contracts and reports come through most cleanly. In our test, the text-based PDF became editable Word text with a real Word table: 140 words, and the rent table's cells could be edited.",
        "Some things need a little work afterwards. Bulleted and numbered lists come through as plain lines of text rather than a live Word list, so you may need to reapply the list formatting. Multi-column layouts, text placed over images and heavily designed pages can need tidying in Word.",
        "Before you rely on the Word file, compare it with the PDF: check the number of pages, every table, any lists, and the headers and footers. Fix anything that has moved before you send or print it.",
    ],
})
_r7_86_g["sources"] = [
    ("Microsoft Support: Edit a PDF (open a PDF in Word)", "https://support.microsoft.com/en-gb/word/training/edit-a-pdf"),
    ("Google Drive Help: Convert PDF and photo files to text", "https://support.google.com/drive/answer/176692?hl=en"),
]
_r7_86_g["updated"] = RELEASE7_DATE
RELEASE7_UPDATED_GUIDES = RELEASE7_UPDATED_GUIDES + ("pdf-to-word-text-vs-scanned",)


# ===========================================================================
# Release 7 final fix (19 Nov 2026): items approved 15-16 Nov 2026 for the
# 19 Nov build. R7-83 videos, R7-87 + spec section 9, R7-88, R7-89, R7-92
# (internal linking P2: L12, L14, L15, L16 and 10 dek links).
# Spec: claude/r7-87-keyword-placement-spec-15112026.md (project notes).
# ===========================================================================

def _r7f_faq_replace(slug, old_q, new_q, new_a=None):
    faq = list(TOOLS_BY_SLUG[slug]["faq"])
    idx = [i for i, (q, a) in enumerate(faq) if q == old_q]
    assert len(idx) == 1, (slug, old_q)
    q, a = faq[idx[0]]
    faq[idx[0]] = (new_q, a if new_a is None else new_a)
    TOOLS_BY_SLUG[slug]["faq"] = faq


def _r7f_faq_add(slug, q, a):
    TOOLS_BY_SLUG[slug]["faq"] = list(TOOLS_BY_SLUG[slug]["faq"]) + [(q, a)]


# ---- R7-87 section 1 + section 9: PNG to JPG (title stays frozen) ----------
_t = TOOLS_BY_SLUG["png-to-jpg"]
_t["meta_description"] = "Convert PNG to JPG online for free, up to 20 images at once. Photos usually get much smaller; transparent areas turn white. No sign-up."
_t["intro"] = "Convert PNG to JPG (JPEG) online for free. JPG is the most widely accepted image format, and usually a much smaller file when the picture is a photo. Change one PNG or up to 20 at a time."
_t["how_to_heading"] = "How to convert PNG to JPG"
_t["h1"] = "PNG to JPG - Convert PNG Images to JPG"
_r7f_faq_replace("png-to-jpg", "Is there any quality loss?",
                 "Can I convert PNG to JPG without losing quality?",
                 "Almost, on photos: images are saved at quality 90, where the difference is hard to see. Sharp text and thin lines can look slightly softer, as with any JPG.")

# ---- R7-87 section 2: Protect PDF (title + H1 exception approved) ----------
_t = TOOLS_BY_SLUG["protect-pdf"]
_t["seo_title"] = "Password Protect PDF Online Free - Lock PDF | KuickKonvert"
_t["h1"] = "Password Protect PDF - Lock PDF Files with a Password"
_t["meta_description"] = "Password protect a PDF online free: lock it with a password and 256-bit AES encryption so only people who know it can open it. No sign-up or install."
_t["intro"] = "Password protect a PDF online for free: Protect PDF locks the file with a password you choose and encrypts it with 256-bit AES, so only someone who has the password can open it -- useful before emailing a document with sensitive information."
_r7f_faq_replace("protect-pdf", "What encryption does this use?",
                 "How does Protect PDF encrypt the PDF?",
                 "With 256-bit AES encryption, applied with the password you choose. This is the method the current PDF standard (PDF 2.0) specifies for password-protected PDFs, and Adobe Acrobat and Reader have supported it since version 9.")

# ---- R7-87 section 3: Compress PDF FAQ (figures from the compression guide) -
_r7f_faq_replace("compress-pdf", "Can I compress a PDF to 1MB or a few hundred KB?",
                 "Can I compress a PDF to 100 KB, 200 KB, 500 KB or 1 MB?",
                 "There's no exact-size setting, so we can't promise 100 KB, 200 KB, 500 KB, 1 MB or any other size -- the result depends on what's inside your PDF. For the biggest reduction, choose \"Smallest file (screen quality)\". In our test (September 2026), a 3.2 MB PDF holding one photo came out at 50 KB on Screen and 127 KB on Ebook, and a 93 KB one-page scan came out at 24 KB on Screen -- but a text-only PDF didn't get smaller at all. If your PDF was made from phone photos, Compress PDF may not shrink it at all -- resize the photos before converting them (our guide on putting photos into one PDF shows how). Check the result's size before uploading it to a form with a limit.")

# ---- R7-87 section 4: Merge PDF ("join pdf") --------------------------------
_t = TOOLS_BY_SLUG["merge-pdf"]
_t["intro"] = "Merge PDF combines multiple PDF files into a single document, in the order you add them. It's a free online PDF merger that can also join PDF files such as separate sections of a report or scanned pages into one file."
_t["meta_description"] = "Merge PDF files free online: combine or join PDFs into one file, in the order you add them. No sign-up, no installation and no watermark on the merged PDF."

# ---- R7-87 section 5: PDF to PPT ("pdf to pptx"); output is .pptx -----------
_t = TOOLS_BY_SLUG["pdf-to-ppt"]
_t["h1"] = "PDF to PPT Converter - PDF to PowerPoint (PPTX)"
_t["intro"] = "PDF to PPT turns each page of a PDF into a slide in a PowerPoint (PPTX) file, keeping each page exactly as it looks in the PDF."
_t["meta_description"] = "Convert PDF to PowerPoint online for free: PDF to PPTX, with each PDF page as a slide and the layout kept exactly. No sign-up or install."
_r7f_faq_add("pdf-to-ppt", "Is this PDF to PPTX or PDF to PPT?",
             "PDF to PPTX: you get a .pptx file, the PowerPoint format used since PowerPoint 2007. It also opens in Google Slides, Keynote and LibreOffice Impress. If you need the older .ppt format, open the file in PowerPoint and use Save As.")

# ---- R7-87 section 6: Split PDF ("separate pdf pages") ----------------------
_t = TOOLS_BY_SLUG["split-pdf"]
_t["h1"] = "Split PDF - Separate PDF Pages into Single Files"
_t["intro"] = "Split PDF is a free online PDF splitter: it separates PDF pages into individual files, saving every page as its own single-page PDF, delivered as a ZIP -- useful when you only need to send someone one page out of a longer document."
_r7f_faq_add("split-pdf", "How do I separate PDF pages into separate files?",
             "Upload the PDF and press Convert: every page is saved as its own single-page PDF, and all of them download together in one ZIP file. Open the ZIP and keep the pages you need.")

# ---- R7-87 section 7: PDF to Excel ("pdf to xlsx") --------------------------
_t = TOOLS_BY_SLUG["pdf-to-excel"]
_t["h1"] = "PDF to Excel Converter - PDF to XLSX"
_t["intro"] = "PDF to Excel (PDF to XLSX) extracts tables from a PDF and rebuilds them as an editable XLSX file, so you can sort, filter, or recalculate data that arrived as a static document."

# ---- R7-87 section 8 + section 9: "JPG (JPEG)" once per image intro ---------
TOOLS_BY_SLUG["heic-to-jpg"]["intro"] = "HEIC to JPG is a free HEIC converter: it turns the HEIC photos taken by iPhones and iPads into ordinary JPG (JPEG) files that open on any computer, phone or website. Convert one photo or up to 20 at a time -- several photos come back together in one ZIP file."
TOOLS_BY_SLUG["webp-to-jpg"]["intro"] = "WEBP to JPG turns WEBP images -- the format many websites now use for their pictures -- into ordinary JPG (JPEG) files that open in any photo viewer or editor and upload anywhere. Convert one image or up to 20 at a time."
TOOLS_BY_SLUG["pdf-to-jpg"]["intro"] = "PDF to JPG turns every page of a PDF into its own JPG (JPEG) image, useful when you need to drop a page into a slide, a website, or a chat message rather than share the whole PDF."
TOOLS_BY_SLUG["jpg-to-pdf"]["intro"] = "Convert images to PDF online for free: turn a single JPG (JPEG) photo into a PDF, or merge JPG to PDF to combine several photos into one file. It's a quick way to turn pictures of documents, receipts, or whiteboards into one shareable PDF -- and PNG images work too."

# ---- R7-88: "converted on our server" unmistakable --------------------------
_r7f_faq_replace("webp-to-jpg", "Do I need special software to open WEBP files as JPG?",
                 "Do I need special software to open WEBP files as JPG?",
                 "No -- you use it from your browser on Windows, Mac, Android or iPhone. Upload your WEBP images, they're converted on our server, and you download the JPGs. There's no sign-up.")
_g = GUIDES_BY_SLUG["how-to-split-pdf-files"]
_hits = [s for s in _g["sections"] if s.get("heading") == "Split a PDF in your browser"]
assert len(_hits) == 1
_hits[0]["heading"] = "Split a PDF online, in any browser"

# ---- R7-89: form-size limits in the photos-to-one-PDF guide -----------------
# Measured 15 Nov 2026 with KuickKonvert's own converter (photo 1920 x 3413);
# readability checked on a phone photo of a printed A4 form (15 Nov 2026).
_r7_84_insert("photos-to-one-pdf-jpg-to-pdf-tips", "The reliable fix: resize the photos first", {
    "heading": "Meeting a form's size limit (100 KB, 200 KB or 500 KB)",
    "paragraphs": [
        "If a form sets a limit such as 100 KB, 200 KB or 500 KB, the photo's pixel size decides the result. In our test (November 2026) with a real phone photo, resized copies saved as JPG came to:",
    ],
    "table": {
        "caption": "One phone photo, resized and saved as JPG (our test, November 2026)",
        "headers": ["Long side", "JPG quality", "Photo / one-page PDF"],
        "rows": [
            ["1,600 px", "85", "253 KB / 254 KB"],
            ["1,200 px", "80", "134 KB / 135 KB"],
            ["1,000 px", "75", "87 KB / 89 KB"],
            ["800 px", "70", "55 KB / 56 KB"],
        ],
        "note": "Combine them with JPG to PDF: a one-page PDF is about 1 KB larger than the photo, and three pages at 1,200 pixels came to 404 KB. In our test with a phone photo of a printed A4 form, normal-size text was still readable at 1,000 pixels; at 800 pixels it was only just readable and small print was hard to read. Check every page before you submit.",
    },
})

# ---- R7-92 (internal linking P2) --------------------------------------------
# L15: pillar guides first in the home "Guides" block (used in app.py index()).
HOME_PILLAR_GUIDES = ("docx-vs-doc", "jpg-vs-png", "pdf-compression-levels-explained")

# L12: docx-vs-doc links the other Office tools and the sibling format guides.
_r7_84_insert("docx-vs-doc", "Switching a file between DOC and DOCX", {
    "heading": "Converting other Office files",
    "paragraphs": [
        "The same old-versus-new format question applies to Excel (XLS and XLSX) and PowerPoint (PPT and PPTX). Our guides [[guide:xls-vs-xlsx|XLS vs XLSX]] and [[guide:ppt-vs-pptx|PPT vs PPTX]] explain the differences.",
        "For spreadsheets, [[excel-to-pdf|Excel to PDF]] accepts both XLS and XLSX, and [[pdf-to-excel|PDF to Excel]] turns tables in a PDF into an XLSX file. For presentations, [[ppt-to-pdf|PowerPoint to PDF]] accepts both PPT and PPTX, and [[pdf-to-ppt|PDF to PowerPoint]] turns each PDF page into a slide in a PPTX file.",
    ],
})

# L14: the compression pillar links the rest of the PDF tools cluster (body
# text only, so the guide is not added to those tools' "Guides for" lists).
_g = GUIDES_BY_SLUG["pdf-compression-levels-explained"]
_g["sections"] = list(_g["sections"]) + [{
    "heading": "Other PDF tools",
    "paragraphs": [
        "Compress PDF is one of six free PDF tools on KuickKonvert. To combine files or take pages out, use [[merge-pdf|Merge PDF]] or [[split-pdf|Split PDF]]; to turn sideways pages, use [[rotate-pdf|Rotate PDF]]; and to label or lock the finished file, use [[watermark-pdf|Watermark PDF]] or [[protect-pdf|Protect PDF]].",
    ],
}]

# Dek tool links on the 10 guides that had none.
_R7_92_DEK_LINKS = {
    "merge-pdf-in-the-right-order": " To combine your files, use our [[merge-pdf|Merge PDF tool]].",
    "pdf-password-protection-explained": " To add a password to a PDF, use our [[protect-pdf|Protect PDF tool]].",
    "pdf-to-excel-table-conversion-results": " To try it on your own file, use our [[pdf-to-excel|PDF to Excel converter]].",
    "photos-to-one-pdf-jpg-to-pdf-tips": " To combine your photos, use our [[jpg-to-pdf|JPG to PDF converter]].",
    "pdf-to-word-text-vs-scanned": " To convert a text-based PDF, use our [[pdf-to-word|PDF to Word converter]].",
    "watermark-pdf-what-it-protects": " To add one, use our [[watermark-pdf|Watermark PDF tool]].",
    "split-and-rotate-pdf-pages": " To try them, use our [[split-pdf|Split PDF]] and [[rotate-pdf|Rotate PDF]] tools.",
    "location-data-in-photos": " For iPhone photos, our [[heic-to-jpg|HEIC to JPG converter]] removes the GPS location as it converts.",
    "submitting-coursework-as-a-pdf": " For a Word file, start with our [[word-to-pdf|Word to PDF converter]].",
    "what-happens-to-your-file": " The same steps apply to every tool, for example our [[pdf-to-word|PDF to Word converter]].",
}
for _s, _extra in _R7_92_DEK_LINKS.items():
    assert "[[" not in GUIDES_BY_SLUG[_s]["dek"], _s
    GUIDES_BY_SLUG[_s]["dek"] = GUIDES_BY_SLUG[_s]["dek"] + _extra

# Guides whose body changed in this fix carry the release date.
for _s in ("photos-to-one-pdf-jpg-to-pdf-tips", "docx-vs-doc", "pdf-compression-levels-explained"):
    GUIDES_BY_SLUG[_s]["updated"] = RELEASE7_DATE
    if _s not in RELEASE7_UPDATED_GUIDES:
        RELEASE7_UPDATED_GUIDES = RELEASE7_UPDATED_GUIDES + (_s,)

# ---- R7-83: new-voice professional videos (uploaded 13 Nov 2026) ------------
# IDs from claude/youtube-new-voice-links-13112026.md. Lengths and upload
# times read from YouTube (video details, 19 Nov 2026). Transcripts = the
# round-2 spoken text in claude/professional-videos-new-voice-13112026.md.
# Thumbnails (static/img/video/) are unchanged: same opening frames.
_R7_83 = {
    # key: (id, seconds, uploaded, transcript)
    "home": ("p8tYDhRRQHc", 29, "2026-11-13T06:54:34-08:00", "Still paying or signing up just to convert one file? Watch this. KuickKonvert does it all. Word, Excel and PowerPoint to and from PDF. Turn iPhone HEIC and WEBP photos into JPG. Merge, split, compress, rotate, watermark or password-protect your PDFs. Twenty-one tools, right in your browser. All free, no sign-up. Files deleted after conversion. kuickkonvert.com."),
    "word-to-pdf": ("4Y2JCxaA9T8", 14, "2026-11-13T06:54:33-08:00", "Ever sent a Word file and the layout fell apart on their screen? Convert it to PDF first. Do it free at kuickkonvert.com. Free, no sign-up. Nothing to install. Files deleted after conversion."),
    "pdf-to-word": ("UqK4o4H9yT8", 15, "2026-11-13T06:54:33-08:00", "Got a PDF you need to edit, but no original file? Turn it back into an editable Word document. Fix the text, change a number, and you're done. Free at kuickkonvert.com. Free, no sign-up. Files deleted after conversion."),
    "excel-to-pdf": ("BwiQh7pkv6w", 16, "2026-11-13T06:54:33-08:00", "Sending an Excel sheet that spills onto six messy pages? Convert it to a clean PDF that holds its layout. Easy to read, easy to share, opens for everyone. Free at kuickkonvert.com. No sign-up. Files deleted after conversion."),
    "pdf-to-excel": ("r8VSFnV1rMs", 17, "2026-11-13T06:54:33-08:00", "Someone sent the report as a PDF, and now you need those numbers in Excel. Convert the PDF to Excel and get your tables back as rows and columns you can actually work with. Free at kuickkonvert.com. No sign-up. Files deleted after conversion."),
    "ppt-to-pdf": ("08v4gGONweo", 15, "2026-11-13T06:54:33-08:00", "Need to share a slide deck with someone who doesn't have PowerPoint? Turn it into a PDF. Your slides open on any phone or laptop, no app needed. Free at kuickkonvert.com. No sign-up. Files deleted after conversion."),
    "pdf-to-ppt": ("PZ9rf1UKdq8", 12, "2026-11-13T06:54:33-08:00", "Only have the slides as a PDF? Convert the PDF back into PowerPoint slides, free at kuickkonvert.com. No sign-up. Files deleted after conversion."),
    "jpg-to-pdf": ("1nxYETXA35Y", 15, "2026-11-13T06:54:33-08:00", "Upload form wants one PDF, but you've got a pile of photos? Drop your JPGs in, put them in order, and get one neat PDF, free at kuickkonvert.com. No sign-up. Files deleted after conversion."),
    "png-to-pdf": ("M6R_SikPg0c", 14, "2026-11-13T06:17:18-08:00", "Got a bunch of PNG screenshots you need to send as one file? Turn your PNGs into a single clean PDF. Free at kuickkonvert.com. No sign-up. Files deleted after conversion."),
    "pdf-to-jpg": ("KWbp5uIROk8", 15, "2026-11-13T06:54:33-08:00", "Want to grab an image or a page out of a PDF? Convert the PDF to JPG and get each page as an image you can post, send or save, free at kuickkonvert.com. No sign-up. Files deleted after conversion."),
    "pdf-to-png": ("kFygV7CKyy0", 15, "2026-11-13T06:54:33-08:00", "Need sharp, high-quality images out of a PDF? Convert it to PNG. Crisp edges, perfect for pages with text or logos. Free at kuickkonvert.com. No sign-up. Files deleted after conversion."),
    "heic-to-jpg": ("_6PwJwiU3Ic", 21, "2026-11-13T06:54:33-08:00", "Sent an iPhone photo and it just won't open on their computer? That's HEIC. Convert it to JPG and it opens anywhere. And we strip the hidden GPS location from your photo while we're at it. Free at kuickkonvert.com. No sign-up. Up to 20 at once. Files deleted after conversion."),
    "webp-to-jpg": ("pSxJcICw1qY", 16, "2026-11-13T06:54:33-08:00", "Saved a picture from a website and now nothing will open it? It's a WEBP. Convert it to JPG, the normal format every app and device understands. Free at kuickkonvert.com. No sign-up. Files deleted after conversion."),
    "png-to-jpg": ("e4lbRyCLLuA", 11, "2026-11-13T06:54:33-08:00", "Your PNG too heavy to email or upload? Convert it to JPG. Free at kuickkonvert.com. No sign-up. Files deleted after conversion."),
    "jpg-to-png": ("IHPBh06crNk", 15, "2026-11-13T06:54:33-08:00", "App or website only accepting PNG files? Convert your JPG to a clean, lossless PNG, ready to upload. Free at kuickkonvert.com. No sign-up. Up to 20 at once. Files deleted after conversion."),
    "merge-pdf": ("hzr82e6NkqY", 14, "2026-11-13T06:54:33-08:00", "Trying to send five separate PDFs in one email? Merge them into one file. Add them in the order you want. Free at kuickkonvert.com. No sign-up. Files deleted after conversion."),
    "split-pdf": ("I2xbhWO4xMI", 15, "2026-11-13T06:54:34-08:00", "Only need one page out of a big PDF? Split it, and every page becomes its own PDF. Keep the one you need, leave the rest behind. Free at kuickkonvert.com. No sign-up. Files deleted after conversion."),
    "compress-pdf": ("InIhMZl77y0", 14, "2026-11-13T06:54:33-08:00", "That annoying \"file too large\" message again? Compress your PDF down to a size that actually uploads, without turning it into mush. Free at kuickkonvert.com. No sign-up. Files deleted after conversion."),
    "rotate-pdf": ("-dEMQIAoPuw", 11, "2026-11-13T06:54:33-08:00", "Scanned a document and it came out sideways? Rotate it the right way up. Free at kuickkonvert.com. No sign-up. Files deleted after conversion."),
    "watermark-pdf": ("hvqWtyb8lq8", 15, "2026-11-13T06:58:11-08:00", "Sending out a draft you don't want passed off as final? Stamp a watermark on it: DRAFT, CONFIDENTIAL or your name, on every page. Free at kuickkonvert.com. No sign-up. Files deleted after conversion."),
    "protect-pdf": ("BGB3Ae-KHh0", 17, "2026-11-13T06:54:33-08:00", "About to email a sensitive PDF with no protection? Add a password first. Locked with strong AES-256 encryption, so only the right person can open it. Free at kuickkonvert.com. No sign-up. Files deleted after conversion."),
    "doc-to-docx": ("pljxa5C-ARk", 20, "2026-11-13T06:53:22-08:00", "Got an old Word file that ends in .doc? Upload portals and Google Docs often want DOCX instead. Convert DOC to DOCX free at kuickkonvert.com. Text, headings, tables and pictures carry over. Free, no sign-up. Nothing to install. Files deleted after conversion."),
    # V23: the all-tools video's voice-over is unchanged; its transcript stays.
    "all-tools": ("1E_AUIg4tZk", 129, "2026-11-13T06:56:36-08:00", None),
}


def _r7f_iso(sec):
    m, s = divmod(sec, 60)
    return f"PT{m}M{s}S" if m else f"PT{s}S"


assert set(_R7_83) == set(VIDEOS), set(_R7_83) ^ set(VIDEOS)
for _k, (_id, _sec, _up, _tr) in _R7_83.items():
    VIDEOS[_k]["id"] = _id
    VIDEOS[_k]["seconds"] = _sec
    VIDEOS[_k]["duration"] = _r7f_iso(_sec)
    VIDEOS[_k]["uploaded"] = _up
    if _tr is not None:
        VIDEOS[_k]["transcript"] = _tr
        VIDEO_TRANSCRIPTS[_k] = _tr
