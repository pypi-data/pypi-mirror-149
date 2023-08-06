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


from typing import Iterable, Optional

import numpy
from .nxobject import NXobject, ElementWithUnit
from .utils import cast_and_check_array_1D, get_data_and_unit, get_data
from silx.utils.proxy import docstring
from tomoscan.nexus.paths.nxtomo import get_paths as get_nexus_paths
from tomoscan.unitsystem.metricsystem import MetricSystem


class NXsample(NXobject):
    def __init__(self, node_name="sample", parent: Optional[NXobject] = None) -> None:
        super().__init__(node_name=node_name, parent=parent)
        self._set_freeze(False)
        self._name = None
        self._rotation_angle = None
        self.rocking = None
        self.n_steps_rocking = None
        self.n_steps_rotation = None
        self._x_translation = ElementWithUnit(default_unit=MetricSystem.METER)
        self._y_translation = ElementWithUnit(default_unit=MetricSystem.METER)
        self._z_translation = ElementWithUnit(default_unit=MetricSystem.METER)
        self._set_freeze(True)

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        if not isinstance(name, (type(None), str)):
            raise TypeError(f"name is expected to be None or str not {type(name)}")
        self._name = name

    @property
    def rotation_angle(self) -> Optional[numpy.ndarray]:
        return self._rotation_angle

    @rotation_angle.setter
    def rotation_angle(self, rotation_angle: Optional[Iterable]):
        self._rotation_angle = cast_and_check_array_1D(rotation_angle, "rotation_angle")

    @property
    def x_translation(self) -> Optional[numpy.ndarray]:
        return self._x_translation

    @x_translation.setter
    def x_translation(self, x_translation: Optional[Iterable]):
        self._x_translation.value = cast_and_check_array_1D(
            x_translation, "x_translation"
        )

    @property
    def y_translation(self) -> Optional[numpy.ndarray]:
        return self._y_translation

    @y_translation.setter
    def y_translation(self, y_translation: Optional[Iterable]):
        self._y_translation.value = cast_and_check_array_1D(
            y_translation, "y_translation"
        )

    @property
    def z_translation(self) -> Optional[numpy.ndarray]:
        return self._z_translation

    @z_translation.setter
    def z_translation(self, z_translation: Optional[Iterable]):
        self._z_translation.value = cast_and_check_array_1D(
            z_translation, "z_translation"
        )

    @docstring(NXobject)
    def to_nx_dict(
        self,
        nexus_path_version: Optional[float] = None,
        data_path: Optional[str] = None,
    ) -> dict:

        nexus_paths = get_nexus_paths(nexus_path_version)
        nexus_sample_paths = nexus_paths.nx_sample_paths

        nx_dict = {}

        if self.name is not None:
            path_name = f"{self.path}/{nexus_sample_paths.NAME}"
            nx_dict[path_name] = self.name
        if self.rotation_angle is not None:
            path_rotation_angle = f"{self.path}/{nexus_sample_paths.ROTATION_ANGLE}"
            nx_dict[path_rotation_angle] = self.rotation_angle
            nx_dict["@".join([path_rotation_angle, "unit"])] = "degree"
        if self.rocking is not None:
            path_rocking = f"{self.path}/{nexus_sample_paths.ROCKING}"
            nx_dict[path_rocking] = self.rocking
        if self.n_steps_rocking is not None:
            path_n_steps_rocking = f"{self.path}/{nexus_sample_paths.N_STEPS_ROCKING}"
            nx_dict[path_n_steps_rocking] = self.n_steps_rocking
        if self.n_steps_rotation is not None:
            path_n_steps_rotation = f"{self.path}/{nexus_sample_paths.N_STEPS_ROTATION}"
            nx_dict[path_n_steps_rotation] = self.n_steps_rotation
        if self.x_translation.value is not None:
            path_x_translation = f"{self.path}/{nexus_sample_paths.X_TRANSLATION}"
            nx_dict[path_x_translation] = self.x_translation.value
            nx_dict["@".join([path_x_translation, "unit"])] = str(
                self.x_translation.unit
            )
        if self.y_translation.value is not None:
            path_y_translation = f"{self.path}/{nexus_sample_paths.Y_TRANSLATION}"
            nx_dict[path_y_translation] = self.y_translation.value
            nx_dict["@".join([path_y_translation, "unit"])] = str(
                self.y_translation.unit
            )
        if self.z_translation.value is not None:
            path_z_translation = f"{self.path}/{nexus_sample_paths.Z_TRANSLATION}"
            nx_dict[path_z_translation] = self.z_translation.value
            nx_dict["@".join([path_z_translation, "unit"])] = str(
                self.z_translation.unit
            )

        if nx_dict != {}:
            nx_dict[f"{self.path}@NX_class"] = "NXsample"
        return nx_dict

    def _load(self, file_path: str, data_path: str, nexus_version: float) -> NXobject:
        """
        Create and load an NXsample from data on disk
        """
        nexus_paths = get_nexus_paths(nexus_version)
        nexus_sample_paths = nexus_paths.nx_sample_paths

        self.name = get_data(
            file_path=file_path,
            data_path="/".join([data_path, nexus_sample_paths.NAME]),
        )
        self.rotation_angle, angle_unit = get_data_and_unit(
            file_path=file_path,
            data_path="/".join([data_path, nexus_sample_paths.ROTATION_ANGLE]),
            default_unit="degree",
        )
        if angle_unit == "degree":
            pass
        elif isinstance(angle_unit, str) and angle_unit.lower() in ("rad", "radian"):
            self.rotation_angle = numpy.rad2deg(self.rotation_angle)
        elif angle_unit is not None:
            raise ValueError(f"rotation angle unit not recognized: {angle_unit}")

        self.x_translation, self.x_translation.unit = get_data_and_unit(
            file_path=file_path,
            data_path="/".join([data_path, nexus_sample_paths.X_TRANSLATION]),
            default_unit=MetricSystem.METER,
        )
        self.y_translation, self.y_translation.unit = get_data_and_unit(
            file_path=file_path,
            data_path="/".join([data_path, nexus_sample_paths.Y_TRANSLATION]),
            default_unit=MetricSystem.METER,
        )
        self.z_translation, self.z_translation.unit = get_data_and_unit(
            file_path=file_path,
            data_path="/".join([data_path, nexus_sample_paths.Z_TRANSLATION]),
            default_unit=MetricSystem.METER,
        )
