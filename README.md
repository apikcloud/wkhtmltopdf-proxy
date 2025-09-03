
# Wkhtmltopdf Proxy

_**Transparent wkhtmltopdf proxy with smart local/remote routing**_

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-BSD%202--clause-green)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha-orange)](https://github.com/apikcloud/wkhtmltopdf-proxy)

A smart drop-in replacement for wkhtmltopdf that can transparently delegate PDF rendering to a remote API or fall back to the local binary. Behavior can be controlled via environment variables and input file size thresholds.



## Installation

Install from source:
```bash
git clone https://github.com/apikcloud/wkhtmltopdf-proxy.git
cd wkhtmltopdf-proxy
pip install -e .
```

Or install directly from GitHub:
```bash
pip install git+https://github.com/apikcloud/wkhtmltopdf-proxy.git
```

## Configuration

### Environment Variables

**Required:**
- `WKHTMLTOPDF_PROXY_URL`: str, URL of the remote PDF generation API

**Optional:**
- `WKHTMLTOPDF_PROXY_MODE`: str, proxy mode - `remote` (default), `local`, or `auto`
- `WKHTMLTOPDF_PROXY_TIMEOUT`: int, request timeout in seconds (default: 600)
- `WKHTMLTOPDF_PROXY_THRESHOLD`: int, file size threshold in bytes for auto mode (default: 2MB)
- `WKHTMLTOPDF_PROXY_VERSION`: str, version to report when using `--version` flag (default: 0.12.6)

### Proxy Modes

- **remote**: Always use the remote API for PDF generation
- **local**: Use local wkhtmltopdf binary (not yet implemented)
- **auto**: Automatically choose between local and remote based on file size threshold (not yet implemented)


## Usage

The proxy acts as a drop-in replacement for wkhtmltopdf with identical command-line interface. All wkhtmltopdf options are supported - see: https://wkhtmltopdf.org/usage/wkhtmltopdf.txt

### Basic Usage

```bash
# Check version
wkhtmltopdf-proxy --version

# Generate PDF with same syntax as wkhtmltopdf
wkhtmltopdf-proxy [options] input.html output.pdf
```

### Example

```bash
wkhtmltopdf-proxy --disable-local-file-access \
  --cookie session_id abcd \
  --quiet \
  --page-size A4 \
  --margin-top 40.0 \
  --dpi 90 \
  --zoom 1.0666666666666667 \
  --header-spacing 35 \
  --margin-left 7.0 \
  --margin-bottom 28.0 \
  --margin-right 7.0 \
  --orientation Portrait \
  --header-html /tmp/report.header.tmp.xxx.html \
  --footer-html /tmp/report.footer.tmp.xxx.html \
  /tmp/report.body.tmp.xxx.html \
  /tmp/report.tmp.xxx.pdf
```

### Features

- **Transparent proxy**: Works exactly like wkhtmltopdf with no code changes required
- **Smart routing**: Choose between local and remote rendering based on file size (when implemented)
- **Cookie support**: Automatically handles session cookies from cookie jar files
- **Error handling**: Proper error reporting and exit codes
- **Logging**: Detailed logging to `~/wkhtmltopdf.log` for debugging

## Development Status

This project is currently in **alpha** status. The following features are planned but not yet implemented:

- `local` mode: Fallback to local wkhtmltopdf binary
- `auto` mode: Intelligent switching between local and remote based on file size threshold

Currently, only `remote` mode is fully functional.

## Requirements

- Python 3.8+
- requests library
- Access to a compatible PDF generation API endpoint

## License

This project is licensed under the BSD 2-Clause License.

## Author

Aurelien ROY <aro@apik.cloud>
