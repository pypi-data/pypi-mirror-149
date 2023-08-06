#!/usr/bin/env python
# encoding: utf-8
"""
fixtures.py

Created by Pierre-Julien Grizel et al.
Copyright (c) 2016 NumeriCube. All rights reserved.

Common fixtures used for dmake tests
"""
import contextlib
import os
import tempfile

import pytest

import dmake

__author__ = ""
__copyright__ = "Copyright 2016, NumeriCube"
__credits__ = ["Pierre-Julien Grizel"]
__license__ = "CLOSED SOURCE"
__version__ = "TBD"
__maintainer__ = "Pierre-Julien Grizel"
__email__ = "pjgrizel@numericube.com"
__status__ = "Production"


@contextlib.contextmanager
def context_cd(path):
    """Taken from https://stackoverflow.com/questions/24469538/sh-cd-using-context-manager"""
    old_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_path)


@contextlib.contextmanager
def context_environ():
    """Save environment variables and restore them later"""
    old_environ = os.environ.copy()
    try:
        yield
    finally:
        for k, v in old_environ.items():
            os.environ[k] = v
        for k in os.environ.keys():
            if k not in old_environ:
                del os.environ[k]


@pytest.fixture
def dmake_module(scope="function"):
    """Test creation of a bootstrap dir"""
    # Create a temp directory where all this shit will happen
    with context_environ():
        with tempfile.TemporaryDirectory() as tmpdirname:
            with context_cd(tmpdirname):
                # Safety belt
                os.chdir(tmpdirname)
                assert os.path.isdir(tmpdirname)

                # Basic file creation
                with open("README.md", "w") as readme:
                    readme.write("Sample project dir")

                # Create repo and first commit
                os.system("git init")
                os.system("git add README.md")
                os.system("git commit -m First")

                # Bootstrap it
                assert os.path.isdir(tmpdirname)
                # import pdb; pdb.set_trace()
                dmake.cmd.main("bootstrap", "-w", "test")
                # os.system("dmake -v bootstrap -w test")
                # assert not os.system("dmake bootstrap -w test")

                # Now we test content :)
                assert os.path.isfile("provision/docker-compose.yml")

                # Ok, happy with this, let's proceed
                yield tmpdirname


@pytest.fixture
def sandbox_dir(scope="function"):
    """Test creation of a sandbox dir (not bootstrapped)"""
    # Create a temp directory where all this shit will happen
    with context_environ():
        with tempfile.TemporaryDirectory() as tmpdirname:
            with context_cd(tmpdirname):
                # Safety belt
                os.chdir(tmpdirname)
                assert os.path.isdir(tmpdirname)

                # Basic file creation
                with open("README.md", "w") as readme:
                    readme.write("Sample project dir")

                # Ok, happy with this, let's proceed
                yield tmpdirname
