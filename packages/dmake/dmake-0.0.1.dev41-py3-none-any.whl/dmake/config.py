#!/usr/bin/env python
# encoding: utf-8
"""
config.py

Created by Pierre-Julien Grizel et al.
Copyright (c) 2019 NumeriCube. All rights reserved.

Simple init of dmake-made projects
"""
# Python3 rocks :)
import json
import os
import shutil

from ruamel.yaml import YAML

from . import base_commands
from .common import HERE
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
# ####                      BOOTSTRAP NEW PROJECT                       #### #
# ########################################################################## #


class Config(base_commands.BaseCommand):
    """Bootstrap a new project. Pass along complimentary options to create a project
    with specific settings. Files are only [OVER]written with the --write option.
    """

    template_dir = None
    target_dir = None
    project_name = None

    arguments = (
        {
            "name": ("project_name",),
            "help": "Name of the project. Optional: can be guessed from directory structure.",
            "action": "store",
            "nargs": "?",
        },
        {
            "name": ("--dry-run",),
            "help": "Write the generated config files. If not set, files will be printed.",
            "action": "store_false",
            "dest": "write",
        },
    )

    def read_and_convert(self, f_source):
        """Read a source template file and convert variable arguments
        """
        # Sanity check
        if not self.project_name:
            raise ValueError(
                "PROJECT_NAME is not set. Pass it as an argument if necessary."
            )

        # List of regexps to replace.
        # Actually, we use env vars to make this easier
        regexps = []
        for key, value in os.environ.items():
            regexps.append(("${}".format(key), value))

        # Open, read, replace
        content = f_source.read()
        for regexp, sub in regexps:
            content = content.replace(regexp, sub)
        return content

    def container_to_docker_compose(self, container_id):
        """Convert a running container into a docker-compose configuration -> dict
        Return a dict ready for Yaml formatting
        """
        # Grab info about running containers
        container_info = json.loads(
            self.system("docker inspect {}".format(container_id), capture=True)
        )[0]
        image_info = json.loads(
            self.system(
                "docker inspect {}".format(container_info["Image"]), capture=True
            )
        )[0]

        # Integrate into a proper structure
        service_name = container_info["Name"][1:]  # Remove heading slash
        return {
            service_name: {
                "image": image_info["RepoTags"][0],
                "command": container_info["Config"]["Cmd"],
                "env_file": ["./settings-common.env", "./settings-${DEPLOY_ENV}.env"],
                # "ports": container_info["NetworkSettings"]["Ports"], # XXX TODO
                "links": [],
                "depends_on": [],
            }
        }

    def update_compose(self, env_name, content):
        """Force-create/update environment of the given name (write on disk)

        env_name -- name of the environment, if None used for top-level (common) env
        content -- the dict or OrderedDict to use for creation.
            Environment can be expanded but not shrunk (no 1st-level key deletion)
        """
        # Basic YAML structure
        yaml = YAML()
        # yaml.indent = 4
        yaml.indent(mapping=4, sequence=4, offset=2)

        # Set filename
        if env_name is None:
            target_file = os.path.join(self.target_dir, "docker-compose.yml")
            template_file = os.path.join(self.template_dir, "docker-compose.yml")
        else:
            target_file = os.path.join(
                self.target_dir, "docker-{}.yml".format(env_name)
            )
            template_file = os.path.join(self.template_dir, "docker-env.yml")

        # Basic file structure.
        # If does not exist, will be copied from template dir.
        if not os.path.isfile(target_file):
            shutil.copyfile(template_file, target_file)
        with open(target_file) as f:
            compose = yaml.load(f.read())

        # Setup services
        for first_level_key in ("services", "version", "volumes"):
            if first_level_key not in compose:
                compose[first_level_key] = {}
            for content_key, content_value in content.get(first_level_key, {}).items():
                if content_key not in compose[first_level_key]:
                    compose[first_level_key][content_key] = {}
                    printc(
                        bcolors.INFO,
                        "  Create '{}:{}'".format(first_level_key, content_key),
                    )
                else:
                    printc(
                        bcolors.INFO,
                        "  Update '{}:{}'".format(first_level_key, content_key),
                    )

                compose[first_level_key][content_key].update(content_value)

        # Record into the target docker-compose.yml file
        with open(target_file, "w") as yaml_f:
            printc(bcolors.INFO, "Writing  {}".format(target_file))
            yaml.dump(compose, yaml_f)

    def setup_compose(self):
        """List running containers and convert them into services
        """
        # Setup services
        services = {"services": {}}
        container_ids = self.system(
            "docker ps --format '{{.ID}}'", capture=True
        ).split()
        for container_id in container_ids:
            container = self.container_to_docker_compose(container_id)
            services["services"].update(container)

        # Write them back
        self.update_compose(None, services)

    def install_templates(self):
        """Install all template files
        """
        # Now let's dig into template_dir and add what matters.
        for filename in os.listdir(self.template_dir):
            # Skip files not ending with 'tpl'
            if not filename.endswith(".tpl"):
                continue

            # Put each file in its proper place
            source = os.path.join(self.template_dir, filename)
            target = os.path.join(self.target_dir, filename[:-4])
            if self.write and os.path.isfile(target):
                printc(bcolors.WARNING, "Skipping {}".format(target))
                continue
            with open(source, "r") as f_source:
                content = self.read_and_convert(f_source)
                if self.write:
                    printc(bcolors.INFO, "Writing  {}".format(target))
                    with open(target, "w") as f_target:
                        f_target.write(content)
                else:
                    printc(bcolors.INFO, target)
                    printc(bcolors.INFO, "=" * len(target))
                    print(content)

    def cmdrun(self,):
        """Perform bootstrapping.
        """
        # Basic directories
        # self.target_dir = self.get_provision_dir()
        self.target_dir = self.get_provision_dir(os.path.abspath(os.path.curdir))
        self.template_dir = os.path.join(HERE, "templates")

        # Guess project name if not given
        if not self.project_name:
            self.project_name = os.environ.get("PROJECT_NAME")
            if not self.project_name:
                self.project_name = os.path.split(os.path.abspath(os.path.curdir))[-1]
                os.environ["PROJECT_NAME"] = self.project_name

        # We may have to create target_dir
        if self.write and not os.path.isdir(self.target_dir):
            os.mkdir(self.target_dir)

        # Now let's dig into template_dir and add what matters.
        self.install_templates()

        # Now let's create docker-compose files for our environments
        # based on running instances
        self.setup_compose()
        self.update_compose("dev", {})
