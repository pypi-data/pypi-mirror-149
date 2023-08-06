#!/usr/bin/env python
# encoding: utf-8
"""
status.py

Created by Pierre-Julien Grizel et al.
Copyright (c) 2019 NumeriCube. All rights reserved.

Status command. Big stuff.
"""
# Python3 rocks :)
import distutils.version
import glob
import os
import re
import textwrap

from . import base_commands
from . import common
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
# ####                        Sanity checks                             #### #
# ########################################################################## #


class Status(base_commands.BaseCommand):
    """Double-check that this project structure is up and running."""

    # See http://lists.logilab.org/pipermail/python-projects/2012-September/003261.html
    # pylint: disable=W1401
    epilog = textwrap.dedent(
        r"""\
        {0.TITLE}
        How to organise your stack?
        ==========================={0.ENDC}

        We kept a few philosophy guidelines when constructing this builder.

        * Keep a 'common' environment that is as close as possible as the target (prod) env.
            This is what './provision/docker-compose.yml' files is for.

        * Use harmless configuration settings in ./provision/settings-common.env.
            Put ALL of your configuration settings in this file, as if you were trying
            to configure either your dev or preprod environment. Then, customize only
            sensible variables in 'settings-dev.env', 'settings-prod.env', etc.
            For example, "DEBUG" settings should be false in 'settings-common.env' but true in settings-dev.env.
            But your database settings/passwords should be those of the preprod in 'settings-common.env'.

        * Make dev environment a "layer" above the common env.
            In dev env, you'll probably have MORE services than in actual production.
            Hence, we provide you the ./provision/docker-dev.yml file to add as much local containers as you want.

        * No manual task beside container starts.
            That means you *HAVE* to forget about manually running "django-admin migrate" because
            it's not compatible with a continuous integration environment. You should always assume
            that you WON'T be the guy deploying your product (in most cases, a robot will do it for you)

        --------

        For the commands of this dmake program, we use those guidelines:

        * Try to keep as close as docker's original commands as possible

        * Intensive use of environment variables INSIDE the dmake program, not outside
          (ie. you should generally avoid defining export=XXX in your shell, use program arguments for that)

        * Some arguments act as "modifiers". This is especially true for --aws --env and --machine arguments.
          Using those arguments will modify inner working of docker commands to make the most of the given parameters.
          For example, "dmake status" behaves differentyl if you add --aws or --machine arguments.

        * We try to avoid pushing you to remember complex commands and arguments (and provide an extensive online help).
          Normally once you get used to it, most commands are straightforward and we make a lot of safety checks.
          If 'dmake --aws --env=prod --machine=my-machine deploy' is too complex for a command line,
          then write it in the README of your project ;) We could make things simpler only by loosing functionality
          (in this example that would mean storing 'env' or 'machine' as env variables but then you'd have to
          keep track of environment-machine matching in a separate file, with a specific syntax, etc.).

        {0.TITLE}
        Sensitive variables for our dmake script
        ============================================
        {0.ENDC}
        We provide a few ENV var shortcuts that we recommend you put in your ./provision/settings-common.env file.

        {0.BOLD}PROJECT_NAME                        {0.ENDC}=> (mandatory) Your stack name ;)
        {0.BOLD}MAKE_DEFAULT_SERVICE                {0.ENDC}=> Default container when running or debugging

        {0.TITLE}
        Variables you can use in your docker-compose.yml or projects
        ============================================================
        {0.ENDC}
        Define those in your settings-xxx.env file
        ------------------------------
        {0.BOLD}${{PROJECT_NAME}}                   {0.ENDC}=> The name of your stack.

        Those are automatically set for you
        -----------------------------------
        {0.BOLD}${{DEPLOY_TAG:-}}                   {0.ENDC}=> The vXXXXXX version you're deploying.
        {0.BOLD}${{DOCKER_REGISTRY:-}}              {0.ENDC}=> Registry used to hold personalized images.
                                                               The variable includes a trailing slash if set.
        {0.BOLD}${{DOCKER_AWS_REGISTRY:-}}          {0.ENDC}=> Same but *only* for AWS registry
                                                               (if you need to use images from different repositories)
        {0.BOLD}${{ADDITIONAL_ARGS:-}}              {0.ENDC}=> Use this in your docker-xxx.yml files to allow appending
                                                               of command arguments for some commands (eg. 'make stack start --args=')
        {0.BOLD}${{GIT_COMMIT}}                     {0.ENDC}=> NOT RECOMMENDED* Commit id of the current HEAD (useful for tracking, for example)

        * Not recommended because it will use your current dir's git status, not the version you're releasing git's status.
          Use ${{DEPLOY_TAG}} instead, preferably.

        {0.TITLE}
        What is environment overriding?
        ===============================
        {0.ENDC}
        One can override specific settings (either env variables or container orchestration)
        in a specific environment.
        {0.FAIL}WARNING: Only containers in main ./docker-compose.yml will be built and pushed{0.ENDC}
        That means you cannot have a production container that's not declared in the main ./docker-compose.yml.
        But you can have replications of an image that's already declared there (useful for django setup, for example).
        For example, this is allowed:

        In ./docker-compose.yml:
          {0.INFO}project-container:
            build: ../project-container                                 # Container's local dir
            image: ${{DOCKER_REGISTRY:-}}numericube/project-container:${{DEPLOY_TAG:-latest}}   # Automatically set image tag
            command: my-command ${{ADDITIONAL_ARGS}}                    # To allow additional command args to be passed along
            [...]
        {0.NONE}

        In ./provision/docker-production.yml:
          {0.INFO}project-other-container:
            build: ../project-container                                 # Same as project-container
            image: ${{DOCKER_REGISTRY:-}}numericube/project-container:${{DEPLOY_TAG:-latest}}   # Same as project-container
            [...]
        {0.NONE}

        {0.TITLE}
        How to configure your inner containers and apps
        ===============================================
        {0.ENDC}
        Short answer: use *exclusively* environment variables!
        The settings-*.env files are made for this: so that you can always have in your correct environment
        the correct variables loaded and ready to use.

        For images built specifically for this project, use the following structure for your services:

          {0.INFO}project-container:
            build: ../project-container                                 # Container's local dir
            image: ${{DOCKER_REGISTRY:-}}numericube/project-container:${{DEPLOY_TAG:-latest}}   # Automatically set image tag
            command: my-command ${{ADDITIONAL_ARGS}}                    # To allow additional command args to be passed along
            env_file:                                                   # Hierarchically set env
              - ./provision/settings-common.env
              - ./provision/settings-${{DEPLOY_ENV}}.env
        {0.NONE}

        {0.FAIL}CAUTION: Never use environment-specific code in your containers.{0.ENDC}
        Everything must be handled via env variables (you can do 'if MYVAR' on env variables, of course)

        Wanna see how powerful it is? Here's an example on how you should setup Postgres from docker-compose.yml:

          {0.INFO}db:
            image: postgres
            environment:
              - PGDATA=/var/lib/postgresql/data/pgdata
            env_file:
              - ./provision/common.env
              - ./provision/settings-${{DEPLOY_ENV}}.env
            volumes:
              - pgdata:/var/lib/postgresql/data/pgdata{0.ENDC}

        In your Django's settings, you just have to reference the DB in the following way:
          {0.INFO}
            DEBUG = bool(os.environ["DJANGO_DEBUG"])
            DATABASES = {{
                "default": {{
                    "ENGINE": "django.db.backends.postgresql",
                    "NAME": os.environ["POSTGRES_DB"],
                    "USER": os.environ["POSTGRES_USER"],
                    "PASSWORD": os.environ["POSTGRES_PASSWORD"],
                    "HOST": os.environ["DJANGO_DB_HOST"],
                    "PORT": "",
                }}
            }}
          {0.ENDC}

        And then, in settings-common.env (that you'll override with specific settings for each env afterwards):
          {0.INFO}
            POSTGRES_DB=myapp
            POSTGRES_USER=myuser
            POSTGRES_PASSWORD=devpassword
            DJANGO_DB_HOST=db
            DJANGO_DEBUG=
          {0.ENDC}

        This way:
        * PG container is automatically setup with the proper settings (thank to Docker's container settings)
        * DEBUG is set in Django only if it's overridden in other envs (in 'dev' environment, for example ;))
        * PG settings are passed along Django

        {0.TITLE}
        How to manage your unit tests
        =============================
        {0.ENDC}
        Here's how to configure unittests in the most practical way.

        Test-specific environment
        -------------------------
        This is very convenient for your continuous-integration platform: you just fire services you want to use
        for your tests, and forget about everything else.
        We recommend keeping your test environment as close to production as possible.

        Create a whole 'test' environment (with settings-test.env and docker-test.yml) and configure your docker-test.yml
        as in the following example (ie. enabling or disabling services):
          {0.INFO}
            services:
              my-django:
                command: ${{UNITTEST_COMMAND}} ${{ADDITIONAL_ARGS:-}}

              my-celery-worker:
                command: sleep infinity

              my-rabbitmq:
                command: sleep infinity
          {0.ENDC}

        REMARK: When running 'dmake stack test', the test environment inheritates from both 'common' and the given
        environment (default being dev). So you stack 3 environments in one command ;)

        Once it's done, tests can be run either in a brand new environment or inside a running stack:
          {0.ECHO}dmake stack test [<args>]{0.NONE}              # Starts a whole new test session
          {0.ECHO}dmake stack exec "\$UNITTEST_COMMAND" [<args>]{0.NONE}     # If your dev stack is running, test on-demand on the default container

        {0.TITLE}
        Getting started with AWS deployment
        ===================================
        {0.ENDC}
        First of all: you can check AWS configuration by doing "dmake --aws status".

        Profile configuration
        ---------------------

        1/ Install AWS (see dmake status output for URL for the documentation)

        2/ Configure AWS depending on your profile. Two ways of doing this:

            - {0.ECHO}aws configure [for your default profile]{0.NONE}
            - {0.ECHO}aws configure --profile <profile> [for eg. another customer]{0.NONE}

        Now, whenever you want to use a non-default profile, use:

            {0.ECHO}dmake --aws-profile=other <rest of your commands>{0.NONE}

        Machine creation / provisioning
        -------------------------------

        Check your AWS status with dmake --aws status first.
        You can use the following command to create an ECS instance on the spot:

            {0.OKBLUE}dmake --aws docker-machine create testdockermachine --amazonec2-subnet-id=<subnet-id> --amazonec2-vpc-id=<vpc-id> --amazonec2-zone={{a|b|c}}{0.NONE}

        Existing machine on AWS? See this documentation: https://docs.docker.com/machine/drivers/generic/

        ECR management
        --------------

        When you pass --aws parameter, everything is taken care of for you.
        Repositories are even created at release time if you include the --create-repository option.


        {0.TITLE}
        Getting started with Azure deployment
        =====================================
        {0.ENDC}
        First of all: you can check Azure configuration by doing "dmake --azure status".

        Put the following variables in settings-common.env (or overload in settings-*.env):

            * {0.BOLD}AZURE_RESOURCE_GROUP{0.NONE}                  Resource group you're putting your project on. We advise same as PROJECT_NAME.
            * {0.BOLD}AZURE_ACR_NAME{0.NONE}                        ACR (Container Registry). We advise same as PROJECT_NAME.

        {0.TITLE}Login / Setup / Ressource group & ACR creation
        ---------------------------------------{0.ENDC}

        On your laptop:

            1/ Install Azure client locally

            2/ Login (will redirect to a browser): az login

            3/ Create a resource group and an ACR (registry), see below.

        This step must be done only once (either globally if you share settings, or on each environment if you use separated settings)

        Basic registries should be okay but check `https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-azure-cli` for other options

            {0.ECHO}dmake shell{0.ENDC}
            {0.ECHO}az group create --name ${{AZURE_RESOURCE_GROUP:?}} --location francecentral{0.ENDC}
            {0.ECHO}az acr create --resource-group ${{AZURE_RESOURCE_GROUP:?}} --name ${{AZURE_ACR_NAME:?}} --sku Basic{0.ENDC} (you may have to use {0.ECHO}--location westeurope{0.ENDC} as France doesn't offer ACR service yet)

        You're done!

        {0.TITLE}Machine creation / provisioning
        -------------------------------{0.ENDC}

        Easy (kinda.).

            # Create machines
            {0.OKBLUE}dmake --env=SET_THIS_TO_YOUR_ENV shell{0.NONE}
            {0.OKBLUE}dmake --azure status{0.NONE} # Check that all mandatory variables are set
            {0.OKBLUE}dmake --azure docker-machine create --azure-resource-group ${{AZURE_RESOURCE_GROUP:?}} --azure-subscription-id ${{AZURE_SUBSCRIPTION_ID:?}} --swarm-master --azure-location francecentral ${{AZURE_RESOURCE_GROUP:?}}-${{DEPLOY_ENV:?}}{0.NONE}
            {0.OKBLUE}dmake --azure --machine ${{AZURE_RESOURCE_GROUP:?}}-${{DEPLOY_ENV:?}} docker swarm init{0.NONE} # This one sometimes fail? Try again until it says your swarm is ok

            # (Didn't solve the Cloudstor driver issue yet :/ Don't execute those commands yet.)
            # (But you can use Docker Swarm without these, but Docker-volumes-over-Blob volumes won't be available.)
            # (docker volumes will use the traditional, legacy driver)
            {0.OKBLUE}dmake --machine $AZURE_RESOURCE_GROUP-$DEPLOY_ENV docker plugin install docker4x/cloudstor:18.06.1-ce-azure{0.NONE}
            {0.OKBLUE}docker plugin install --alias cloudstor:azure --grant-all-permissions docker4x/cloudstor:17.06.0-ce-azure1 CLOUD_PLATFORM=AZURE AZURE_STORAGE_ACCOUNT_KEY="$SA_KEY" AZURE_STORAGE_ACCOUNT="$SA" DEBUG=1


        {0.TITLE}Cluster creation (WORK IN PROGRESS)
        -----------------------------------{0.ENDC}

        (advanced users only! Alternatively, use Azure Portal to create nodes "by hand" and connect them to your Swarm master)

        docker run -ti -v /Users/pjgrizel/.ssh:/root/.ssh -v /Users/pjgrizel/.azure:/root/.azure docker4x/create-sp-azure sp-swarm-$PROJECT_NAME-preprod $AZURE_RESOURCE_GROUP francecentral

        => Take good note of the output:

        Your access credentials:
        AD ServicePrincipal App ID:       => put this in AZURE_AD_SP_APP_ID
        AD ServicePrincipal App Secret:   => put this in AZURE_AD_SP_APP_SECRET
        AD ServicePrincipal Tenant ID:    => put this in AZURE_AD_SP_TENANT_ID

        Then:

        az group deployment create --resource-group $AZURE_RESOURCE_GROUP --name docker.template --template-uri https://download.docker.com/azure/stable/Docker.tmpl

        """.format(
            bcolors
        )
    )

    def get_env_names(self,):
        """Return available env names
        """
        env_files = glob.glob(os.path.join(self.get_provision_dir(), "settings-*.env"))
        env_names = [
            os.path.splitext(os.path.split(env)[1])[0].replace("settings-", "")
            for env in env_files
        ]
        if "common" in env_names:
            env_names.pop(env_names.index("common"))
        env_names.sort()
        return env_names

    def check_paths(self):
        """Double check that paths are ok
        """
        ok = True

        # Double check that there's a 'docker-compose'
        if not os.path.isfile(
            os.path.join(os.environ["PROVISION_DIR"], "docker-compose.yml")
        ):
            ok = False
            printc(bcolors.WARNING, "File ./docker-compose.yml missing")

        # Check 'provision' structure
        if not os.path.isdir(os.environ["PROVISION_DIR"]):
            ok = False
            printc(
                bcolors.WARNING,
                "Directory {} missing".format(os.environ["PROVISION_DIR"]),
            )

        # Check docker-compose file structure for every environment
        env_names = self.get_env_names()
        if not env_names:
            ok = False
            printc(bcolors.WARNING, "[DMAKE] No environment set!")
            print(
                textwrap.dedent(
                    """\
                => To fix this, you must include a few settings-xxx.env and docker-xxx.yml files in the provision/ directory.
                You should have at least a docker-dev.yml file for your dev environment.
                It could be as simple as the string "version: '3.4'" on the top of the file, but it must be there.
            """
                )
            )

        # Do we have a dev env?
        if "dev" not in env_names:
            ok = False
            printc(
                bcolors.WARNING,
                "[DMAKE] dev environment missing, please add docker-dev.yml and settings-dev.env files.",
            )
        if not os.path.isfile(
            os.path.join(os.environ["PROVISION_DIR"], "settings-common.env")
        ):
            ok = False
            printc(
                bcolors.WARNING,
                "[DMAKE] Common environment missing, please add settings-common.env file.",
            )

        # Are environments ok?
        for env_name in env_names:
            if self.verbose:
                printc(
                    bcolors.DESCRIBE,
                    "[DMAKE] Checking {} environment...".format(env_name),
                )

            # Check docker-xxx.yml file structure
            if not os.path.isfile(
                os.path.join(
                    os.environ["PROVISION_DIR"], "docker-{}.yml".format(env_name)
                )
            ):
                ok = False
                printc(
                    bcolors.WARNING,
                    "  {}/docker-{}.yml file missing!".format(
                        os.environ["PROVISION_DIR"], env_name
                    ),
                )

            # Check if there are no spaces in env files
            env_content = open(
                os.path.join(
                    os.environ["PROVISION_DIR"], "settings-{}.env".format(env_name)
                ),
                "r",
            ).read()
            if " =" in env_content or "= " in env_content:
                ok = False
                printc(
                    bcolors.WARNING,
                    "  File settings-{}.env has spaces around the '=' sign (it's forbidden)".format(
                        env_name
                    ),
                )

        return ok

    def check_env_overrides(self,):
        """Double check that only variables defined in 'settings-common.env' are overridden in other envs.
        """
        ok = True
        env_file = os.path.join(os.environ["PROVISION_DIR"], "settings-common.env")
        if not os.path.isfile(env_file):
            return False

        # Check that each line is ok
        common_vars = []
        for common_var in [
            self._check_env_line(s) for s in open(env_file, "r").read().splitlines()
        ]:
            if common_var in (True, False):
                continue
            common_vars.append(common_var)

        # Ok, so now we're going to do the same for other envs!
        for env in self.get_env_names():
            env_file = os.path.join(
                os.environ["PROVISION_DIR"], "settings-{}.env".format(env)
            )
            if not os.path.isfile(env_file):
                continue
            for env_var in [
                self._check_env_line(s) for s in open(env_file, "r").read().splitlines()
            ]:
                if env_var in (True, False):
                    continue
                if env_var not in common_vars:
                    printc(
                        bcolors.WARNING,
                        "Variable '{}' in settings-{}.env but not in settings-common.env".format(
                            env_var, env
                        ),
                    )
                    ok = False

        # Thank you
        return ok

    def check_docker(self,):
        """Double-check Docker and Docker-compose versions
        """
        # Execute Docker cli
        try:
            version = self.system(
                "docker --version",
                raise_on_error=True,
                capture=True,
                capture_stderr=True,
            )
        except OSError:
            printc(bcolors.WARNING, "Docker not installed.")
            return False

        # Check minimum version
        # Example return:
        # Docker version 18.06.1-ce, build e68fc7a
        docker_v = re.match("Docker version ([0-9.]*)", version).groups()[0]
        if distutils.version.LooseVersion(docker_v) < distutils.version.LooseVersion(
            common.DOCKER_MINIMUM_VERSION
        ):
            printc(
                bcolors.WARNING,
                "Docker version too old ({}). Use at least {}.".format(
                    docker_v, common.DOCKER_MINIMUM_VERSION
                ),
            )
            return False

        # We're good!
        return True

    def check_awscli(self,):
        """Double-check AWS CLI version
        """
        # Execute AWS cli
        try:
            version = self.system(
                "aws --version", raise_on_error=True, capture=True, capture_stderr=True
            )
        except OSError:
            printc(
                bcolors.WARNING,
                "awscli not installed. See https://docs.aws.amazon.com/fr_fr/cli/latest/userguide/cli-chap-install.html for instructions on how to install it.",
            )
            return False

        # Check minimum version
        # Example return:
        # aws-cli/1.9.17 Python/2.7.10 Darwin/18.2.0 botocore/1.3.17
        awscli_v = re.match("aws-cli/([0-9.]*)", version).groups()[0]
        if distutils.version.LooseVersion(awscli_v) < distutils.version.LooseVersion(
            common.AWSCLI_MINIMUM_VERSION
        ):
            printc(
                bcolors.WARNING,
                "awscli version too old ({}). Use at least {}.\n"
                "See https://docs.aws.amazon.com/fr_fr/cli/latest/userguide/cli-chap-install.html for upgrade instructions.".format(
                    awscli_v, common.AWSCLI_MINIMUM_VERSION
                ),
            )
            return False

        # We're good!
        return True

    def check_env(self,):
        """Check mandatory/highly recommended variables
        """
        ok = True
        for var in common.RECOMMENDED_VARIABLES:
            if not os.environ.get(var):
                ok = False
                print(
                    "{0.WARNING}Missing '{1}' variable in your settings-common.env file: {0.NONE}{2}".format(
                        bcolors, var, common.RECOMMENDED_VARIABLES[var]
                    )
                )
        return ok

    def cmdrun(self):
        """Check that project structure is up and running
        """
        # Display basic information
        # We use variables here in order to have the same behaviour
        # with or without 'verbose'.
        project_root_dir = self.get_project_root_dir()
        provision_dir = self.get_provision_dir()
        git_branch = self.get_git_branch()
        if self.verbose:
            printc(bcolors.INFO, "Project root dir: {}".format(project_root_dir))
            printc(bcolors.INFO, "Provision dir: {}".format(provision_dir))
            printc(bcolors.INFO, "Current branch: {}".format(git_branch))

        # Check paths and files
        ok = self.check_paths()
        ok = self.check_env_overrides() and ok

        # Check various CLI versions
        ok = self.check_awscli() and ok
        ok = self.check_docker() and ok

        # Check variables
        ok = self.check_env() and ok

        # Linespace if necessary
        if not ok:
            print()

        # Print GIT branch
        if self.verbose:
            print(
                "{0.BOLD}Git branch{0.NONE}: {1}".format(bcolors, self.get_git_branch())
            )

        # Docker machine info
        print("{0.TITLE}Docker Machines{0.NONE}".format(bcolors))
        print("{0.TITLE}==============={0.NONE}".format(bcolors))
        self.system("docker-machine ls")

        # Docker stack?
        error = self.system(
            "docker stack ls", capture=True, capture_stderr=True, fail_silently=True
        )
        if "Error response" not in error:
            print()
            print("{0.TITLE}Docker Swarm Stacks{0.NONE}".format(bcolors))
            print("{0.TITLE}==================={0.NONE}".format(bcolors))
            print(error)
            current_swarm = self.get_current_swarm()
            if current_swarm:
                print()
                command = (
                    r"docker stack ps %s --format 'table {{.Name}}\t{{.Image}}\t{{.CurrentState}}\t{{.Error}}'  -f 'Desired-state=Running' -f 'Desired-state=Ready'"
                    % (current_swarm,)
                )
                print(
                    "{0.TITLE}'{1}' stack{0.NONE} ({0.ECHO}{2}{0.NONE})".format(
                        bcolors, current_swarm, command
                    )
                )
                self.system(command)
            print()
            print(
                "{0.TITLE}Active services{0.NONE} ({0.ECHO}docker service ls{0.NONE})".format(
                    bcolors
                )
            )
            self.system(
                "docker stack ls", capture=False, capture_stderr=False, fail_silently=True
            )

        # AWS stuff is precised
        if self.cloud_manager:
            print()
            self.cloud_manager.print_status()

        # Print status message
        if not ok:
            printc(bcolors.FAIL, "[DMAKE] Please correct the indicated errors.")
