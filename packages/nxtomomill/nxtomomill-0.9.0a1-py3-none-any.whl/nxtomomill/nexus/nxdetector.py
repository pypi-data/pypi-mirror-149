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


from silx.utils.proxy import docstring
from silx.io.url import DataUrl
from h5py import VirtualSource
from typing import Iterable, Optional, Union
import numpy
import h5py
from nxtomomill.utils.h5pyutils import from_virtual_source_to_data_url

try:
    from tomoscan.esrf.scan.hdf5scan import ImageKey
except ImportError:
    from tomoscan.esrf.hdf5scan import ImageKey
from tomoscan.nexus.paths.nxtomo import get_paths as get_nexus_path
from tomoscan.unitsystem.metricsystem import MetricSystem
from nxtomomill.nexus.utils import cast_and_check_array_1D, get_data, get_data_and_unit
from .nxobject import ElementWithUnit, NXobject
from tomoscan.scanbase import FOV as FieldOfView
from tomoscan.unitsystem import TimeSystem
from tomoscan.unitsystem import Unit
from tomoscan.io import HDF5File
from h5py import h5s as h5py_h5s
import h5py._hl.selections as selection


class NXdetector(NXobject):
    def __init__(
        self,
        node_name="detector",
        parent=None,
        field_of_view=None,
        expected_dim: Optional[tuple] = None,
    ) -> None:
        """
        :param Optional[tuple] expected_dim: user can provide expected dimesions as a tuple of int to be checked when data is set
        """
        super().__init__(node_name=node_name, parent=parent)
        self._set_freeze(False)

        self._expected_dim = expected_dim

        self._data = None
        self.image_key_control = None
        self._x_pixel_size = ElementWithUnit(default_unit=MetricSystem.METER)
        self._y_pixel_size = ElementWithUnit(default_unit=MetricSystem.METER)
        self._distance = ElementWithUnit(
            default_unit=MetricSystem.METER
        )  # detector / sample distance
        self.field_of_view = field_of_view
        self._count_time = ElementWithUnit(default_unit=TimeSystem.SECOND)
        self.estimated_cor_from_motor = None
        self.tomo_n = None
        self.group_size = None
        self._set_freeze(True)

    @property
    def data(self) -> Union[numpy.ndarray, tuple]:
        """data can be None, a numpy array or a list of DataUrl xor h5py Virtual Source"""
        return self._data

    @data.setter
    def data(self, data: Optional[Union[numpy.ndarray, tuple]]):
        if isinstance(data, numpy.ndarray):
            if (
                self._expected_dim is not None
                and data is not None
                and data.ndim not in self._expected_dim
            ):
                raise ValueError(
                    f"data is expected to be {self._expected_dim}d not {data.ndim}d"
                )
        elif isinstance(data, (tuple, list)):
            for elmt in data:
                if not isinstance(elmt, (DataUrl, VirtualSource)):
                    raise TypeError(
                        f"element of 'data' are expected to be silx DataUrl or h5py virtualSource. Not {type(elmt)}"
                    )
            data = tuple(data)
        elif data is None:
            pass
        else:
            raise TypeError(
                f"data is expected to be an instance of {numpy.ndarray}, None or a list of silx DataUrl or h5py Virtual Source. Not {type(data)}"
            )
        self._data = data

    @property
    def x_pixel_size(self) -> Optional[float]:
        """x pixel size in meter (S.I.)"""
        return self._x_pixel_size

    @x_pixel_size.setter
    def x_pixel_size(self, x_pixel_size: Optional[float]) -> None:
        if not isinstance(x_pixel_size, (type(None), float)):
            raise TypeError(
                f"x_pixel_size is expected ot be an instance of {float} or None. Not {type(x_pixel_size)}"
            )
        self._x_pixel_size.value = x_pixel_size

    @property
    def y_pixel_size(self) -> Optional[float]:
        """y pixel size in meter (S.I.)"""
        return self._y_pixel_size

    @y_pixel_size.setter
    def y_pixel_size(self, y_pixel_size: Optional[float]) -> None:
        if not isinstance(y_pixel_size, (type(None), float)):
            raise TypeError(
                f"y_pixel_size is expected ot be an instance of {float} or None. Not {type(y_pixel_size)}"
            )
        self._y_pixel_size.value = y_pixel_size

    @property
    def distance(self) -> Optional[float]:
        """
        sample / detector distance in meter
        """
        return self._distance

    @distance.setter
    def distance(self, distance: Optional[float]) -> None:
        if not isinstance(distance, (type(None), float)):
            raise TypeError(
                f"distance is expected ot be an instance of {float} or None. Not {type(distance)}"
            )
        self._distance.value = distance

    @property
    def field_of_view(self) -> Optional[FieldOfView]:
        return self._field_of_view

    @field_of_view.setter
    def field_of_view(
        self, field_of_view: Optional[Union[FieldOfView, str, None]]
    ) -> None:
        if field_of_view is not None:
            field_of_view = FieldOfView.from_value(field_of_view)
        self._field_of_view = field_of_view

    @property
    def count_time(self) -> Optional[numpy.ndarray]:
        return self._count_time

    @count_time.setter
    def count_time(self, count_time: Optional[Iterable]):
        self._count_time.value = cast_and_check_array_1D(count_time, "count_time")

    @property
    def estimated_cor_from_motor(self) -> Optional[float]:
        return self._estimated_cor_from_motor

    @estimated_cor_from_motor.setter
    def estimated_cor_from_motor(self, estimated_cor_from_motor: Optional[float]):
        if not isinstance(estimated_cor_from_motor, (type(None), float)):
            raise TypeError(
                f"estimated_cor_from_motor is expected to be None, or an instance of float. Not {type(estimated_cor_from_motor)}"
            )
        self._estimated_cor_from_motor = estimated_cor_from_motor

    @property
    def image_key_control(self) -> Optional[numpy.ndarray]:
        """
        control image key are the same as image key except that they can contain negative values for return / alignment projection.
        """
        return self._image_key_control

    @image_key_control.setter
    def image_key_control(self, control_image_key: Optional[Iterable]):
        control_image_key = cast_and_check_array_1D(
            control_image_key, "control_image_key"
        )
        if control_image_key is None:
            self._image_key_control = None
        else:
            # cast all value to instances of ImageKey
            self._image_key_control = numpy.asarray(
                [ImageKey.from_value(key) for key in control_image_key]
            )

    @property
    def image_key(self) -> Optional[numpy.ndarray]:
        """
        control_image_key with ALIGNEMENT keys cast to PROJECTION
        """
        if self.image_key_control is None:
            return None
        else:
            control_image_key = self.image_key_control.copy()
            control_image_key[
                control_image_key == ImageKey.ALIGNMENT
            ] = ImageKey.PROJECTION
            return control_image_key

    @property
    def tomo_n(self) -> Optional[int]:
        return self._tomo_n

    @tomo_n.setter
    def tomo_n(self, tomo_n: Optional[int]):
        self._tomo_n = tomo_n

    @property
    def group_size(self) -> Optional[int]:
        return self._group_size

    @group_size.setter
    def group_size(self, group_size: Optional[int]):
        self._group_size = group_size

    @docstring(NXobject)
    def to_nx_dict(
        self,
        nexus_path_version: Optional[float] = None,
        data_path: Optional[str] = None,
    ) -> dict:
        nexus_paths = get_nexus_path(nexus_path_version)
        nexus_detector_paths = nexus_paths.nx_detector_paths

        nx_dict = {}

        if self.image_key_control is not None:
            path_img_key = f"{self.path}/{nexus_detector_paths.IMAGE_KEY}"
            nx_dict[path_img_key] = [img_key.value for img_key in self.image_key]
            path_img_key_ctrl = f"{self.path}/{nexus_detector_paths.IMAGE_KEY_CONTROL}"
            nx_dict[path_img_key_ctrl] = [
                img_key.value for img_key in self.image_key_control
            ]
        if self.x_pixel_size.value is not None:
            path_x_pixel_size = f"{self.path}/{nexus_detector_paths.X_PIXEL_SIZE}"
            nx_dict[path_x_pixel_size] = self.x_pixel_size.value
            nx_dict["@".join([path_x_pixel_size, "unit"])] = str(self.x_pixel_size.unit)
        if self.y_pixel_size.value is not None:
            path_y_pixel_size = f"{self.path}/{nexus_detector_paths.Y_PIXEL_SIZE}"
            nx_dict[path_y_pixel_size] = self.y_pixel_size.value
            nx_dict["@".join([path_y_pixel_size, "unit"])] = str(self.y_pixel_size.unit)
        if self.distance.value is not None:
            path_distance = f"{self.path}/{nexus_detector_paths.DISTANCE}"
            nx_dict[path_distance] = self.distance.value
            nx_dict["@".join([path_distance, "unit"])] = str(self.distance.unit)
        if self.field_of_view is not None:
            path_fov = f"{self.path}/{nexus_detector_paths.FOV}"
            nx_dict[path_fov] = self.field_of_view.value
        if self.count_time.value is not None:
            path_count_time = f"{self.path}/{nexus_detector_paths.EXPOSURE_TIME}"
            nx_dict[path_count_time] = self.count_time.value
            nx_dict["@".join([path_count_time, "unit"])] = str(self.count_time.unit)
        if self.tomo_n is not None:
            tomo_n_fov_path = f"{nexus_paths.TOMO_N_SCAN}"
            nx_dict[tomo_n_fov_path] = self.tomo_n
        if self.group_size is not None:
            group_size_path = f"{self.path}/{nexus_paths.GRP_SIZE_ATTR}"
            nx_dict[group_size_path] = self.group_size
        if self.estimated_cor_from_motor is not None:
            path_estimated_cor = (
                f"{self.path}/{nexus_detector_paths.ESTIMATED_COR_FRM_MOTOR}"
            )
            nx_dict[path_estimated_cor] = self.estimated_cor_from_motor
            nx_dict["@".join([path_estimated_cor, "unit"])] = "pixel"

        nx_dict.update(
            self._data_to_nx_dict(
                nexus_path_version=nexus_path_version,
                data_path=data_path,
            )
        )
        return nx_dict

    def _data_to_nx_dict(
        self,
        nexus_path_version: Optional[float] = None,
        data_path: Optional[str] = None,
    ) -> dict:
        nexus_paths = get_nexus_path(nexus_path_version)
        nexus_detector_paths = nexus_paths.nx_detector_paths

        nx_dict = {}
        if self.data is not None:
            # add data
            path_data = f"{self.path}/{nexus_detector_paths.DATA}"
            nx_dict[path_data] = self.data
            nx_dict["@".join([path_data, "interpretation"])] = "image"
            # add attributes to data
            nx_dict[f"{self.path}@NX_class"] = "NXdetector"
            nx_dict[f"{self.path}@signal"] = nexus_detector_paths.DATA
            nx_dict[f"{self.path}@SILX_style/axis_scale_types"] = [
                "linear",
                "linear",
            ]
        return nx_dict

    def _load(
        self, file_path: str, data_path: str, nexus_version: float, load_data_as: str
    ) -> None:
        possible_as_values = ("as_virtual_source", "as_data_url", "as_numpy_array")
        if load_data_as not in possible_as_values:
            raise ValueError(
                f"load_data_as is expected to be in {possible_as_values} and not {load_data_as}"
            )

        nexus_paths = get_nexus_path(nexus_version)
        nexus_detector_paths = nexus_paths.nx_detector_paths

        data_dataset_path = f"{data_path}/{nexus_detector_paths.DATA}"
        with HDF5File(file_path, mode="r") as h5f:
            if data_dataset_path in h5f:
                dataset = h5f[data_dataset_path]
            else:
                raise KeyError("unable to find", data_dataset_path)
            if load_data_as == "as_numpy_array":
                self.data = dataset[()]
            elif load_data_as == "as_data_url":
                if dataset.is_virtual:
                    urls = []
                    for vs_info in dataset.virtual_sources():

                        select_bounds = vs_info.vspace.get_select_bounds()
                        left_bound = select_bounds[0]
                        right_bound = select_bounds[1]
                        # warning: for now step is not managed with virtual
                        # dataset

                        length = right_bound[0] - left_bound[0] + 1
                        # warning: for now step is not managed with virtual
                        # dataset

                        virtual_source = h5py.VirtualSource(
                            vs_info.file_name,
                            vs_info.dset_name,
                            vs_info.vspace.shape,
                        )
                        # here we could provide dataset but we won't to
                        # insure file path will be relative.
                        type_code = vs_info.src_space.get_select_type()
                        # check for unlimited selections in case where selection is regular
                        # hyperslab, which is the only allowed case for h5s.UNLIMITED to be
                        # in the selection
                        if (
                            type_code == h5py_h5s.SEL_HYPERSLABS
                            and vs_info.src_space.is_regular_hyperslab()
                        ):
                            (
                                source_start,
                                stride,
                                count,
                                block,
                            ) = vs_info.src_space.get_regular_hyperslab()
                            source_end = source_start[0] + length

                            sel = selection.select(
                                dataset.shape,
                                slice(source_start[0], source_end),
                                dataset=dataset,
                            )
                            virtual_source.sel = sel

                        urls.append(from_virtual_source_to_data_url(virtual_source))
                else:
                    urls = [
                        DataUrl(
                            file_path=file_path,
                            data_path=data_dataset_path,
                            scheme="silx",
                        )
                    ]
                self.data = urls
            elif load_data_as == "as_virtual_source":
                if dataset.is_virtual:
                    self.data = dataset.virtual_sources()
                else:
                    raise ValueError(f"{data_dataset_path} is not virtual")

        self.x_pixel_size, self.x_pixel_size.unit = get_data_and_unit(
            file_path=file_path,
            data_path="/".join([data_path, nexus_detector_paths.X_PIXEL_SIZE]),
            default_unit=MetricSystem.METER,
        )
        self.y_pixel_size, self.y_pixel_size.unit = get_data_and_unit(
            file_path=file_path,
            data_path="/".join([data_path, nexus_detector_paths.Y_PIXEL_SIZE]),
            default_unit=MetricSystem.METER,
        )
        self.distance, self.distance.unit = get_data_and_unit(
            file_path=file_path,
            data_path="/".join([data_path, nexus_detector_paths.DISTANCE]),
            default_unit=MetricSystem.METER,
        )
        self.distance, self.distance.unit = get_data_and_unit(
            file_path=file_path,
            data_path="/".join([data_path, nexus_detector_paths.DISTANCE]),
            default_unit=MetricSystem.METER,
        )
        self.field_of_view = get_data(
            file_path=file_path,
            data_path="/".join([data_path, nexus_detector_paths.FOV]),
        )
        self.count_time, self.count_time.unit = get_data_and_unit(
            file_path=file_path,
            data_path="/".join([data_path, nexus_detector_paths.EXPOSURE_TIME]),
            default_unit=TimeSystem.SECOND,
        )
        self.tomo_n = get_data(
            file_path=file_path,
            data_path="/".join([data_path, nexus_paths.TOMO_N_SCAN]),
        )
        self.group_size = get_data(
            file_path=file_path,
            data_path="/".join([data_path, nexus_paths.GRP_SIZE_ATTR]),
        )
        self.estimated_cor_from_motor = get_data(
            file_path=file_path,
            data_path="/".join(
                [data_path, nexus_detector_paths.ESTIMATED_COR_FRM_MOTOR]
            ),
        )
        self.image_key_control = get_data(
            file_path=file_path,
            data_path="/".join([data_path, nexus_detector_paths.IMAGE_KEY_CONTROL]),
        )


class NXdetectorWithUnit(NXdetector):
    def __init__(
        self,
        default_unit: Unit,
        node_name="detector",
        parent=None,
        field_of_view=None,
        expected_dim: Optional[tuple] = None,
    ) -> None:
        super().__init__(node_name, parent, field_of_view, expected_dim)
        self._data = ElementWithUnit(default_unit=default_unit)

    @property
    def data(self) -> Union[numpy.ndarray, tuple]:
        """data can be None, a numpy array or a list of DataUrl xor h5py Virtual Source"""
        return self._data

    @data.setter
    def data(self, data: Optional[Union[numpy.ndarray, tuple]]):
        if isinstance(data, numpy.ndarray):
            if (
                self._expected_dim is not None
                and data is not None
                and data.ndim not in self._expected_dim
            ):
                raise ValueError(
                    f"data is expected to be {self._expected_dim}d not {data.ndim}d"
                )
        elif isinstance(data, (tuple, list)):
            for elmt in data:
                if not isinstance(elmt, (DataUrl, VirtualSource)):
                    raise TypeError(
                        f"'data' is expected to be a numpy array or a list/tuple composed of DataUrl or h5py virtualSource. Not {type(elmt)}"
                    )
            data = tuple(data)
        elif data is None:
            pass
        else:
            raise TypeError(
                f"data is expected to be an instance of {numpy.ndarray}, None or a list of silx DataUrl or h5py Virtual Source. Not {type(data)}"
            )
        self._data.value = data

    def _data_to_nx_dict(
        self,
        nexus_path_version: Optional[float] = None,
        data_path: Optional[str] = None,
    ) -> dict:
        nexus_paths = get_nexus_path(nexus_path_version)
        nexus_detector_paths = nexus_paths.nx_detector_paths

        nx_dict = {}
        if self.data.value is not None:
            # add data
            path_data = f"{self.path}/{nexus_detector_paths.DATA}"
            nx_dict[path_data] = self.data.value
            nx_dict["@".join([path_data, "interpretation"])] = "image"
            # add attributes to data
            nx_dict[f"{self.path}@NX_class"] = "NXdetector"
            nx_dict[f"{self.path}@signal"] = nexus_detector_paths.DATA
            nx_dict[f"{self.path}@SILX_style/axis_scale_types"] = [
                "linear",
                "linear",
            ]
        return nx_dict
