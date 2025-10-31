import json
import logging
import os
import re
import sys
import time
from functools import wraps
from typing import List

import requests
from icecream import ic

DEFAULT_TIMEOUT = 600
DEFAULT_VERSION = "0.12.6"
DEFAULT_THRESHOLD = 2 * 1024 * 1024
DEFAULT_LIMIT_SIZE = 100000000
VALID_MODES = {"auto", "local", "remote"}
SESSION_PATTERN = r"session_id=([^;]+)"

logging.basicConfig(
    level=logging.DEBUG,
    filename=os.path.join(os.path.expanduser("~"), "wkhtmltopdf.log"),
    format="%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d %(levelname)s - '%(message)s'",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def logs(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        logging.info("%s: start", function.__qualname__)
        output = function(*args, **kwargs)

        end = time.perf_counter()
        message = f"{function.__qualname__}: end ({end - start:.6f})"
        logging.info(message)

        return output

    return wrapper


def get_version() -> str:
    """Emulate wkhtmltopdf --version output."""

    version = os.getenv("WKHTMLTOPDF_PROXY_VERSION", DEFAULT_VERSION)
    return f"wkhtmltopdf {version} (with patched qt)"


def get_timeout() -> int:
    """Get the timeout for the report API requests."""

    timeout = os.getenv("WKHTMLTOPDF_PROXY_TIMEOUT", DEFAULT_TIMEOUT)
    return int(timeout)


def get_url() -> str:
    """Get the report API URL from environment variable."""

    return os.getenv("WKHTMLTOPDF_PROXY_URL", "")


def get_mode() -> str:
    """Get the proxy mode from environment variable."""

    return os.getenv("WKHTMLTOPDF_PROXY_MODE", "remote").lower()


def get_threshold() -> int:
    """Get the size threshold for auto mode from environment variable."""

    return int(os.getenv("WKHTMLTOPDF_PROXY_THRESHOLD", DEFAULT_THRESHOLD))


@logs
def parse_args(input_args: List) -> dict:
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

    args = input_args.copy()
    vals = {
        "output": args.pop(),
        "header": False,
        "footer": False,
        "header-html": False,
        "footer-html": False,
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

    # session_id=af8671bxxxxxxxxxxxxxxxx; HttpOnly; domain=test.com; path=/;
    if cookie_jar := dict_args.pop("cookie-jar", None):
        with open(cookie_jar, encoding="utf-8") as file:
            cookie = re.search(SESSION_PATTERN, file.read().strip()).group(0).split("=")
            # Cookies must be paired by name and value.
            # https://stackoverflow.com/questions/58571962/how-to-send-cookies-with-pdfkit-in-python
            # FIXME: Is it used? Even without it works...
            dict_args["cookie"] = [(cookie[0], cookie[1])]
            # TODO: make cookies

    vals.update(
        {
            "dict_args": dict_args,
            "bodies": args[last_index + 1:],
        }
    )

    return vals


@logs
def send_request(url: str, files: List, data: dict, output_filepath: str) -> None:
    with requests.post(
        url,
        files=files,
        data=data,
        stream=True,
        timeout=get_timeout()
    ) as response:
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            logging.error(error)
            sys.exit(f"Error during PDF generation: {error}")

        logging.debug(response.headers)

        with open(output_filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)


def sizeof(paths: List[str]) -> int:
    """Calculate the total size of given file paths in bytes."""
    return sum([os.stat(path).st_size for path in paths])


def guess_output(paths: List) -> str:
    # TODO: don't remember why I did this
    total = sizeof(paths)
    logging.warning("Total size of files: %d", total)

    return "auto" if total >= DEFAULT_LIMIT_SIZE else "standard"


@logs
def main(args: list = None) -> None:
    if args is None:
        args = []

    if not args:
        args = sys.argv[1:]

    if not args:
        sys.exit(0)

    # Emulate wkhtmltopdf version command
    if len(args) == 1 and args[0] == "--version":
        print(get_version())
        sys.exit(0)

    url = get_url()
    mode = get_mode()
    threshold = get_threshold()

    if not url:
        logging.error("Proxy URL is not defined.")
        sys.exit("Proxy URL is not defined.")

    if mode not in VALID_MODES:
        logging.error("Invalid mode: %s", mode)
        sys.exit(
            f"Invalid proxy mode '{mode}'. Must be one of {', '.join(VALID_MODES)}."
        )

    # TODO: Implement local mode. Act as a wrapper to local wkhtmltopdf binary.
    if mode == "local":
        logging.info("Using local wkhtmltopdf.")
        return os.execvp("wkhtmltopdf", ["wkhtmltopdf"] + args)

    parsed_args = parse_args(args)

    logging.debug(f"Parsed args: {parsed_args}")

    header_path = parsed_args["dict_args"].get("header-html", "")
    footer_path = parsed_args["dict_args"].get("footer-html", "")
    paths = parsed_args.get("bodies", [])

    if header_path:
        paths.append(header_path)

    if footer_path:
        paths.append(footer_path)

    logging.debug(f"Paths: {paths}")

    files = [("files", open(path, "rb")) for path in paths if os.path.exists(path)]

    if not files:
        logging.error("No files provided.")
        sys.exit("No files provided.")

    # TODO: Implement auto mode, decide based on total size of files.
    if mode == "auto" and sizeof(paths) < threshold:
        logging.info(
            "Total size of files (%d bytes) is below threshold (%d bytes). Using local wkhtmltopdf.",
            sizeof(paths),
            threshold,
        )
        raise NotImplementedError("Auto mode is not implemented yet.")

    for key in ["header-html", "footer-html"]:
        if value := parsed_args["dict_args"].get(key):
            parsed_args["dict_args"][key] = os.path.basename(value)

    # Construct the nested JSON structure to send to the API not to send a plain string.
    metadata_json_str = json.dumps(parsed_args["dict_args"])
    args_dict = {"metadata": metadata_json_str}
    args_payload_str = json.dumps(args_dict)

    data_payload = {
        "args": args_payload_str,
        "header": os.path.basename(header_path),
        "footer": os.path.basename(footer_path),
        "output": guess_output(paths),
        "clean": False,
    }

    logging.debug(f"Data: {args_payload_str}")

    send_request(url, files, data_payload, parsed_args["output"])

    sys.exit(0)
