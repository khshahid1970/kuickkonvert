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

  let selectedFiles = [];

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
    convertBtn.disabled = selectedFiles.length === 0;
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    }[c]));
  }

  function addFiles(fileListLike) {
    const incoming = Array.from(fileListLike);
    if (!multi) {
      selectedFiles = incoming.slice(0, 1);
    } else {
      selectedFiles = selectedFiles.concat(incoming);
    }
    renderFileList();
  }

  input.addEventListener("change", () => addFiles(input.files));

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

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (selectedFiles.length === 0) return;

    convertBtn.disabled = true;
    setStatus('<span class="spinner"></span>Converting&hellip;');

    const fd = new FormData();
    selectedFiles.forEach((f) => fd.append("file", f));
    // include any extra fields (rotation, watermark text, password, etc.)
    Array.from(form.elements).forEach((el) => {
      if (el.name && el.type !== "file" && el.type !== "submit") {
        fd.append(el.name, el.value);
      }
    });

    try {
      const resp = await fetch(`/convert/${slug}`, { method: "POST", body: fd });
      if (!resp.ok) {
        let message = "Conversion failed. Please try again.";
        try {
          const data = await resp.json();
          if (data && data.error) message = data.error;
        } catch (_) {}
        setStatus(escapeHtml(message), "error");
        convertBtn.disabled = false;
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
      setStatus("Done -- your download has started.", "success");
      // Google Ads conversion ("File conversion completed"), sent only here,
      // i.e. after the server returned a converted file and the download was
      // started -- never for failed conversions or plain page views. The
      // gtag() function is defined in base.html; the check keeps this line
      // harmless if analytics is ever removed or blocked by the visitor.
      if (typeof window.gtag === "function") {
        window.gtag("event", "conversion", {
          send_to: "AW-18473004328/meE0CPKWqokdEKjazuhE",
        });
        // Same moment, reported to Google Analytics 4 so the owner can count
        // successful conversions per tool (parameter "tool" = page slug,
        // e.g. "pdf-to-word"). send_to keeps it out of Google Ads.
        window.gtag("event", "file_conversion", {
          send_to: "G-K0VJLC113K",
          tool: slug,
        });
      }
      // Suggest related tools only after a successful conversion. Looked up
      // here (not at page load) so this is harmless on a page without the
      // #next-steps block.
      const nextSteps = document.getElementById("next-steps");
      if (nextSteps) nextSteps.hidden = false;
    } catch (err) {
      setStatus("Network error. Please check your connection and try again.", "error");
    } finally {
      convertBtn.disabled = false;
    }
  });
})();
