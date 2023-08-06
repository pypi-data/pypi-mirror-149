#!/usr/bin/env python
# encoding: utf-8
"""
command_registry.py

Created by Pierre-Julien Grizel et al.
Copyright (c) 2016 NumeriCube. All rights reserved.

A simple way to register commands (and sort them in the proper order)
"""

__author__ = ""
__copyright__ = "Copyright 2016, NumeriCube"
__credits__ = ["Pierre-Julien Grizel"]
__license__ = "CLOSED SOURCE"
__version__ = "TBD"
__maintainer__ = "Pierre-Julien Grizel"
__email__ = "pjgrizel@numericube.com"
__status__ = "Production"


class _CommandRegistry(list):
    """CommandRegistry singleton class.
    Will just store and retreive commands in the right order.
    """

    def append(self, command_class):
        """Register command class
        """
        from .base_commands import _BaseCommand

        if not issubclass(command_class, _BaseCommand):
            raise ValueError("Must pass a _BaseCommand-inherited class")
        return super(_CommandRegistry, self).append(command_class)


COMMAND_REGISTRY = _CommandRegistry()


def command(cls):
    COMMAND_REGISTRY.append(cls)
    return cls
