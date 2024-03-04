import pytest

from app.main import main, parse_args
from base import BaseClass


class TestClass1(BaseClass):
    args = [
        "--disable-local-file-access",
        "--cookie",
        "session_id",
        "b93c54121419ae98e81a6e038d93b503b706e04c",
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
        "28.0",
        "--margin-right",
        "7.0",
        "--orientation",
        "Portrait",
        "--header-html",
        "/tmp/report.header.tmp.9vjh34yx.html",
        "--footer-html",
        "/tmp/report.footer.tmp.0khx6434.html",
        "/tmp/report.body.tmp.0.uwctzvc6.html",
        "/tmp/report.tmp.gzumzohi.pdf",
    ]

    dict_args = {
        "disable-local-file-access": None,
        "cookie": ["session_id", "b93c54121419ae98e81a6e038d93b503b706e04c"],
        "quiet": None,
        "page-size": "A4",
        "margin-top": "40.0",
        "dpi": "90",
        "zoom": "1.0666666666666667",
        "header-spacing": "35",
        "margin-left": "7.0",
        "margin-bottom": "28.0",
        "margin-right": "7.0",
        "orientation": "Portrait",
        "header-html": "/tmp/report.header.tmp.9vjh34yx.html",
        "footer-html": "/tmp/report.footer.tmp.0khx6434.html",
    }

    output = "/tmp/report.tmp.gzumzohi.pdf"
    bodies = ["/tmp/report.body.tmp.0.uwctzvc6.html"]
    cookies = ["session_id", "b93c54121419ae98e81a6e038d93b503b706e04c"]
