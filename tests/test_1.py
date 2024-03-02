from app.core.tools import parse_args


def test_base_url():
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

    res = parse_args(args)

    assert res["output"] == "/tmp/report.tmp.gzumzohi.pdf"

    assert len(res["dict_args"].keys()) == 14

    assert list(res["dict_args"].keys()) == [
        "disable-local-file-access",
        "cookie",
        "quiet",
        "page-size",
        "margin-top",
        "dpi",
        "zoom",
        "header-spacing",
        "margin-left",
        "margin-bottom",
        "margin-right",
        "orientation",
        "header-html",
        "footer-html",
    ]

    assert list(res["dict_args"].values()) == [
        None,
        ["session_id", "b93c54121419ae98e81a6e038d93b503b706e04c"],
        None,
        "A4",
        "40.0",
        "90",
        "1.0666666666666667",
        "35",
        "7.0",
        "28.0",
        "7.0",
        "Portrait",
        "/tmp/report.header.tmp.9vjh34yx.html",
        "/tmp/report.footer.tmp.0khx6434.html",
    ]

    assert res["bodies"] == ["/tmp/report.body.tmp.0.uwctzvc6.html"]
