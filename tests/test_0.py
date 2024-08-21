import pytest

from app.main import main


def test_01_exit():
    with pytest.raises(SystemExit, match="Report API url is not defined."):
        main()


def test_02_version():
    # with pytest.raises(SystemExit):
    assert main(["--version"]) == "wkhtmltopdf 0.12.6 (with patched qt)"
