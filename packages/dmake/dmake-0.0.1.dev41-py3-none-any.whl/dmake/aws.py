#!/usr/bin/env python
# encoding: utf-8
"""
aws.py

Created by Pierre-Julien Grizel et al.
Copyright (c) 2019 NumeriCube. All rights reserved.

AWS-specific stuff
"""
# Python3 rocks :)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import os

from . import base_commands
from .common import bcolors
from .common import printc

# pylint: disable=E0401
__author__ = ""
__copyright__ = "Copyright 2016, NumeriCube"
__credits__ = ["Pierre-Julien Grizel"]
__license__ = "CLOSED SOURCE"
__version__ = "TBD"
__maintainer__ = "Pierre-Julien Grizel"
__email__ = "pjgrizel@numericube.com"
__status__ = "Production"


# ########################################################################## #
# ####                          AWS management                          #### #
# ########################################################################## #


class AWSManager(base_commands.CloudManagerCommand):
    """Basic configuration and management of AWS services.
    If AWS is registered, you will have a 'self.cloud_manager' object in your task.
    """

    aws_region = None
    aws_account_id = None

    def print_status(self,):
        """This is a convenient way to add AWS-specific information in the status command.
        """
        # Basic configuration
        printc(bcolors.TITLE, "AWS configuration")
        printc(bcolors.TITLE, "=================")
        print(
            "Profile: {0.BOLD}{1}{0.NONE} (see 'aws configure' doc for more information)".format(
                bcolors, self.aws_profile
            )
        )
        print("Region: {0.BOLD}{1}{0.NONE}".format(bcolors, self.aws_region))
        print(
            "ECR Registry: {0.BOLD}{1}{0.NONE}".format(
                bcolors, os.environ["DOCKER_AWS_REGISTRY"]
            )
        )

        # Subnets
        self.system(
            "aws ec2 describe-subnets --output table --query 'Subnets[*].[SubnetId, AvailabilityZone, State, VpcId, MapPublicIpOnLaunch]'"
        )

    def push_image(self, image, release_tag):
        """Push image to ECR (tagging it if necessary).
        'image' is a verrrrry long name possibly (includes repo's base name)
        """
        image_id = self.system(
            "docker images -f reference='{}:{}' -q".format(image, release_tag),
            capture=True,
        )
        if not image_id:
            printc(
                bcolors.FAIL, "Unable to find '{}:{}' image".format(image, release_tag)
            )
            return

        # Create repository if necessary
        image_without_repo = image.replace(
            self.get_registry_uri(trailing_slash=True), ""
        )
        repo_names = self.get_ecr_repositories()
        if image_without_repo not in repo_names:
            if self.create_repository:
                printc(bcolors.INFO, "Creating repository")
                self.system(
                    "aws ecr create-repository --repository-name {}".format(
                        image_without_repo
                    )
                )
            else:
                printc(
                    bcolors.FAIL,
                    "Unable to find '{}' repository in AWS ECR (use --create-repository if necessary)".format(
                        image
                    ),
                )

        # Tag & push to target
        # image_target = "{}.dkr.ecr.{}.amazonaws.com/{}:{}".format(
        #     self.aws_account_id, self.aws_region, image, release_tag
        # )
        self.system("docker tag {} {}".format(image_id, image))
        self.system("docker push {}".format(image))

    def get_image_info(self, image, tag):
        """Return info from the given tag
        """
        image_without_repo = image.replace(
            self.get_registry_uri(trailing_slash=True), ""
        )
        all_images = self.system(
            "aws ecr list-images --repository-name {}".format(image_without_repo),
            capture=True,
        )
        return tag in all_images

    def get_ecr_repositories(self,):
        """Return a dict of ECR repositories
        """
        command = "aws ecr describe-repositories --output json"
        describe = self.system(
            command, capture=True, description="Describing AWS repositories..."
        )
        repositories = json.loads(describe)["repositories"]
        return [repo["repositoryName"] for repo in repositories]
        # return repositories

    def get_registry_uri(self, trailing_slash=False):
        """Return registry UTI with trailing slash if necessary
        """
        registry_uri = "{}.dkr.ecr.{}.amazonaws.com{}".format(
            self.aws_account_id, self.aws_region, trailing_slash and "/" or ""
        )
        return registry_uri

    def setup(self):
        """Configure AWS services."""
        # General parameters
        os.environ["AWS_DEFAULT_OUTPUT"] = "json"

        # Display an account confirmation
        if self.verbose:
            printc(
                bcolors.CONFIG_INFO, "Using AWS profile: {}".format(self.aws_profile)
            )
        os.environ["AWS_PROFILE"] = self.aws_profile

        # Find account id
        self.aws_account_id = json.loads(
            self.system("aws sts get-caller-identity", capture=True)
        )["Account"]

        # Configure / Store region
        if not self.aws_region:
            self.aws_region = self.system("aws configure get region", capture=True)
        if self.verbose:
            printc(bcolors.CONFIG_INFO, "Using AWS region: {}".format(self.aws_region))
        os.environ["AWS_DEFAULT_REGION"] = self.aws_region

        # Check if the given ECR exists, provide hints if it does not
        if not self.get_ecr_repositories():
            printc(
                bcolors.WARNING,
                "No ECR repository on your AWS account, you should create some first.",
            )
            print("Maybe you should check if your configuration is ok")
            print(
                "Alternatively, you can use 'dmake release --create-repository' to create them for you."
            )
        # names = [repo["repositoryName"] for repo in repositories]
        # if not self.aws_ecr in names:
        #     printc(
        #         bcolors.FAIL, "Invalid AWS ECR repository name: {}".format(self.aws_ecr)
        #     )
        #     printc(bcolors.INFO, "Valid names are: {}".format(names))
        #     exit(-1)

        # Set DOCKER_REGISTRY accordingly
        os.environ["DOCKER_AWS_REGISTRY"] = self.get_registry_uri(trailing_slash=True)
        os.environ["DOCKER_REGISTRY"] = os.environ["DOCKER_AWS_REGISTRY"]

        # Docker-machine setup
        os.environ["MACHINE_DRIVER"] = "amazonec2"

        # Login and we're good to go!
        login_cmd = self.system("aws ecr get-login --no-include-email", capture=True)
        self.system(login_cmd)
