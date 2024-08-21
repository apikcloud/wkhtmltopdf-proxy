from base import BaseClass


class TestClass2(BaseClass):
    args = [
        "--disable-local-file-access",
        "--quiet",
        "--page-size",
        "A4",
        "--orientation",
        "Portrait",
        "--header-html",
        "/tmp/report.header.tmp.9vjh34yx.html",
        "/tmp/report.body.tmp.0.uwctzvc6.html",
        "/tmp/report.tmp.gzumzohi.pdf",
    ]

    dict_args = {
        "disable-local-file-access": None,
        "quiet": None,
        "page-size": "A4",
        "orientation": "Portrait",
        "header-html": "/tmp/report.header.tmp.9vjh34yx.html",
    }

    output = "/tmp/report.tmp.gzumzohi.pdf"
    bodies = ["/tmp/report.body.tmp.0.uwctzvc6.html"]
