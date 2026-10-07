"""Run one conversion in its own child process with a memory cap.

Added 2026-10-07 after Render restarted the whole server twice ("Ran out of
memory (used over 2GB)", 7 Oct 2026, 4:28 and 4:29 PM PKT). Before this,
every conversion ran inside the web worker itself, so one very large or
unusual file could push the entire 2 GB instance over its limit and take the
site offline for everyone for about a minute.

Now each conversion runs in a short-lived child process (os.fork) with a
memory cap (RLIMIT_DATA). The cap is inherited by everything the child
starts -- LibreOffice, Ghostscript and poppler (pdftoppm) -- so if a file
needs more memory than the cap allows, only that one conversion fails and
the visitor gets a clear message; the website itself stays up.

Settings (Render > Environment; both optional):
  JOB_MEMORY_MB        memory allowance per conversion, default 700 (MB),
                       on top of the web worker's own starting size
  JOB_TIMEOUT_SECONDS  hard time limit per conversion, default 170 (s);
                       gunicorn's own request timeout is 180 s
With CONVERT_SLOTS=1 (one conversion at a time per worker, 2 workers) the
worst case is about 2 x 700 MB plus the two workers themselves, which stays
under the 2 GB instance limit.

Measured 2026-10-07 (test files, 700 MB cap): Word to PDF, PowerPoint to
PDF, PDF to Word (text PDF), PDF to Excel, PDF to JPG (20 scanned pages),
PDF to PowerPoint, Compress PDF and JPG to PDF all finished normally (peak
60-290 MB). PDF to Word on a 20-page scanned PDF (13 MB) needs a larger
allowance (it failed at 1,000 and 1,100 MB and succeeded at 1,500 MB), so at
700 MB it now gets the "too large" message instead of risking a server
restart. Raising JOB_MEMORY_MB to 1500 would allow it, but then two such
files at once could again exceed 2 GB.
"""
import json
import os
import resource
import select
import signal
import time

JOB_MEMORY_MB = int(os.environ.get("JOB_MEMORY_MB", "700"))
JOB_TIMEOUT_SECONDS = int(os.environ.get("JOB_TIMEOUT_SECONDS", "170"))

TOO_LARGE_MESSAGE = (
    "This file is too large or complex to convert on our server. "
    "Please try a smaller file, or split a long PDF with Split PDF and convert it in parts."
)
TOO_SLOW_MESSAGE = (
    "The conversion took too long. The file may be very large or complex -- "
    "please try a smaller file."
)


_OOM_HINTS = ("malloc", "out of memory", "cannot allocate", "bad_alloc", "memoryerror")


def is_out_of_memory(exc):
    """True if exc means the memory cap was hit. Python raises MemoryError,
    but some libraries report it differently -- e.g. PyMuPDF (used by
    pdf2docx) raises FzErrorSystem("malloc (... bytes) failed")."""
    if isinstance(exc, MemoryError):
        return True
    text = ("%s %s" % (type(exc).__name__, exc)).lower()
    return any(hint in text for hint in _OOM_HINTS)


class JobFailed(Exception):
    """The isolated conversion could not finish (memory cap, crash or time limit).
    str(exc) is the message for the visitor; exc.detail is a short technical
    note for the server log (never contains file names or file content)."""

    def __init__(self, message, detail=""):
        super().__init__(message)
        self.detail = detail or "no detail"


def _vm_data_mb():
    """This process's current data/heap size in MB (Linux /proc), or 0."""
    try:
        with open("/proc/self/status") as fh:
            for line in fh:
                if line.startswith("VmData:"):
                    return int(line.split()[1]) // 1024
    except (OSError, ValueError, IndexError):
        pass
    return 0


def _child(func, args, write_fd, conversion_error_cls):
    """Runs in the child process only. Never returns (always os._exit)."""
    exit_code = 1
    try:
        os.setpgid(0, 0)  # own process group, so a timeout can stop LibreOffice too
        # The child starts with a copy of the web worker's address space
        # (mostly shared, untouched memory). The cap is set as an ALLOWANCE on
        # top of that starting size, so the worker's own size never eats into
        # the memory a conversion may use. (Fix 7 Oct 2026: an absolute cap
        # made PDF to Word fail on Render, even for a 3-page file.)
        base_mb = _vm_data_mb()
        limit = (base_mb + JOB_MEMORY_MB) * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_DATA, (limit, limit))
        try:
            out_path, download_name, mimetype = func(*args)
            payload = {"ok": True, "out_path": out_path,
                       "download_name": download_name, "mimetype": mimetype}
        except conversion_error_cls as exc:
            if is_out_of_memory(exc):  # e.g. "...: std::bad_alloc"
                payload = {"ok": False, "kind": "memory", "error": type(exc).__name__,
                           "base_mb": base_mb, "peak_mb": _vm_data_mb()}
            else:
                payload = {"ok": False, "kind": "conversion", "message": str(exc)}
        except BaseException as exc:  # noqa: BLE001 -- reported to the parent
            if is_out_of_memory(exc):
                payload = {"ok": False, "kind": "memory", "error": type(exc).__name__,
                           "base_mb": base_mb, "peak_mb": _vm_data_mb()}
            else:
                payload = {"ok": False, "kind": "error", "error": type(exc).__name__}
        data = json.dumps(payload).encode("utf-8")
        view = memoryview(data)
        while view:
            n = os.write(write_fd, view)
            view = view[n:]
        exit_code = 0
    except BaseException:  # noqa: BLE001
        pass
    finally:
        os._exit(exit_code)


def run_isolated(func, args, conversion_error_cls):
    """Call func(*args) in a memory-capped child process.

    func must return (out_path, download_name, mimetype) and write its output
    file to disk (the parent reads it back from the same path).
    Raises conversion_error_cls(message) for normal conversion errors, and
    JobFailed(message) if the child ran out of memory, crashed or timed out.
    """
    read_fd, write_fd = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(read_fd)
        _child(func, args, write_fd, conversion_error_cls)  # never returns

    os.close(write_fd)
    chunks = []
    deadline = time.monotonic() + JOB_TIMEOUT_SECONDS
    timed_out = False
    try:
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                timed_out = True
                break
            ready, _, _ = select.select([read_fd], [], [], min(remaining, 1.0))
            if ready:
                chunk = os.read(read_fd, 65536)
                if not chunk:
                    break  # child closed the pipe (finished or died)
                chunks.append(chunk)
    finally:
        os.close(read_fd)

    if timed_out:
        try:
            os.killpg(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    _, status = os.waitpid(pid, 0)
    # Make sure nothing the child started (e.g. LibreOffice) is left running.
    try:
        os.killpg(pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass

    if timed_out:
        raise JobFailed(TOO_SLOW_MESSAGE, "time limit %ss" % JOB_TIMEOUT_SECONDS)

    try:
        payload = json.loads(b"".join(chunks).decode("utf-8"))
    except ValueError:
        payload = None
    if not payload:
        # Child was killed or crashed before reporting (typically memory).
        if os.WIFSIGNALED(status):
            how = "killed by signal %d" % os.WTERMSIG(status)
        else:
            how = "exit code %d" % os.WEXITSTATUS(status)
        raise JobFailed(TOO_LARGE_MESSAGE, "child ended without result, %s" % how)
    if payload.get("ok"):
        return payload["out_path"], payload["download_name"], payload["mimetype"]
    if payload.get("kind") == "conversion":
        raise conversion_error_cls(payload.get("message") or "Conversion failed.")
    if payload.get("kind") == "memory":
        raise JobFailed(TOO_LARGE_MESSAGE, "memory cap: %s, start %s MB + allowance %s MB, at failure %s MB" % (
            payload.get("error"), payload.get("base_mb"), JOB_MEMORY_MB, payload.get("peak_mb")))
    # Any other unexpected error inside the child.
    raise RuntimeError("Isolated conversion failed: %s" % payload.get("error", "unknown"))
