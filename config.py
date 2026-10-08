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
        "description": "Turn each PDF page into a slide in a PPTX presentation.",
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
        "description": "Combine one or more JPG or PNG images into a single PDF.",
        "accept": ".jpg,.jpeg,.png",
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
#
# Optional keys (added 8 Oct 2026, keyword-gap plan): "h1" replaces the
# page's H1 (the short "name" is still used in the menu, cards and
# breadcrumb), and "how_to_heading" replaces the default "How to convert
# <name>" heading -- used by the PDF tools, where "convert" doesn't fit.
TOOL_CONTENT = {
    "word-to-pdf": {
        "intro": "Word to PDF is a free online converter that turns MS Word files into PDF -- DOC to PDF or DOCX to PDF -- so your document looks the same on every device. It's the simplest way to share a Word document with someone you can't be sure has Microsoft Word installed, or to lock in a finished document's layout before sending it.",
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
        "seo_title": "Word to PDF Converter - DOC & DOCX to PDF | KuickKonvert",
        "meta_description": "Free online DOC to PDF converter: convert Word files (DOC and DOCX) to PDF with no sign-up or installation. Files are deleted automatically.",
    },
    "pdf-to-word": {
        "intro": "PDF to Word lets you convert PDF to Word online for free: it turns a PDF's pages into an editable DOCX file (PDF to DOCX), so you can update text you'd otherwise have to retype. It works best on PDFs that already contain real text, rather than a scan of a printed page.",
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
            ("Can I convert PDF to DOC instead of DOCX?", "Our PDF to Word converter creates a DOCX file -- the standard Word format since Word 2007, which opens in Microsoft Word, Google Docs and LibreOffice. If you specifically need the older .doc format, open the DOCX in Word and choose File → Save As → Word 97-2003 Document (*.doc)."),
        ],
        "related": ["word-to-pdf", "pdf-to-excel", "pdf-to-ppt", "compress-pdf"],
        "seo_title": "PDF to Word Converter Online Free (DOCX) | KuickKonvert",
        "meta_description": "Free online PDF to Word converter: turn a PDF into an editable Word (DOCX) file with no sign-up. Best results with text-based PDFs.",
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
            ("Can I convert Excel to PDF without Excel installed?", "Yes -- you upload the file from your browser and the conversion runs on our server, so you can convert an XLS or XLSX file to PDF even on a device that doesn't have Excel installed."),
            ("Is this free, and is there a file size limit?", "It's free with no sign-up. The only limit is a 50MB file size cap, which covers the vast majority of spreadsheets."),
        ],
        "related": ["pdf-to-excel", "word-to-pdf", "compress-pdf"],
        "seo_title": "Excel to PDF Converter - XLS & XLSX to PDF | KuickKonvert",
        "meta_description": "Convert XLS and XLSX spreadsheets to PDF online for free. No installation or sign-up -- fast, private Excel to PDF conversion.",
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
            ("Is this PDF to Excel converter really free?", "Yes -- no sign-up, subscription, or watermark on the output file. The only limit is the 50MB upload cap."),
        ],
        "related": ["excel-to-pdf", "pdf-to-word", "merge-pdf"],
        "seo_title": "PDF to Excel Converter Online Free | KuickKonvert",
        "meta_description": "Convert PDF tables into editable Excel XLSX files online. Free PDF to Excel converter with no sign-up or installation.",
    },
    "ppt-to-pdf": {
        "intro": "PPT to PDF converts PowerPoint presentations to PDF online for free -- PPT and PPTX to PDF -- so slides display exactly as designed on any device, without needing PowerPoint installed.",
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
        "seo_title": "PPT to PDF Converter - PowerPoint to PDF Free | KuickKonvert",
        "meta_description": "Convert PPT and PPTX presentations to PDF online for free. Fast, simple, private -- no sign-up or software required.",
    },
    "pdf-to-ppt": {
        "intro": "PDF to PPT turns each page of a PDF into a slide in a PowerPoint file, preserving the exact visual layout of the original document.",
        "good_to_know": "Each PDF page becomes a full-slide image on its own slide, so the layout is reproduced exactly -- but the text on those slides isn't editable, since it's an image rather than live PowerPoint text. Up to 50 pages can be converted at a time; for a longer PDF, split it with Split PDF and convert it in parts.",
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
        "seo_title": "PDF to PPT Converter - PDF to PowerPoint Free | KuickKonvert",
        "meta_description": "Convert PDF to PowerPoint online for free: each PDF page becomes a slide in a PPTX file, with the layout kept exactly. No sign-up.",
    },
    "jpg-to-pdf": {
        "h1": "JPG to PDF Converter - Photo to PDF",
        "intro": "Convert images to PDF online for free: turn a single JPG photo into a PDF, or merge JPG to PDF to combine several photos into one file. It's a quick way to turn pictures of documents, receipts, or whiteboards into one shareable PDF -- and PNG images work too.",
        "good_to_know": "Images are combined into the PDF in the order you add them. You can remove a file from the list before converting if you added the wrong one, but there's no reorder option -- if you need a different order, remove all the files and re-add them in the order you want. Your JPG files are placed into the PDF exactly as uploaded -- they aren't re-compressed, so there's no extra quality loss. PNG files are embedded losslessly, and any transparent areas are placed on a white background.",
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
        "meta_description": "Free image to PDF converter: convert JPG or PNG photos and pictures to PDF online, or combine several images into one PDF. No sign-up.",
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
            ("Can I mix JPG and PNG files in one PDF?", "Yes -- use JPG to PDF, which accepts JPG and PNG images together and combines them in the order you add them. This page accepts PNG files only."),
            ("Can I convert PNG to PDF online for free?", "Yes -- this tool is completely free, with no account or software installation needed. You upload from your browser and the PDF is built on our server."),
        ],
        "related": ["jpg-to-pdf", "pdf-to-png", "merge-pdf"],
        "seo_title": "PNG to PDF Converter Online Free | KuickKonvert",
        "meta_description": "Convert PNG images to PDF online for free. Combine multiple PNG files into a single PDF with no sign-up or installation.",
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
            ("Is converting PDF to JPG online free?", "Yes -- there's no charge or sign-up; the only limits are the 50MB upload cap and 50 pages per conversion, and there's nothing to install: you upload from your browser and the images are created on our server."),
        ],
        "related": ["pdf-to-png", "jpg-to-pdf", "compress-pdf"],
        "seo_title": "PDF to JPG Converter - PDF to Image Free | KuickKonvert",
        "meta_description": "Convert PDF to JPG images online for free: every page becomes a 300 DPI JPG (one JPG, or a ZIP for multi-page PDFs). No sign-up.",
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
            ("What do I get for a multi-page PDF?", "A ZIP file containing one PNG image per page."),
        ],
        "related": ["pdf-to-jpg", "png-to-pdf", "compress-pdf"],
        "seo_title": "PDF to PNG Converter Online Free | KuickKonvert",
        "meta_description": "Convert PDF pages to PNG images online for free. Fast, private PDF to PNG conversion with no sign-up.",
    },
    "merge-pdf": {
        "h1": "Merge PDF Files - PDF Combiner",
        "how_to_heading": "How to combine PDF files",
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
            ("Can I merge PDF files without sign-up?", "Yes -- Merge PDF is free with no account or email needed. Add your files, merge them, and download the combined PDF."),
        ],
        "related": ["split-pdf", "compress-pdf", "pdf-to-word"],
        "seo_title": "Merge PDF Online Free - Combine PDF Files | KuickKonvert",
        "meta_description": "Merge PDF files online for free: combine PDF documents into one file, in the order you add them. A simple PDF merger with no sign-up or installation.",
    },
    "split-pdf": {
        "how_to_heading": "How to split a PDF into separate pages",
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
        "meta_description": "Split a PDF into separate pages online for free. Download individual PDF pages in a ZIP file with no sign-up.",
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
            ("Can I compress a PDF without losing quality?", "Partly. Text and vector graphics stay sharp at every level, because compression only works on images. To keep images as close to the original as possible, choose \"Best quality, larger file\" (the Printer preset): it keeps image resolution and uses a gentler JPEG setting, but it usually shrinks the file only a little. A noticeably smaller file always means some loss of image detail -- our PDF compression guide shows real test results."),
            ("Can I reduce a PDF's file size online for free?", "Yes -- use Compress PDF without sign-up or payment. Upload your PDF, choose a compression level, and our server returns the smaller file."),
            ("Can I compress a PDF to 1MB or a few hundred KB?", "There's no exact-size setting, so we can't promise a specific size. For the biggest reduction, choose \"Smallest file (screen quality)\": image-heavy and scanned PDFs usually shrink a lot, while a text-only PDF may already be close to its smallest size. Check the result's size before uploading it to a form with a limit."),
            ("Is this a PDF resize tool?", "It resizes the file, not the pages. Compress PDF makes the file smaller (fewer KB or MB) by reducing embedded images; the page dimensions -- for example A4 or Letter -- stay exactly the same."),
        ],
        "related": ["merge-pdf", "split-pdf", "pdf-to-jpg"],
        "seo_title": "Compress PDF Online Free - PDF Size Reducer | KuickKonvert",
        "meta_description": "Free PDF size reducer online: compress PDF files and reduce PDF size while keeping them readable. Choose a compression level -- no sign-up.",
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
        "meta_description": "Rotate PDF pages by 90°, 180° or 270° online for free. Simple, fast, private PDF rotation with no installation.",
    },
    "watermark-pdf": {
        "how_to_heading": "How to add a watermark to a PDF",
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
            ("What if I forget the password?", "There's no way to recover it -- we don't keep a copy of your file or password after the conversion finishes, so choose a password you'll remember or store securely."),
            ("Is password-protecting a PDF online really free here?", "Yes -- Protect PDF, like every tool on KuickKonvert, is completely free with no sign-up, subscription, or hidden limits beyond the 50MB file size cap."),
            ("Do I need to install anything?", "No -- upload your PDF from your browser, choose a password, and download the protected file. The encryption runs on our server; nothing is installed on your device."),
        ],
        "related": ["watermark-pdf", "compress-pdf", "merge-pdf"],
        "seo_title": "Protect PDF with Password Online | KuickKonvert",
        "meta_description": "Password protect a PDF online for free. No sign-up or installation -- add a password so only people who know it can open the file.",
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
        "title": "DOCX vs DOC: What's Actually Different (and When It Matters)",
        "seo_title": "DOCX vs DOC: The Real Difference Explained | KuickKonvert",
        "meta_description": "DOC and DOCX both open in Word but aren't the same format underneath. What changed, what our own size test found, and when the difference affects you.",
        "dek": "Both open in Word, but DOC and DOCX are built on completely different technology. Here's what that changes for you -- including one common claim our own test didn't bear out.",
        "published": "2026-09-14",
        "updated": "2026-10-05",
        "related_tools": ["word-to-pdf"],
        "sections": [
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
                    "If a form or portal asks for \"a Word document\" without saying which, DOCX is the safe choice. If it must not be edited at all, send a PDF instead -- our Word to PDF tool accepts both .doc and .docx. Your upload and the PDF are deleted from our server as soon as your download is ready.",
                ],
            },
        ],
    },
    {
        "slug": "why-pdf-layout-shifts",
        "title": "Why a PDF's Layout Sometimes Shifts After Conversion (and How to Avoid It)",
        "seo_title": "Why PDF Layout Shifts After Conversion | KuickKonvert",
        "meta_description": "Converted a Word document to PDF and the fonts or page count changed? Our test shows exactly why -- and why Word's newer default font, Aptos, is affected.",
        "dek": "It's almost never a bug. In the overwhelming majority of cases it comes down to one specific, well-understood cause: font substitution. Our test shows how much difference it can make.",
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
                    "Commercial fonts such as Calibri, Cambria, Arial and Times New Roman are licensed by Microsoft and aren't necessarily installed on the server that performs the conversion. Our Office-to-PDF conversions run through LibreOffice, and our server has free, metric-compatible replacements installed for the most common ones: Carlito for Calibri, Caladea for Cambria, and the Liberation fonts for Arial, Times New Roman and Courier New.",
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
        "title": "PDF Compression Explained: Screen vs eBook vs Printer (With Real Test Results)",
        "seo_title": "PDF Compression Levels: Screen vs eBook vs Printer | KuickKonvert",
        "meta_description": "What Screen, eBook and Printer PDF compression really change, why some PDFs barely shrink, and our own test results on photos, scans and text-only files.",
        "dek": "Each level is a fixed recipe for shrinking the images inside a PDF. Knowing the recipe tells you in advance which level will actually make your file smaller -- and which won't.",
        "published": "2026-09-14",
        "updated": "2026-10-02",
        "related_tools": ["compress-pdf"],
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
                    "Our Compress PDF tool rewrites your file with Ghostscript, a long-established open-source PDF engine, using one of its three standard presets: /screen, /ebook or /printer. Each preset combines two techniques.",
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
                    "If you want to compress a PDF without losing quality you can see, choose Printer (\"Best quality, larger file\" in our tool). It keeps every image at its original resolution and uses the gentler JPEG setting. The trade-off, as our test showed, is that the file usually gets only slightly smaller, if at all.",
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
        "title": "JPG vs PNG for Documents: Which Format to Use (With Real Test Results)",
        "seo_title": "JPG vs PNG for Documents and Scans: Which Is Better? | KuickKonvert",
        "meta_description": "JPG or PNG for scans, screenshots and document pages? What each format does to text and photos, our own size tests, and how our converters handle both.",
        "dek": "JPG is built for photos, PNG for sharp edges. For pages full of text, our own test found PNG was both sharper and smaller -- here's why, and when JPG is still the right call.",
        "published": "2026-09-14",
        "updated": "2026-10-02",
        "related_tools": ["jpg-to-pdf", "png-to-pdf", "pdf-to-jpg", "pdf-to-png"],
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
                    "We created a one-page A4 letter -- a heading and six paragraphs of ordinary 11-point text -- and turned it into images with our own PDF to PNG and PDF to JPG tools, which render at 300 dpi (2481 x 3508 pixels).",
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
                    "Already have a JPG? Converting it to PNG won't bring back the detail JPG discarded; it only makes the file bigger. Keep JPGs as JPGs.",
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
                    "JPG to PDF places your JPG files into the PDF exactly as uploaded -- byte for byte -- so there's no second round of compression and no extra quality loss.",
                    "PNG to PDF embeds your images without any lossy compression and keeps greyscale images in greyscale. Transparent areas are placed on a white background, the same as a logo printed on paper.",
                    "Every uploaded image and every result is deleted from our server as soon as your download is ready.",
                ],
            },
        ],
    },
    {
        "slug": "merge-pdf-in-the-right-order",
        "title": "How to Merge PDFs in the Right Order (and Fix the Page Order If It's Wrong)",
        "seo_title": "How to Merge PDFs in the Right Order | KuickKonvert",
        "meta_description": "How our Merge PDF tool decides page order, what survives a merge in our own tests, and how to fix a merged PDF whose pages came out in the wrong order.",
        "dek": "A merged PDF follows one simple rule: files are joined in the order they appear in your list. Here's how to get that list right first time, what a merge keeps and drops, and how to repair a file that came out wrong.",
        "published": "2026-10-05",
        "related_tools": ["merge-pdf", "split-pdf", "rotate-pdf"],
        "sections": [
            {
                "heading": "The one rule: list order is page order",
                "paragraphs": [
                    "Our Merge PDF tool takes your files from top to bottom of the list shown under the upload box and copies every page of each file, in that order, into one new PDF. Nothing is sorted by name, date or size. If the list reads Cover, Report, Appendix, the merged file starts with every page of Cover, then every page of Report, then every page of Appendix.",
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
                    "If you no longer have the originals, or need to move individual pages, use Split PDF and then Merge PDF. Split PDF breaks a file into one PDF per page and gives you a ZIP of files named page-001.pdf, page-002.pdf and so on. Unzip it, then merge the pages back together in the order you want, adding them one at a time.",
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
        "title": "Password-Protecting a PDF: What AES-256 Encryption Protects (and What It Doesn't)",
        "seo_title": "PDF Password Protection Explained (AES-256) | KuickKonvert",
        "meta_description": "What our Protect PDF tool's AES-256 encryption hides, what stays visible, why your password still matters most, and our own test results.",
        "dek": "A password-protected PDF hides its contents from anyone without the password. But some details stay visible, and in practice the strength of your password decides how safe the file is.",
        "published": "2026-10-05",
        "related_tools": ["protect-pdf"],
        "sections": [
            {
                "heading": "What our Protect PDF tool actually does",
                "paragraphs": [
                    "Protect PDF encrypts your file with a password you choose (at least 4 characters), using 256-bit AES encryption -- the method the current PDF standard, PDF 2.0 (ISO 32000-2), specifies for password-protected PDFs. Adobe Acrobat and Reader have supported 256-bit AES since version 9, so the recipient only needs the password and an up-to-date PDF reader.",
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
        "title": "Excel to PDF: How to Make a Spreadsheet Fit on One Page",
        "seo_title": "Excel to PDF: Fit a Spreadsheet on One Page | KuickKonvert",
        "meta_description": "Why spreadsheets split across pages in a PDF, what our Excel to PDF tool does automatically, our measured results, and how to keep the text readable.",
        "dek": "Our Excel to PDF tool always fits every column across the page width. The real question is how small the text becomes -- and that is something you can control before you upload.",
        "published": "2026-10-05",
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
                    "Before converting, our Excel to PDF tool adjusts the page setup of every sheet in your workbook.",
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
                "heading": "Quick checklist before converting",
                "paragraphs": [
                    "Hide or delete columns the reader doesn't need, set a print area if only part of the sheet matters, shorten very long headings, set a print title on long sheets, and unhide any sheet you want included. Then convert and zoom in on the PDF to check the smallest text. Your upload and the PDF are deleted from our server as soon as your download is ready.",
                ],
            },
        ],
    },
    {
        "slug": "pdf-to-excel-table-conversion-results",
        "title": "PDF to Excel: Why Some Tables Don't Convert Cleanly (With Test Results)",
        "seo_title": "PDF to Excel: Why Tables Don't Convert Cleanly | KuickKonvert",
        "meta_description": "Why some PDF tables convert to Excel cleanly and others don't: our tests on ruled, borderless, merged and multi-page tables, and how to fix each one.",
        "dek": "A PDF doesn't actually contain a table -- just text and lines placed on a page. How well a table converts to Excel depends on how clearly those lines mark out the cells. Here's what we found.",
        "published": "2026-10-05",
        "related_tools": ["pdf-to-excel"],
        "sections": [
            {
                "heading": "Why tables are hard to get out of a PDF",
                "paragraphs": [
                    "A spreadsheet knows which cell every value is in. A PDF doesn't: it records each piece of text and each line as a drawing instruction at a position on the page. When you look at a PDF table you see rows and columns, but the file only knows that some text sits near some lines.",
                    "So a PDF to Excel converter has to rebuild the table. Our tool uses an open-source library called pdfplumber to find table structures on each page, mainly from the ruling lines drawn around and between cells, and then writes each table into a worksheet, with the text found above and below it.",
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
        "title": "How to Turn Photos into One PDF for Applications and Forms (JPG to PDF Tips)",
        "seo_title": "Photos to One PDF: JPG to PDF Tips for Forms | KuickKonvert",
        "meta_description": "Combine phone photos into one PDF for an application or form: why photo PDFs get huge, why compression may not help, and our tested fix.",
        "dek": "Combining photos into one PDF is easy. Getting a PDF small enough for an upload portal, with sensibly sized pages, takes one extra step before you upload -- here's what our tests showed.",
        "published": "2026-10-05",
        "related_tools": ["jpg-to-pdf", "compress-pdf", "merge-pdf"],
        "sections": [
            {
                "heading": "How our JPG to PDF tool builds the PDF",
                "paragraphs": [
                    "Our JPG to PDF tool puts each photo on its own page, in the order of the file list. Files are added to the end of the list each time you choose more, and each one has a Remove button, so the easiest way to get the order right is to add the photos one at a time.",
                    "Your JPGs are placed into the PDF exactly as uploaded, byte for byte. There is no second round of compression, so no quality is lost -- but it also means the PDF ends up about the same size as all your photos added together. In our test, three images totalling 14,124 KB produced a 14,126 KB PDF.",
                    "Photos taken with the phone held upright are shown upright. Phones often store such photos sideways with a tag telling viewers how to turn them, and our tool follows that tag: our sideways-stored test photo was set to display upright in the PDF.",
                ],
            },
            {
                "heading": "Why the pages can come out enormous",
                "paragraphs": [
                    "The page size of each PDF page is worked out from the photo's pixel count and its dpi label (dots per inch) -- the setting that says how big the picture should be when printed. Photos from cameras and phones are often labelled 72 dpi, or have no dpi label at all.",
                    "In our test, a 12-megapixel photo (4032 x 3024 pixels) labelled 72 dpi became a page of 56 x 42 inches -- about 142 x 107 cm, far larger than A4. The same photo with no dpi label became a 42 x 31.5 inch page. A scan saved at 300 dpi by contrast came out at its true size, 8.3 x 11.7 inches (A4).",
                    "Most people won't notice, because PDF readers zoom to fit the screen. But a reviewer who prints the file, or a portal that checks page size, may.",
                ],
            },
            {
                "heading": "Why Compress PDF may not shrink a photo PDF",
                "paragraphs": [
                    "This surprised us. We combined two realistic phone photos (about 2.7 MB each) into a 5,456 KB PDF and ran it through Compress PDF at all three levels. The file stayed at 5,456 KB every time.",
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
                    "Our JPG to PDF tool accepts JPG files. For PNG screenshots, use PNG to PDF, then join the two PDFs with Merge PDF.",
                    "Open the finished PDF and check every page is upright, readable and in order before you submit. Your photos and the PDF are deleted from our server as soon as your download is ready.",
                ],
            },
        ],
    },
    {
        "slug": "pdf-to-word-text-vs-scanned",
        "title": "PDF to Word: Text-Based vs Scanned PDFs, and What to Do With a Scan",
        "seo_title": "PDF to Word: Text vs Scanned PDFs Explained | KuickKonvert",
        "meta_description": "Why some PDFs convert to editable Word text and others become a picture: how to spot a scan, our own test results, and a free way to handle scans.",
        "dek": "Whether a PDF converts into editable Word text depends on one thing: whether the PDF contains real text or a picture of text. Here's how to tell in five seconds, and what to do when it's a scan.",
        "published": "2026-10-05",
        "related_tools": ["pdf-to-word"],
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
                    "We made a one-page test document -- a heading, four short clauses and a small rent table -- and converted three versions of it with the same code our tool runs (October 2026). Our PDF to Word tool uses an open-source converter called pdf2docx, with LibreOffice as a fallback.",
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
        "title": "PowerPoint to PDF and PDF to PowerPoint: What Carries Over (With Test Results)",
        "seo_title": "PowerPoint to PDF and PDF to PPT: What Carries Over | KuickKonvert",
        "meta_description": "What happens to hidden slides, speaker notes, links and fonts when you convert PowerPoint to PDF -- and why PDF to PowerPoint gives picture slides. Our tests.",
        "dek": "Converting a presentation to PDF keeps what the audience sees and drops what only the presenter sees. Converting back gives you slides you can show, but not edit. Here's exactly what our tests found.",
        "published": "2026-10-05",
        "related_tools": ["ppt-to-pdf", "pdf-to-ppt"],
        "sections": [
            {
                "heading": "What PowerPoint to PDF does",
                "paragraphs": [
                    "Our PPT to PDF tool converts .ppt and .pptx files with LibreOffice and produces one PDF page per slide. The page has the same shape as your slides, so a widescreen 16:9 deck gives widescreen 13.33 x 7.5 inch pages, not A4 or Letter.",
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
                    "Our PDF to PPT tool makes one slide per PDF page (up to 50 pages at a time), and each slide holds a single picture of that page, rendered at 200 dpi. When we converted our four-page test PDF back, we got four slides of the same 13.33 x 7.5 inch size, each containing one picture -- with no text boxes and no speaker notes.",
                    "That is a deliberate choice. When we built the tool, LibreOffice's own PDF-to-PowerPoint route reported success but produced presentations with no slides at all for every test file we tried. A picture of each page is a guaranteed, exact copy of how the page looks, which is more useful than an \"editable\" file that is silently empty.",
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
        "title": "Watermarking a PDF: What a Text Watermark Does and Doesn't Protect",
        "seo_title": "Watermark PDF: What a Text Watermark Protects | KuickKonvert",
        "meta_description": "What our Watermark PDF tool adds to each page, how much text fits, what a watermark can't stop, and how to combine it with a password. Our own test results.",
        "dek": "A watermark labels every page -- CONFIDENTIAL, DRAFT, COPY -- so nobody can mistake what the document is. It doesn't lock anything. Here's what our tests showed, and how to use one well.",
        "published": "2026-10-05",
        "related_tools": ["watermark-pdf", "protect-pdf"],
        "sections": [
            {
                "heading": "What our Watermark PDF tool adds",
                "paragraphs": [
                    "The tool stamps the text you type diagonally across the centre of every page, at a 45-degree angle, in bold grey letters that are 35% opaque, so the page underneath stays readable. The letters are sized to the page's shorter side: 49 points on an A4 page and 51 points on US Letter, whether the page is portrait or landscape.",
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
                    "If a document needs both a label and protection, watermark it first, then run the watermarked file through Protect PDF. Our tools can't open a password-protected PDF, so if you protect it first, the watermark step will stop with a message that the file is password-protected.",
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
        "title": "Split PDF and Rotate PDF: What Happens Inside the File (With Test Results)",
        "seo_title": "Split and Rotate PDF Pages: What Changes Inside | KuickKonvert",
        "meta_description": "Why split PDF pages can add up to far more than the original, why rotating a PDF loses no quality, and how to rotate or extract just some pages. Our tests.",
        "dek": "Splitting and rotating look like the simplest PDF jobs, but our tests turned up two things worth knowing: split pages can take up many times the space of the original, and rotation never touches your content.",
        "published": "2026-10-05",
        "related_tools": ["split-pdf", "rotate-pdf", "merge-pdf"],
        "sections": [
            {
                "heading": "What Split PDF gives you",
                "paragraphs": [
                    "Split PDF turns every page of your file into its own one-page PDF. For a multi-page file you download a ZIP containing page-001.pdf, page-002.pdf and so on, in page order; a one-page PDF simply comes back as a PDF. There is no option to choose a page range -- every page is split.",
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
                    "Rotate PDF turns every page by 90, 180 or 270 degrees. In the PDF format, page rotation is a setting stored with each page that tells the reader how to display it; the PDF standard defines it as a clockwise turn. So 90 degrees turns pages a quarter turn clockwise, 270 degrees a quarter turn anticlockwise, and 180 degrees turns them upside down.",
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
        "title": "Word to PDF: What Carries Over -- Links, Headings, Comments and Photos (With Test Results)",
        "seo_title": "Word to PDF: What Carries Over (Tested) | KuickKonvert",
        "meta_description": "Do links, headings, headers, comments and photos survive Word to PDF conversion? Our test results, including how photos are resized, and what to check first.",
        "dek": "A Word document holds more than the words on the page: links, heading structure, comments, full-size photos. We tested which of these make it into the PDF our tool creates.",
        "published": "2026-10-05",
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
            },
            {
                "heading": "Checklist before converting",
                "paragraphs": [
                    "Use Word's Heading styles if you want bookmarks, use a common font such as Calibri or Arial, remember that comments won't appear, and keep the original photos if anyone needs them at full size. Then open the PDF, check the page count and click a link or two. Our Word to PDF tool accepts both .doc and .docx, and your upload and the PDF are deleted from our server as soon as your download is ready.",
                ],
            },
        ],
    },
]

GUIDES_BY_SLUG = {g["slug"]: g for g in GUIDES}

# Reverse index: tool slug -> the guides that reference it, so tool.html can
# render a "Further reading" block without every TOOL_CONTENT entry having
# to separately know which guides exist.
from collections import defaultdict as _defaultdict

GUIDES_BY_TOOL = _defaultdict(list)
for _g in GUIDES:
    for _slug in _g.get("related_tools", []):
        GUIDES_BY_TOOL[_slug].append(_g)
