"""R7-91 (17 Nov 2026): the image tools decode only JPEG, PNG, WEBP and HEIF.

Files in any other format (TIFF, BMP, GIF, ...) are refused with the usual
"not a valid image" message before one of Pillow's other decoders runs,
whatever the file is called. iPhone multi-picture JPEGs (MPO) still work.
"""
import io
import os

import pytest
from PIL import Image

from converters.images import convert_images, images_to_pdf
from converters.office import ConversionError


def _save(tmp_path, name, fmt, **kw):
    p = tmp_path / name
    Image.new("RGB", (40, 30), (200, 30, 30)).save(p, fmt, **kw)
    return str(p)


@pytest.mark.parametrize("fmt", ["TIFF", "BMP", "GIF", "TGA", "PPM"])
def test_other_formats_refused_in_jpg_to_pdf(tmp_path, fmt):
    src = _save(tmp_path, "disguised.jpg", fmt)  # wrong extension on purpose
    with pytest.raises(ConversionError, match="not a valid image"):
        images_to_pdf([src], str(tmp_path / "out.pdf"))


@pytest.mark.parametrize("fmt", ["TIFF", "BMP", "GIF"])
def test_other_formats_refused_in_convert_images(tmp_path, fmt):
    src = _save(tmp_path, "disguised.png", fmt)
    out = tmp_path / "out"
    out.mkdir()
    with pytest.raises(ConversionError):
        convert_images([src], str(out), "JPEG", ["disguised.jpg"])
    assert not os.listdir(out)


@pytest.mark.parametrize("name,fmt,target", [
    ("a.jpg", "JPEG", "PNG"),
    ("a.png", "PNG", "JPEG"),
    ("a.webp", "WEBP", "PNG"),
])
def test_accepted_formats_still_convert(tmp_path, name, fmt, target):
    src = _save(tmp_path, name, fmt)
    out = tmp_path / "out"
    out.mkdir()
    ext = ".png" if target == "PNG" else ".jpg"
    written = convert_images([src], str(out), target, ["a" + ext])
    assert written and os.path.getsize(written[0]) > 0


def test_jpg_and_png_still_make_a_pdf(tmp_path):
    a = _save(tmp_path, "a.jpg", "JPEG")
    b = _save(tmp_path, "b.png", "PNG")
    out = images_to_pdf([a, b], str(tmp_path / "out.pdf"))
    with open(out, "rb") as f:
        assert f.read(5) == b"%PDF-"


def test_iphone_style_mpo_jpeg_still_opens(tmp_path):
    p = tmp_path / "iphone.jpg"
    frames = [Image.new("RGB", (40, 30), c) for c in ((10, 10, 200), (200, 200, 10))]
    frames[0].save(p, "MPO", save_all=True, append_images=frames[1:])
    with Image.open(p) as im:
        assert im.format == "MPO"  # really a multi-picture file
    out = images_to_pdf([str(p)], str(tmp_path / "out.pdf"))
    assert os.path.getsize(out) > 0


def test_heic_still_converts(tmp_path):
    pi_heif = pytest.importorskip("pi_heif")
    pi_heif.register_heif_opener()
    p = tmp_path / "photo.heic"
    try:
        Image.new("RGB", (40, 30), (20, 120, 20)).save(p, "HEIF")
    except Exception as exc:  # encoder not available in this build
        pytest.skip(f"no HEIF encoder: {exc}")
    out = tmp_path / "out"
    out.mkdir()
    written = convert_images([str(p)], str(out), "JPEG", ["photo.jpg"])
    assert written and os.path.getsize(written[0]) > 0
