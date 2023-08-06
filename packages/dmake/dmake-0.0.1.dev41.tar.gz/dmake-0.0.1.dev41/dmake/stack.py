#!/usr/bin/env python
# encoding: utf-8
"""
stack.py

Created by Pierre-Julien Grizel et al.
Copyright (c) 2019 NumeriCube. All rights reserved.


"""
# Python3 rocks :)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import json
import os
import re
import textwrap

from . import base_commands
from .common import HERE
from .common import bcolors
from .common import printc

# pylint: disable=E0401,C0301
__author__ = ""
__copyright__ = "Copyright 2016, NumeriCube"
__credits__ = ["Pierre-Julien Grizel"]
__license__ = "CLOSED SOURCE"
__version__ = "TBD"
__maintainer__ = "Pierre-Julien Grizel"
__email__ = "pjgrizel@numericube.com"
__status__ = "Production"


class Stack(base_commands.BaseSubCommand):
    """Manage a (live) docker-compose stack: start, exec, inspect (attach), etc"""

    rebuild = False

    arguments = (
        {
            "name": ("--container",),
            "help": "Specify which container (or service) you wanna work with for debug/run/shell commands. Default can be taken from env's MAKE_DEFAULT_SERVICE",
            "dest": "container",
            "action": "store",
            # "default": os.environ.get("MAKE_DEFAULT_SERVICE"),
        },
    )

    start_arguments = (
        {
            "name": ("--args",),
            "help": "Passes along complementary arguments as $ADDITIONAL_ARGS (your docker-xxx.yml file must mention "
            "these args in the 'command:' setting, see dmake status -h for more information on this.",
            "dest": "additional_args",
            "action": "store",
        },
        {
            "name": ("--rebuild",),
            "help": "Re-build your stack before starting it (takes time)",
            "dest": "rebuild",
            "action": "store_true",
        },
        {
            "name": ("--detach",),
            "help": "Detach your stack to make it run in background",
            "dest": "detach",
            "action": "store_true",
        },
    )

    clean_arguments = (
        {
            "name": ("--all",),
            "help": "Deletes everything we can. THIS WILL PROBABLY DELETE STUFF FROM OTHER PROJECTS, TOO!",
            "dest": "all",
            "action": "store_true",
        },
        {
            "name": ("-y",),
            "help": "Do not ask for confirmation.",
            "action": "store_true",
            "dest": "yes",
        },
    )

    test_arguments = (
        {
            "name": ("additional_args",),
            "help": "Passes along complementary arguments to the test command",
            # "dest": "additional_args",
            "action": "store",
            "nargs": argparse.REMAINDER,
        },
    )

    exec__arguments = (
        {
            "name": ("-T",),
            "help": "Disable terminal interaction",
            "action": "store_true",
            "dest": "noterm",
        },
        {
            "name": ("container_command",),
            "help": "Command to pass along to the container. Put it in quotes to make sure it's treated correctly. Example: '/bin/bash'.",
            "action": "store",
            "nargs": argparse.REMAINDER,
            "default": "",
        },
    )

    def get_default_container(self, exit_on_error=True):
        """Get default container/service.
        Will either use the provided positional arg or directly ask question.
        """
        # Grab regular container.
        container = self.container
        # or os.environ.get("MAKE_DEFAULT_SERVICE")
        if not container:
            # WARNING: THIS WILL NOT WORK WELL IN SWARM MODE.
            # We'll have to perform slightly different stack operations in Swarm mode.
            services = self.docker_compose("ps --services", capture=True).split()

            # We order alphabetically, isolate MAKE_DEFAULT_SERVICE and display a nice counter
            services.sort()
            if "MAKE_DEFAULT_SERVICE" in os.environ:
                services.remove(os.environ["MAKE_DEFAULT_SERVICE"])
                services.insert(0, os.environ["MAKE_DEFAULT_SERVICE"])
            for idx, service_name in enumerate(services):
                print(f"[{idx}] {service_name}")
            default_service = services[0]
            default_text = " [{}]".format(default_service)
            container = (
                input(
                    "Type service name or number you want to operate on{}: ".format(default_text)
                )
                or default_service
            )
            if not container:
                printc(
                    bcolors.FAIL,
                    "Give a valid --container option or use MAKE_DEFAULT_SERVICE in 'settings-common.env'.",
                )
                if exit_on_error:
                    exit(-1)
            if container.isnumeric():
                container = services[int(container)]
        return container

    @base_commands.subcommand
    def exec_(self,):
        """Execute a command on the given container. You can also use MAKE_DEFAULT_SERVICE to specify a default value for this (we'll connect to the first container matching this default service)
        """
        container = self.get_default_container()
        printc(bcolors.DESCRIBE, "Connecting {}...".format(container))
        if self.noterm:
            noterm = "-T"
        else:
            noterm = ""
        return self.docker_compose(
            "exec {} {} {}".format(noterm, container, " ".join(self.container_command))
        )

    @base_commands.subcommand
    def ssh(self,):
        """Connect with bash on the given container. You can also use MAKE_DEFAULT_SERVICE to specify a default value for this."""
        container = self.get_default_container()
        printc(bcolors.DESCRIBE, "Connecting {}...".format(container))
        return self.docker_compose("exec {} /bin/bash".format(container))

    @base_commands.subcommand
    def logs(self,):
        """View logs on the given container or on MAKE_DEFAULT_SERVICE service."""
        container = self.get_default_container()
        return self.docker_compose("logs {}".format(container))

    @base_commands.subcommand
    def restart(self,):
        """Restart a specific service.
        """
        container = self.get_default_container()
        return self.docker_compose(
            "restart {}".format(container)
        )

    @base_commands.subcommand
    def start(self,):
        """Start your dev environment"""
        # Basic information about what to run
        append_args = ""
        if self.verbose:
            printc(bcolors.ENDC, "Starting dev containers.")

        # Remove all trailing pyc files
        self.system(
            r'find "{}" -name \*.pyc -delete'.format(HERE),
            description="Removing trailing pyc files...",
        )

        # Make sure you stop before you start
        self.stop()

        # Message a caractere informatif
        printc(
            bcolors.INFO,
            textwrap.dedent(
                """\
            **************************************************************************
            USE Ctrl+C to stop running containers.
            USE dmake stack clean TO STOP AND CLEAN YOUR RUNNING CONTAINERS.
            Open another terminal and use dmake attach to attach a running console
            **************************************************************************
        """
            ),
        )
        # Run docker
        if self.additional_args:
            os.environ["ADDITIONAL_ARGS"] = self.additional_args
        if self.rebuild:
            append_args = "--force-recreate --always-recreate-deps --build"
        if self.detach:
            self.docker_compose(
                "up", "--remove-orphans --detach {}".format(append_args)
            )
        else:
            self.docker_compose(
                "up",
                "--remove-orphans {}".format(append_args),
            )

    @base_commands.subcommand
    def clean(self,):
        """Shortcut for make dev --clean --prune stop"""
        print(
            "This command can delete all container data that's not stored outside Docker."
        )
        if not self.yes:
            res = input("\nProceed? [Y/n] ")
            if res.strip().upper() != "Y":
                exit(-1)

        # Stop containers
        self.stop()
        self.docker_compose("rm -v")

        # If 'all', stop/delete everything. We're gonna be VERY greedy here!
        if self.all:
            printc(bcolors.INFO, "Removing all containers")
            self.system("docker system prune -f")
            printc(bcolors.INFO, "Removing all volumes")
            self.system("docker system prune --volumes -f")
            # container_ids = " ".join(
            #     self.system("docker ps -a -q", capture=True).split()
            # )
            # if container_ids:
            #     self.system("docker stop {}".format(container_ids))
            #     self.system("docker rm {}".format(container_ids))
            # image_ids = " ".join(self.system("docker images -q", capture=True).split())
            # if image_ids:
            #     self.system("docker rmi {}".format(image_ids))

    @base_commands.subcommand
    def status(self,):
        """Display information about currently running dev stack (if any)
        """
        self.docker_compose("ps")

    @base_commands.subcommand
    def test(self,):
        """Run unittests. Stack must be up and running.
        Configuration is made via ./provision/provision.json (simple syntax).
        All commands will be executed but if any command returns >0 we'll propagate this.
        """
        # Execute all commands sequentially
        with open(
            os.path.join(self.get_provision_dir(), "provision.json"), "r"
        ) as provision_json:
            provisionning = json.load(provision_json)
            for to_exec in provisionning["test"]:
                self.docker_compose(
                    "exec {} {}".format(
                        to_exec.get("service", self.get_default_container()),
                        to_exec.get("exec"),
                    )
                )

    @base_commands.subcommand
    def doc(self,):
        """Generate container-dependant documentation. Stack must be up and running.
        Configuration is made via ./provision/provision.json (simple syntax).
        All commands will be executed but if any command returns >0 we'll propagate this.
        It's up to you to symlink the generated doc to where you want it to be accessed.
        """
        with open(
            os.path.join(self.get_provision_dir(), "provision.json"), "r"
        ) as provision_json:
            provisionning = json.load(provision_json)

            # Execute all commands sequentially
            for to_exec in provisionning["doc"]:
                self.docker_compose(
                    "exec {} {}".format(
                        to_exec.get("service", self.get_default_container()),
                        to_exec.get("exec"),
                    )
                )

    @base_commands.subcommand
    def stop(self):
        """Stop your dev environment. In case it doesn't work, call 'dmake clean' :)."""
        self.docker_compose("stop")
        # container_ids = " ".join(self.docker_compose("ps -q", capture=True).split())
        # command = r"docker stop {}".format(container_ids)
        # self.system(
        #     command,
        #     fail_silently=True,
        #     description="Stopping containers referenced in this docker-compose file...",
        # )

    @base_commands.subcommand
    def attach(self,):
        """Attach the current console to the running container. Useful for terminal debugging.
        """
        # Find container. Not an easy job...
        container = self.get_default_container()
        containers = self.docker_compose("ps", capture=True)
        match = re.search(r"[-\w]*{}_[0-9]".format(container), containers)
        if not match:
            printc(
                bcolors.FAIL,
                "Container '{}' seems not to be running.".format(container),
            )
            printc(
                bcolors.NONE,
                "See './dmake docker-compose ps' output to check what's going on (do not include prefix nor suffix in container name).",
            )
            exit(-1)
        container = match.group()

        # Help text
        printc(
            bcolors.DESCRIBE,
            """This command should be used in conjonction with 'make stack start'.
It attaches the main container and allows pdb signals to be catched.
Run 'make stack attach' from another terminal window to avoid crippled output ;)
To exit your debug session without sending Ctrl+C to your instance,
type Ctrl+p Ctrl+q

*********************************************************
**           Exit session with Ctrl+p Ctrl+q.          **
*********************************************************

Enjoy!""",
        )
        self.system("docker attach {}".format(container))
