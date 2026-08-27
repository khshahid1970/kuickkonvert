# KuickKonvert -- production image
# Office<->PDF needs LibreOffice; PDF<->image needs poppler-utils;
# PDF compression prefers Ghostscript. All three are system packages that
# most "just run pip install" hosting platforms (Render's native Python env,
# Railway's default Nixpacks Python build, etc.) do NOT include -- so deploy
# this app from this Dockerfile, not from a bare requirements.txt build.
#
# Font packages (added 2026-08-27): fonts-dejavu alone is NOT enough for
# accurate Word/Excel/PowerPoint -> PDF conversion. Verified in testing that
# a .docx set to Calibri (Word's own default body font) silently rendered
# in DejaVu Sans instead when only fonts-dejavu was installed -- DejaVu has
# different character widths than Calibri, which changes line wrapping and
# page breaks, not just appearance. fonts-crosextra-carlito/-caladea and
# fonts-liberation are free, metric-compatible substitutes for Microsoft's
# Calibri/Cambria and Arial/Times New Roman/Courier New respectively (same
# character widths, so line breaks and page counts match; the letterforms
# are similar but not pixel-identical to the proprietary originals, which
# can't legally be redistributed). Installing them measurably fixed the
# substitution in testing.
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice \
    poppler-utils \
    ghostscript \
    fonts-dejavu \
    fonts-crosextra-carlito \
    fonts-crosextra-caladea \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p tmp

ENV PORT=8080
EXPOSE 8080

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "--timeout", "180"]
