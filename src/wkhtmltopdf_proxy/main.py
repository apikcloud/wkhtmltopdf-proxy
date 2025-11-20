import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass
from functools import wraps
from typing import List, Literal, cast

import requests

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


@dataclass(frozen=True)
class ProxyConfig:
    timeout: int
    version: str
    threshold: int
    clean_html: bool
    mode: Literal["auto", "local", "remote"]
    url: str
    skip_cookie: bool = False

    @classmethod
    def load(cls) -> "ProxyConfig":
        """Load configuration from environment variables."""
        mode = os.getenv("WKHTMLTOPDF_PROXY_MODE", "remote").lower()
        if mode not in VALID_MODES:
            logging.warning(f"Invalid mode '{mode}', falling back to 'remote'")
            mode = "remote"

        return cls(
            timeout=int(os.getenv("WKHTMLTOPDF_PROXY_TIMEOUT", 600)),
            version=os.getenv("WKHTMLTOPDF_PROXY_VERSION", "0.12.6"),
            threshold=int(os.getenv("WKHTMLTOPDF_PROXY_THRESHOLD", 2 * 1024 * 1024)),
            clean_html=bool(int(os.getenv("WKHTMLTOPDF_CLEAN_HTML", 0))),
            mode=cast(Literal["auto", "local", "remote"], mode),
            url=os.getenv("WKHTMLTOPDF_PROXY_URL", ""),
            skip_cookie=bool(int(os.getenv("WKHTMLTOPDF_PROXY_SKIP_COOKIE", 0))),
        )

    @property
    def version_string(self) -> str:
        return f"wkhtmltopdf {self.version} (with patched qt)"

    def to_json(self) -> str:
        return json.dumps(self.__dict__, indent=2)


@logs
def parse_args(input_args: List, skip_cookie: bool = False) -> dict:
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

    logging.debug(f"Input arguments: \n{input_args}")

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

    # Handle cookie-jar to extract session_id cookie
    if not skip_cookie and (cookie_jar := dict_args.pop("cookie-jar", None)):
        with open(cookie_jar, encoding="utf-8") as file:
            match = re.search(SESSION_PATTERN, file.read().strip())

            if match and (cookie := match.group(0).split("=")):
                # Cookies must be paired by name and value.
                # session_id=af8671bxxxxxxxxxxxxxxxx; HttpOnly; domain=test.com; path=/;
                # https://stackoverflow.com/questions/58571962/how-to-send-cookies-with-pdfkit-in-python

                dict_args["cookie"] = [(cookie[0], cookie[1])]

    vals.update(
        {
            "dict_args": dict_args,
            "bodies": args[last_index + 1 :],
        }
    )

    logging.debug(f"Parsed values: \n{vals}")

    return vals


@logs
def send_request(
    url: str, files: List, data: dict, output_filepath: str, **kwargs
) -> None:
    with requests.post(url, files=files, data=data, stream=True, **kwargs) as response:
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


def guess_output(paths: List, threshold: int) -> str:
    # TODO: don't remember why I did this
    total = sizeof(paths)
    logging.warning("Total size of files: %d", total)

    return "auto" if total >= threshold else "standard"


def minify_html(html: str) -> str:
    """Minify HTML by removing extra whitespace and line breaks."""

    lines = html.splitlines()
    compact = [line.strip() for line in lines if line.strip()]
    return "".join(compact)


@logs
def main(args: list | None = None) -> None:
    if args is None:
        args = []

    if not args:
        args = sys.argv[1:]

    if not args:
        sys.exit(0)

    logging.debug(" ".join(args))

    config = ProxyConfig.load()

    # Emulate wkhtmltopdf version command
    if len(args) == 1 and args[0] == "--version":
        print(config.version_string)
        sys.exit(0)

    if not config.url:
        logging.error("Proxy URL is not defined.")
        sys.exit("Proxy URL is not defined.")

    if config.mode not in VALID_MODES:
        logging.error("Invalid mode: %s", config.mode)
        sys.exit(
            f"Invalid proxy mode '{config.mode}'. Must be one of {', '.join(VALID_MODES)}."
        )

    logging.info("New wkhtmltopdf proxy request")
    logging.info(f"Using configuration: {config.to_json()}")

    # TODO: Implement local mode. Act as a wrapper to local wkhtmltopdf binary.
    if config.mode == "local":
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

    # Clean HTML files if enabled
    if config.clean_html:
        for path in paths:
            if not os.path.exists(path):
                continue

            old_size = os.stat(path).st_size

            with open(path, encoding="utf-8", mode="r+") as file:
                minified_content = minify_html(file.read())
                file.seek(0)
                file.write(minified_content)
                file.truncate()

            new_size = os.stat(path).st_size
            logging.info(f"Minified {path}: {old_size} bytes to {new_size} bytes")

    # Prepare files for request (multipart/form-data)
    files = [("files", open(path, "rb")) for path in paths if os.path.exists(path)]

    if not files:
        logging.error("No files provided.")
        sys.exit("No files provided.")

    # Auto mode: decide based on total size of files
    if config.mode == "auto" and sizeof(paths) < config.threshold:
        logging.info(
            "Total size of files (%d bytes) is below threshold (%d bytes). Using local wkhtmltopdf.",
            sizeof(paths),
            config.threshold,
        )
        return os.execvp("wkhtmltopdf", ["wkhtmltopdf"] + args)

    # Header and footer filenames need to be known by the API
    for key in ["header-html", "footer-html"]:
        if value := parsed_args["dict_args"].get(key):
            parsed_args["dict_args"][key] = os.path.basename(value)

    data_payload = {
        "args": json.dumps(parsed_args["dict_args"]),
        "header": os.path.basename(header_path),
        "footer": os.path.basename(footer_path),
        "output": guess_output(paths, config.threshold),
        "clean": config.clean_html,
    }

    logging.debug(f"Data: {data_payload['args']}")

    send_request(config.url, files, data_payload, parsed_args["output"])

    sys.exit(0)
