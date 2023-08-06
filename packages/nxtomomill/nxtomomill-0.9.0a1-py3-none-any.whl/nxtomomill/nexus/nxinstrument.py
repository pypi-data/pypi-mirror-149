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
__date__ = "10/02/2022"


from silx.utils.proxy import docstring
from typing import Optional
from nxtomomill.nexus.nxdetector import NXdetector, NXdetectorWithUnit
from nxtomomill.nexus.nxsource import NXsource
from nxtomomill.nexus.nxsource import DefaultESRFSource
from tomoscan.nexus.paths.nxtomo import get_paths as get_nexus_paths
from tomoscan.unitsystem.voltagesystem import VoltageSystem
from .utils import get_data
from tomoscan.io import HDF5File
from .nxobject import NXobject


class NXinstrument(NXobject):
    def __init__(
        self, node_name: str = "instrument", parent: Optional[NXobject] = None
    ) -> None:
        super().__init__(node_name=node_name, parent=parent)
        self._set_freeze(False)
        self._detector = NXdetector(
            node_name="detector",
            parent=self,
            field_of_view="Full",
            expected_dim=(2, 3),
        )
        self._diode = NXdetectorWithUnit(
            node_name="diode",
            parent=self,
            expected_dim=(1,),
            default_unit=VoltageSystem.VOLT,
        )
        self._source = DefaultESRFSource(node_name="source", parent=self)
        self._name = None
        self._set_freeze(True)

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, name: Optional[str]):
        if not isinstance(name, (str, type(None))):
            raise TypeError(f"name is expected to be None or a str. Not {type(name)}")
        self._name = name

    @property
    def detector(self) -> Optional[NXdetector]:
        return self._detector

    @detector.setter
    def detector(self, detector: Optional[NXdetector]):
        if not isinstance(detector, (NXdetector, type(None))):
            raise TypeError(
                f"detector is expected to be None or an instance of NXdetecetor. Not {type(detector)}"
            )
        self._detector = detector

    @property
    def diode(self) -> Optional[NXdetector]:
        return self._diode

    @diode.setter
    def diode(self, diode: Optional[NXdetector]):
        if not isinstance(diode, (NXdetector, type(None))):
            raise TypeError(
                f"diode is expected to be None or an instance of NXdetecetor. Not {type(diode)}"
            )
        self._diode = diode

    @property
    def source(self) -> Optional[NXsource]:
        return self._source

    @source.setter
    def source(self, source: Optional[NXsource]) -> None:
        if not isinstance(source, (NXsource, type(None))):
            raise TypeError(
                f"source is expected to be None or an instance of NXsource. Not {type(source)}"
            )
        self._source = source

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        if not isinstance(name, (str, type(None))):
            raise TypeError(
                f"name is expected to be None or an instance of str. Not {type(name)}"
            )
        self._name = name

    @docstring(NXobject)
    def to_nx_dict(
        self,
        nexus_path_version: Optional[float] = None,
        data_path: Optional[str] = None,
    ) -> dict:
        nexus_paths = get_nexus_paths(nexus_path_version)
        nexus_instrument_paths = nexus_paths.nx_instrument_paths
        nx_dict = {}

        if self._detector is not None:
            nx_dict.update(
                self._detector.to_nx_dict(nexus_path_version=nexus_path_version)
            )

        if self._diode is not None:
            nx_dict.update(
                self._diode.to_nx_dict(nexus_path_version=nexus_path_version)
            )

        if self._source is not None:
            nx_dict.update(
                self.source.to_nx_dict(nexus_path_version=nexus_path_version)
            )

        if self.name is not None:
            nx_dict[f"{self.name}/{nexus_instrument_paths.NAME}"] = self.name
        if nx_dict != {}:
            nx_dict[f"{self.path}@NX_class"] = "NXinstrument"

        return nx_dict

    def _load(
        self,
        file_path: str,
        data_path: str,
        nexus_version: float,
        detector_data_as: str,
    ) -> NXobject:
        """
        Create and load an NXsample from data on disk
        """
        nexus_paths = get_nexus_paths(nexus_version)
        nexus_instrument_paths = nexus_paths.nx_instrument_paths

        with HDF5File(file_path, mode="r") as h5f:
            if data_path in h5f:
                has_detector = "detector" in h5f[data_path]
                has_diode = "diode" in h5f[data_path]
                has_source = "source" in h5f[data_path]
            else:
                has_detector = False
                has_diode = False
                has_source = False
        # TODO: loading detector might be done using the NXclass instead of some hard coded names
        if has_detector:
            self.detector._load(
                file_path=file_path,
                data_path="/".join(
                    [data_path, "detector"],
                ),
                nexus_version=nexus_version,
                load_data_as=detector_data_as,
            )
        if has_diode:
            self.diode._load(
                file_path=file_path,
                data_path="/".join(
                    [data_path, "diode"],
                ),
                nexus_version=nexus_version,
                load_data_as="as_numpy_array",
            )
        if has_source:
            self.source._load(
                file_path=file_path,
                data_path="/".join([data_path, "source"]),
                nexus_version=nexus_version,
            )
        if nexus_instrument_paths.NAME is not None:
            self.name = get_data(
                file_path=file_path,
                data_path="/".join([data_path, nexus_instrument_paths.NAME]),
            )
