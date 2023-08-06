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


import os
from typing import Optional, Union
from tomoscan.io import HDF5File
from tomoscan.nexus.paths.nxtomo import LATEST_VERSION as LATEST_NXTOMO_VERSION
from .nxobject import NXobject, ElementWithUnit
from .nxinstrument import NXinstrument
from .nxsample import NXsample
from .utils import get_data_and_unit, get_data
from datetime import datetime
from silx.utils.proxy import docstring
from tomoscan.unitsystem.energysystem import EnergySI
from tomoscan.nexus.paths.nxtomo import get_paths as get_nexus_paths
from silx.io.url import DataUrl
import logging
import h5py
import numpy

_logger = logging.getLogger(__name__)


class NXtomo(NXobject):
    """
    Class defining an NXTomo.
    His final goal is to save data to disk.
    """

    def __init__(self, node_name: str = "", parent: Optional[NXobject] = None) -> None:
        super().__init__(node_name=node_name, parent=parent)
        self._set_freeze(False)
        self._start_time = None
        self._end_time = None
        self._instrument = NXinstrument(node_name="instrument", parent=self)
        self._sample = NXsample(node_name="sample", parent=self)
        self._group_size = None
        self._energy = ElementWithUnit(
            default_unit=EnergySI.KILOELECTRONVOLT
        )  # energy in kev
        self._title = None
        self._set_freeze(True)

    @property
    def start_time(self) -> Optional[Union[datetime, str]]:
        return self._start_time

    @start_time.setter
    def start_time(self, start_time: Optional[Union[datetime, str]]):
        if not isinstance(start_time, (type(None), datetime, str)):
            raise TypeError(
                f"start_time is expected ot be an instance of datetime or None. Not {type(start_time)}"
            )
        self._start_time = start_time

    @property
    def end_time(self) -> Optional[Union[datetime, str]]:
        return self._end_time

    @end_time.setter
    def end_time(self, end_time: Optional[Union[datetime, str]]):
        if not isinstance(end_time, (type(None), datetime, str)):
            raise TypeError(
                f"end_time is expected ot be an instance of datetime or None. Not {type(end_time)}"
            )
        self._end_time = end_time

    @property
    def title(self) -> Optional[str]:
        return self._title

    @title.setter
    def title(self, title: Optional[str]):
        if not isinstance(title, (type(None), str)):
            raise TypeError(
                f"title is expected ot be an instance of str or None. Not {type(title)}"
            )
        self._title = title

    @property
    def instrument(self) -> Optional[NXinstrument]:
        return self._instrument

    @instrument.setter
    def instrument(self, instrument: Optional[NXinstrument]) -> None:
        if not isinstance(instrument, (type(None), NXinstrument)):
            raise TypeError(
                f"instrument is expected ot be an instance of {NXinstrument} or None. Not {type(instrument)}"
            )
        self._instrument = instrument

    @property
    def sample(self) -> Optional[NXsample]:
        return self._sample

    @sample.setter
    def sample(self, sample: Optional[NXsample]):
        if not isinstance(sample, (type(None), NXsample)):
            raise TypeError(
                f"sample is expected ot be an instance of {NXsample} or None. Not {type(sample)}"
            )

    @property
    def energy(self) -> Optional[float]:
        """
        incident energy in keV
        """
        return self._energy

    @energy.setter
    def energy(self, energy: Optional[float]) -> None:
        if not isinstance(energy, (type(None), float)):
            raise TypeError(
                f"energy is expected ot be an instance of {float} or None. Not {type(energy)}"
            )
        self._energy.value = energy

    @property
    def group_size(self) -> Optional[int]:
        return self._group_size

    @group_size.setter
    def group_size(self, group_size: Optional[int]):
        if not (
            isinstance(group_size, (type(None), int))
            or (numpy.isscalar(group_size) and not isinstance(group_size, (str, bytes)))
        ):
            raise TypeError(
                f"group_size is expected ot be None or a scalar. Not {type(group_size)}"
            )
        self._group_size = group_size

    @docstring(NXobject)
    def to_nx_dict(
        self,
        nexus_path_version: Optional[float] = None,
        data_path: Optional[str] = None,
    ) -> dict:
        if data_path is None:
            data_path = ""

        nexus_paths = get_nexus_paths(nexus_path_version)
        nx_dict = {}

        if self.sample is not None:
            nx_dict.update(
                self.sample.to_nx_dict(nexus_path_version=nexus_path_version)
            )
        else:
            _logger.info("no sample found. Won't be saved")

        if self.instrument is not None:
            nx_dict.update(
                self.instrument.to_nx_dict(nexus_path_version=nexus_path_version)
            )
        else:
            _logger.info("no instrument found. Won't be saved")

        if self.start_time is not None:
            path_start_time = f"{self.path}/{nexus_paths.START_TIME_PATH}"
            if isinstance(self.start_time, datetime):
                start_time = self.start_time.isoformat()
            else:
                start_time = self.start_time
            nx_dict[path_start_time] = start_time
        if self.end_time is not None:
            path_end_time = f"{self.path}/{nexus_paths.END_TIME_PATH}"
            if isinstance(self.end_time, datetime):
                end_time = self.end_time.isoformat()
            else:
                end_time = self.end_time
            nx_dict[path_end_time] = end_time
        if self.group_size is not None:
            path_grp_size = f"{self.path}/{nexus_paths.GRP_SIZE_ATTR}"
            nx_dict[path_grp_size] = self.group_size
        if self.energy.value is not None:
            path_energy = f"{self.path}/{nexus_paths.ENERGY_PATH}"

            nx_dict[path_energy] = self.energy.value
            nx_dict["@".join([path_energy, "unit"])] = str(self.energy.unit)
            path_beam = f"{self.path}/{nexus_paths.BEAM_PATH}"
            nx_dict["@".join([path_beam, "NX_class"])] = "NXbeam"

            if nexus_paths.VERSION > 1.0:
                nx_dict[
                    f">/{self.path}/beam/incident_energy"
                ] = f"/{data_path}/{self.path}/{nexus_paths.ENERGY_PATH}"
        if self.title is not None:
            path_title = f"{self.path}/{nexus_paths.NAME_PATH}"
            nx_dict[path_title] = self.title

        # create data group from symbolic links

        if self.instrument.detector.image_key is not None:
            nx_dict[
                f">/{self.path}/data/image_key"
            ] = f"/{data_path}/{self.instrument.detector.path}/{nexus_paths.nx_detector_paths.IMAGE_KEY}"
            nx_dict[
                f">/{self.path}/data/image_key_control"
            ] = f"/{data_path}/{self.instrument.detector.path}/{nexus_paths.nx_detector_paths.IMAGE_KEY_CONTROL}"
        if self.instrument.detector.data is not None:
            nx_dict[
                f">/{self.path}/data/data"
            ] = f"/{data_path}/{self.instrument.detector.path}/{nexus_paths.nx_detector_paths.DATA}"
            nx_dict[f"/{self.path}/data@NX_class"] = "NXdata"
            nx_dict[f"/{self.path}/data@signal"] = "data"
            nx_dict[f"/{self.path}@default"] = "data"
            nx_dict[f"{self.path}/data@SILX_style/axis_scale_types"] = [
                "linear",
                "linear",
            ]
        if self.sample.rotation_angle is not None:
            nx_dict[
                f">/{self.path}/data/rotation_angle"
            ] = f"/{data_path}/{self.sample.path}/{nexus_paths.nx_sample_paths.ROTATION_ANGLE}"

        if nx_dict != {}:
            nx_dict[f"{self.path}@NX_class"] = "NXentry"

        nx_dict[f"{self.path}@version"] = nexus_paths.VERSION

        return nx_dict

    def detector_data_is_defined_by_url(self) -> bool:
        return self._detector_data_is_defined_by_type(DataUrl)

    def detector_data_is_defined_by_virtual_source(self) -> bool:
        return self._detector_data_is_defined_by_type(h5py.VirtualSource)

    def _detector_data_is_defined_by_type(self, type_):
        return (
            self.instrument is not None
            and self.instrument.detector is not None
            and self.instrument.detector.data is not None
            and isinstance(self.instrument.detector.data, (str, tuple))
            and isinstance(self.instrument.detector.data[0], type_)
        )

    def load(
        self, file_path: str, data_path: str, detector_data_as="as_data_url"
    ) -> NXobject:
        """
        Load NXtomo instance from file_path and data_path

        :param str file_path: hdf5 file path containing the NXtomo
        :param str data_path: location of the NXtomo
        """
        possible_as_values = ("as_virtual_source", "as_data_url", "as_numpy_array")
        if detector_data_as not in possible_as_values:
            raise ValueError(
                f"detector_data_as is expected to be in {possible_as_values} and not {detector_data_as}"
            )

        if not os.path.exists(file_path):
            raise IOError(f"{file_path} does not exists")
        with HDF5File(file_path, mode="r") as h5f:
            if data_path not in h5f:
                raise ValueError(f"{data_path} cannot be find in {file_path}")
            root_node = h5f[data_path]

            if "version" in root_node.attrs:
                nexus_version = root_node.attrs["version"]
            else:
                _logger.warning(
                    f"Unable to find nexus version associated with {data_path}@{file_path}"
                )
                nexus_version = LATEST_NXTOMO_VERSION
        nexus_paths = get_nexus_paths(nexus_version)
        self.energy, self.energy.unit = get_data_and_unit(
            file_path=file_path,
            data_path="/".join([data_path, nexus_paths.ENERGY_PATH]),
            default_unit="kev",
        )
        start_time = get_data(
            file_path=file_path,
            data_path="/".join([data_path, nexus_paths.START_TIME_PATH]),
        )
        try:
            start_time = datetime.fromisoformat(start_time)
        except Exception:
            start_time = str(start_time) if start_time is not None else None
        self.start_time = start_time

        end_time = get_data(
            file_path=file_path,
            data_path="/".join([data_path, nexus_paths.END_TIME_PATH]),
        )
        try:
            end_time = datetime.fromisoformat(end_time)
        except Exception:
            end_time = str(end_time) if end_time is not None else None
        self.end_time = end_time

        self.title = get_data(
            file_path=file_path, data_path="/".join([data_path, nexus_paths.NAME_PATH])
        )

        self.sample._load(
            file_path, "/".join([data_path, "sample"]), nexus_version=nexus_version
        )
        self.instrument._load(
            file_path,
            "/".join([data_path, "instrument"]),
            nexus_version=nexus_version,
            detector_data_as=detector_data_as,
        )
        return self
