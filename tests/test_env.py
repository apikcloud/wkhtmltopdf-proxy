# Copyright 2025 apik (https://apik.cloud).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import os
import unittest
from unittest.mock import patch

import wkhtmltopdf_proxy.main as wk


class TestWkhtmltopdfProxyEnv(unittest.TestCase):
    def test_get_version_default(self):
        if "WKHTMLTOPDF_PROXY_VERSION" in os.environ:
            del os.environ["WKHTMLTOPDF_PROXY_VERSION"]
        expected = f"wkhtmltopdf {wk.DEFAULT_VERSION} (with patched qt)"
        self.assertEqual(wk.get_version(), expected)

    def test_get_version_env_set(self):
        with patch.dict(os.environ, {"WKHTMLTOPDF_PROXY_VERSION": "0.13.0"}):
            expected = "wkhtmltopdf 0.13.0 (with patched qt)"
            self.assertEqual(wk.get_version(), expected)

    def test_get_timeout_default(self):
        if "WKHTMLTOPDF_PROXY_TIMEOUT" in os.environ:
            del os.environ["WKHTMLTOPDF_PROXY_TIMEOUT"]
        self.assertEqual(wk.get_timeout(), wk.DEFAULT_TIMEOUT)

    def test_get_timeout_env_set(self):
        with patch.dict(os.environ, {"WKHTMLTOPDF_PROXY_TIMEOUT": "60"}):
            expected = 60
            self.assertEqual(wk.get_timeout(), expected)

    def test_get_url_default(self):
        if "WKHTMLTOPDF_PROXY_URL" in os.environ:
            del os.environ["WKHTMLTOPDF_PROXY_URL"]
        self.assertEqual(wk.get_url(), "")

    def test_get_url_env_set(self):
        with patch.dict(os.environ, {"WKHTMLTOPDF_PROXY_URL": "http://custom-url:8080"}):
            expected = "http://custom-url:8080"
            self.assertEqual(wk.get_url(), expected)

    def test_get_mode_default(self):
        if "WKHTMLTOPDF_PROXY_MODE" in os.environ:
            del os.environ["WKHTMLTOPDF_PROXY_MODE"]
        self.assertEqual(wk.get_mode(), "remote")

    def test_get_mode_env_set(self):
        with patch.dict(os.environ, {"WKHTMLTOPDF_PROXY_MODE": "AUTO"}):
            expected = "auto"
            self.assertEqual(wk.get_mode(), expected)

    def test_get_threshold_default(self):
        if "WKHTMLTOPDF_PROXY_THRESHOLD" in os.environ:
            del os.environ["WKHTMLTOPDF_PROXY_THRESHOLD"]
        self.assertEqual(wk.get_threshold(), wk.DEFAULT_THRESHOLD)

    def test_get_threshold_env_set(self):
        with patch.dict(os.environ, {"WKHTMLTOPDF_PROXY_THRESHOLD": "10485760"}):
            expected = 10485760
            self.assertEqual(wk.get_threshold(), expected)
