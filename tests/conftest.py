"""Shared test setup (Release 10).

The test suite checks the official site's markup (Google tag, consent banner,
AdSense meta tag), which is only sent when KK_OFFICIAL_SITE=1 (R-2). Default
it to "1" here; tests for a self-hosted copy unset it with monkeypatch.
"""
import os

os.environ.setdefault("KK_OFFICIAL_SITE", "1")
