# KuickKonvert

**Free online file converter — Word, Excel, PowerPoint, images and PDF. No sign-up, and every file is deleted after conversion.**

🔗 **Live site: [kuickkonvert.com](https://kuickkonvert.com)**

---

## What it does

| Category | Tools |
|---|---|
| Documents | Word → PDF, PDF → Word, Excel → PDF, PDF → Excel, PowerPoint → PDF, PDF → PowerPoint |
| Images | JPG → PDF, PNG → PDF, PDF → JPG, PDF → PNG |
| PDF tools | Merge, Split, Compress, Rotate, Watermark, Password-protect |

- **No account, no credit card** — open a tool and convert.
- **Private by design** — each file is processed in a temporary workspace and deleted as soon as the converted file is returned (or immediately if a conversion fails).
- **Works in any modern browser** — desktop or mobile, nothing to install.
- **Free** — the only limit is a 50 MB upload size per conversion.

## Guides

Short explainers on common file questions: [kuickkonvert.com/guides](https://kuickkonvert.com/guides)

## Built with

- Python 3.11 and Flask, served by Gunicorn
- LibreOffice (Office ↔ PDF), Poppler (PDF ↔ images), Ghostscript (PDF compression)
- pypdf, pikepdf, pdf2docx, pdfplumber, python-pptx, openpyxl, Pillow, img2pdf
- Plain HTML, CSS and JavaScript on the front end
- Deployed as a Docker container

## Running it locally

Requirements: Python 3.11, plus the system packages LibreOffice and poppler-utils. Ghostscript is optional (without it, compression still works but shrinks files less).

```bash
# system packages (Debian/Ubuntu -- adjust for your OS)
sudo apt-get install libreoffice poppler-utils ghostscript

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 app.py
# open http://localhost:5000
```

## Privacy

Uploaded files are used only to perform the requested conversion and are never stored, reviewed, or used to train any model. Full details: [Privacy notice](https://kuickkonvert.com/privacy).

## Feedback

Found a bug or want a new tool? Open an issue here, or use the [contact page](https://kuickkonvert.com/contact).

## Copyright

© 2026 Shahid Iqbal. All rights reserved. The source code is published for transparency; no licence is granted to copy, modify or redistribute it.
