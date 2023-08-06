#!/usr/bin/env python
# encoding: utf-8
"""
conftest.py

Created by Pierre-Julien Grizel et al.
Copyright (c) 2016 NumeriCube. All rights reserved.

See official pytest doc
https://docs.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option
"""
from __future__ import unicode_literals

import pytest

__author__ = ""
__copyright__ = "Copyright 2016, NumeriCube"
__credits__ = ["Pierre-Julien Grizel"]
__license__ = "CLOSED SOURCE"
__version__ = "TBD"
__maintainer__ = "Pierre-Julien Grizel"
__email__ = "pjgrizel@numericube.com"
__status__ = "Production"


def pytest_addoption(parser):
    parser.addoption(
        "--skipslow", action="store_true", default=False, help="skip slow tests"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--skipslow"):
        skip_slow = pytest.mark.skip(reason="remove --skipslow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
