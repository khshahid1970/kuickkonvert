# KuickKonvert -- production image
# Office<->PDF needs LibreOffice; PDF<->image needs poppler-utils;
# PDF compression prefers Ghostscript. All three are system packages that
# most "just run pip install" hosting platforms (Render's native Python env,
# Railway's default Nixpacks Python build, etc.) do NOT include -- so deploy
# this app from this Dockerfile, not from a bare requirements.txt build.
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice \
    poppler-utils \
    ghostscript \
    fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p tmp

ENV PORT=8080
EXPOSE 8080

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "--timeout", "180"]
