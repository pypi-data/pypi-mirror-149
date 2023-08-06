#!/usr/bin/env python
# encoding: utf-8
"""
common.py

Created by Pierre-Julien Grizel et al.
Copyright (c) 2019 NumeriCube. All rights reserved.

Common stuff for dmake
"""
# Python3 rocks :)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import functools
import os
import pkgutil
import weakref
from subprocess import PIPE
from subprocess import Popen

# pylint: disable=E0401,C0301
__author__ = ""
__copyright__ = "Copyright 2016, NumeriCube"
__credits__ = ["Pierre-Julien Grizel"]
__license__ = "CLOSED SOURCE"
__version__ = "TBD"
__maintainer__ = "Pierre-Julien Grizel"
__email__ = "pjgrizel@numericube.com"
__status__ = "Production"


HERE = os.path.dirname(os.path.realpath(__file__))
AWSCLI_MINIMUM_VERSION = "1.11.91"
DOCKER_MINIMUM_VERSION = "17.06.00"

RECOMMENDED_VARIABLES = {
    "MAKE_DEFAULT_SERVICE": "(optional) Default service name used for practical operations like ssh, attach, test...",
    "PROJECT_NAME": "Your stack name (duh!)",
    "AZURE_RESOURCE_GROUP": "(optional, except for Azure) The Azure Resource Group to put this project resources to",
    "AZURE_ACR_NAME": "(optional, except for Azure) The Azure ACR name you're gonna use for this project",
    "AZURE_SUBSCRIPTION_ID": "(optional, except for Azure) Your Azure subscription id (use `az account list`)",
}


def system(
    command,
    raise_on_error=True,
    fail_silently=False,
    description=None,
    capture=False,
    capture_stderr=False,
    strip_output=True,
    verbose=False,
):
    """Wrapper around os.system

    Keyword arguments:
    raise_on_error -- will throm an exception if return code is not 0
    fail_silently -- ignores if failure
    capture -- return captured string instead of error code
    """
    # Prepare command (pre-expand)
    data = ""
    expcommand = os.path.expandvars(command)
    if description and verbose:
        print(description)
    if capture_stderr:
        expcommand = expcommand + " 2>&1"
    if verbose:
        printc(
            bcolors.ECHO, "    [{}]$ {}".format(os.path.abspath(os.curdir), expcommand)
        )

    # Execute
    if capture:
        subp = Popen(expcommand, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = subp.communicate()
        ret = subp.returncode
        data = " ".join((stdout.decode(), stderr.decode()))
    else:
        ret = os.system(expcommand)

    # Handle return values
    if ret and not fail_silently:
        if verbose:
            printc(bcolors.FAIL, "    Command returned {}".format(ret))
            printc(bcolors.FAIL, data)
        if raise_on_error:
            raise OSError(ret)

    # Return value if we reached here
    if capture:
        if strip_output:
            data = data.strip()
        return data
    return ret


def memoized_method(*lru_args, **lru_kwargs):
    """See https://stackoverflow.com/questions/33672412/python-functools-lru-cache-with-class-methods-release-object
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(self, *args, **kwargs):
            # We're storing the wrapped method inside the instance. If we had
            # a strong reference to self the instance would never die.
            self_weak = weakref.ref(self)

            @functools.wraps(func)
            @functools.lru_cache(*lru_args, **lru_kwargs)
            def cached_method(*args, **kwargs):
                return func(self_weak(), *args, **kwargs)

            setattr(self, func.__name__, cached_method)
            return cached_method(*args, **kwargs)

        return wrapped_func

    return decorator


class bcolors:
    """See https://stackoverflow.com/questions/287871/print-in-terminal-with-colors"""

    # Symbolic
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # Semantic
    CONFIG_INFO = "\033[95m"  # Display config information
    DESCRIBE = "\033[2m"  # Describe what we're doing
    WARNING = "\033[93m"
    SUCCESS = "\033[92m"
    TITLE = "\033[93m"  # Used for help titles
    NONE = "\033[0m"
    INFO = "\033[96m"  # Context-specific information / heads up
    ECHO = "\033[94m"  # Echo a shell command
    FAIL = "\033[91m"


def printc(color, text):
    """Print in color"""
    print("{}{}{}".format(color, text, bcolors.ENDC))


def available_addons(search_path=HERE):
    """Return a list of available add-ons to extend Make functions and classes
    """
    search_path = (search_path,)
    return [x[1] for x in pkgutil.iter_modules(path=search_path)]
