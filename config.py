import os

# ---- Tool catalogue -------------------------------------------------------
# Single source of truth for the homepage grid, each tool's page, and the
# /convert dispatcher in app.py. Add a new converter by adding an entry here
# plus a handler function in app.py's HANDLERS dict with the same slug.

TOOLS = [
    # -- Document conversions --
    {
        "slug": "word-to-pdf",
        "name": "Word to PDF",
        "category": "Documents",
        "description": "Convert DOC and DOCX files to PDF.",
        "accept": ".doc,.docx",
        "multi": False,
    },
    {
        "slug": "pdf-to-word",
        "name": "PDF to Word",
        "category": "Documents",
        "description": "Convert PDF pages into an editable DOCX file. Best results with text-based PDFs.",
        "accept": ".pdf",
        "multi": False,
    },
    {
        "slug": "excel-to-pdf",
        "name": "Excel to PDF",
        "category": "Documents",
        "description": "Convert XLS and XLSX spreadsheets to PDF.",
        "accept": ".xls,.xlsx",
        "multi": False,
    },
    {
        "slug": "pdf-to-excel",
        "name": "PDF to Excel",
        "category": "Documents",
        "description": "Pull tables from a PDF into an editable XLSX file.",
        "accept": ".pdf",
        "multi": False,
    },
    {
        "slug": "ppt-to-pdf",
        "name": "PPT to PDF",
        "category": "Documents",
        "description": "Convert PPT and PPTX presentations to PDF.",
        "accept": ".ppt,.pptx",
        "multi": False,
    },
    {
        "slug": "pdf-to-ppt",
        "name": "PDF to PPT",
        "category": "Documents",
        "description": "Convert PDF pages into an editable PPTX presentation.",
        "accept": ".pdf",
        "multi": False,
    },
    # -- Image conversions --
    {
        "slug": "jpg-to-pdf",
        "name": "JPG to PDF",
        "category": "Images",
        "description": "Combine one or more JPG images into a single PDF.",
        "accept": ".jpg,.jpeg",
        "multi": True,
    },
    {
        "slug": "png-to-pdf",
        "name": "PNG to PDF",
        "category": "Images",
        "description": "Combine one or more PNG images into a single PDF.",
        "accept": ".png",
        "multi": True,
    },
    {
        "slug": "pdf-to-jpg",
        "name": "PDF to JPG",
        "category": "Images",
        "description": "Turn each PDF page into a JPG image (downloaded as a ZIP for multi-page files).",
        "accept": ".pdf",
        "multi": False,
    },
    {
        "slug": "pdf-to-png",
        "name": "PDF to PNG",
        "category": "Images",
        "description": "Turn each PDF page into a PNG image (downloaded as a ZIP for multi-page files).",
        "accept": ".pdf",
        "multi": False,
    },
    # -- PDF tools --
    {
        "slug": "merge-pdf",
        "name": "Merge PDF",
        "category": "PDF Tools",
        "description": "Combine multiple PDFs into one, in the order you add them.",
        "accept": ".pdf",
        "multi": True,
    },
    {
        "slug": "split-pdf",
        "name": "Split PDF",
        "category": "PDF Tools",
        "description": "Split every page of a PDF into separate single-page PDFs (downloaded as a ZIP).",
        "accept": ".pdf",
        "multi": False,
    },
    {
        "slug": "compress-pdf",
        "name": "Compress PDF",
        "category": "PDF Tools",
        "description": "Reduce a PDF's file size while keeping it readable.",
        "accept": ".pdf",
        "multi": False,
        "fields": [
            {
                "name": "level",
                "label": "Compression level",
                "type": "select",
                "options": [
                    ("screen", "Smallest file (screen quality)"),
                    ("ebook", "Balanced (recommended)"),
                    ("printer", "Best quality, larger file"),
                ],
                "default": "ebook",
            }
        ],
    },
    {
        "slug": "rotate-pdf",
        "name": "Rotate PDF",
        "category": "PDF Tools",
        "description": "Rotate every page of a PDF by 90, 180, or 270 degrees.",
        "accept": ".pdf",
        "multi": False,
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
        "description": "Stamp a text watermark diagonally across every page.",
        "accept": ".pdf",
        "multi": False,
        "fields": [
            {"name": "text", "label": "Watermark text", "type": "text", "default": "CONFIDENTIAL"}
        ],
    },
    {
        "slug": "protect-pdf",
        "name": "Protect PDF",
        "category": "PDF Tools",
        "description": "Add a password so only people who have it can open the PDF.",
        "accept": ".pdf",
        "multi": False,
        "fields": [
            {"name": "password", "label": "Password", "type": "password", "default": ""}
        ],
    },
]

TOOLS_BY_SLUG = {t["slug"]: t for t in TOOLS}

CATEGORIES = ["Documents", "Images", "PDF Tools"]

MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH_MB", "50")) * 1024 * 1024
ALLOWED_EXTENSIONS = {
    "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "jpg", "jpeg", "png"
}
