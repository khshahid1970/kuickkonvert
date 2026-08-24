# KuickKonvert

Free, no-sign-up file conversion tools: Word/Excel/PowerPoint ⇄ PDF, JPG/PNG ⇄ PDF,
and everyday PDF tools (merge, split, compress, rotate, watermark, protect).

This is the **Core MVP** build agreed for the first release -- it covers the
tools a visitor reaches for first (matching what CloudConvert leads with on
its homepage), out of the full approved feature list in
`File_Conversion_Website_Feature_List_18082026.pdf`. OCR and the AI features
(Chat with PDF, Summarizer, Translate, Question Generator) are intentionally
**not** in this build; see "What's not in this build" below for why and what
to do next.

## What's included

| Category | Tools |
|---|---|
| Documents | Word→PDF, PDF→Word, Excel→PDF, PDF→Excel, PPT→PDF, PDF→PPT |
| Images | JPG→PDF, PNG→PDF, PDF→JPG, PDF→PNG |
| PDF Tools | Merge, Split, Compress, Rotate, Watermark, Protect (password) |

No files are stored. Every upload is processed in an isolated temp folder
that is deleted the instant the response is sent -- see the privacy notice
draft at `/privacy` (source in `templates/privacy.html`) and
`converters/utils.py`.

## Running it locally

Requirements: Python 3.11, and the system packages LibreOffice, poppler-utils
(for `pdftoppm`), and optionally Ghostscript (for best PDF compression --
without it, compression still works but shrinks files less).

```bash
# system packages (Debian/Ubuntu -- adjust for your OS)
sudo apt-get install libreoffice poppler-utils ghostscript

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 app.py
# open http://localhost:5000
```

For production locally: `gunicorn app:app --bind 0.0.0.0:8080`

## Deploying it

**Use the included `Dockerfile`.** LibreOffice, poppler-utils and Ghostscript
are system packages that most "just push my Python code" platforms (Render's
native Python environment, Railway's default Nixpacks build, plain Heroku)
do **not** install for you -- if you deploy from `requirements.txt` alone on
those platforms, every Office/PDF conversion will fail at runtime. Both
Render and Railway support deploying directly from a Dockerfile:

- **Render**: New → Web Service → connect this repo → Render auto-detects
  the `Dockerfile` → set instance size (LibreOffice needs at least 512 MB
  RAM, 1 GB is safer) → deploy.
- **Railway**: New Project → Deploy from repo → Railway auto-detects the
  `Dockerfile` → deploy.

Either way you get a free HTTPS URL automatically. Point your domain's DNS
at it afterwards (see below) and both platforms issue a matching SSL
certificate automatically.

Environment variables you can set (all optional, sensible defaults built in):

| Variable | Default | Purpose |
|---|---|---|
| `PORT` | `8080` (Docker) / `5000` (local) | Port Flask/gunicorn listens on |
| `MAX_CONTENT_LENGTH_MB` | `50` | Reject uploads larger than this |
| `CONVERT_TIMEOUT_SECONDS` | `120` | Kill a stuck LibreOffice conversion |

## Buying the domain

1. Register `kuickkonvert.com` (or your preferred TLD) via any registrar
   (Namecheap, GoDaddy, Google Domains successor Squarespace, etc.) --
   budget roughly US$10-15/year.
2. Point the domain's DNS at whichever host you deployed to (Render/Railway
   both give you a CNAME/A-record target in their dashboard).
3. SSL is issued automatically by both platforms once DNS resolves -- no
   separate certificate purchase needed.

## What's not in this build (and why)

Left out of this first release deliberately, per the feasibility notes in
`File_Conversion_Website_Feature_List_18082026.pdf`:

- **OCR (PDF OCR, Image to Text)** -- needs a Tesseract-based pipeline and
  more testing on scan quality; natural next tool to add.
- **AI features** (Chat with PDF, Summarizer, Question Generator, Translate)
  -- each call to an AI API costs money per use and raises a data-privacy
  question (client documents leaving the server to a third-party API).
  Recommend building these last, and restricting them to non-confidential
  document types unless a private/self-hosted model is used.
- **Redact PDF** -- must genuinely strip the underlying data, not just draw
  a box over it, or it's a false sense of security for sensitive client
  files. Needs careful, tested implementation before it ships.
- **Sign PDF** -- a *visual* signature stamp is straightforward; a
  legally-binding e-signature is a separate feature requiring PKI/
  certificate infrastructure and compliance review.
- Remaining Tier 2 PDF tools not yet wired up: Crop, Flatten, Add/Remove
  Pages, Extract Pages, Number Pages, Organize, Edit (annotate), Scan to
  PDF, Repair, Compare, PDF/A, plus the remaining document formats (HTML→PDF,
  TXT/RTF/ODT/EPUB/CSV↔PDF, BMP/TIFF/GIF/WebP↔image). The architecture
  (`converters/` modules + the `TOOLS` list in `config.py`) is built so each
  of these is a small, additive change -- add one entry to `config.py`, one
  handler function in `app.py`, and (if it's a new conversion, not a
  variation on an existing one) one function in the matching `converters/*.py`
  file.
- Video/Audio conversion and HEIC were explicitly excluded from scope in the
  approved feature list.

## Before a public launch -- please review

- **Privacy notice** (`/privacy`, source in `templates/privacy.html`): drafted
  to match the "delete immediately, don't retain" architecture actually
  built. Replace the bracketed contact-details placeholder, and confirm the
  Pakistan data-protection law reference is still current with legal counsel
  before publishing -- law here was still moving through the legislative
  process as of the last check (18 Aug 2026).
- **Branding**: the color palette is finalized -- "Deep Indigo & Gold"
  (`--color-primary: #2A2E7F`, `--color-accent: #D4A72C`, full set at the top
  of `static/css/style.css`). The wordmark is still a plain text "KK" mark;
  swap in a real logo file when one is ready, no layout changes needed.
- **File size limit**: defaults to 50 MB per upload (`MAX_CONTENT_LENGTH_MB`).
  Raise it if you expect larger bank-statement PDFs or scanned documents, but
  test conversion time first -- LibreOffice conversions of very large files
  can be slow.
- **Malware scanning**: not included. If this becomes public-facing at scale,
  add a virus-scan step (e.g. ClamAV) before processing uploads, per the
  roadmap document's security-basics checklist.

## Project structure

```
app.py                 Flask routes + per-tool request handlers
config.py               TOOLS catalogue (single source of truth for the UI + routing)
converters/
  office.py              Word/Excel/PPT <-> PDF (LibreOffice headless)
  images.py               JPG/PNG <-> PDF
  pdf_tools.py             Merge/split/compress/rotate/watermark/protect
  utils.py                  Temp workspace (auto-delete) + filename helpers
templates/               Jinja2 pages (homepage tool grid, per-tool page, privacy, errors)
static/                  CSS + vanilla JS (drag-drop upload, progress, download)
Dockerfile              Production image with LibreOffice/poppler/Ghostscript baked in
Procfile                For platforms that run gunicorn directly (Docker CMD takes priority)
```

## Adding a new tool later

1. Add an entry to `TOOLS` in `config.py` (slug, name, category, description,
   accepted extensions, whether it takes multiple files, any extra form
   fields).
2. Write (or reuse) a conversion function in the right `converters/*.py`
   module -- raise `converters.office.ConversionError` with a user-facing
   message on any failure.
3. Add a handler function in `app.py` and register it in the `HANDLERS` dict
   under the same slug.

No template or routing changes needed -- the homepage grid, tool page, and
`/convert/<slug>` dispatcher all read from that one list.
