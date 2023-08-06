#!/usr/bin/env python
# encoding: utf-8
"""
test_config.py

Created by Pierre-Julien Grizel et al.
Copyright (c) 2016 NumeriCube. All rights reserved.

Test if dmake is able to perform a basic config end-to-end
"""
import contextlib
import io
import os
import sys

import dmake

from .fixtures import sandbox_dir

__author__ = ""
__copyright__ = "Copyright 2016, NumeriCube"
__credits__ = ["Pierre-Julien Grizel"]
__license__ = "CLOSED SOURCE"
__version__ = "TBD"
__maintainer__ = "Pierre-Julien Grizel"
__email__ = "pjgrizel@numericube.com"
__status__ = "Production"


@contextlib.contextmanager
def capture_stdout():
    oldout, olderr = sys.stdout, sys.stderr
    try:
        out = [io.StringIO(), io.StringIO()]
        sys.stdout, sys.stderr = out
        yield out
    finally:
        sys.stdout, sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()


def test_basic():
    """Test if I can call dmake"""
    # dmake will fail as no command is provided
    assert os.system("dmake") == 512
    assert not os.system("dmake --help")


def test_sandbox(sandbox_dir):  # noqa: F811
    """Test from a sandbox
    """
    # Start a few containers
    assert not os.system(
        "docker run -d --rm --name dmake_test_container1 ubuntu sleep infinity"
    )
    assert not os.system(
        "docker run -d --rm --name dmake_test_container2 ubuntu sleep infinity"
    )
    assert not os.system(
        "docker run -d --rm --name dmake_test_container3 ubuntu sleep infinity"
    )

    # Prepare our structure
    dmake.cmd.main("config")

    # Stop containers
    assert not os.system("docker stop -t 0 dmake_test_container1")
    assert not os.system("docker stop -t 0 dmake_test_container2")
    assert not os.system("docker stop -t 0 dmake_test_container3")

    # Start containers. They should be up and running!
    dmake.cmd.main("stack", "start", "--detach")

    # Test that our containers are alive
    containers = dmake.common.system("docker ps", capture=True).split()
    project_name = os.path.split(os.path.abspath(os.curdir))[-1]
    active_containers = " ".join(containers)
    print(containers)
    for container_name in (
        "{}_dmake_test_container1_1".format(project_name),
        "{}_dmake_test_container2_1".format(project_name),
        "{}_dmake_test_container3_1".format(project_name),
    ):
        for cname in containers:
            assert container_name in active_containers

    # Stop 'em all
    dmake.cmd.main("stack", "stop")
    dmake.cmd.main("stack", "clean", "-y")

    # Check if they're NOT alive anymore
    containers = dmake.common.system("docker ps", capture=True).split()
    for container_name in (
        "{}_dmake_test_container1_1".format(project_name),
        "{}_dmake_test_container2_1".format(project_name),
        "{}_dmake_test_container3_1".format(project_name),
    ):
        assert container_name not in containers


def test_custom_dockerfile(sandbox_dir):  # noqa: F811
    """Test if we can create an integrate a Dockerfile as a whole
    """
