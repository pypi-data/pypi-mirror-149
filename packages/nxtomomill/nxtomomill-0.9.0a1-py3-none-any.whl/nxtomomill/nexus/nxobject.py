# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2022 European Synchrotron Radiation Facility
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


__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "03/02/2022"


from typing import Optional
from silx.io.url import DataUrl
from tomoscan.unitsystem import Unit
from tomoscan.nexus.paths.nxtomo import LATEST_VERSION as LATEST_NXTOMO_VERSION
from silx.io.dictdump import dicttonx
import h5py
import os


class ElementWithUnit:
    """Util class to let the user define a unit with a value"""

    def __init__(self, default_unit: Unit) -> None:
        if not isinstance(default_unit, Unit):
            raise TypeError(f"{default_unit} should be an instance of {Unit}")
        self._value = None
        self._unit = default_unit
        self._unit_type = type(default_unit)

    @property
    def unit(self) -> Optional[float]:
        return self._unit

    @unit.setter
    def unit(self, unit) -> None:
        try:
            unit = self._unit_type.from_value(unit)
        except Exception:
            pass
        if not isinstance(unit, self._unit_type):
            if isinstance(unit, str):
                raise ValueError(f"Unable to cast {unit} to a {type(self._unit_type)}")
            else:
                raise TypeError(
                    f"invalid unit type. {type(unit)} provided when {type(self._unit_type)} expected"
                )
        self._unit = unit

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def si_value(self):
        return self._value * self.unit.value

    def __str__(self):
        return f"{self.value} {str(self.unit)}"


class NXobject:

    __isfrozen = False
    # to ease API and avoid setting wrong attributes we 'freeze' the attributes
    # see https://stackoverflow.com/questions/3603502/prevent-creating-new-attributes-outside-init

    def __init__(self, node_name: str, parent=None) -> None:
        if not isinstance(node_name, str):
            raise TypeError(
                f"name is expected to be an instance of str. Not {type(node_name)}"
            )
        self.node_name = node_name
        self.parent = parent
        self._set_freeze()

    def _set_freeze(self, freeze=True):
        self.__isfrozen = freeze

    @property
    def parent(self):  # -> Optional[NXobject]:
        return self._parent

    @parent.setter
    def parent(self, parent) -> None:
        if not isinstance(parent, (type(None), NXobject)):
            raise TypeError(
                f"parent is expected to be None or an instance of {NXobject}"
            )
        self._parent = parent

    @property
    def is_root(self) -> bool:
        return self.parent is None

    @property
    def root_path(self) -> str:
        """return path of the root NXobject"""
        if self.is_root:
            return self.path
        else:
            return self.parent.root_path

    @property
    def path(self):
        if self.parent is not None:
            path = "/".join([self.parent.path, self.node_name])
        else:
            path = self.node_name
        # clean some possible issues with "//"
        path = path.replace("//", "/")
        return path

    @property
    def node_name(self) -> str:
        return self._node_name

    @node_name.setter
    def node_name(self, node_name: str):
        if not isinstance(node_name, str):
            raise TypeError(
                f"nexus_name should be an instance of str and not {type(node_name)}"
            )
        self._node_name = node_name

    def save(
        self,
        file_path: str,
        data_path: str = "/",
        nexus_path_version: Optional[float] = None,
        overwrite: bool = False,
    ) -> None:
        """
        save NXtomo to disk.

        :param str file_path: hdf5 file
        :param Optional[str] entry: HDF5 group to save the data. If entry is already provided in
        """
        for key, value in dict(
            [("file_path", file_path), ("entry", data_path)]
        ).items():
            if not isinstance(value, (type(None), str)):
                raise TypeError(
                    f"{key} is expected to be None or an instance of str not {type(value)}"
                )
        if not isinstance(overwrite, bool):
            raise TypeError

        entry_path = "/".join([data_path, self.path])
        # not fully sure about the dicttoh5 "add" behavior
        if os.path.exists(file_path):
            with h5py.File(file_path, mode="a") as h5f:
                if entry_path in h5f:
                    if overwrite:
                        del h5f[entry_path]
                    else:
                        raise KeyError(f"{entry_path} already exists")
        if nexus_path_version is None:
            nexus_path_version = LATEST_NXTOMO_VERSION

        nx_dict = self.to_nx_dict(
            nexus_path_version=nexus_path_version, data_path=data_path
        )
        # retrieve virtual sources and DataUrl
        datasets_to_handle_in_postprocessing = {}
        for key in self._get_virtual_sources(nx_dict):
            datasets_to_handle_in_postprocessing[key] = nx_dict.pop(key)
        for key in self._get_data_urls(nx_dict):
            datasets_to_handle_in_postprocessing[key] = nx_dict.pop(key)

        # retrieve attributes
        attributes = {}

        dataset_to_postpone = tuple(datasets_to_handle_in_postprocessing.keys())
        for key, value in nx_dict.items():
            if key.startswith(dataset_to_postpone):
                attributes[key] = value
        # clean attributes
        for key in attributes:
            del nx_dict[key]

        dicttonx(
            nx_dict,
            h5file=file_path,
            h5path=data_path,
            update_mode="replace",
            mode="a",
        )
        assert os.path.exists(file_path)
        # now handle nx_dict containing h5py.virtualSource or DataUrl
        # this cannot be handled from the nxdetector class because not aware about
        # the output file.
        for (
            dataset_path,
            v_sources_or_data_urls,
        ) in datasets_to_handle_in_postprocessing.items():
            for v_source_or_data_url in v_sources_or_data_urls:
                if isinstance(v_source_or_data_url, DataUrl):
                    data = DataUrl(
                        file_path=v_source_or_data_url.file_path(),
                        data_path=v_source_or_data_url.data_path(),
                        scheme=v_source_or_data_url.scheme(),
                        data_slice=v_source_or_data_url.data_slice(),
                    )
                else:
                    data = v_source_or_data_url
                from nxtomomill.utils.frameappender import (
                    FrameAppender,
                )  # avoid cyclic import

                frame_appender = FrameAppender(
                    data=data,
                    file_path=file_path,
                    data_path="/".join([data_path, dataset_path]),
                    where="end",
                )
                frame_appender.process()

        # write attributes of dataset defined from a list of DataUrl or VirtualSource
        assert os.path.exists(file_path)
        dicttonx(
            attributes,
            h5file=file_path,
            h5path=data_path,
            update_mode="add",
            mode="a",
        )

    def to_nx_dict(
        self,
        nexus_path_version: Optional[float] = None,
        data_path: Optional[str] = None,
    ) -> dict:
        """
        convert the NXobject to an nx dict. Dictionnary that we can dump to hdf5 file

        :param Optional[float] nexus_path_version: version of the nexus path version to use
        :param Optional[str] data_path: can be provided to create some link in the file
        """
        raise NotImplementedError("Base class")

    def __str__(self):
        f"{type(self)}: {self.path}"

    @staticmethod
    def _get_virtual_sources(ddict) -> tuple:
        """Return key / path containing a list or a tuple of h5py.VirtualSource"""

        def has_virtual_sources(value):
            if isinstance(value, h5py.VirtualSource):
                return True
            elif isinstance(value, (list, tuple)):
                for v in value:
                    if has_virtual_sources(v):
                        return True
            return False

        keys = []
        for key, value in ddict.items():
            if has_virtual_sources(value):
                keys.append(key)
        return tuple(keys)

    @staticmethod
    def _get_data_urls(ddict) -> tuple:
        """Return key / path containing a list or a tuple of silx.io.url.DataUrl"""

        def has_data_url(value):
            if isinstance(value, DataUrl):
                return True
            elif isinstance(value, (list, tuple)):
                for v in value:
                    if has_data_url(v):
                        return True
            return False

        keys = []
        for key, value in ddict.items():
            if has_data_url(value):
                keys.append(key)
        return tuple(keys)

    def __setattr__(self, __name, __value):
        if self.__isfrozen and not hasattr(self, __name):
            raise AttributeError("can't set attribute", __name)
        else:
            super().__setattr__(__name, __value)
