import os

# Canonical site origin (no trailing slash). Used to build absolute canonical
# URLs, Open Graph/Twitter URLs, and the sitemap -- always the primary custom
# domain, even when a visitor is browsing via the onrender.com URL, so search
# engines consolidate both origins onto one canonical address instead of
# treating them as duplicate content.
SITE_URL = "https://kuickkonvert.com"

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
        "description": "Convert DOC and DOCX files to PDF.",
        "accept": ".doc,.docx",
        "multi": False,
        "from_fmt": "DOC",
        "to_fmt": "PDF",
    },
    {
        "slug": "pdf-to-word",
        "name": "PDF to Word",
        "category": "Documents",
        "description": "Convert PDF pages into an editable DOCX file. Best results with text-based PDFs.",
        "accept": ".pdf",
        "multi": False,
        "from_fmt": "PDF",
        "to_fmt": "DOC",
    },
    {
        "slug": "excel-to-pdf",
        "name": "Excel to PDF",
        "category": "Documents",
        "description": "Convert XLS and XLSX spreadsheets to PDF.",
        "accept": ".xls,.xlsx",
        "multi": False,
        "from_fmt": "XLS",
        "to_fmt": "PDF",
    },
    {
        "slug": "pdf-to-excel",
        "name": "PDF to Excel",
        "category": "Documents",
        "description": "Pull tables from a PDF into an editable XLSX file.",
        "accept": ".pdf",
        "multi": False,
        "from_fmt": "PDF",
        "to_fmt": "XLS",
    },
    {
        "slug": "ppt-to-pdf",
        "name": "PPT to PDF",
        "category": "Documents",
        "description": "Convert PPT and PPTX presentations to PDF.",
        "accept": ".ppt,.pptx",
        "multi": False,
        "from_fmt": "PPT",
        "to_fmt": "PDF",
    },
    {
        "slug": "pdf-to-ppt",
        "name": "PDF to PPT",
        "category": "Documents",
        "description": "Convert PDF pages into an editable PPTX presentation.",
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
        "description": "Combine one or more JPG images into a single PDF.",
        "accept": ".jpg,.jpeg",
        "multi": True,
        "from_fmt": "JPG",
        "to_fmt": "PDF",
    },
    {
        "slug": "png-to-pdf",
        "name": "PNG to PDF",
        "category": "Images",
        "description": "Combine one or more PNG images into a single PDF.",
        "accept": ".png",
        "multi": True,
        "from_fmt": "PNG",
        "to_fmt": "PDF",
    },
    {
        "slug": "pdf-to-jpg",
        "name": "PDF to JPG",
        "category": "Images",
        "description": "Turn each PDF page into a JPG image (downloaded as a ZIP for multi-page files).",
        "accept": ".pdf",
        "multi": False,
        "from_fmt": "PDF",
        "to_fmt": "JPG",
    },
    {
        "slug": "pdf-to-png",
        "name": "PDF to PNG",
        "category": "Images",
        "description": "Turn each PDF page into a PNG image (downloaded as a ZIP for multi-page files).",
        "accept": ".pdf",
        "multi": False,
        "from_fmt": "PDF",
        "to_fmt": "PNG",
    },
    # -- PDF tools --
    {
        "slug": "merge-pdf",
        "name": "Merge PDF",
        "category": "PDF Tools",
        "description": "Combine multiple PDFs into one, in the order you add them.",
        "accept": ".pdf",
        "multi": True,
        "from_fmt": "PDF",
        "to_fmt": "PDF",
    },
    {
        "slug": "split-pdf",
        "name": "Split PDF",
        "category": "PDF Tools",
        "description": "Split every page of a PDF into separate single-page PDFs (downloaded as a ZIP).",
        "accept": ".pdf",
        "multi": False,
        "from_fmt": "PDF",
        "to_fmt": "PDF",
    },
    {
        "slug": "compress-pdf",
        "name": "Compress PDF",
        "category": "PDF Tools",
        "description": "Reduce a PDF's file size while keeping it readable.",
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
        "description": "Stamp a text watermark diagonally across every page.",
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
        "description": "Add a password so only people who have it can open the PDF.",
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
TOOL_CONTENT = {
    "word-to-pdf": {
        "intro": "Word to PDF turns a DOC or DOCX file into a PDF that looks the same on every device. It's the simplest way to share a Word document with someone you can't be sure has Microsoft Word installed, or to lock in a finished document's layout before sending it.",
        "good_to_know": "Converting to PDF preserves your document's current layout, so it won't shift when opened elsewhere. If your file uses a font we don't have installed, we substitute a metrically-compatible alternative (for example Carlito in place of Calibri) -- line breaks stay the same, though exact letterforms may differ slightly.",
        "use_cases": [
            "Sending a document to someone you're not sure has Word installed.",
            "Submitting a CV, invoice, or contract in a format the recipient can't accidentally edit.",
            "Archiving a finished document in a format that won't change if you update Word later.",
        ],
        "faq": [
            ("Will my formatting change?", "Page layout, fonts, and images are preserved as closely as possible. The one exception is font substitution (see \"Good to know\" above) if your document uses a font we don't have."),
            ("Can I convert a password-protected Word file?", "No -- remove the password in Word first (File → Info → Protect Document), then convert."),
        ],
        "related": ["pdf-to-word", "excel-to-pdf", "ppt-to-pdf"],
        "seo_title": "Word to PDF Converter -- DOC & DOCX Online | KuickKonvert",
        "meta_description": "Convert DOC and DOCX files to PDF online for free. No sign-up or installation -- fast, simple, private Word to PDF conversion.",
    },
    "pdf-to-word": {
        "intro": "PDF to Word converts a PDF's pages into an editable DOCX file, so you can update text you'd otherwise have to retype. It works best on PDFs that already contain real text, rather than a scan of a printed page.",
        "good_to_know": "We use pdf2docx first, with a LibreOffice-based fallback if that doesn't produce a usable result. Bulleted and numbered lists currently convert to plain text lines rather than a live Word list -- you may need to reapply bullet formatting afterward. Complex layouts, tables, and heavily designed pages may need manual adjustment once opened in Word.",
        "use_cases": [
            "Editing text from a PDF you only have as a final, uneditable file.",
            "Updating an old contract or letter you no longer have the original Word file for.",
            "Pulling text out of a report to reuse in a new document.",
        ],
        "faq": [
            ("Will bullet points and numbering be preserved?", "They convert to plain text lines rather than a live bulleted list -- you may need to reapply list formatting in Word."),
            ("Does this work on a scanned PDF?", "This tool extracts text that's already embedded in the PDF; it doesn't perform OCR, so a scanned image-only PDF won't produce editable text."),
        ],
        "related": ["word-to-pdf", "pdf-to-excel", "pdf-to-ppt", "compress-pdf"],
        "seo_title": "PDF to Word Converter -- Editable DOCX | KuickKonvert",
        "meta_description": "Convert PDF files to editable DOCX documents online. Free, fast, private PDF to Word conversion with no sign-up -- best results with text-based PDFs.",
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
            ("Are my formulas or macros preserved?", "The PDF shows the calculated values currently in your sheet -- formulas and macros themselves aren't carried into the PDF, since PDF is a fixed, non-editable format."),
        ],
        "related": ["pdf-to-excel", "word-to-pdf", "compress-pdf"],
        "seo_title": "Excel to PDF Converter -- XLS & XLSX Online | KuickKonvert",
        "meta_description": "Convert XLS and XLSX spreadsheets to PDF online for free. No installation or sign-up -- fast, private Excel to PDF conversion.",
    },
    "pdf-to-excel": {
        "intro": "PDF to Excel pulls tables out of a PDF and rebuilds them as an editable XLSX file, so you can sort, filter, or recalculate data that arrived as a static document.",
        "good_to_know": "Tables are detected by their visible layout on the page, along with the text immediately around them. Cell values and column structure carry over, but formatting like colors, borders, and merged cells doesn't -- this works best on PDFs with genuinely tabular data rather than free-flowing text.",
        "use_cases": [
            "Pulling a table from a bank statement or invoice into a spreadsheet for review.",
            "Getting data out of a report PDF to analyze or chart in Excel.",
            "Rebuilding an old price list you only have as a PDF.",
        ],
        "faq": [
            ("Will colors and cell formatting carry over?", "No -- only the data and its column layout are extracted; visual styling isn't preserved."),
            ("What if my PDF isn't a clear table?", "The tool works best on genuinely tabular content. Text outside a detected table is still included alongside it, but results are less structured for free-form pages."),
        ],
        "related": ["excel-to-pdf", "pdf-to-word", "merge-pdf"],
        "seo_title": "PDF to Excel Converter -- Extract Tables | KuickKonvert",
        "meta_description": "Convert PDF tables into editable Excel XLSX files online. Free PDF to Excel converter with no sign-up or installation.",
    },
    "ppt-to-pdf": {
        "intro": "PPT to PDF converts a PowerPoint presentation to PDF, so slides display exactly as designed on any device without needing PowerPoint installed.",
        "good_to_know": "Slide layout, images, and text positioning are preserved. As with other Office conversions, a font we don't have installed is substituted with a metrically-compatible alternative, which can very slightly affect line spacing on text-heavy slides.",
        "use_cases": [
            "Sending a deck to someone without PowerPoint.",
            "Sharing slides that can't be accidentally edited before a meeting.",
            "Printing handouts from a presentation.",
        ],
        "faq": [
            ("Will animations or transitions be included?", "No -- PDF is a static format, so each slide converts to a single fixed page; animations and transitions don't carry over."),
            ("Will my fonts look exactly the same?", "If your presentation uses a font we don't have, a metrically-compatible substitute is used, which keeps layout intact but may look slightly different from the original."),
        ],
        "related": ["pdf-to-ppt", "word-to-pdf", "compress-pdf"],
        "seo_title": "PowerPoint to PDF Converter Online | KuickKonvert",
        "meta_description": "Convert PPT and PPTX presentations to PDF online for free. Fast, simple, private -- no sign-up or software required.",
    },
    "pdf-to-ppt": {
        "intro": "PDF to PPT turns each page of a PDF into a slide in a PowerPoint file, preserving the exact visual layout of the original document.",
        "good_to_know": "Each PDF page becomes a full-slide image on its own slide, so the layout is reproduced exactly -- but the text on those slides isn't editable, since it's an image rather than live PowerPoint text.",
        "use_cases": [
            "Turning a PDF report into slides for a presentation without redesigning it.",
            "Getting PDF content into a format you can present directly from PowerPoint.",
            "Combining PDF pages with other slides in an existing deck.",
        ],
        "faq": [
            ("Can I edit the text after converting?", "No -- each PDF page becomes a static image on its own slide, so layout is preserved exactly but the text itself isn't editable."),
            ("Will the slide size match my PDF's page size?", "Yes, each slide is sized to match the corresponding PDF page."),
        ],
        "related": ["ppt-to-pdf", "pdf-to-word", "pdf-to-jpg"],
        "seo_title": "PDF to PowerPoint Converter Online | KuickKonvert",
        "meta_description": "Convert PDF pages to editable PPTX presentations online. Free PDF to PowerPoint conversion with no sign-up.",
    },
    "jpg-to-pdf": {
        "intro": "JPG to PDF combines one or more JPG images into a single PDF file -- a quick way to turn photos of documents, receipts, or whiteboards into one shareable file.",
        "good_to_know": "Images are combined into the PDF in the order you add them. You can remove a file from the list before converting if you added the wrong one, but there's no reorder option -- if you need a different order, remove all the files and re-add them in the order you want.",
        "use_cases": [
            "Combining several photographed pages of a document into one PDF to email.",
            "Turning receipt photos into a single PDF for an expense claim.",
            "Creating a simple PDF portfolio from a set of images.",
        ],
        "faq": [
            ("Can I reorder the images after adding them?", "Not directly -- images are combined in the order you add them. Remove the files and re-add them in your preferred order if needed."),
            ("Is there a limit to how many images I can combine?", "There's no fixed count limit, but the combined upload must stay under the 50MB file size limit."),
        ],
        "related": ["png-to-pdf", "pdf-to-jpg", "merge-pdf"],
        "seo_title": "JPG to PDF Converter -- Images to PDF | KuickKonvert",
        "meta_description": "Convert JPG images to PDF online for free. Combine multiple JPG files into one PDF without installing software or creating an account.",
    },
    "png-to-pdf": {
        "intro": "PNG to PDF combines one or more PNG images into a single PDF file, keeping the sharp edges and transparency-free areas PNG is known for.",
        "good_to_know": "Images are combined into the PDF in the order you add them, the same as JPG to PDF. Transparent areas in a PNG are filled in (PDF pages don't support transparency the way PNG does), so images with a transparent background will show a solid background in the PDF.",
        "use_cases": [
            "Combining screenshots into a single PDF for a bug report or walkthrough.",
            "Turning a set of scanned PNG pages into one document.",
            "Creating a simple PDF handout from PNG graphics.",
        ],
        "faq": [
            ("What happens to transparent backgrounds?", "PDF pages don't support transparency, so any transparent area in your PNG is filled in with a solid background in the output."),
            ("Can I mix JPG and PNG files in one PDF?", "Use this tool for PNGs and JPG to PDF for JPGs -- each tool accepts one image type at a time to keep the upload validation simple."),
        ],
        "related": ["jpg-to-pdf", "pdf-to-png", "merge-pdf"],
        "seo_title": "PNG to PDF Converter -- Images to PDF | KuickKonvert",
        "meta_description": "Convert PNG images to PDF online for free. Combine multiple PNG files into a single PDF with no sign-up or installation.",
    },
    "pdf-to-jpg": {
        "intro": "PDF to JPG turns every page of a PDF into its own JPG image, useful when you need to drop a page into a slide, a website, or a chat message rather than share the whole PDF.",
        "good_to_know": "Pages are rendered at 300 DPI, sharp enough for most printing and on-screen use. A single-page PDF downloads as one JPG; a multi-page PDF downloads as a ZIP file containing one JPG per page.",
        "use_cases": [
            "Dropping one page of a PDF into a presentation or webpage as an image.",
            "Sharing a document preview somewhere that only accepts images, not PDFs.",
            "Turning a scanned form into an image for further editing in an image editor.",
        ],
        "faq": [
            ("What resolution are the images?", "Pages are rendered at 300 DPI, which is sharp enough for most printing and screen use."),
            ("What do I get for a multi-page PDF?", "A ZIP file containing one JPG image per page."),
        ],
        "related": ["pdf-to-png", "jpg-to-pdf", "compress-pdf"],
        "seo_title": "PDF to JPG Converter -- PDF Pages to JPG | KuickKonvert",
        "meta_description": "Convert PDF pages to JPG images online for free. Download individual images or a ZIP file for multi-page PDFs.",
    },
    "pdf-to-png": {
        "intro": "PDF to PNG turns every page of a PDF into its own PNG image -- a good choice when you need a crisp image of a page with sharp text or line art, such as a diagram or a form.",
        "good_to_know": "Pages are rendered at 300 DPI. A single-page PDF downloads as one PNG; a multi-page PDF downloads as a ZIP file containing one PNG per page.",
        "use_cases": [
            "Extracting a diagram or chart from a PDF as a clean image.",
            "Getting a sharp image of a form or certificate to insert elsewhere.",
            "Preparing PDF pages for use in a design or editing tool.",
        ],
        "faq": [
            ("Why PNG instead of JPG?", "PNG uses lossless compression, so sharp text and line art stay crisp -- JPG can be a better choice for photo-heavy pages where a smaller file size matters more."),
            ("What do I get for a multi-page PDF?", "A ZIP file containing one PNG image per page."),
        ],
        "related": ["pdf-to-jpg", "png-to-pdf", "compress-pdf"],
        "seo_title": "PDF to PNG Converter -- PDF Pages to PNG | KuickKonvert",
        "meta_description": "Convert PDF pages to PNG images online for free. Fast, private PDF to PNG conversion with no sign-up.",
    },
    "merge-pdf": {
        "intro": "Merge PDF combines multiple PDF files into a single document, in the order you add them -- handy for putting together a report from separate sections or combining scanned pages into one file.",
        "good_to_know": "Files are combined in the order you add them. You can remove a file from the list before merging if you added the wrong one; there's no drag-to-reorder option, so remove and re-add files in your preferred order if needed.",
        "use_cases": [
            "Combining a cover letter, CV, and references into one PDF for a job application.",
            "Putting separate scanned pages together into a single document.",
            "Assembling several reports into one file before sending.",
        ],
        "faq": [
            ("Can I change the order after adding files?", "Not directly -- files merge in the order you add them. Remove the files and re-add them in your preferred order if needed."),
            ("Is there a limit on how many files I can merge?", "There's no fixed file-count limit, but the combined upload must stay under the 50MB size limit."),
        ],
        "related": ["split-pdf", "compress-pdf", "pdf-to-word"],
        "seo_title": "Merge PDF Files Online Free | KuickKonvert",
        "meta_description": "Merge multiple PDF files into one document online for free. Combine files in the order you add them, with no installation.",
    },
    "split-pdf": {
        "intro": "Split PDF breaks every page of a PDF into its own single-page PDF file, delivered as a ZIP -- useful when you only need to send someone one page out of a longer document.",
        "good_to_know": "This splits every page of the PDF into a separate file -- there's currently no option to choose a specific page range. If you only need a few pages, split the whole file and keep just the ones you want.",
        "use_cases": [
            "Pulling a single page out of a long PDF to send on its own.",
            "Breaking a scanned multi-page document into individual page files.",
            "Preparing individual pages for a page-by-page workflow.",
        ],
        "faq": [
            ("Can I choose which pages to split out?", "This splits every page into its own file; if you only need a range, split the whole file and discard the pages you don't need."),
            ("What format do I get the pages in?", "A ZIP file containing one single-page PDF for every page in your original file."),
        ],
        "related": ["merge-pdf", "rotate-pdf", "compress-pdf"],
        "seo_title": "Split PDF Online Free | KuickKonvert",
        "meta_description": "Split a PDF into separate pages online for free. Download individual PDF pages in a ZIP file with no sign-up.",
    },
    "compress-pdf": {
        "intro": "Compress PDF reduces a PDF's file size while keeping it readable -- useful when a file is too large to email or upload, or you just want a smaller version to store.",
        "good_to_know": "Three compression levels are available: Screen (smallest file, most aggressive image downsampling), Ebook (a balanced default), and Printer (best quality, least size reduction). Compression mainly shrinks embedded images -- a text-only PDF will compress less dramatically than an image-heavy one.",
        "use_cases": [
            "Shrinking a scanned document so it fits under an email attachment limit.",
            "Reducing a large PDF before uploading it to a form or portal with a size cap.",
            "Making an image-heavy report smaller to store or archive.",
        ],
        "faq": [
            ("Which compression level should I choose?", "Ebook is a good default balance. Choose Screen for the smallest possible file if quality matters less, or Printer if quality matters most."),
            ("Will text quality be affected?", "Text stays sharp at every level -- compression mainly targets embedded images, so an image-heavy PDF will shrink more than a text-only one."),
        ],
        "related": ["merge-pdf", "split-pdf", "pdf-to-jpg"],
        "seo_title": "Compress PDF Online -- Reduce File Size | KuickKonvert",
        "meta_description": "Compress PDF files online for free and reduce file size while keeping documents readable. No sign-up or installation.",
    },
    "rotate-pdf": {
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
        ],
        "related": ["split-pdf", "merge-pdf", "compress-pdf"],
        "seo_title": "Rotate PDF Pages Online Free | KuickKonvert",
        "meta_description": "Rotate PDF pages by 90°, 180° or 270° online for free. Simple, fast, private PDF rotation with no installation.",
    },
    "watermark-pdf": {
        "intro": "Watermark PDF stamps your own text diagonally across every page of a PDF -- a simple way to mark a document as a draft, confidential, or belonging to you before sharing it.",
        "good_to_know": "The watermark is applied as semi-transparent gray text, rotated diagonally across each page, using the text you enter. Its size, color, and position aren't currently configurable -- only the text itself is.",
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
        "meta_description": "Add a text watermark to every page of a PDF online for free. Fast and private, with no sign-up required.",
    },
    "protect-pdf": {
        "intro": "Protect PDF adds a password to a PDF file, so only someone who has the password can open it -- useful before emailing a document with sensitive information.",
        "good_to_know": "The file is encrypted with a password you choose (at least 4 characters) using standard 128-bit PDF encryption. Keep the password somewhere safe -- if it's lost, the file can't be opened or recovered by KuickKonvert, since we don't keep a copy of your file or password.",
        "use_cases": [
            "Password-protecting a document with personal or financial details before emailing it.",
            "Restricting who can open a contract before it's signed.",
            "Adding a basic layer of protection to a file shared over an unsecured channel.",
        ],
        "faq": [
            ("What encryption does this use?", "Standard 128-bit PDF encryption, applied with the password you choose."),
            ("What if I forget the password?", "There's no way to recover it -- we don't keep a copy of your file or password after the conversion finishes, so choose a password you'll remember or store securely."),
        ],
        "related": ["watermark-pdf", "compress-pdf", "merge-pdf"],
        "seo_title": "Protect PDF with Password Online | KuickKonvert",
        "meta_description": "Add password protection to a PDF online for free. Protect your PDF without installing software or creating an account.",
    },
}

for _t in TOOLS:
    _t.update(TOOL_CONTENT.get(_t["slug"], {}))

CATEGORIES = ["Documents", "Images", "PDF Tools"]

# Maps a format label to the CSS badge class used on homepage tool cards.
FORMAT_BADGE_CLASS = {
    "DOC": "badge-doc",
    "XLS": "badge-xls",
    "PPT": "badge-ppt",
    "PDF": "badge-pdf",
    "JPG": "badge-jpg",
    "PNG": "badge-png",
}

MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH_MB", "50")) * 1024 * 1024
ALLOWED_EXTENSIONS = {
    "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "jpg", "jpeg", "png"
}
