(function () {
  const form = document.getElementById("convert-form");
  if (!form) return;

  const slug = form.dataset.slug;
  const multi = form.dataset.multi === "true";
  const input = document.getElementById("file-input");
  const dropzone = document.getElementById("dropzone");
  const chooseLabel = document.getElementById("file-input-label");
  const fileListEl = document.getElementById("file-list");
  const convertBtn = document.getElementById("convert-btn");
  const statusEl = document.getElementById("status");

  // Upload rules (Package 1, 16 Oct 2026), rendered into data-* attributes by
  // tool.html from the same values the server enforces. Checked here only to
  // stop an upload that would certainly fail; the server still checks all.
  const acceptExts = (form.dataset.accept || "")
    .split(",").map((s) => s.trim().toLowerCase()).filter(Boolean);
  const maxBytes = (parseInt(form.dataset.maxMb, 10) || 50) * 1024 * 1024 - 64 * 1024;
  const minFiles = parseInt(form.dataset.minFiles, 10) || 1;
  const maxFiles = parseInt(form.dataset.maxFiles, 10) || 0;
  const typesText = (document.getElementById("upload-limits") || {}).textContent || "";

  let selectedFiles = [];

  // Release 7, WP14 (Package 2, 11 Nov 2026) -----------------------------
  // R7-63: a selection the server refused for a reason that a second try
  // can't fix (the pdf-to-ppt loop: 31 of 35 attempts failed for 2 users)
  // is remembered here, in memory only, and not sent again until the visitor
  // changes the file or an option. Nothing is stored or sent anywhere.
  const REFUSAL_CODES = new Set([
    "pdf_scanned", "pdf_too_complex", "pdf_pictures_too_big", "pdf_locked",
    "pdf_restricted", "pdf_damaged", "image_damaged", "wrong_type",
    "already_target_format", "empty_file", "too_many_pages", "image_too_big",
    "output_too_big", "server_memory_limit", "server_time_limit", "too_slow",
    "office_failed",
  ]);
  const refused = new Map();
  function selectionKey() {
    const opts = Array.from(form.elements)
      .filter((el) => el.name && el.type !== "file" && el.type !== "submit" && el.type !== "password")
      .map((el) => el.name + "=" + el.value).join("&");
    return selectedFiles.map((f) => [f.name, f.size, f.lastModified].join("|")).join("\n") + "\n" + opts;
  }
  // R7-59: 2 automatic retries with back-off (Package 1 had 1) when the
  // connection drops before the server answers.
  const RETRY_DELAYS_MS = [1500, 4000];
  // R7-64: the server's pixel limit for this tool (0 = no in-browser
  // reduction). Only an image that the server would certainly refuse is
  // reduced, and the visitor is told; normal images are sent unchanged.
  const maxPixels = (parseInt(form.dataset.maxMp, 10) || 0) * 1000000;
  const REDUCIBLE_TYPES = ["image/jpeg", "image/png", "image/webp"];

  function totalBytes() {
    return selectedFiles.reduce((sum, f) => sum + (f.size || 0), 0);
  }

  function extOk(name) {
    if (acceptExts.length === 0) return true;
    const dot = (name || "").lastIndexOf(".");
    return dot !== -1 && acceptExts.indexOf(name.slice(dot).toLowerCase()) !== -1;
  }

  // Returns null when the current selection can be sent, otherwise
  // {code, message} describing the first problem found.
  function selectionProblem() {
    if (selectedFiles.length < minFiles) {
      return { code: "merge_needs_two", message: `Add ${minFiles} or more PDFs to merge (you have ${selectedFiles.length}).` };
    }
    if (maxFiles && selectedFiles.length > maxFiles) {
      return { code: "too_many_files", message: `You can convert up to ${maxFiles} files at a time -- please remove ${selectedFiles.length - maxFiles}.` };
    }
    if (refused.has(selectionKey())) {
      return { code: "repeat_refused", message: `This file was refused a moment ago, so it wasn't sent again. ${refused.get(selectionKey())} Please choose a different file.` };
    }
    if (totalBytes() > maxBytes) {
      const mb = (totalBytes() / 1048576).toFixed(1);
      const limit = form.dataset.maxMb || "50";
      return { code: "file_too_large", message: `These files add up to ${mb} MB; the limit is ${limit} MB${multi ? " in total" : ""}. Please use ${multi ? "fewer or smaller files" : "a smaller file"}.` };
    }
    return null;
  }

  function renderFileList() {
    fileListEl.innerHTML = "";
    selectedFiles.forEach((file, idx) => {
      const li = document.createElement("li");
      const sizeKb = (file.size / 1024).toFixed(0);
      li.innerHTML = `<span>${escapeHtml(file.name)} (${sizeKb} KB)</span>`;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "file-remove";
      btn.textContent = "Remove";
      btn.addEventListener("click", () => {
        selectedFiles.splice(idx, 1);
        renderFileList();
      });
      li.appendChild(btn);
      fileListEl.appendChild(li);
    });
    const problem = selectedFiles.length ? selectionProblem() : null;
    convertBtn.disabled = selectedFiles.length === 0 || !!problem;
    if (problem) {
      // Too few files is a "keep going" hint, not an error.
      setStatus(escapeHtml(problem.message), problem.code === "merge_needs_two" ? "" : "error");
    } else if (statusEl.classList.contains("error") || statusEl.dataset.hint === "1") {
      setStatus("");
    }
    statusEl.dataset.hint = problem && problem.code === "merge_needs_two" ? "1" : "";
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    }[c]));
  }

  // --- Google Analytics 4 funnel (added 10 Oct 2026, review item C8) --------
  // Sends only the tool slug and, for a failure, an error *category* -- never a
  // filename, file contents, error text or e-mail. Guarded so it stays harmless
  // if gtag is absent or blocked by the visitor. The Google Ads "conversion"
  // event below is deliberately left exactly as it was (fired after download),
  // so Ads bidding is not disturbed.
  // Consent regions, basic mode (added 11 Oct 2026): static/js/consent.js
  // exposes a frozen window.__kkConsent ({mode, current()}). In "basic" mode
  // a GA4 event is sent only with Analytics consent and the Google Ads
  // conversion only with Advertising consent. Everywhere else this returns
  // true, so behaviour is exactly as before: non-consent regions (whose
  // unchanged head script defines only a legacy __kkConsent {accept, reject}
  // with no "mode") and "advanced" mode.
  function consentAllows(category) {
    // Global Privacy Control (12 Nov 2026): no advertising conversion event.
    if (category === "advertising" && navigator.globalPrivacyControl === true) return false;
    const c = window.__kkConsent;
    if (!c || c.mode !== "basic") return true;
    const cur = typeof c.current === "function" ? c.current() : null;
    return !!(cur && cur[category]);
  }

  function ga4(name, params) {
    if (typeof window.gtag !== "function") return;
    if (!consentAllows("analytics")) return;
    const payload = { send_to: "G-K0VJLC113K", tool: slug };
    if (params) Object.assign(payload, params);
    window.gtag("event", name, payload);
  }

  // Package 1 (16 Oct 2026): the server now sends a stable "code" with every
  // failure. error_type keeps the broad categories used since 10 Oct; the new
  // error_code parameter carries the precise reason.
  const CODE_TYPES = {
    pdf_damaged: "damaged", image_damaged: "damaged", pdf_locked: "damaged",
    wrong_type: "unsupported", already_target_format: "unsupported", pdf_scanned: "unsupported",
    pdf_restricted: "unsupported",
    file_too_large: "too_large", image_too_big: "too_large", output_too_big: "too_large",
    too_many_pages: "too_large", server_memory_limit: "too_large", server_time_limit: "too_large",
    too_slow: "too_large",
    rate_limited: "rate_limited", busy: "busy", network_upload: "network",
    // Release 6 pre-check codes (R7-43) and Release 7 WP14 codes (R7-65).
    pdf_too_complex: "too_large", pdf_pictures_too_big: "too_large",
    too_many_files: "too_large", empty_file: "damaged",
    download_interrupted: "network",
    office_failed: "converter", compress_failed: "converter",
    images_pdf_failed: "converter", server_error: "converter",
    repeat_refused: "repeat",
  };

  function errorTypeFromCode(code) {
    return CODE_TYPES[code] || (code && code.indexOf("http_") === 0 ? "gateway" : "other");
  }

  function errorTypeFromStatus(status, message) {
    if (status === 413) return "too_large";
    if (status === 429) return "rate_limited";
    if (status === 503) return "busy";
    if (status === 415) return "unsupported";
    if (status === 400) {
      const m = (message || "").toLowerCase();
      if (m.indexOf("valid pdf") !== -1 || m.indexOf("damaged") !== -1 ||
          m.indexOf("could not read") !== -1 || m.indexOf("couldn't read") !== -1) return "damaged";
      if (m.indexOf("unsupported") !== -1 || m.indexOf("not supported") !== -1) return "unsupported";
      // EPS/PostScript (or PDF) uploaded to an image tool (converters/images.py
      // _reject_non_raster): "... is a PostScript/EPS or PDF file, not an image
      // this tool can convert ..." (added 11 Oct 2026; was counted as "other").
      if (m.indexOf("not an image") !== -1 || m.indexOf("postscript") !== -1) return "unsupported";
      return "other";
    }
    return "other";
  }

  function addFiles(fileListLike) {
    const all = Array.from(fileListLike);
    // Drop files of a type this tool can't take, before any upload.
    const incoming = all.filter((f) => extOk(f.name));
    const rejected = all.length - incoming.length;
    if (!multi) {
      selectedFiles = incoming.slice(0, 1);
    } else {
      selectedFiles = selectedFiles.concat(incoming);
    }
    renderFileList();
    if (incoming.length > 0) ga4("file_selected");
    if (rejected > 0) {
      ga4("conversion_blocked", { error_type: "unsupported", error_code: "wrong_type" });
      const which = rejected === 1 ? "That file isn't" : `${rejected} files aren't`;
      setStatus(escapeHtml(`${which} the right type for this tool. Accepted: ${typesText.split("·")[0].trim()}.`), "error");
    }
  }

  input.addEventListener("change", () => addFiles(input.files));
  // R7-63: changing an option (e.g. the compression level) makes a refused
  // selection worth trying again.
  form.addEventListener("change", (e) => {
    if (e.target !== input && selectedFiles.length) renderFileList();
  });

  // The "Choose file" control is a <label for="file-input">, styled as a
  // button, with the real <input type="file"> hidden. A native click on the
  // label already opens the file picker via the for/id association -- but
  // <label> elements are not in the browser's default tab order (unlike
  // <button> or <a>), and even a focusable label does not respond to
  // Enter/Space the way a real button does. tabindex="0" was added on the
  // label in tool.html to make it keyboard-reachable; this handler makes it
  // keyboard-operable once reached, by forwarding Enter/Space to a real
  // click on the hidden input.
  if (chooseLabel) {
    chooseLabel.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " " || e.key === "Spacebar") {
        e.preventDefault();
        input.click();
      }
    });
  }

  ["dragenter", "dragover"].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.add("dragover");
    });
  });
  ["dragleave", "drop"].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.remove("dragover");
    });
  });
  dropzone.addEventListener("drop", (e) => {
    if (e.dataTransfer && e.dataTransfer.files) {
      addFiles(e.dataTransfer.files);
    }
  });

  function setStatus(html, cls) {
    statusEl.className = "status" + (cls ? " " + cls : "");
    statusEl.innerHTML = html;
  }

  function filenameFromDisposition(disposition, fallback) {
    if (!disposition) return fallback;
    // Prefer the UTF-8 form (filename*=UTF-8''...), which carries names in
    // any language (e.g. Urdu, Arabic, Hindi) exactly as the user saved them.
    const star = /filename\*\s*=\s*UTF-8''([^;]+)/i.exec(disposition);
    if (star) {
      try {
        return decodeURIComponent(star[1].trim());
      } catch (_) {}
    }
    const match = /filename="?([^";]+)"?/i.exec(disposition);
    return match ? match[1] : fallback;
  }

  function mpText(px) {
    const mp = px / 1e6;
    return mp < 10 ? mp.toFixed(1) : String(Math.round(mp));
  }

  async function reduceIfNeeded(file) {
    if (!maxPixels || REDUCIBLE_TYPES.indexOf(file.type) === -1 ||
        typeof createImageBitmap !== "function") return { file };
    let bmp;
    try { bmp = await createImageBitmap(file); } catch (_) { return { file }; }
    const w = bmp.width, h = bmp.height;
    if (w * h <= maxPixels) { if (bmp.close) bmp.close(); return { file }; }
    const scale = Math.sqrt((maxPixels * 0.98) / (w * h));
    const nw = Math.max(1, Math.floor(w * scale));
    const nh = Math.max(1, Math.floor(h * scale));
    try {
      const canvas = document.createElement("canvas");
      canvas.width = nw;
      canvas.height = nh;
      const ctx = canvas.getContext("2d");
      if (file.type === "image/jpeg") { ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, nw, nh); }
      ctx.drawImage(bmp, 0, 0, nw, nh);
      if (bmp.close) bmp.close();
      const blob = await new Promise((res) => canvas.toBlob(res, file.type, 0.92));
      // If the browser can't write this format, send the original and let
      // the server give its usual message.
      if (!blob || blob.type !== file.type) return { file };
      return {
        file: new File([blob], file.name, { type: file.type, lastModified: file.lastModified }),
        note: `'${file.name}' was ${mpText(w * h)} megapixels, above this tool's ` +
              `${Math.round(maxPixels / 1e6)}-megapixel limit, so your browser reduced it to ` +
              `${nw.toLocaleString()} x ${nh.toLocaleString()} pixels before upload. ` +
              "Photo details such as the date and camera are not kept in a reduced image.",
      };
    } catch (_) {
      return { file };
    }
  }

  async function postWithRetries(fd) {
    for (let attempt = 0; ; attempt++) {
      try {
        return await fetch(`/convert/${slug}`, { method: "POST", body: fd });
      } catch (err) {
        // Only a dropped connection lands here (fetch rejects); a server
        // answer, even an error, is never retried.
        if (attempt >= RETRY_DELAYS_MS.length) throw err;
        setStatus(`<span class="spinner"></span>Connection dropped &ndash; trying again (${attempt + 2} of ${RETRY_DELAYS_MS.length + 1})&hellip;`);
        ga4("upload_retried", { attempt: attempt + 1 });
        await new Promise((r) => setTimeout(r, RETRY_DELAYS_MS[attempt]));
      }
    }
  }

  function refreshButton() {
    convertBtn.disabled = selectedFiles.length === 0 || !!selectionProblem();
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (selectedFiles.length === 0) return;
    const problem = selectionProblem();
    if (problem) {
      ga4("conversion_blocked", { error_type: errorTypeFromCode(problem.code), error_code: problem.code });
      setStatus(escapeHtml(problem.message), "error");
      return;
    }

    convertBtn.disabled = true;
    setStatus('<span class="spinner"></span>Converting&hellip;');
    ga4("conversion_started");

    const fd = new FormData();
    const notes = [];
    for (const f of selectedFiles) {
      const r = await reduceIfNeeded(f);
      if (r.note) { notes.push(r.note); ga4("image_downscaled"); }
      fd.append("file", r.file);
    }
    const notesHtml = notes.map((n) => `<span class="status-note">${escapeHtml(n)}</span>`).join("");
    if (notes.length) setStatus('<span class="spinner"></span>Converting&hellip;' + notesHtml);
    // include any extra fields (rotation, watermark text, password, etc.)
    Array.from(form.elements).forEach((el) => {
      if (el.name && el.type !== "file" && el.type !== "submit") {
        fd.append(el.name, el.value);
      }
    });

    let resp;
    const key = selectionKey();
    try {
      resp = await postWithRetries(fd);
      if (!resp.ok) {
        let message = "Conversion failed. Please try again.";
        let code = "";
        try {
          const data = await resp.json();
          if (data && data.error) message = data.error;
          if (data && data.code) code = String(data.code);
        } catch (_) {
          // Not our JSON: a gateway/proxy page (e.g. 502 during a deploy).
          code = "http_" + resp.status;
          if (resp.status >= 500) message = "The server didn't respond properly. Please try again in a minute.";
        }
        ga4("conversion_failed", {
          error_type: code ? errorTypeFromCode(code) : errorTypeFromStatus(resp.status, message),
          error_code: code || ("http_" + resp.status),
        });
        if (REFUSAL_CODES.has(code)) refused.set(key, message);
        setStatus(escapeHtml(message), "error");
        return;
      }
      const blob = await resp.blob();
      const disposition = resp.headers.get("Content-Disposition");
      const filename = filenameFromDisposition(disposition, "converted");
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 4000);
      setStatus("Done -- your download has started." + notesHtml, "success");
      // Google Ads conversion ("File conversion completed"), sent only here,
      // i.e. after the server returned a converted file and the download was
      // started -- never for failed conversions or plain page views. The
      // gtag() function is defined in base.html; the check keeps this line
      // harmless if analytics is ever removed or blocked by the visitor.
      if (typeof window.gtag === "function") {
        if (consentAllows("advertising")) {
          window.gtag("event", "conversion", {
            send_to: "AW-18473004328/meE0CPKWqokdEKjazuhE",
          });
        }
        // Same moment, reported to Google Analytics 4 so the owner can count
        // successful conversions per tool (parameter "tool" = page slug,
        // e.g. "pdf-to-word"). send_to keeps it out of Google Ads.
        if (consentAllows("analytics")) {
          window.gtag("event", "file_conversion", {
            send_to: "G-K0VJLC113K",
            tool: slug,
          });
        }
      }
      // Suggest related tools only after a successful conversion. Looked up
      // here (not at page load) so this is harmless on a page without the
      // #next-steps block.
      const nextSteps = document.getElementById("next-steps");
      if (nextSteps) nextSteps.hidden = false;
    } catch (err) {
      // No reply at all (upload dropped twice) vs. reply cut off mid-download.
      const code = resp ? "download_interrupted" : "network_upload";
      ga4("conversion_failed", { error_type: "network", error_code: code });
      if (resp) {
        // R7-60: the conversion worked but the download was cut off.
        setStatus('The download was interrupted. <button type="button" class="btn btn-secondary btn-again" id="download-again">Download again</button>' +
          '<span class="status-note">Your file is uploaded and converted again: files are deleted automatically after conversion.</span>', "error");
        const again = document.getElementById("download-again");
        if (again) {
          again.addEventListener("click", () => {
            ga4("download_retried");
            if (typeof form.requestSubmit === "function") form.requestSubmit();
            else convertBtn.click();
          });
        }
      } else {
        // R7-59: after 3 tries in all.
        setStatus("Your connection dropped. Try a smaller file or a stronger connection.", "error");
      }
    } finally {
      refreshButton();
    }
  });
})();
