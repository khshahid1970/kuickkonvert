"""Shared helpers: temp workspace management and safe filenames."""
import os
import shutil
import tempfile
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
