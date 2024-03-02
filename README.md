
# Wkhtmltopdf API Wrapper

_**wkhtmltopdf-api** Command Line Tool_

![PyPI](https://img.shields.io/pypi/v/wkhtmltopdf-api) ![PyPI](https://img.shields.io/pypi/pyversions/wkhtmltopdf-api)


In short, the script acts as a wrapper for Wkhtmltopdf. It replaces the local binary and transfers the job of generating pdf files to an external api.



## Installation

Install from PyPI:
```bash
pip install wkhtmltopdf-api
```

## Configuration

### Environment vars

  - REPORT_API_URL: str, required


  - REPORT_API_TIMEOUT: seconds, default 300
  - REPORT_API_SIZE_LIMIT: bytes, default 100000000 (100mb)
  - WKHTMLTOPDF_VERSION: str, default 0.12.6


### Usage



Same as wkhtmltopdf, see options : https://wkhtmltopdf.org/usage/wkhtmltopdf.txt

```bash
wkhtmltopdf-api --disable-local-file-access --cookie session_id abcd --quiet --page-size A4 --margin-top 40.0 --dpi 90 --zoom 1.0666666666666667 --header-spacing 35 --margin-left 7.0 --margin-bottom 28.0 --margin-right 7.0 --orientation Portrait --header-html /tmp/report.header.tmp.xxx.html --footer-html /tmp/report.footer.tmp.xxx.html /tmp/report.body.tmp.xxx.html /tmp/report.tmp.xxx.pdf

```

