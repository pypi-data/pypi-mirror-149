#!/usr/bin/env python
# encoding: utf-8
"""
commands.py

Created by Pierre-Julien Grizel et al.
Copyright (c) 2019 NumeriCube. All rights reserved.

Basic commands for dmake
"""
# Python3 rocks :)
import argparse
import inspect
import os
import pprint
import re
import sys

from . import command_registry
from .common import HERE
from .common import bcolors
from .common import printc
from .common import system

# pylint: disable=E0401,E1101
__author__ = ""
__copyright__ = "Copyright 2016, NumeriCube"
__credits__ = ["Pierre-Julien Grizel"]
__license__ = "CLOSED SOURCE"
__version__ = "TBD"
__maintainer__ = "Pierre-Julien Grizel"
__email__ = "pjgrizel@numericube.com"
__status__ = "Production"


def subcommand(method):
    """Decorator to mark a method as a command.
    Arguments is the same syntax as elsewhere."""

    def inner_subcommand(command_instance, *args, **kwargs):
        """Just call the command instance"""
        return method(command_instance, *args, **kwargs)

    inner_subcommand.__doc__ = method.__doc__
    return inner_subcommand


class _BaseCommand(object):
    """This is what all commands inherit from
    """

    arguments = ()
    verbose = False
    epilog = ""
    cloud_manager = None
    env = "dev"

    def __init__(self, *args, **kwargs):
        """Basic init (register parameters).
        After that you can use eg "self.verbose" to find back stored values.
        """
        # Load kwargs vars (command arguments)
        for name, value in kwargs.items():
            setattr(self, name, value)

        # Load environment
        self.load_environment()

    def re_make(self, *args):
        """Re-run the internal make command with the given (probably string) args
        """
        from . import cmd

        if self.verbose:
            printc(
                bcolors.INFO,
                "Re-running dmake with the following args: {}".format(args),
            )
        cmd.main(*args)

    def get_today_tag(self,):
        """Compute today's tag
        """
        if not os.environ.get("TODAY_TAG"):
            if self.verbose:
                print("Compute today's tag")
            os.environ["TODAY_TAG"] = "v{}-{}".format(
                os.popen('date "+%Y-%m-%d-%H%M%S"').read().strip(),
                self.get_git_branch(),
            )
        return os.environ["TODAY_TAG"]

    def get_git_branch(self):
        """Return the git branch we're in ('master', 'develop', etc)
        Special treatment for TRAVIS here.
        """
        if os.environ.get("TRAVIS_BRANCH"):
            return os.environ["TRAVIS_BRANCH"]
        ret = self.system(
            r"""git -C %s branch|awk '/\*/ { print $2; }'"""
            % (self.get_project_root_dir()),
            capture=True,
            capture_stderr=True,
            fail_silently=True,
        )
        return ret
        # return (
        #     os.popen(
        #         r"""git -C %s branch|awk '/\*/ { print $2; }'"""
        #         % (self.get_project_root_dir())
        #     )
        #     .read()
        #     .strip()
        # )

    def get_project_root_dir(self,):
        """Return root dir for this project (according to git).
        If this is not a git project, return current directory.
        """
        if not os.environ.get("PROJECT_ROOT_DIR"):
            try:
                os.environ["PROJECT_ROOT_DIR"] = self.system(
                    "git rev-parse --show-toplevel", capture=True, capture_stderr=True
                ).strip()
            except OSError:
                os.environ["PROJECT_ROOT_DIR"] = os.path.abspath(os.path.curdir)
        return os.environ["PROJECT_ROOT_DIR"]

    def get_git_status(self,):
        """Return a dict holding information about current git status. Keys are:
        - modified: True if current repo has been modified since last commit (unsaved changes)
        - current_branch: Current branch name
        - current_commit: Latest commit id (on current branch)
        - latest_release: Latest release tag IN THIS TREE
            (will not consider releases this tree is not a child of)
            Format: tag-n-commit (where n is a number of commits this branch is ahead from).
            If no latest release is available, set to "norelease".
        - latest_release_commit: Commit hash of the latest release OR 1st commit,
            useful to make elaborated diffs.
        - revision: A string that indicates the revision number
        - revision_no_x: Same but without star
        """
        # Compute latest release and remove the trailing part if necessary
        try:
            latest_release = self.system(
                """git describe --tags --match="v????-??-??-??????*" --candidates=1000""",
                capture=True,
            )
            latest_release = re.sub(r"-[0-9]{1,5}-g[0-9a-f]{7}$", "", latest_release)
            latest_release_commit = self.system(
                "git rev-list -n 1 {}".format(latest_release), capture=True
            )[:7]
        except OSError:
            printc(bcolors.INFO, "You can safely ignore previous error message")
            latest_release = "norelease"
            latest_release_commit = self.system(
                "git rev-list --max-parents=0 HEAD", capture=True, capture_stderr=True
            )[:7]

        # Return our pretty dict
        base_dict = {
            "modified": bool(
                self.system("""git status -uno --porcelain""", capture=True)
            )
            and "*"
            or "",
            "current_branch": self.get_git_branch(),
            "current_commit": self.system("git rev-parse HEAD", capture=True)[:7],
            "latest_release": latest_release,
            "latest_release_commit": latest_release_commit,
        }

        # Additional vars
        base_dict["revision"] = "{}-{}{}".format(
            base_dict["current_branch"],
            base_dict["current_commit"],
            base_dict["modified"],
        )
        base_dict["revision_no_x"] = base_dict["revision"].replace("*", "")
        if self.verbose:
            pprint.pprint(base_dict)
        return base_dict

    def get_provision_dir(self, project_root_dir=None):
        """Try to find where docker-compose et al. files are lying.
        We look at the first 'docker-compose.yml' file we meet around here.
        We go up at most go_up levels from the 'HERE' directory.
        """
        # Easy case: we use env variable.
        # If we are given a project_root_dir, we reset it
        if not project_root_dir and os.environ.get("PROVISION_DIR"):
            return os.environ["PROVISION_DIR"]
        else:
            os.environ["PROVISION_DIR"] = ""

        # No PROVISION_DIR?
        # Then we start from current directory and go up,
        # until we find a 'provision' directory with a 'docker-compose.yml' file inside.
        # When we hit 'project_root_dir', we stop.
        # If we're not on a github repo, this will stop quite soon!
        if not project_root_dir:
            project_root_dir = os.path.abspath(self.get_project_root_dir())
        curdir = os.path.abspath(os.curdir)
        while True:
            provision_dir = os.path.join(curdir, "provision")
            if "provision" in os.listdir(curdir):
                # provision_dir = os.path.join(curdir, "provision")
                if "docker-compose.yml" in os.listdir(provision_dir):
                    break
            curdir = os.path.split(curdir)[0]
            if project_root_dir not in curdir:
                break

        # Still no provision dir? Then, default is './provision'.
        # Warning though: this directory may not exist.
        os.environ["PROVISION_DIR"] = provision_dir
        return os.environ["PROVISION_DIR"]

    def load_environment(self, ignore=("COMPOSE_PROJECT_NAME",)):
        """Load environment variables from the *.env files.
        Of course, we'll load the proper env depending on the env set in the options.
        """
        # Which env files we're working with
        os.environ["PROVISION_DIR"] = self.get_provision_dir()
        os.environ["PROVISION_HISTORY_DIR"] = os.path.join(
            self.get_provision_dir(), "history"
        )
        env_files = (
            os.path.join(os.environ["PROVISION_DIR"], "settings-common.env"),
            os.path.join(
                os.environ["PROVISION_DIR"], "settings-{}.env".format(self.env)
            ),
        )
        os.environ["TODAY_TAG"] = self.get_today_tag()

        # Append vars
        added_vars = {}
        for env_file in env_files:
            if not os.path.isfile(env_file):
                if self.verbose:
                    printc(bcolors.WARNING, "Ignoring {}".format(env_file))
                continue
            for item in [
                self._check_env_line(s, name_only=False)
                for s in open(env_file, "r").read().splitlines()
            ]:
                if item in (True, False):
                    continue

                # Skip items that make a mess, add other ones
                if item[0] in ignore:
                    continue
                os.environ[item[0]] = item[1]
                added_vars[item[0]] = True

        # Set specific vars
        os.environ["COMPOSE_PROJECT_NAME"] = os.environ.get(
            "PROJECT_NAME", "please-set-PROJECT_NAME"
        )

        # Display the resulting settings
        if self.verbose:
            added_vars = sorted(added_vars.keys())
            for v in added_vars:
                printc(bcolors.NONE, "{}={}".format(v, os.environ[v]))
            for v in ignore:
                printc(bcolors.NONE, "Ignored {} env variable".format(v))

    def _check_env_line(self, line, name_only=True):
        """Check that given env line is okay.
        Will return False is line is invalid.
        Will return the VARIABLE NAME if line is valid
        Will return True if it's a comment.
        Sorry for this crappy method signature...
        """
        # Empty line? We just skip
        if not line.strip():
            return True

        # Comment? Ok we accept.
        if re.match(r"#.*", line):
            return True

        # Check name/var
        match = re.match(r"(\w+)=(.*)", line)
        if not match:
            if self.verbose:
                printc(
                    bcolors.WARNING,
                    "Invalid line: '{}'. Avoid trailing spaces!".format(line),
                )
            return False

        # We're good
        if name_only:
            return match.groups()[0]
        return match.groups()

    @classmethod
    def register_parser(cls, subparsers):
        """Automatically register parser.
        Handles most basic cases but feel free to override for a more complex env.
        """
        # Double check that the calling method is available
        assert hasattr(
            cls, "cmdrun"
        ), "{} class must have a 'cmdrun' staticmethod".format(cls.__name__)

        # Register arguments
        parser = subparsers.add_parser(
            cls.__name__.replace("_", "-").lower(),
            help=cls.__doc__,
            description=cls.__doc__,
            epilog=cls.epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        for argument in cls.arguments:
            argument = argument.copy()
            name_or_flags = argument.pop("name")
            parser.add_argument(*name_or_flags, **argument)

        # Register call method, return the generated parser
        parser.set_defaults(cls=cls)

        # Return the generated parser (you never know)
        return parser

    def system(
        self,
        command,
        raise_on_error=True,
        fail_silently=False,
        description=None,
        capture=False,
        capture_stderr=False,
        strip_output=True,
    ):
        """Wrapper around os.system

        Keyword arguments:
        raise_on_error -- will throm an exception if return code is not 0
        fail_silently -- ignores if failure
        capture -- return captured string instead of error code
        """
        return system(
            command,
            raise_on_error=raise_on_error,
            fail_silently=fail_silently,
            description=description,
            capture=capture,
            capture_stderr=capture_stderr,
            strip_output=strip_output,
            verbose=self.verbose,
        )

    def docker_compose(self, *args, **kwargs):
        """Basic docker-compose execution.
        You just have to provide command parameters either as a list or a string.
        Use 'description' as a named parameter to change default description
        """
        # Set appropriate description
        if "description" in kwargs:
            description = kwargs.pop("description")
        else:
            description = "Executing docker-compose..."

        # Propagate to docker-compose
        basic_compose = (
            r"DEPLOY_ENV=%s docker-compose -f %s/docker-compose.yml -f %s/docker-${DEPLOY_ENV}.yml"
            % (self.env, os.environ["PROVISION_DIR"], os.environ["PROVISION_DIR"])
        )
        return self.system(
            r"{} {}".format(basic_compose, " ".join(args)),
            description=description,
            **kwargs
        )

    def get_latest_tag(self,):
        """Return the most recent branch from GH
        """
        branch = getattr(self, "branch", None) or self.get_git_branch()
        command = """git tag -l "v[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9]-*{}" --sort=version:refname""".format(
            branch
        )
        tags = self.system(
            command, description="Searching for the latest available tag", capture=True
        ).split()
        if not tags:
            printc(
                bcolors.WARNING,
                "No release has been made on the '{}' branch (yet)".format(branch),
            )
            return None
        return tags[-1]

    def get_current_swarm(self,):
        """Retreive (if possible) current swarm stack name
        """
        error = self.system(
            "docker stack ls", capture=True, capture_stderr=True, fail_silently=True
        )
        if "Error response" not in error:
            project_stack_re = re.search(
                r"({}-\w*)".format(os.environ["PROJECT_NAME"]), error
            )
            if project_stack_re:
                project_stack = project_stack_re.groups()[0]
                return project_stack
        return None


class LooseCommand(_BaseCommand):
    """Used of an argument instead of a command.
    Just override the run() method.
    """


class BaseCommand(_BaseCommand):
    """A command that's reported in the 'help' section.
    """


class BaseSubCommand(BaseCommand):
    """These classes can have a run() method _and_ subcommands,
    which are commands decorated with the subcommand() decorator.
    Default implementation is just to call the subcommand
    """

    method = None

    def cmdrun(self):
        """Execute (sub)command. You can overload this if necessary.
        Default is to execute submethod and report help if it's not found."""
        # No submethod specified? Stop here.
        if not self.method:
            self.parser.error("Subcommand is required.")

        # Bind method and execute it
        method = self.method.__get__(self, self.__class__)
        return method()

    @classmethod
    def register_parser(cls, subparsers):
        """Register the sub-commands
        """
        # Regular registery
        cls.parser = super(BaseSubCommand, cls).register_parser(subparsers)

        # Register sub-sub-parsers and their arguments
        # (well I should put arguments as a decorator parameter, but I'm lazy today)
        methods = [
            method
            for method in inspect.getmembers(cls, predicate=inspect.isfunction)
            if method[1].__name__ in ("inner_subcommand", "real_subcommand")
        ]
        if methods:
            subsubparsers = cls.parser.add_subparsers(
                help="Action to perform on your source tree", dest="subcommand"
            )
            for method in methods:
                if method[1].__name__ not in ("inner_subcommand", "real_subcommand"):
                    continue
                method_name = method[0].replace("_", "-")
                while method_name.endswith("-"):
                    method_name = method_name[:-1]
                sub = subsubparsers.add_parser(method_name, help=method[1].__doc__)
                sub.set_defaults(method=method[1])

                # Arguments are xxx_arguments, xxx being the subcommand name
                for argument in getattr(cls, "{}_arguments".format(method[0]), ()):
                    argument = argument.copy()
                    name_or_flags = argument.pop("name")
                    sub.add_argument(*name_or_flags, **argument)


# ########################################################################## #
# ####                    Cloud Management (generic)                    #### #
# ########################################################################## #


class CloudManagerCommand(LooseCommand):
    """Abstract class of a cloud manager.
    Override this with your own provider (AWS, Azure, ...)
    """

    def print_status(self,):
        """Print status about your cloud manager
        """
        raise NotImplementedError("Please override this")

    def push_image(self, image, release_tag):
        """Push an image on your cloud manager
        """
        raise NotImplementedError("Please override this")

    def get_image_info(self, image, tag):
        """Return info from the given tag on the repository
        """
        raise NotImplementedError("Please override this")

    def setup(self):
        """Configure your cloud services."""
        raise NotImplementedError("Please override this")


# ########################################################################## #
# ########################################################################## #
# ####                                                                  #### #
# ####                 THE ACTUAL COMMANDS START HERE                   #### #
# ####                                                                  #### #
# ########################################################################## #
# ########################################################################## #


# ########################################################################## #
# ####                          Stack management                        #### #
# ########################################################################## #


class Docker(BaseCommand):
    """Execute docker with the proper arguments. Especially useful with '--machine'.
    Put your arguments in quotes to have them processed correctly (sorry).
    If your command starts by a modifier, add a space before it to avoid it being processed by dmake.
    For example: dmake docker " -help".
    """

    arguments = (
        {
            "name": ("pass_along_command",),
            "help": "Command to pass along to the whole docker-compose chain. Example: 'ps --services'.",
            "action": "store",
            "nargs": argparse.REMAINDER,
            "default": " --help",  # Space here to avoid the argument being consumed by argparse()
        },
    )

    def cmdrun(self):
        """Run docker-compose against the stack
        """
        # if not isinstance(self.pass_along_command, list):
        #     self.pass_along_command = [self.pass_along_command]
        return self.system("docker {}".format(" ".join(self.pass_along_command)))


class Upgrade(BaseCommand):
    """Upgrade dmake to the most recent version.
    """

    # arguments = (
    #     {
    #         "name": ("-y",),
    #         "help": "Do not ask for confirmation.",
    #         "action": "store_true",
    #         "dest": "yes",
    #     },
    # )

    def cmdrun(self,):
        """Upgrade pip to the latest version
        """
        return self.system(
            "{} -m pip install https://numericube.blob.core.windows.net/dmake-public/dmake-generic-py3-none-any.whl".format(
                sys.executable
            )
        )


class Docker_Compose(BaseCommand):
    """Execute docker-compose with the proper arguments. Pass them in quotes to have them processed correctly (sorry).
If your command starts by a modifier, add a space before it to avoid it being processed by dmake.
For example: dmake docker-compose " -help".
    """

    arguments = (
        {
            "name": ("pass_along_command",),
            "help": "Command to pass along to the whole docker-compose chain. Example: 'ps --services'.",
            "action": "store",
            "nargs": argparse.REMAINDER,
            "default": " --help",  # Space here to avoid the argument being consumed by argparse()
        },
    )

    def cmdrun(self):
        """Run docker-compose against the stack
        """
        return self.docker_compose(" ".join(self.pass_along_command))


class Docker_Machine(BaseCommand):
    """Execute docker-machine with the proper arguments. Pass them in quotes to have them processed correctly (sorry).
If your command starts by a modifier, add a space before it to avoid it being processed by dmake.
For example: dmake docker-machine " -help".
    """

    arguments = (
        {
            "name": ("pass_along_command",),
            "help": "Command to pass along to the whole docker-compose chain. Example: 'ps --services'.",
            "action": "store",
            "nargs": argparse.REMAINDER,
            "default": " --help",  # Space here to avoid the argument being consumed by argparse()
        },
    )

    def cmdrun(self):
        """Run docker-machine against the stack
        """
        return self.system(
            "docker-machine {}".format(" ".join(self.pass_along_command))
        )


class Shell(BaseCommand):
    """Run a sub-shell with all environment variables set according to your project settings
    AND envionment.
    """

    def cmdrun(self,):
        """Run a shell with the proper env variables
        """
        # Display environment we're working on
        printc(
            bcolors.INFO,
            "Starting dmake in '{}' env".format(self.env),
        )

        # See https://stackoverflow.com/questions/8687940/start-bash-process-with-changed-prompt-ps1
        current_swarm = self.get_current_swarm()
        if current_swarm and self.machine:
            prompt = "{}@{}".format(current_swarm, self.machine)
        elif self.machine:
            prompt = "@{}".format(self.machine)
        else:
            prompt = "@local"

        # Say nice things about what's happening here
        printc(bcolors.INFO, "You're running a customized shell.")
        printc(
            bcolors.INFO,
            "All your env variables are set according to your docker-compose files.",
        )
        printc(
            bcolors.INFO,
            "Also, 'docker*' commands are aliased to their 'dmake docker*' counterparts.",
        )
        if self.env == "dev":
            printc(
                bcolors.WARNING,
                "Don't forget to set 'export ENV=xxx' according to your stack.",
            )
        print()

        # Execute shell with proper options
        dmake_program = sys.argv[0]
        if os.path.isfile(os.path.expanduser("~/.bashrc")):
            self.system("cat ~/.bashrc > /tmp/provision-bash-rc")
        self.system(
            """echo 'PS1="DOCKER {0}> "' >> /tmp/provision-bash-rc""".format(
                prompt
            )
        )
        # self.system(
        #     """echo '{} status' >> /tmp/provision-bash-rc""".format(dmake_program)
        # )
        self.system(
            """echo 'alias docker="{} docker"' >> /tmp/provision-bash-rc""".format(
                dmake_program
            )
        )
        self.system(
            """echo 'alias docker-compose="{} docker-compose"' >> /tmp/provision-bash-rc""".format(
                dmake_program
            )
        )
        self.system(
            """echo 'alias docker-machine="{} docker-machine"' >> /tmp/provision-bash-rc""".format(
                dmake_program
            )
        )
        self.system("""PS1=DOCKER /bin/bash --rcfile /tmp/provision-bash-rc""")
