# NOTICE: third-party components

KuickKonvert's own source code is licensed under the **GNU Affero General Public License, version 3 (AGPL-3.0)**; see [`LICENSE`](LICENSE). The live site at https://kuickkonvert.com runs this code together with the unmodified third-party programs and packages listed below. Each one remains under its own licence and copyright, and keeps its own licence text.

This list is for information. The licence names are as each package declares them in its own metadata. The licence files and headers shipped with each component are authoritative, and listing a component here does not grant any licence to it.

Last checked: 24 Oct 2026 (Package 2).

## 1. System programs (installed in the Docker image from Debian packages)

Versions come from the Debian release used by the `python:3.11-slim` base image at build time; see the `Dockerfile`.

| Component | Debian package | Used for | Licence |
|---|---|---|---|
| LibreOffice | `libreoffice` | Word, Excel and PowerPoint to PDF; DOC to DOCX; part of PDF to Word | MPL-2.0 |
| Ghostscript | `ghostscript` | Compress PDF | AGPL-3.0 |
| Poppler (pdftoppm and other utilities) | `poppler-utils` | Turning PDF pages into images: PDF to JPG, PDF to PNG and PDF to PPT (via pdf2image) | GPL (GPL-2.0 or GPL-3.0) |
| DejaVu fonts | `fonts-dejavu` | Default fonts | Bitstream Vera Fonts licence (with public-domain changes) |
| Carlito | `fonts-crosextra-carlito` | Replaces Calibri | SIL Open Font License 1.1 |
| Caladea | `fonts-crosextra-caladea` | Replaces Cambria | Apache-2.0 |
| Liberation fonts | `fonts-liberation` | Replace Arial, Times New Roman and Courier New | SIL Open Font License 1.1 |
| Python 3.11 | base image | Runs the application | PSF License |

## 2. Python packages (44 packages, exact versions in `requirements-lock.txt`)

Generated with `pip-licenses` from a fresh Python 3.11 install of `requirements-lock.txt`, on 24 Oct 2026, for the set that resolved on 16 Oct 2026. Packages marked **(copyleft)** are under a copyleft or weak-copyleft licence.

| Package | Version | Licence (as declared) | Project page |
|---|---|---|---|
| blinker | 1.9.0 | MIT | https://github.com/pallets-eco/blinker/ |
| cffi | 2.1.1 | MIT-0 | https://cffi.readthedocs.io/en/latest/whatsnew.html |
| chardet | 7.6.0 | 0BSD | https://github.com/chardet/chardet |
| charset-normalizer | 3.5.2 | MIT | https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md |
| click | 8.5.0 | BSD-3-Clause | https://github.com/pallets/click/ |
| cryptography | 50.0.2 | Apache-2.0 OR BSD-3-Clause | https://github.com/pyca/cryptography |
| Deprecated | 1.3.1 | MIT | https://github.com/laurent-laporte-pro/deprecated |
| et_xmlfile | 2.0.0 | MIT | https://foss.heptapod.net/openpyxl/et_xmlfile |
| fire | 0.7.1 | Apache-2.0 | https://github.com/google/python-fire |
| Flask | 3.1.3 | BSD-3-Clause | https://github.com/pallets/flask/ |
| Flask-Limiter | 4.1.1 | MIT | https://flask-limiter.readthedocs.org |
| fonttools | 4.67.0 | MIT | http://github.com/fonttools/fonttools |
| gunicorn | 22.0.0 | MIT | https://gunicorn.org |
| img2pdf | 0.5.1 | LGPL-3.0 **(copyleft)** | https://gitlab.mister-muffin.de/josch/img2pdf |
| itsdangerous | 2.2.0 | BSD | https://github.com/pallets/itsdangerous/ |
| Jinja2 | 3.1.6 | BSD | https://github.com/pallets/jinja/ |
| limits | 5.8.0 | MIT | https://limits.readthedocs.org |
| lxml | 6.1.3 | BSD-3-Clause | https://lxml.de/ |
| MarkupSafe | 3.0.4 | BSD-3-Clause | https://github.com/pallets/markupsafe/ |
| numpy | 2.4.6 | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 | https://numpy.org |
| opencv-python-headless | 5.0.0.93 | Apache-2.0 | https://github.com/opencv/opencv-python |
| openpyxl | 3.1.5 | MIT | https://openpyxl.readthedocs.io |
| ordered-set | 4.1.0 | MIT | https://pypi.org/project/ordered-set/ |
| packaging | 26.3 | Apache-2.0 OR BSD-2-Clause | https://github.com/pypa/packaging |
| pdf2docx | 0.5.13 | MIT | https://artifex.com/ |
| pdf2image | 1.17.0 | MIT | https://github.com/Belval/pdf2image |
| pdfminer.six | 20260107 | MIT | https://github.com/pdfminer/pdfminer.six |
| pdfplumber | 0.11.10 | MIT | https://github.com/jsvine/pdfplumber |
| pi_heif | 1.4.0 | LGPL-3.0 **(copyleft)** | https://github.com/bigcat88/pillow_heif |
| pikepdf | 9.3.0 | MPL-2.0 **(copyleft)** | https://github.com/pikepdf/pikepdf |
| pillow | 12.3.0 | MIT-CMU | https://python-pillow.github.io |
| pycparser | 3.11 | BSD-3-Clause | https://github.com/eliben/pycparser |
| pymupdf | 1.28.2 | AGPL-3.0 or Artifex commercial licence **(copyleft)** | https://github.com/pymupdf/pymupdf |
| pypdf | 6.19.0 | BSD-3-Clause | https://github.com/py-pdf/pypdf |
| pypdfium2 | 5.14.0 | BSD-3-Clause, Apache-2.0, dependency licenses | https://github.com/pypdfium2-team/pypdfium2 |
| python-docx | 1.2.0 | MIT | https://github.com/python-openxml/python-docx |
| python-dotenv | 1.2.2 | BSD-3-Clause | https://github.com/theskumar/python-dotenv |
| python-pptx | 1.0.2 | MIT | https://github.com/scanny/python-pptx |
| reportlab | 4.2.5 | BSD | https://www.reportlab.com/ |
| termcolor | 3.3.0 | MIT | https://github.com/termcolor/termcolor |
| typing_extensions | 4.16.0 | PSF-2.0 | https://github.com/python/typing_extensions |
| Werkzeug | 3.1.9 | BSD-3-Clause | https://github.com/pallets/werkzeug/ |
| wrapt | 2.5.1 | BSD-2-Clause | https://github.com/GrahamDumpleton/wrapt |
| xlsxwriter | 3.2.9 | BSD | https://github.com/jmcnamara/XlsxWriter |

Notes:
- **PyMuPDF** is used through `pdf2docx` (PDF to Word). It is offered under the AGPL-3.0 or a commercial licence from Artifex; KuickKonvert uses it under the AGPL-3.0, which is one reason KuickKonvert itself is licensed under the AGPL-3.0.
- **pi-heif** (HEIC to JPG): its Python code is BSD-3-Clause; the bundled libheif and libde265 libraries are LGPL-3.0. Its metadata declares LGPL-3.0.
- **pypdfium2** bundles the PDFium library; see its own licence files for the bundled components.

## 3. Front-end assets

| Component | Used for | Licence |
|---|---|---|
| Font Awesome Free 6.7.2 icons (inline SVG) | Social icons in the site footer | CC BY 4.0 |

## Updating this file

When `requirements-lock.txt` changes, regenerate section 2:

```bash
pip install -r requirements-lock.txt pip-licenses
pip-licenses --format=markdown --with-urls --ignore-packages pip-licenses prettytable wcwidth
```
