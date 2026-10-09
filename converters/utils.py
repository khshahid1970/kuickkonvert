"""Shared helpers: temp workspace management and safe filenames."""
import os
import re
import shutil
import tempfile
import time
import uuid
from contextlib import contextmanager

from werkzeug.utils import secure_filename

# Root temp directory for this app's ephemeral work. Nothing here is ever
# treated as permanent storage -- every conversion gets its own subfolder
# that is deleted immediately after the response is sent (see app.py).
BASE_TMP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tmp")
os.makedirs(BASE_TMP_DIR, exist_ok=True)


@contextmanager
def job_workspace():
    """Yield a fresh, isolated temp directory for one conversion job.

    The directory (and everything written into it -- uploaded originals,
    intermediate files, and the final output) is deleted as soon as the
    'with' block exits, whether it succeeded or raised.
    """
    job_id = uuid.uuid4().hex
    path = os.path.join(BASE_TMP_DIR, job_id)
    os.makedirs(path, exist_ok=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def safe_name(filename: str) -> str:
    name = secure_filename(filename or "file")
    return name or "file"


def change_ext(filename: str, new_ext: str) -> str:
    base = os.path.splitext(safe_name(filename))[0] or "file"
    return f"{base}.{new_ext.lstrip('.')}"


def make_tempdir(prefix="kk_"):
    return tempfile.mkdtemp(prefix=prefix, dir=BASE_TMP_DIR)


# ---- Temp files of helper programs (added 9 Oct 2026, forensic audit E3) --
# LibreOffice and Ghostscript write their own working files to the system
# temp folder (TMPDIR, /tmp by default) -- outside the job folder that
# job_workspace() deletes. On a normal exit they tidy up, but a job stopped
# for taking too long left those files behind (reproduced: a partial PDF of
# the document from LibreOffice, ~54 MB of gs_* files from Ghostscript).
# subprocess_env() points TMPDIR into the job folder, so those files are
# deleted with it; sweep_stale_temp() removes anything left over from before
# the fix or from a worker that died mid-job.

def subprocess_env(job_dir: str) -> dict:
    """Environment for a helper program whose temp files must stay inside job_dir."""
    tmp = os.path.join(job_dir, "_tmp")
    os.makedirs(tmp, exist_ok=True)
    env = dict(os.environ)
    env.update({"TMPDIR": tmp, "TMP": tmp, "TEMP": tmp})
    return env


# Names LibreOffice and Ghostscript use in the system temp folder (OSL_PIPE_*
# is an empty socket LibreOffice leaves when it is stopped -- no file content).
_STALE_TMP_NAME = re.compile(r"^(gs_\w+|lu\w{4,}(\.tmp)?|OSL_PIPE_\w+)$")
# Job folders inside BASE_TMP_DIR (never touches anything else there, e.g. .gitkeep).
_JOB_DIR_NAME = re.compile(r"^([0-9a-f]{32}|kk_\w+)$")


def sweep_stale_temp(max_age_seconds: int = 1800) -> int:
    """Delete job folders and helper-program temp files older than max_age_seconds.

    Safe to run while other conversions are in progress: a conversion is
    stopped after 170 s, so nothing that old is still in use. Returns the
    number of entries removed."""
    removed = 0
    cutoff = time.time() - max_age_seconds
    candidates = []
    try:
        # only job folders (uuid hex names from job_workspace, kk_* from make_tempdir)
        candidates += [os.path.join(BASE_TMP_DIR, n) for n in os.listdir(BASE_TMP_DIR)
                       if _JOB_DIR_NAME.match(n)]
    except OSError:
        pass
    system_tmp = tempfile.gettempdir()
    try:
        candidates += [os.path.join(system_tmp, n) for n in os.listdir(system_tmp)
                       if _STALE_TMP_NAME.match(n)]
    except OSError:
        pass
    for path in candidates:
        try:
            if os.lstat(path).st_mtime > cutoff:
                continue
            if os.path.isdir(path) and not os.path.islink(path):
                shutil.rmtree(path, ignore_errors=True)
            else:
                os.remove(path)
            removed += 1
        except OSError:
            pass
    return removed
