# Copyright 2025 apik (https://apik.cloud).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import unittest
from unittest.mock import patch

import wkhtmltopdf_proxy.main as wk


class TestWkhtmltopdfMain(unittest.TestCase):

    def test_local_mode_execvp_called(self):
        args = ["--some-arg", "value", "output.pdf"]
        with patch("os.execvp") as mock_execvp, \
            patch("wkhtmltopdf_proxy.main.get_url", return_value="http://example.com"), \
            patch("wkhtmltopdf_proxy.main.get_mode", return_value="local"):
            wk.main(args)
            mock_execvp.assert_called_once_with("wkhtmltopdf", ["wkhtmltopdf"] + args)

    def test_invalid_mode_exits(self):
        args = ["--some-arg", "value", "output.pdf"]
        with patch("wkhtmltopdf_proxy.main.get_url", return_value="http://example.com"), \
            patch("wkhtmltopdf_proxy.main.get_mode", return_value="invalid_mode"), \
            patch("sys.exit") as mock_exit:
            wk.main(args)
            mock_exit.assert_called_once()

    def test_auto_mode_below_threshold_execvp_called(self):
        args = ["--some-arg", "value", "output.pdf"]
        with patch("os.execvp") as mock_execvp, \
            patch("wkhtmltopdf_proxy.main.get_url", return_value="http://example.com"), \
            patch("wkhtmltopdf_proxy.main.get_mode", return_value="auto"), \
            patch("wkhtmltopdf_proxy.main.get_threshold", return_value=10485760), \
            patch("wkhtmltopdf_proxy.main.sizeof", return_value=1024):
            wk.main(args)
            mock_execvp.assert_called_once_with("wkhtmltopdf", ["wkhtmltopdf"] + args)

    def test_auto_mode_above_threshold_send_request_called(self):
        args = ["--some-arg", "value", "output.pdf"]
        with patch("wkhtmltopdf_proxy.main.send_request") as mock_send_request, \
            patch("wkhtmltopdf_proxy.main.get_url", return_value="http://example.com"), \
            patch("wkhtmltopdf_proxy.main.get_mode", return_value="auto"), \
            patch("wkhtmltopdf_proxy.main.get_threshold", return_value=1024), \
            patch("wkhtmltopdf_proxy.main.sizeof", return_value=10485760):
            wk.main(args)
            mock_send_request.assert_called_once()

    def test_remote_mode_send_request_called(self):
        args = ["--some-arg", "value", "output.pdf"]
        with patch("wkhtmltopdf_proxy.main.send_request") as mock_send_request, \
            patch("wkhtmltopdf_proxy.main.get_url", return_value="http://example.com"), \
            patch("wkhtmltopdf_proxy.main.get_mode", return_value="remote"):
            wk.main(args)
            mock_send_request.assert_called_once()
