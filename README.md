# KuickKonvert

**Free online file converter — Word, Excel, PowerPoint, images and PDF. No sign-up, and every file is deleted after conversion.**

🔗 **Live site: [kuickkonvert.com](https://kuickkonvert.com)**

---

## What it does

21 free tools:

| Category | Tools |
|---|---|
| Documents (7) | [Word → PDF](https://kuickkonvert.com/tools/word-to-pdf), [PDF → Word](https://kuickkonvert.com/tools/pdf-to-word), [DOC → DOCX](https://kuickkonvert.com/tools/doc-to-docx), [Excel → PDF](https://kuickkonvert.com/tools/excel-to-pdf), [PDF → Excel](https://kuickkonvert.com/tools/pdf-to-excel), [PowerPoint → PDF](https://kuickkonvert.com/tools/ppt-to-pdf), [PDF → PowerPoint](https://kuickkonvert.com/tools/pdf-to-ppt) |
| Images (8) | [JPG → PDF](https://kuickkonvert.com/tools/jpg-to-pdf), [PNG → PDF](https://kuickkonvert.com/tools/png-to-pdf), [PDF → JPG](https://kuickkonvert.com/tools/pdf-to-jpg), [PDF → PNG](https://kuickkonvert.com/tools/pdf-to-png), [HEIC → JPG](https://kuickkonvert.com/tools/heic-to-jpg), [WEBP → JPG](https://kuickkonvert.com/tools/webp-to-jpg), [PNG → JPG](https://kuickkonvert.com/tools/png-to-jpg), [JPG → PNG](https://kuickkonvert.com/tools/jpg-to-png) |
| PDF tools (6) | [Merge](https://kuickkonvert.com/tools/merge-pdf), [Split](https://kuickkonvert.com/tools/split-pdf), [Compress](https://kuickkonvert.com/tools/compress-pdf), [Rotate](https://kuickkonvert.com/tools/rotate-pdf), [Watermark](https://kuickkonvert.com/tools/watermark-pdf), [Password-protect](https://kuickkonvert.com/tools/protect-pdf) |

- **No account, no credit card** — open a tool and convert.
- **Private by design** — each file is processed in a temporary workspace and deleted as soon as the converted file is returned (or immediately if a conversion fails).
- **Works in any modern browser** — desktop or mobile, nothing to install.
- **Free** — up to 50 MB per upload (all files together), and up to 20 images at a time in the image converters.

Files are converted on the server (Render, Singapore region, behind Cloudflare), not in the browser. What happens to an upload, step by step: [What happens to your file](https://kuickkonvert.com/guides/what-happens-to-your-file).

## Guides

Short explainers on common file questions: [kuickkonvert.com/guides](https://kuickkonvert.com/guides)

## Built with

- Python 3.11 and Flask, served by Gunicorn
- LibreOffice (Office ↔ PDF), Poppler (PDF ↔ images), Ghostscript (PDF compression)
- pypdf, pikepdf, pdf2docx (with PyMuPDF), pdfplumber, python-pptx, openpyxl, Pillow, pi-heif, img2pdf
- Plain HTML, CSS and JavaScript on the front end
- Deployed as a Docker container

## Running it locally

Requirements: Python 3.11, plus the system packages LibreOffice and poppler-utils. Ghostscript is optional (without it, compression still works but shrinks files less).

```bash
# system packages (Debian/Ubuntu -- adjust for your OS)
sudo apt-get install libreoffice poppler-utils ghostscript

python3 -m venv venv
source venv/bin/activate
pip install -r requirements-lock.txt   # the exact pinned versions the live site uses

python3 app.py
# open http://localhost:5000
```

## Privacy

Uploaded files are used only to perform the requested conversion, are deleted automatically after conversion, and are never reviewed or used to train any model. Full details: [Privacy notice](https://kuickkonvert.com/privacy).

## Reporting a problem

See [`SECURITY.md`](SECURITY.md).

## Feedback

Found a bug or want a new tool? Open an issue here, or use the [contact page](https://kuickkonvert.com/contact).

## Licence

© 2026 Shahid Iqbal. KuickKonvert is free software: you can use, study, share and modify it under the terms of the **GNU Affero General Public License, version 3 (AGPL-3.0)**, as published by the Free Software Foundation. See the [`LICENSE`](LICENSE) file for the full text.

The complete, corresponding source code for the version running at **[kuickkonvert.com](https://kuickkonvert.com)** is available at **https://github.com/khshahid1970/kuickkonvert**, as required by section 13 of the AGPL.

KuickKonvert uses **PyMuPDF** (via `pdf2docx`), which is distributed under the AGPL-3.0; licensing KuickKonvert under the AGPL-3.0 keeps the project compliant with that dependency.

Third-party programs and packages, with their licences, are listed in [`NOTICE.md`](NOTICE.md). The exact versions of every Python package are pinned in [`requirements-lock.txt`](requirements-lock.txt), which the `Dockerfile` installs.
