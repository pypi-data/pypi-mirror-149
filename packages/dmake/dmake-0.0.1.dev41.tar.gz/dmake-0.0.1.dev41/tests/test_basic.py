#!/usr/bin/env python
# encoding: utf-8
"""
test_basic.py

Created by Pierre-Julien Grizel et al.
Copyright (c) 2016 NumeriCube. All rights reserved.

Test if dmake is just callable
"""
from __future__ import unicode_literals

import pytest

import dmake

from .fixtures import dmake_module

__author__ = ""
__copyright__ = "Copyright 2016, NumeriCube"
__credits__ = ["Pierre-Julien Grizel"]
__license__ = "CLOSED SOURCE"
__version__ = "TBD"
__maintainer__ = "Pierre-Julien Grizel"
__email__ = "pjgrizel@numericube.com"
__status__ = "Production"


def test_basic():
    """Test if I can call dmake"""
    # dmake will fail as no command is provided
    with pytest.raises(SystemExit):
        dmake.cmd.main("")
    with pytest.raises(SystemExit):
        dmake.cmd.main("--help")
