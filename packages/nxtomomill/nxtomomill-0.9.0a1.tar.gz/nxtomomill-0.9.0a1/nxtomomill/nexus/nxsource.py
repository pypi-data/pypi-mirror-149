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


from typing import Optional, Union
from silx.utils.proxy import docstring
from .nxobject import NXobject
from silx.utils.enum import Enum as _Enum
from tomoscan.nexus.paths.nxtomo import get_paths as get_nexus_paths
from .utils import get_data


class SourceType(_Enum):
    SPALLATION_NEUTRON = "Spallation Neutron Source"
    PULSED_REACTOR_NEUTRON_SOURCE = "Pulsed Reactor Neutron Source"
    REACTOR_NEUTRON_SOURCE = "Reactor Neutron Source"
    SYNCHROTRON_X_RAY_SOURCE = "Synchrotron X-ray Source"
    PULSED_MUON_SOURCE = "Pulsed Muon Source"
    ROTATING_ANODE_X_RAY = "Rotating Anode X-ray"
    FIXED_TUBE_X_RAY = "Fixed Tube X-ray"
    UV_LASER = "UV Laser"
    FREE_ELECTRON_LASER = "Free-Electron Laser"
    OPTICAL_LASER = "Optical Laser"
    ION_SOURCE = "Ion Source"
    UV_PLASMA_SOURCE = "UV Plasma Source"
    METAL_JET_X_RAY = "Metal Jet X-ray"


class NXsource(NXobject):
    """Information regarding the x-ray storage ring/facility"""

    def __init__(
        self, node_name="source", parent=None, source_name=None, source_type=None
    ):
        super().__init__(node_name=node_name, parent=parent)
        self._set_freeze(False)
        self._name = source_name
        self._type = source_type
        self._set_freeze(True)

    @property
    def name(self) -> Union[None, str]:
        return self._name

    @name.setter
    def name(self, source_name: Union[str, None]):
        if not isinstance(source_name, (str, type(None))):
            raise TypeError(
                f"source_name is expected to be None or a str not {type(source_name)}"
            )
        self._name = source_name

    @property
    def type(self) -> Union[None, SourceType]:
        return self._type

    @type.setter
    def type(self, type_: Union[None, str, SourceType]):
        if type_ is None:
            self._type = None
        else:
            type_ = SourceType.from_value(type_)
            self._type = type_

    def __str__(self):
        return (
            f"{super().__str__}, (source name: {self.name}, source type: {self.type})"
        )

    @docstring(NXobject)
    def to_nx_dict(
        self,
        nexus_path_version: Optional[float] = None,
        data_path: Optional[str] = None,
    ) -> dict:
        nexus_paths = get_nexus_paths(nexus_path_version)
        nexus_source_paths = nexus_paths.nx_source_paths
        nx_dict = {}

        # warning: source is integrated only since 1.1 version of the nexus path
        if self.name is not None and nexus_paths.SOURCE_NAME is not None:
            path_name = f"{self.path}/{nexus_source_paths.NAME}"
            nx_dict[path_name] = self.name
        if self.type is not None and nexus_paths.SOURCE_TYPE is not None:
            path_type = f"{self.path}/{nexus_source_paths.TYPE}"
            nx_dict[path_type] = self.type.value
        if nx_dict != {}:
            nx_dict[f"{self.path}@NX_class"] = "NXsource"

        return nx_dict

    def _load(self, file_path: str, data_path: str, nexus_version: float) -> None:
        nexus_paths = get_nexus_paths(nexus_version)
        nexus_source_paths = nexus_paths.nx_source_paths
        self.name = get_data(
            file_path=file_path,
            data_path="/".join([data_path, nexus_source_paths.NAME]),
        )
        self.type = get_data(
            file_path=file_path,
            data_path="/".join([data_path, nexus_source_paths.TYPE]),
        )


class DefaultESRFSource(NXsource):
    def __init__(self, node_name="source", parent=None) -> None:
        super().__init__(
            node_name=node_name,
            parent=parent,
            source_name="ESRF",
            source_type=SourceType.SYNCHROTRON_X_RAY_SOURCE,
        )
