#!/usr/bin/env python
# encoding: utf-8
"""
doc.py

Created by Pierre-Julien Grizel et al.
Copyright (c) 2019 NumeriCube. All rights reserved.

Documentation management
"""
# Python3 rocks :)
import csv
import os
import re

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

LATEX_RESERVED = r"\#$%&~_^{}"  # Slash is first because we would replace everything ;)


def latex_quote(my_str, squash=False):
    """Quote LaTeX strings.
    If squash, will not quote but remove invalid characters
    """
    for kr in LATEX_RESERVED:
        my_str = my_str.replace(kr, not squash and r"\{}".format(kr) or "")
    return my_str


class Doc(base_commands.BaseCommand):
    """Make a new release from the given source tree, ready for Continuous Integration process.

    If you want to create a new doc, use the following command:

    dmake doc --create N3-CUS-PRJ-TYP

    You can see the doc generation progress with dmake -v option.
    """

    arguments = (
        {
            "name": ("--create",),
            "help": "New doc name (format is N3-CUS-PRJ-TYP)",
            "action": "store",
        },
        {
            "name": ("--nolatex",),
            "help": "Do everything BUT latex processing",
            "action": "store_true",
        },
        {
            "name": ("--without-dmake",),
            "help": "Do NOT include dmake official documentation (aka quality plan)",
            "action": "store_true",
        },
    )

    def preprocess(self, doc_reference, doc_dir, docgen_dir):
        """Preprocess documentation by pre-writing tex stuff
        """
        self.preprocess_commit_history(doc_reference, doc_dir, docgen_dir)
        self.preprocess_variables(doc_reference, doc_dir, docgen_dir)

    def preprocess_commit_history(self, doc_reference, doc_dir, docgen_dir):
        r"""Build a complete commit history as a (possibly very big) table.
        Outputs are:
        - commit_history.tex
        - release_history.csv (headers: commit,tag)
        """
        # RELEASE HISTORY
        awk_reverse = r"""awk '{ x = $0 "\n" x } END { printf "%s", x }'"""
        ls_remote = latex_quote(
            self.system(
                "git ls-remote --tags --refs | {}".format(awk_reverse), capture=True
            )
        )
        ls_remote = ls_remote.replace("refs/tags/", "")
        reader = csv.reader(ls_remote.split("\n"), delimiter="\t")
        with open(os.path.join(docgen_dir, "release_history.csv"), "w") as output_f:
            output_f.write("commit,tag,date\r\n")
            writer = csv.writer(output_f)
            for row in reader:
                if not row:
                    continue
                row[0] = row[0][:7]  # Shorten commit hash
                row.append(
                    re.sub(r"v([0-9]+)-([0-9]+)-([0-9]+)-.*", r"\1-\2-\3", row[1])
                )
                writer.writerow(row)

        # Doc release history
        try:
            doc_git_log = latex_quote(
                self.system(
                    """git log --date=short --pretty=format:"%h%x09%an%x09%ad%x09%s" {}""".format(
                        doc_dir
                    ),
                    capture=True,
                )
            )
        except OSError:
            doc_git_log = ""
        reader = csv.reader(doc_git_log.split("\n"), delimiter="\t")
        with open(os.path.join(docgen_dir, "doc_commit_history.csv"), "w") as output_f:
            output_f.write("commit,author,date,message\r\n")
            writer = csv.writer(output_f)
            for row in reader:
                if not row:
                    continue
                writer.writerow(row)

        # Latest changes
        doc_latest_changes = latex_quote(
            self.system(
                "git diff {}..HEAD --numstat".format(
                    self.get_git_status()["latest_release_commit"]
                ),
                capture=True,
            )
        )
        reader = csv.reader(doc_latest_changes.split("\n"), delimiter="\t")
        with open(os.path.join(docgen_dir, "doc_latest_changes.csv"), "w") as output_f:
            output_f.write("added,deleted,file\r\n")
            writer = csv.writer(output_f)
            for row in reader:
                if not row:
                    continue
                writer.writerow(row)

    def preprocess_variables(self, doc_reference, doc_dir, docgen_dir):
        """Auto-generate a few variables in docgen/variables.tex
        """
        git_status = self.get_git_status()
        tex_output = ""
        for k, v in git_status.items():
            k = latex_quote("git{}".format(k), squash=True)
            tex_output += r"""\def\{}{{{}}}
            """.format(
                k, latex_quote(v)
            )

        # Write it
        with open(os.path.join(docgen_dir, "variables.tex"), "w") as f:
            f.write(tex_output)

    def add_symlink(self, doc_dir):
        """Add symlink to the given doc dir
        # Create symlink to host the documentation
        # This is for convenience only and this include symlink MUST NOT be put into git!
        """
        if not os.path.exists(os.path.join(doc_dir, "include")):
            include_dir = os.path.join(HERE, "docs", "include")
            assert os.path.isdir(include_dir)
            self.system(
                "ln -s {} {}".format(include_dir, os.path.join(doc_dir, "include"))
            )

    def build_doc(self, doc_dir):
        """Build doc in the given directory
        """
        # Build paths we're gonna use in the process.
        # Either we're in the project dir, either we're in dmake, in either case
        # we remove the part of the path.
        doc_dir = os.path.abspath(doc_dir)
        # if doc_dir.startswith(self.get_project_root_dir()):
        #     relative_root = self.get_project_root_dir()
        # elif doc_dir.startswith(HERE):
        #     relative_root = HERE
        # else:
        #     raise ValueError("Don't know how to compile this doc")

        # # ...do it for real
        # doc_dir_relative = doc_dir[
        #     len(os.path.abspath(relative_root)) + 1 :
        # ]
        # if doc_dir_relative.startswith('/'):
        #     doc_dir_relative = doc_dir_relative[1:]
        #
        # Create symlinks for convenient use
        self.add_symlink(doc_dir)

        # Additional data
        doc_reference = os.path.split(doc_dir)[1]
        docgen_dir = os.path.join(doc_dir, "docgen")

        # Create the 'docgen' folder on the fly
        self.system("mkdir -p {}".format(docgen_dir))

        # Preprocess documentation and prepare output directory
        printc(bcolors.TITLE, "Preprocessing {}".format(doc_reference))
        self.preprocess(doc_reference, doc_dir, docgen_dir)
        self.system(
            "mkdir -p {}".format(
                os.path.join(self.get_project_root_dir(), "docs", "build")
            )
        )

        # LaTeX it!! First we build the command and all the necessary stuff
        printc(
            bcolors.TITLE,
            "Running LaTeX in Docker. This may take time (large container). Use dmake -v to see what's happening",
        )
        target_name = "{}-{}".format(
            doc_reference, self.get_git_status()["revision_no_x"]
        )
        target_filename = "{}.pdf".format(target_name)
        target_file_relative = os.path.join("docs", "build", target_filename)
        target_file = os.path.join(self.get_project_root_dir(), target_file_relative)
        self.system("rm -f {}".format(target_file))
        if self.verbose:
            capture = False
            has_ti = "-ti"
        else:
            capture = True
            has_ti = ""
        source_volume = """-v "{}":/data/""".format(doc_dir)
        include_volume = """-v "{}":/data/include""".format(
            os.path.join(HERE, "docs", "include")
        )
        build_volume = """-v {}:/data/build""".format(
            os.path.join(self.get_project_root_dir(), "docs", "build")
        )

        # Prepare the actual commands
        inner_command = """latexmk -lualatex -interaction=nonstopmode -shell-escape -synctex=1 -g \
            -cd \
            -r ./include/latexmkrc \
            -outdir=/tmp/ \
            ./main.tex \
            -jobname={} ; \
            cp /tmp/{} /data/build/""".format(
            target_name, target_filename
        )
        command = """docker run --rm {} --user="$(id -u):$(id -g)" --net=none \
            {} {} {} \
            -w /data \
            blang/latex:ctanfull \
            /bin/bash -c "{}" """.format(
            has_ti, source_volume, include_volume, build_volume, inner_command
        )

        # Then let's go!!!
        self.system(command, capture=capture)

        # Check if compiled successfully
        if os.path.isfile(target_file):
            printc(
                bcolors.SUCCESS, "Your PDF document is ready at: {}".format(target_file)
            )
            return target_file
        else:
            printc(
                bcolors.FAIL,
                "Your PDF document didn't compile correctly. Check output logs.",
            )
            return None

    def cmdrun(self):
        """Execute command.
        Will either build the doc or preprocess it.
        """
        # Got to create a doc? Create it ;)
        if self.create:
            # Sanity checks
            if not self.create.startswith("N3-"):
                raise RuntimeError("Your doc name must start with 'N3-'")

            # Create the main docs directory
            doc_root = os.path.join(self.get_project_root_dir(), "docs")
            target_dir = os.path.join(doc_root, self.create)
            if os.path.isdir(target_dir):
                raise ValueError(
                    "Your doc folder already exists: {}".format(target_dir)
                )
            self.system("mkdir -p {}".format(target_dir))

            # Create document root and containing folders
            source_dirs = (
                os.path.join(HERE, "docs", "N3-INT-DMK-TEC", "annexes"),
                os.path.join(HERE, "docs", "N3-INT-DMK-TEC", "assets"),
                os.path.join(HERE, "docs", "N3-INT-DMK-TEC", "chapters"),
                os.path.join(HERE, "docs", "N3-INT-DMK-TEC", "forewords"),
                os.path.join(HERE, "docs", "N3-INT-DMK-TEC", "glossary.tex"),
                os.path.join(HERE, "docs", "N3-INT-DMK-TEC", "main.tex"),
                os.path.join(HERE, "docs", "N3-INT-DMK-TEC", ".gitignore"),
            )
            self.system("cp -R {} {}".format(" ".join(source_dirs), target_dir))

            # Good! Lets NOT stop here and pre-build documentation right now.
            self.build_doc(target_dir)
            return

        # Prepare list of docs. Include dmake official doc in building
        doc_folders = [
            os.path.join(self.get_project_root_dir(), "docs", fold)
            for fold in os.listdir(os.path.join(self.get_project_root_dir(), "docs"))
        ]
        if not self.without_dmake:
            doc_folders.extend(
                [
                    os.path.join(HERE, "docs", fold)
                    for fold in os.listdir(os.path.join(HERE, "docs"))
                ]
            )

        # Find doc folders (folders having a main.tex file inside)
        doc_paths = []
        for doc_dir in doc_folders:
            if not self.nolatex:
                if not os.path.isfile(os.path.join(doc_dir, "main.tex")):
                    if self.verbose:
                        printc(
                            bcolors.WARNING, "No main.tex file in {}".format(doc_dir)
                        )
                    continue

                # Delegate doc building to this method
                doc_paths.append(self.build_doc(doc_dir))

        # Tell what we built
        doc_paths = [p for p in doc_paths if p]
        if not doc_paths:
            printc(bcolors.FAIL, "No doc has been built")
            raise RuntimeError("No doc has been built")
        else:
            for p in doc_paths:
                printc(bcolors.INFO, "Documentation available here:\n    {}".format(p))
