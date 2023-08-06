#!/usr/bin/env python
# encoding: utf-8
"""
dmake

Created by Pierre-Julien Grizel et al.
Copyright (c) 2016 NumeriCube. All rights reserved.

This is a Makefile-inspired python script used to build and deploy our containers
in a simple and friendly way.

"""
import argparse
import os
import re
import sys

from .aws import AWSManager
from .azure import AzureManager
from .base_commands import BaseCommand
from .base_commands import BaseSubCommand
from .base_commands import Docker
from .base_commands import Docker_Compose
from .base_commands import Docker_Machine
from .base_commands import Shell
from .base_commands import Upgrade
from .command_registry import COMMAND_REGISTRY
from .common import bcolors
from .common import printc
from .config import Config
from .deploy import Deploy
from .release import Release
from .stack import Stack
from .status import Status

# pylint: disable=E0401,C0301

__author__ = ""
__copyright__ = "Copyright 2016, NumeriCube"
__credits__ = ["Pierre-Julien Grizel"]
__license__ = "CLOSED SOURCE"
__version__ = "TBD"
__maintainer__ = "Pierre-Julien Grizel"
__email__ = "pjgrizel@numericube.com"
__status__ = "Production"

# Register commands in the right order
for cls in Config, Status, Stack, Docker, Docker_Compose, Docker_Machine, Shell, Release, Deploy:
    COMMAND_REGISTRY.append(cls)


# ########################################################################## #
# ####                          MAIN ENTRY POINT                        #### #
# ########################################################################## #


class DefaultHelpParser(argparse.ArgumentParser):
    """Will display help on error.
    See https://stackoverflow.com/questions/3636967/python-argparse-how-can-i-display-help-automatically-on-error
    """

    def error(self, message):
        """Display usage information (WITHOUT the whole epilog)
        """
        sys.stderr.write(
            "{}[DMAKE] error: {}{}\n\n".format(bcolors.FAIL, message, bcolors.ENDC)
        )
        self.epilog = ""
        self.print_help()
        sys.exit(2)


def main(*argv):
    """Handle all commands related to the project: prepare, build, release and maintain it.
Are you lost? Start with 'status'.
    """
    # Prepare parser
    # See http://lists.logilab.org/pipermail/python-projects/2012-September/003261.html
    # pylint: disable=E1305
    parser = DefaultHelpParser(
        description="Handle all commands related to the project: prepare, build, release and maintain it. Are you lost? Start with 'dmake status' or 'dmake status -h' to have hints on how to organize your stack.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=r"""-----------------------
The commands below are shell-env-expanded if they are all upercased! This is convenient,
as it could allow you, from within your shell, to use the following, provided
either your ./*env file contains a MAIN_CONTAINER variable
(don't forget to escape the dollar sign or your shell would send an empty command):
    {0.ECHO}dmake stack exec \$MAIN_CONTAINER my_test_command{0.ENDC}

{0.TITLE}Development / Getting started:
==============================={0.NONE}

{0.TITLE}[RECOMMENDED]{0.NONE} Check if your project structure is fine:
    {0.ECHO}dmake status{0.ENDC}
    {0.ECHO}dmake status --help{0.ENDC}  # Prints advices on how should it look like

Start your LOCAL dev envionment / run your unittests:
    {0.ECHO}dmake stack start{0.ENDC}
    {0.ECHO}dmake stack test [<args>]{0.ENDC}

Start /test your stack for ANOTHER environment:
    {0.ECHO}dmake --env=<my-env> stack start{0.ENDC}

Stop your local dev envionment (and clean your turd if necessary):
    {0.ECHO}dmake stack stop{0.ENDC}
    {0.ECHO}dmake stack clean{0.ENDC}

Start a debugging session for the given container (in another terminal preferably)
    {0.ECHO}dmake stack [--container <container>] attach{0.ENDC}

Inspect or run a command in a (running) container:
    {0.ECHO}dmake stack [--container <container>] exec <command>{0.ENDC}
    {0.ECHO}dmake stack [--container <container>] ssh{0.ENDC}
    {0.ECHO}dmake stack [--container <container>] logs{0.ENDC}
    (etc)

{0.TITLE}Release / Prod management:
=========================={0.NONE}

Either your Travis chain takes care of the release process detail or it doesn not. We detail the two options.
.travis.yml configuration is not explained here, see detailed dmake PDF doc for more information.

Common release chain WITH GH/Travis CI 100% configured (only commits into GitHub, the rest will have to be done for ex in .travis.yml):
    {0.ECHO}dmake release{0.ENDC}    # Just marks the release in GH and let Travis do the rest

Common release chain WITHOUT GH/Travis CI:
    {0.ECHO}dmake --aws release --build --push{0.ENDC}
    {0.ECHO}dmake [--aws|--azure] --env=<env> --machine <docker-machine-name> deploy [--release=<v2018-01-01-120000-master]{0.ENDC}

If you forget the --push, you can do it 2-way:
    {0.ECHO}dmake release{0.ENDC}        # Aw, crap, I forgot the --push
    {0.ECHO}dmake --aws release --build --push --latest{0.ENDC}
    {0.ECHO}dmake [--aws|--azure] --env=<env> --machine <docker-machine-name> deploy [--release=<v2018-01-01-120000-master]{0.ENDC}

{0.TITLE}Other procedures
------------------{0.NONE}

Find the latest release number from the master branch:
    {0.ECHO}dmake release --latest --branch=master{0.ENDC}

Deploy on a SWARM cluster on a given machine (must be swarm's manager node machine id from docker-machine)
    {0.ECHO}dmake [--aws|--azure] --env=<env> --machine <docker-machine-name> deploy [--release=v2018-01-01-120000-master]{0.ENDC}

Manage your SWARM cluster (see what's running, inspect logs, etc). Then use ./dmake docker* commands to manage it seamlessly
    {0.ECHO}dmake --machine <docker-machine-name> --env<my-env> shell

{0.TITLE}Extending dmake
------------------------{0.NONE}

You can extend dmake by putting .py files in your 'provision' directory.
Each .py must contain a class that extends BaseCommand

""".format(
            bcolors
        ),
    )

    # Common parameters
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument(
        "-e",
        "--env",
        help="Environment you're working with (default=%s)" % os.environ.get("DEPLOY_ENV", "dev"),
        default=os.environ.get("DEPLOY_ENV", "dev"),
    )
    parser.add_argument(
        "-m",
        "--machine",
        help="Specify a docker-machine name to work on. Use 'dmake status' to get available machines and don't forget the driver argument if necessary.",
    )
    parser.add_argument(
        "--version",
        help="Print version number and exit.",
        action="store_true",
        dest="print_version",
    )

    # AWS-specific parameters
    parser.add_argument(
        "--aws",
        help="Run everything with Amazon Web Services (esp. AWS-ECR)",
        action="store_true",
    )
    parser.add_argument(
        "--aws-profile",
        help="Use another (non-default) profile",
        default="default",
        action="store",
    )
    parser.add_argument(
        "--aws-region", help="Specify which region to use", action="store", default=""
    )

    # Azure arguments
    parser.add_argument(
        "--azure", help="Run everything within Azure", action="store_true"
    )

    # Add sub-parsers
    subparsers = parser.add_subparsers(
        help="Action to perform on your source tree", dest="command"
    )
    # New in Py3, see https://stackoverflow.com/questions/22990977/why-does-this-argparse-code-behave-differently-between-python-2-and-3
    subparsers.required = True
    for command in COMMAND_REGISTRY:
        # Include parser and its arguments
        command.register_parser(subparsers)

    # Ok, let's go!
    # See http://lists.logilab.org/pipermail/python-projects/2012-September/003261.html
    # pylint: disable=W0212
    if not argv:
        argv = sys.argv[1:]

    # Cheating mode here: we check if --version is asked
    if "--version" in argv:
        import pkg_resources  # part of setuptools

        print(pkg_resources.require("dmake")[0].version)
        exit(0)

    # Actual parsing
    args = parser.parse_args(argv)
    cmd_args = args._get_args()
    cmd_kwargs = dict(args._get_kwargs())

    # Deduce environment from machine name
    # and also check that env file is present
    if cmd_kwargs["env"] == "dev" and "-" in (cmd_kwargs.get("machine", "") or ""):
        cmd_kwargs["env"] = cmd_kwargs["machine"].split("-")[-1]
        if cmd_kwargs["verbose"]:
            print(
                "Implicitly switching to environment {} set by machine name. Use explicit --env to avoid this.".format(
                    cmd_kwargs["env"]
                )
            )
    if cmd_kwargs["env"] != "dev":
        if not cmd_kwargs["env"] in Status(*cmd_args, **cmd_kwargs).get_env_names():
            print(
                "Environment {} is not set in your provision files :(".format(
                    cmd_kwargs["env"]
                )
            )
            exit(-1)

    # Double check configuration and instanciate basic command object
    cmd_instance = args.cls(*cmd_args, **cmd_kwargs)

    # Add common environment variables
    os.environ["DEPLOY_ENV"] = cmd_kwargs["env"]
    try:
        os.environ["GIT_COMMIT"] = cmd_instance.system(
            "git rev-parse HEAD", capture=True, capture_stderr=True
        ).strip()
    except OSError:
        printc(
            bcolors.WARNING,
            "This directory doesn't seem to be a git repository. Some dmake commands won't work.",
        )

    # Execute CLOUD pre-processing and register AWS manager
    if cmd_kwargs["aws"]:
        aws_manager = AWSManager(*cmd_args, **cmd_kwargs)
        aws_manager.setup()
        cmd_instance.aws_manager = aws_manager
    if cmd_kwargs["azure"]:
        azure_manager = AzureManager(*cmd_args, **cmd_kwargs)
        azure_manager.setup()
        cmd_instance.cloud_manager = azure_manager

    # Connect to machine if specified
    if cmd_kwargs["machine"]:
        variables = cmd_instance.system(
            "docker-machine env {}".format(cmd_kwargs["machine"]), capture=True
        )
        for sh_var, sh_value in [
            s.split("=") for s in re.findall(r"\w+=.*", variables)
        ]:
            os.environ[sh_var] = eval(sh_value)

    # Execute command
    return cmd_instance.cmdrun()


# Let's RUUUUUN!!!
if __name__ == "__main__":
    # print(available_addons())
    # importlib.import_module("make_add_on")
    # Addon:
    # import importlib
    # make = importlib.import_module("make")
    main()
