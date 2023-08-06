# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan import lazy_import

lazy_import.lazy_module("numpy")
lazy_import.lazy_module("pandas")
lazy_import.lazy_module("imageio")

from suanpan import asyncio  # noqa
from suanpan.g import g  # noqa
from suanpan.run import cli, helper, env, run  # noqa

__version__ = "0.17.3"

if __name__ == "__main__":
    print(f"Suanpan SDK (ver: {__version__})")
