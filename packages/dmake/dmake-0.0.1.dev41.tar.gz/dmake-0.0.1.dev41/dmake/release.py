#!/usr/bin/env python
# encoding: utf-8
"""
release.py

Created by Pierre-Julien Grizel et al.
Copyright (c) 2019 NumeriCube. All rights reserved.


"""
# Python3 rocks :)
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


# ########################################################################## #
# ####                       Release (very simple)                      #### #
# ########################################################################## #


class Release(base_commands.BaseCommand):
    """Make a new release from the given source tree, ready for Continuous Integration process.
If $DMAKE_XBUILD_PLATFORM is set (eg. linux/amd64), will cross-build for this specific patform.
Useful if you're building from a Mac M1 to a cloud infra!"""

    latest = False
    arguments = (
        {
            "name": ("-l", "--latest"),
            "help": "Instead of releasing a new one, retreive the latest released tag from the branch you're in",
            "action": "store_true",
            "dest": "latest",
        },
        {
            "name": ("-b", "--branch"),
            "help": "Perform these operations on another branch",
            "action": "store",
            "dest": "branch",
        },
        {
            "name": ("--no-push",),
            "help": "Push to the central repository (if set)",
            "action": "store_false",
            "dest": "push",
        },
        {
            "name": ("--build",),
            "help": "Build the images locally",
            "action": "store_true",
            "dest": "build",
        },
        {
            "name": ("--create-repository",),
            "help": "Create target Docker Image repository if it doesn't exist (and if possible)",
            "action": "store_true",
            "dest": "create_repository",
        },
        {
            "name": ("--force-rm",),
            "help": "Always remove intermediate containers",
            "action": "store_true",
            "dest": "force_rm",
        },
        {
            "name": ("--no-cache",),
            "help": "Do not use cache when building the image",
            "action": "store_true",
            "dest": "no_cache",
        },
    )

    def check_git_status(self,):
        """Check if GIT status is ready to release
        """
        # See https://stackoverflow.com/questions/3258243/check-if-pull-needed-in-git
        if self.system("""git status -uno --porcelain""", capture=True):
            printc(bcolors.FAIL, "Please commit+push your code before moving forward.")
            exit(-1)
        self.system("git remote update")
        local_rev = self.system("git rev-parse @", capture=True)
        remote_rev = self.system("git rev-parse @{u}", capture=True)
        base_rev = self.system("git merge-base @ @{u}", capture=True)
        if local_rev == remote_rev:
            if self.verbose:
                printc(bcolors.INFO, "Local and remote branches are in sync.")
        elif local_rev == base_rev:
            printc(
                bcolors.FAIL, "Local and remote branches not in sync. Use 'git pull'."
            )
            exit(-1)
        elif remote_rev == base_rev:
            printc(
                bcolors.FAIL, "Local and remote branches not in sync. Use 'git push'."
            )
            exit(-1)
        else:
            printc(
                bcolors.FAIL,
                "Local and remote branches diverged. Don't know what to do here.",
            )
            exit(-1)

    def cmdrun(self):
        """Execute command.
        - if no parameter, we just tag/commit
        - if 'build', we build images locally
        - if 'push', we push to the ECR-et-al repository
        - if 'latest' (without push nor build) we display the latest version
        - if 'latest' AND 'push', we push the latest version
        """
        # If we're asking for the latest tag, get it here
        # and display additional information
        if self.latest:
            release_tag = self.get_latest_tag()
            if release_tag:
                printc(
                    bcolors.NONE,
                    "Latest release tag in Git: {1.SUCCESS}{0}{1.NONE}".format(
                        release_tag, bcolors
                    ),
                )
                os.environ["DEPLOY_TAG"] = release_tag
                images_to_push = self.get_candidate_images(release_tag)
                for image in images_to_push:
                    info = "{0.FAIL}No information.{0.NONE}".format(bcolors)
                    if self.cloud_manager:
                        info = (
                            self.cloud_manager.get_image_info(image, release_tag)
                            and "{0.SUCCESS}Available on repository{0.NONE}".format(
                                bcolors
                            )
                            or "{0.FAIL}Absent from repository{0.NONE}".format(bcolors)
                        )
                    printc(
                        bcolors.NONE,
                        "    Image {1}:{3}: {0.SUCCESS}{2}{0.NONE}".format(
                            bcolors, image, info, release_tag
                        ),
                    )
            if not self.push and not self.build:
                return
        else:
            release_tag = self.get_today_tag()

        # Sanity checks
        if self.branch:
            printc(
                bcolors.FAIL, "Sorry, you cannot release a remote branch for the moment"
            )
            exit(-1)

        # Check git status
        self.check_git_status()

        # If we have create a new one, do it
        if not self.latest:
            self.system(
                "git tag {}".format(release_tag), description="Tagging source code..."
            )
            self.system("git push --tags", description="Pushing on source server...")

        # Build if necessary
        # Images are tagged automatically thanks to the DEPLOY_TAG setting.
        os.environ["DEPLOY_TAG"] = release_tag
        if self.push or self.build:
            if self.verbose:
                printc(
                    bcolors.DESCRIBE,
                    "Building images (env-independant). Only images in docker-compose.yml will be built...",
                )
            self.re_make(
                "docker-compose",
                "build --compress {} {} --pull".format(
                    self.force_rm and "--force-rm" or "",
                    self.no_cache and "--no-cache" or "",
                ),
            )

        # I like to push it push it
        if self.push:
            self.push_images(release_tag)

        # What to do now? Say it!
        platform = ""
        if self.aws:
            platform = "--aws "
        elif self.azure:
            platform = "--azure "
        printc(
            bcolors.SUCCESS,
            textwrap.dedent(
                """\
        Release success. Depending on your CI configuration, images should be available in a few minutes.
        You can start deploying, though."""
            ),
        )
        if not self.push:
            printc(
                bcolors.WARNING,
                textwrap.dedent(
                    """\

            Before making your deploy, make sure your images are uploaded.
            Use the following command if your Travis CI isn't configured to take care of it automatically:
                dmake [--azure|--aws] release --push --latest
            """
                ),
            )
        printc(
            bcolors.SUCCESS,
            textwrap.dedent(
                """\
        To deploy this, use the following command:

            dmake {}deploy --release={}
        """.format(
                    platform, release_tag
                )
            ),
        )

    def get_candidate_images(self, release_tag):
        """Return the list of images to build and/or push for the given release tag
        """
        image_matches = filter(
            None,
            [
                re.search("image: (.*):{}".format(release_tag), s)
                for s in self.docker_compose("config", capture=True).splitlines()
            ],
        )
        return set([match.groups()[0] for match in image_matches])

    def push_images(self, release_tag):
        """Actually push to the target repository
        """
        # Explicit
        if self.verbose:
            printc(bcolors.DESCRIBE, "Pushing to Docker repository...")
            printc(
                bcolors.DESCRIBE,
                "We look for images tagged with {}".format(release_tag),
            )

        # Find images to push and then push them to the repository
        images_to_push = self.get_candidate_images(release_tag)
        if not images_to_push:
            printc(
                bcolors.WARNING,
                "No images to push. Make sure you built them and/or used the proper tag.",
            )

        # Push images individually
        for image in images_to_push:
            if self.cloud_manager:
                self.cloud_manager.push_image(image, release_tag)
            else:
                printc(
                    bcolors.NONE,
                    "No (aws|azure) set for image '{}', pushing it to Docker.".format(
                        image
                    ),
                )
                self.system("docker push {}:{}".format(image, release_tag))
