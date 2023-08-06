#!/usr/bin/env python
# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/
"""This module describe nxtomomill applications which are available  through
the silx launcher.

Your environment should provide a command `nxtomomill`. You can reach help with
`tomwer --help`, and check the version with `nxtomomill --version`.
"""

__authors__ = ["V. Valls", "P. Knobel", "H. Payno"]
__license__ = "MIT"
__date__ = "04/01/2018"


import logging
import sys
from silx.utils.launcher import Launcher as _Launcher
import nxtomomill.version
from collections import namedtuple
import traceback

logging.basicConfig()


DeprecationWarning = namedtuple(
    "DeprecationWarning", ["since", "reason", "replacement"]
)


depreclog = logging.getLogger("nxtomomill.DEPRECATION")


def deprecated_warning(
    type_,
    name,
    reason=None,
    replacement=None,
    since_version=None,
    skip_backtrace_count=0,
):
    """
    Function to log a deprecation warning

    :param str type_: Nature of the object to be deprecated:
        "Module", "Function", "Class" ...
    :param name: Object name.
    :param str reason: Reason for deprecating this function
        (e.g. "feature no longer provided",
    :param str replacement: Name of replacement function (if the reason for
        deprecating was to rename the function)
    :param str since_version: First *silx* version for which the function was
        deprecated (e.g. "0.5.0").
    :param int skip_backtrace_count: Amount of last backtrace to ignore when
        logging the backtrace
    """
    if not depreclog.isEnabledFor(logging.WARNING):
        # Avoid computation when it is not logged
        return

    msg = "%s %s is deprecated"
    if since_version is not None:
        msg += " since silx version %s" % since_version
    msg += "."
    if reason is not None:
        msg += " Reason: %s." % reason
    if replacement is not None:
        msg += " Use '%s' instead." % replacement
    msg += "\n%s"
    limit = 2 + skip_backtrace_count
    backtrace = "".join(traceback.format_stack(limit=limit)[0])
    backtrace = backtrace.rstrip()
    depreclog.warning(msg, type_, name, backtrace)


class Launcher(_Launcher):
    """
    Manage launch of module.

    Provides an API to describe available commands and feature to display help
    and execute the commands.
    """

    def __init__(
        self, prog=None, usage=None, description=None, epilog=None, version=None
    ):
        super().__init__(
            prog=prog,
            usage=usage,
            description=description,
            epilog=epilog,
            version=version,
        )
        self._deprecations = {}
        "deprecations with prog names as key and deprecation info as values"

    def add_command(
        self,
        name=None,
        module_name=None,
        description=None,
        command=None,
        deprecated=False,
        deprecated_since_version=None,
        deprecated_reason=None,
        deprecated_replacement=None,
    ):

        super().add_command(
            name=name, module_name=module_name, description=description, command=command
        )
        if deprecated:
            self._deprecations[name] = DeprecationWarning(
                since=deprecated_since_version,
                reason=deprecated_reason,
                replacement=deprecated_replacement,
            )

    def execute(self, argv=None):
        if argv is None:
            argv = sys.argv

        if len(argv) <= 1:
            self.print_help()
            return 0

        command_name = argv[1]

        if command_name in self._deprecations:
            deprecation_info = self._deprecations[command_name]
            deprecated_warning(
                type_="application",
                name=command_name,
                reason=deprecation_info.reason,
                replacement=deprecation_info.replacement,
                since_version=deprecation_info.since,
            )
        super().execute(argv=argv)

    def print_help(self):
        """Print the help to stdout."""
        usage = self.usage
        if usage is None:
            usage = "usage: {0.prog} [--version|--help] <command> [<args>]"
        description = self.description
        epilog = self.epilog
        if epilog is None:
            epilog = "See '{0.prog} help <command>' to read about a specific subcommand"

        print(usage.format(self))
        print("")
        if description is not None:
            print(description)
            print("")
        print("The {0.prog} commands are:".format(self))
        commands = sorted(self._commands.keys())
        for command in commands:
            command = self._commands[command]
            print("   {:15} {:s}".format(command.name, command.description))
        print("")
        print(epilog.format(self))


def main():
    """Main function of the launcher

    This function is referenced in the setup.py file, to create a
    launcher script generated by setuptools.

    :rtype: int
    :returns: The execution status
    """
    _version = nxtomomill.version.version
    launcher = Launcher(prog="nxtomomill", version=_version)
    launcher.add_command(
        "dxfile2nx",
        module_name="nxtomomill.app.dxfile2nx",
        description="Convert dx file to NXTomo",
    )
    launcher.add_command(
        "patch-nx",
        module_name="nxtomomill.app.patch_nx",
        description="allow to patch an NXTomo entry",
    )
    launcher.add_command(
        "tomoedf2nx",
        module_name="nxtomomill.app.edf2nx",
        description="convert spec-edf acquisition to nexus - hdf5",
        deprecated=True,
        deprecated_reason="remove `tomo` repetition. The shorter the better",
        deprecated_replacement="edf2nx",
        deprecated_since_version=0.5,
    )
    launcher.add_command(
        "edf2nx",
        module_name="nxtomomill.app.edf2nx",
        description="convert spec-edf acquisition to nexus - hdf5"
        "format to nx compliant file format",
    )
    launcher.add_command(
        "edf-quick-start",
        module_name="nxtomomill.app.edfquickstart",
        description="create a configuration file to convert from spec-edf to NXtomo",
    )
    launcher.add_command(
        "tomoh52nx",
        module_name="nxtomomill.app.h52nx",
        description="convert bliss hdf5 to nexus hdf5",
        deprecated=True,
        deprecated_reason="remove `tomo` repetition. The shorter the better",
        deprecated_replacement="h52nx",
        deprecated_since_version=0.5,
    )
    launcher.add_command(
        "h52nx",
        module_name="nxtomomill.app.h52nx",
        description="convert bliss hdf5 to nexus hdf5",
    )
    launcher.add_command(
        "h5-3dxrd-2nx",
        module_name="nxtomomill.app.h5_3dxrd2nx",
        description="Compute center of rotation of a scan or "
        "between two projections",
    )
    launcher.add_command(
        "h5-quick-start",
        module_name="nxtomomill.app.h5quickstart",
        description="Create a default configuration file",
    )
    status = launcher.execute(sys.argv)
    return status


if __name__ == "__main__":
    # executed when using python -m PROJECT_NAME
    status = main()
    sys.exit(status)
