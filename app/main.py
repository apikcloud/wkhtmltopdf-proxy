import logging
import os
import sys
import requests
from functools import wraps
import time
from typing import List

from logging import Formatter, getLogger, FileHandler

_logger = getLogger(__name__)
_logger.setLevel(logging.DEBUG)

DEFAULT_TIMEOUT = 600
DEFAULT_VERSION = "0.12.6"
LIMIT_SIZE = 100000000
LOG_FILEPATH = os.path.join(os.path.expanduser("~"), "wkhtmltopdf.log")
REPORT_API_URL = os.getenv("REPORT_API_URL")

handler = FileHandler(LOG_FILEPATH)

formatter = Formatter(
    fmt="%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d %(levelname)s - '%(message)s'",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(formatter)
_logger.addHandler(handler)


def logs(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        _logger.info("%s: start", function.__qualname__)
        output = function(*args, **kwargs)

        end = time.perf_counter()
        message = f"{function.__qualname__}: end ({end - start:.6f})"
        _logger.info(message)

        return output

    return wrapper


@logs
def parse_args(args: List) -> dict:
    def is_arg(value):
        return value.startswith("--")

    def find_values(items, start):
        for item in items[start:]:
            if is_arg(item):
                break
            yield item

    def removeprefix(value, prefix="--"):
        # Python <= 3.8
        return value.replace(prefix, "") if value.startswith(prefix) else value

    vals = {
        "output": args.pop(),
        "header": False,
        "footer": False,
    }
    dict_args = {}
    first_index, last_index = 0, 0

    for key in ["--header-html", "--footer-html"]:
        if key in args:
            name = removeprefix(key)
            index = args.index(key)

            vals[name] = True
            if index < first_index:
                first_index = index
            if index + 1 > last_index:
                last_index = index + 1

    command_args = args[: first_index - 1]
    for index, item in enumerate(command_args):
        if not is_arg(item):
            continue

        name = removeprefix(item)
        dict_args.setdefault(name)

        values = list(iter(find_values(command_args, index + 1)))
        if not values:
            dict_args[name] = None
        elif len(values) == 1:
            dict_args[name] = values[0]
        else:
            dict_args[name] = values

    vals.update(
        {
            "dict_args": dict_args,
            "bodies": args[last_index + 1 :],
        }
    )

    return vals


def get_version() -> str:
    version = os.getenv("WKHTMLTOPDF_VERSION", DEFAULT_VERSION)
    return f"wkhtmltopdf {version} (with patched qt)"


def get_timeout() -> int:
    timeout = os.getenv("REPORT_API_TIMEOUT", DEFAULT_TIMEOUT)
    return int(timeout)


@logs
def send_request(url: str, files: List, data: dict, output_filepath: str) -> None:
    with requests.post(
        url, files=files, data=data, stream=True, timeout=get_timeout()
    ) as response:
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            _logger.error(error)
            sys.exit("Error, %s", error)

        _logger.debug(response.headers)

        with open(output_filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)


def sizeof(paths: List[str]) -> int:
    return sum([os.stat(path).st_size for path in paths])


def guess_output(paths: List) -> str:
    total = sizeof(paths)
    _logger.warning("Total size of files: %d", total)

    return "auto" if total >= LIMIT_SIZE else "standard"


@logs
def main() -> None:
    args = sys.argv[1:]

    if not REPORT_API_URL:
        _logger.error("Report API url is not defined.")
        sys.exit("Report API url is not defined.")

    if not args:
        sys.exit(0)

    if len(args) == 1 and args[0] == "--version":
        return get_version()

    parsed_args = parse_args(args)

    header_path = parsed_args["dict_args"].get("header-html", "")
    footer_path = parsed_args["dict_args"].get("footer-html", "")
    paths = parsed_args.get("bodies", [])

    if header_path:
        paths.append(header_path)

    if footer_path:
        paths.append(footer_path)

    _logger.debug("Paths: %s", paths)

    files = [("files", open(path, "rb")) for path in paths if os.path.exists(path)]

    if not files:
        _logger.error("No files provided.")
        sys.exit("No files provided.")

    data = {
        "args": parsed_args["dict_args"],
        "header": header_path,
        "footer": footer_path,
        "output": guess_output(paths),
        "clean": False,
    }

    url = REPORT_API_URL
    url += "/pdf"

    send_request(url, files, data, parsed_args["output"])

    sys.exit(0)
