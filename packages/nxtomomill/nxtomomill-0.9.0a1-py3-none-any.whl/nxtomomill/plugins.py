# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2015-2020 European Synchrotron Radiation Facility
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

"""
module to define and manage Plugin
"""

__authors__ = ["H. Payno"]


import os
from importlib.machinery import SourceFileLoader
import logging
import inspect

from nxtomomill.nexus.nxtomo import NXtomo

_logger = logging.getLogger(__name__)


_NXTOMOMILL_PLUGINS_ENV_VAR = "NXTOMOMILL_PLUGINS_DIR"


def get_plugins_instances_frm_env_var():
    """

    :return: list of plugins contains in `_NXTOMOMILL_PLUGINS_ENV_VAR`
    """
    if _NXTOMOMILL_PLUGINS_ENV_VAR in os.environ:
        if not os.path.isdir(os.environ[_NXTOMOMILL_PLUGINS_ENV_VAR]):
            err = " ".join(
                (os.environ[_NXTOMOMILL_PLUGINS_ENV_VAR], "is not a directory")
            )
            raise ValueError(err)
        else:
            return get_plugins_instances(os.environ[_NXTOMOMILL_PLUGINS_ENV_VAR])
    else:
        err = " ".join(
            (
                "environment variable",
                _NXTOMOMILL_PLUGINS_ENV_VAR,
                "is not defined. Unable to find plugins",
            )
        )
        raise ValueError(err)


def get_plugins_instances(directory: str):
    """

    :param directory: directory to brower
    :return: list of instances of 'Plugin' in a given directory
    """
    plugins = []
    for file_ in os.listdir(directory):
        if (
            os.path.isfile(os.path.join(directory, file_))
            and file_.endswith(".py")
            and not file_.startswith("__")
        ):
            full_path = os.path.join(directory, file_)
            try:
                mod = SourceFileLoader(file_, full_path).load_module()
            except Exception:
                _logger.warning("Fail to import " + full_path)
            else:
                plugins.extend(_load_plugin_from_module(mod))
    return plugins


def _load_plugin_from_module(module) -> list:
    """Create an instance of each class from module which inherite from
    _PluginBase"""
    instances = []
    for name, cls in inspect.getmembers(module, inspect.isclass):
        # filter _PluginBase instances only (which are not HDF5Plugin)
        if name != HDF5Plugin.__name__ and _PluginBase in inspect.getmro(cls):
            instance = cls()
            _logger.info("cretate instance of " + name)
            instances.append(instance)
    return instances


def get_plugins_positioners_resources(plugins) -> tuple:
    """

    :param plugins: plugins to inspect
    :return: tuple of all possible resources requested by the plugin
    """
    res = []
    for plugin in plugins:
        res.extend(plugin.positioners_names)
    res = set(res)
    return tuple(res)


def get_plugins_instrument_resources(plugins) -> tuple:
    """

    :param plugins: plugins to inspect
    :return: tuple of all possible resources requested by the plugin
    """
    res = []
    for plugin in plugins:
        res.extend(plugin.instrument_names)
    res = set(res)
    return tuple(res)


class _PluginBase:
    """Base class for a plugin"""

    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def __str__(self):
        return self.name


class HDF5Plugin(_PluginBase):
    """Define a Plugin to create some motor / array which are not part
    of the original .hdf5 file but that can be created from existing
    information from the motor

    :param str name: name of the plugin
    :param positioner_keys: which information you will need for the plugin.
    :param instrument_keys: which information to be read from the "instrument"
                            dataset of the input bliss scan.
    """

    def __init__(
        self,
        name,
        positioner_keys=tuple(),
        instrument_keys=tuple(),
    ):
        super().__init__(name)
        """As the sequence is splitted into several scan we need to parse
        each scan to retrieve all the information.
        We need you to define which resources (motor position...) you require
        initially to avoid browsing several time the file
        """

        self.__positioners_info = {}
        for key in positioner_keys:
            if not isinstance(key, str):
                raise TypeError("resource names should be strings")
            self.__positioners_info[key] = None
        self.__instrument_info = {}
        for key in instrument_keys:
            if not isinstance(key, str):
                raise TypeError("resource names should be strings")
            self.__instrument_info[key] = None

    def process(self) -> list:
        """

        :return: list of `Resource`
        """
        pass

    def set_positioners_infos(self, resources):
        self.__positioners_info = resources

    @property
    def positioners_names(self):
        return self.__positioners_info.keys()

    @property
    def positioners_infos(self):
        return self.__positioners_info

    def get_positioner_info(self, name):
        """

        :param name: key to get on the positioners section
        :return: data requested from the positioners section
        """
        return self.__positioners_info[name]

    def set_instrument_infos(self, resources):
        self.__instrument_info = resources

    @property
    def instrument_names(self):
        return self.__instrument_info

    @property
    def instrument_infos(self):
        return self.__instrument_info

    def get_instrument_info(self, name):
        """

        :param name: key to get on the positioners section
        :return: data requested from the positioners section
        """
        return self.__instrument_info[name]

    def update_nx_tomo(self, nx_tomo: NXtomo):
        raise NotImplementedError("Base class")
