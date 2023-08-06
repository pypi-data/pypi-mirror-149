#!/usr/bin/env python
# encoding: utf-8
"""
deploy.py

Created by Pierre-Julien Grizel et al.
Copyright (c) 2019 NumeriCube. All rights reserved.


"""
# Python3 rocks :)
import os

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


# ########################################################################## #
# ####                         DEPLOY (SWARM ONLY)                      #### #
# ########################################################################## #


class Deploy(base_commands.BaseCommand):
    """Deploy a released stack into a production environment.
    IT WON'T WORK NEITHER ON DEV ENVIRONMENT NOR IF IMAGES HAS NOT BEEN PUSHED
    """

    arguments = (
        {
            "name": ("-r", "--release"),
            "help": "Specify the release version you want to deploy (v2018-01-01-120101-master for example). Default is to release the latest version.",
            "action": "store",
            "dest": "release",
        },
        {
            "name": ("-s", "--status"),
            "help": "Show what is deployed.",
            "action": "store_true",
            "dest": "deploy_status",
        },
        {
            "name": ("-y",),
            "help": "Do not ask for confirmation.",
            "action": "store_true",
            "dest": "yes",
        },
    )

    def show_deploy_status(self,):
        """Show what's live
        """
        try:
            self.system(
                "docker stack ps ${PROJECT_NAME}-${DEPLOY_ENV} --format 'table {{.Name}}\t{{.Image}}\t{{.CurrentState}}\t{{.Error}}'  -f 'Desired-state=Running' -f 'Desired-state=Ready'"
            )
        except OSError:
            printc(
                bcolors.INFO,
                "Can't read the status of your stack (it may not have been created yet)",
            )

    def cmdrun(self,):
        """Perform deployment.
        NEW: Will assist deployment with semi-automagical stuff here :)
        """
        # Execute status display
        if self.deploy_status:
            return self.show_deploy_status()

        # Semi-assisted mode: we display the list of machines and ask the user to decide
        # which machine he wants to deploy on :)
        machines = self.system("docker-machine ls", capture=True)
        if not self.machine:
            print(machines)
            self.machine = input("Which machine do you want to deploy on: ")

        # According to the machine name, set the correct environment and driver
        if self.machine not in machines:
            printc(bcolors.FAIL, "Unknown machine name.")
            exit(-1)
        if self.env.startswith("dev"):
            if "-" not in self.machine:
                printc(
                    bcolors.FAIL,
                    "You cannot run this on the 'dev' environment. Use the '--env' option or use machine names with -env naming convention.",
                )
                exit(-1)
            self.env = self.machine.split("-")[-1]
            os.environ["DEPLOY_ENV"] = self.env

        # Deploy latest tag (default) and display brief information
        os.environ["DEPLOY_TAG"] = self.release or self.get_latest_tag()
        printc(
            bcolors.INFO,
            "DEPLOYMENT CONFIGURATION:\nMachine: {}\nProject tag: {}\nEnvironment: {}".format(
                self.machine, os.environ["DEPLOY_TAG"], os.environ["DEPLOY_ENV"]
            ),
        )
        printc(bcolors.WARNING, "\nCURRENT STACK STATE:")
        self.re_make(
            "--env={}".format(self.env),
            '--machine="{}"'.format(self.machine),
            "deploy",
            "--status",
        )

        # Confirmation message
        if not self.yes:
            res = input("\nProceed? [Y/n] ")
            if res.strip().upper() != "Y":
                printc(bcolors.FAIL, "Deploy aborted.")
                exit(-1)
            return self.re_make(
                "--env={}".format(self.env),
                "--machine={}".format(self.machine),
                "deploy",
                "--release={}".format(os.environ["DEPLOY_TAG"]),
                "-y",
            )

        # Generate configuration
        self.system("mkdir -p {}".format(os.environ["PROVISION_HISTORY_DIR"]))
        target_conf = "{}/$PROJECT_NAME-$DEPLOY_TAG.yml".format(
            os.environ["PROVISION_HISTORY_DIR"]
        )
        self.system(
            r"""docker-compose -f {}/docker-compose.yml -f {}/docker-{}.yml config | sed "s,${},..,g" | sed 's,\$$,$$$$,g' | sed "s,name: noop-.*,,g" > {}""".format(
                os.environ["PROVISION_DIR"],
                os.environ["PROVISION_DIR"],
                self.env,
                os.environ["PROVISION_DIR"],
                target_conf,
            )
        )

        # Check that images are available by pre-downloading them on the remote machine (yeaaah it's that simple)
        ret = self.system(
            "docker-compose -f {} pull".format(target_conf), raise_on_error=False
        )
        if ret:
            exit(-1)

        # Actually deploy and display return status
        self.system(
            "docker stack deploy --with-registry-auth --prune -c {} $PROJECT_NAME-$DEPLOY_ENV".format(
                target_conf
            )
        )
        self.show_deploy_status()

        # Little message
        print("Wanna see this message again? Run the following command:")
        printc(
            bcolors.INFO,
            "dmake --env {} --machine {} status".format(
                os.environ["DEPLOY_ENV"], self.machine
            ),
        )
