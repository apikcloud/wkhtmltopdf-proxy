import pytest

from app.main import main, parse_args
from base import BaseClass


class TestClass3(BaseClass):
    args = [
        "--disable-local-file-access",
        "--quiet",
        "--page-size",
        "A4",
        "--margin-top",
        "40.0",
        "--dpi",
        "90",
        "--zoom",
        "1.0666666666666667",
        "--header-spacing",
        "35",
        "--margin-left",
        "7.0",
        "--margin-bottom",
        "32.0",
        "--margin-right",
        "7.0",
        "--orientation",
        "Portrait",
        "--javascript-delay",
        "1000",
        "--cookie-jar",
        "test_3_cookie.txt",
        "--header-html",
        "/tmp/report.header.tmp.mhumnhzg.html",
        "--footer-html",
        "/tmp/report.footer.tmp.rgg3nfk0.html",
        "/tmp/report.body.tmp.0.2x3usqzz.html",
        "/tmp/output.pdf",
    ]

    dict_args = {
        "disable-local-file-access": None,
        "quiet": None,
        "page-size": "A4",
        "margin-top": "40.0",
        "dpi": "90",
        "zoom": "1.0666666666666667",
        "header-spacing": "35",
        "margin-left": "7.0",
        "margin-bottom": "32.0",
        "margin-right": "7.0",
        "orientation": "Portrait",
        "javascript-delay": "1000",
        "header-html": "/tmp/report.header.tmp.mhumnhzg.html",
        "footer-html": "/tmp/report.footer.tmp.rgg3nfk0.html",
        "cookie": ["session_id", "af8671bxxxxxxxxxxxxxxxx"],
    }

    output = "/tmp/output.pdf"
    bodies = ["/tmp/report.body.tmp.0.2x3usqzz.html"]
