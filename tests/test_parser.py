# Copyright 2025 apik (https://apik.cloud).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import re
import unittest
from unittest.mock import mock_open, patch

import wkhtmltopdf_proxy.main as wk


class TestWkhtmltopdfProxyParser(unittest.TestCase):

    pass

# def parse_args(input_args: List) -> dict:
#     def is_arg(value):
#         return value.startswith("--")
#
#     def find_values(items, start):
#         for item in items[start:]:
#             if is_arg(item):
#                 break
#             yield item
#
#     def removeprefix(value, prefix="--"):
#         # Python <= 3.8
#         return value.replace(prefix, "") if value.startswith(prefix) else value
#
#     args = input_args.copy()
# vals = {
#     "output": args.pop(),
#     "header": False,
#     "footer": False,
#     "header-html": False,
#     "footer-html": False,
# }
# dict_args = {}
# first_index, last_index = 0, 0
#
# for key in ["--header-html", "--footer-html"]:
#     if key in args:
#         name = removeprefix(key)
#         index = args.index(key)
#
#         vals[name] = True
#         if index < first_index:
#             first_index = index
#         if index + 1 > last_index:
#             last_index = index + 1
#
#     command_args = args[: first_index - 1]
#     for index, item in enumerate(command_args):
#         if not is_arg(item):
#             continue
#
#         name = removeprefix(item)
#         dict_args.setdefault(name)
#
#         values = list(iter(find_values(command_args, index + 1)))
#         if not values:
#             dict_args[name] = None
#         elif len(values) == 1:
#             dict_args[name] = values[0]
#         else:
#             dict_args[name] = values
#
#     # session_id=af8671bxxxxxxxxxxxxxxxx; HttpOnly; domain=test.com; path=/;
#     if cookie_jar := dict_args.pop("cookie-jar", None):
#         with open(cookie_jar, encoding="utf-8") as file:
#             cookie = re.search(SESSION_PATTERN, file.read().strip()).group(0).split("=")
#             dict_args["cookie"] = [(cookie[0], cookie[1])]
#
#     vals.update(
#         {
#             "dict_args": dict_args,
#             "bodies": args[last_index + 1:],
#         }
#     )
#
#     return vals

def test_parse_cookie_jar(self):
    cookie_content = "session_id=af8671bxxxxxxxxxxxxxxxx; HttpOnly; domain=test.com; path=/;"
    with patch("builtins.open", mock_open(read_data=cookie_content)):
        with open("cookies.txt", encoding="utf-8") as file:
            cookie = re.search(wk.SESSION_PATTERN, file.read().strip()).group(0).split("=")
            self.assertEqual(cookie, ["session_id", "af8671bxxxxxxxxxxxxxxxx"])
