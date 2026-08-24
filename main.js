(function () {
  const form = document.getElementById("convert-form");
  if (!form) return;

  const slug = form.dataset.slug;
  const multi = form.dataset.multi === "true";
  const input = document.getElementById("file-input");
  const dropzone = document.getElementById("dropzone");
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
    const match = /filename="?([^";]+)"?/.exec(disposition);
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
    } catch (err) {
      setStatus("Network error. Please check your connection and try again.", "error");
    } finally {
      convertBtn.disabled = false;
    }
  });
})();
