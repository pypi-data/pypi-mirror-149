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
__date__ = "17/02/2022"


from typing import Optional, Union
from nxtomomill.utils.hdf5 import DatasetReader
from silx.io.url import DataUrl
from nxtomomill.nexus.nxtomo import NXtomo
import numpy
import h5py
from silx.io.utils import get_data
import copy
import h5py._hl.selections as selection


class _NXtomoDetectorDataSplitter:
    """Splitter to split the dataset nxtomo.instrument.detector.data
    into several NXtomo.
    This will also keep up to date rotation_angle, image_key, x_translation... datasets.
    In order to start the processing it requires a correctly formed NXtomo (same number of image_key, rotation_angle...)
    This is required for the pcotomo acquisition.
    """

    def __init__(self, nx_tomo: NXtomo) -> None:
        if not isinstance(nx_tomo, NXtomo):
            raise TypeError(
                f"nxtomo is expected to be an instance of {NXtomo} and not {type(nx_tomo)}"
            )
        self._nx_tomo = nx_tomo

    @property
    def nx_tomo(self) -> NXtomo:
        return self._nx_tomo

    def split(self, data_slice: slice, nb_part: int) -> tuple:
        """
        split the dataset targetted to have a set of h5py.VirtualSource.

        :param int nb_part: in how many contiguous dataset the instruement.detector.data must be splitted.
        :raises: ValueError if the number of frame, image_key, x_translation... is incoherent.
        """
        if not isinstance(nb_part, int):
            raise TypeError(f"nb_part is expected to be an int not {type(nb_part)}")
        invalid_datasets = self.get_invalid_datasets()
        if len(invalid_datasets) > 0:
            raise ValueError(
                f"Some datasets have incoherent length compared to nx_tomo.instrument.detector.data length: {invalid_datasets}"
            )
        elif nb_part <= 0:
            raise ValueError(f"nb_part is expected to be >=1 not {nb_part}")
        elif nb_part == 1:
            return [
                self.nx_tomo,
            ]
        elif data_slice.step not in (1, None):
            raise ValueError("slice step must be one.")
        elif (data_slice.stop - data_slice.start) % nb_part != 0:
            raise ValueError(
                f"incoherent split requested. Request to spluit {(data_slice.stop - data_slice.start)} slices into {nb_part} parts"
            )
        else:
            parts = []
            for i_part in range(nb_part):
                current_slice = data_slice
                new_slice_size = (current_slice.stop - current_slice.start) // nb_part
                new_slice = slice(
                    current_slice.start + new_slice_size * i_part,
                    current_slice.start + new_slice_size * (i_part + 1),
                    1,
                )
                nx_tomo_part = self.replace(old_slice=data_slice, new_slice=new_slice)
                parts.append(nx_tomo_part)
            return parts

    def replace(self, old_slice: slice, new_slice: slice) -> NXtomo:
        """
        replace a section of the NXtomo instrument.detector.data by a subsection of it
        """
        if not isinstance(old_slice, slice):
            raise TypeError("old_slice is expected to be a slice")
        if not isinstance(new_slice, slice):
            raise TypeError("new_slice is expected to be a slice")
        if old_slice.step not in (None, 1):
            raise ValueError("old_slice step is expected to be one")
        if new_slice.step not in (None, 1):
            raise ValueError("new_slice step is expected to be one")

        if new_slice.start < old_slice.start or new_slice.stop > old_slice.stop:
            raise ValueError(
                f"new_slice ({new_slice}) must be contained in old_slice ({old_slice})"
            )

        if old_slice.start < 0:
            raise ValueError(
                f"old_slice.start must be at least 0 not {old_slice.start}"
            )
        n_frames = self._get_n_frames()
        if n_frames is not None and old_slice.stop > n_frames:
            raise ValueError(
                f"old_slice.start must be at most {n_frames} not {old_slice.stop}"
            )

        # handles datasets other than instrument.detector.data
        result_nx_tomo = copy.deepcopy(self.nx_tomo)
        if result_nx_tomo.sample.rotation_angle is not None:
            result_nx_tomo.sample.rotation_angle = numpy.concatenate(
                [
                    self.nx_tomo.sample.rotation_angle[: old_slice.start],
                    self.nx_tomo.sample.rotation_angle[new_slice],
                    self.nx_tomo.sample.rotation_angle[old_slice.stop :],
                ]
            )

        if result_nx_tomo.sample.x_translation.value is not None:
            result_nx_tomo.sample.x_translation.value = numpy.concatenate(
                [
                    self.nx_tomo.sample.x_translation.value[: old_slice.start],
                    self.nx_tomo.sample.x_translation.value[new_slice],
                    self.nx_tomo.sample.x_translation.value[old_slice.stop :],
                ]
            )

        if result_nx_tomo.sample.y_translation.value is not None:
            result_nx_tomo.sample.y_translation.value = numpy.concatenate(
                [
                    self.nx_tomo.sample.y_translation.value[: old_slice.start],
                    self.nx_tomo.sample.y_translation.value[new_slice],
                    self.nx_tomo.sample.y_translation.value[old_slice.stop :],
                ]
            )

        if result_nx_tomo.sample.z_translation.value is not None:
            result_nx_tomo.sample.z_translation.value = numpy.concatenate(
                [
                    self.nx_tomo.sample.z_translation.value[: old_slice.start],
                    self.nx_tomo.sample.z_translation.value[new_slice],
                    self.nx_tomo.sample.z_translation.value[old_slice.stop :],
                ]
            )

        if result_nx_tomo.instrument.detector.image_key_control is not None:
            result_nx_tomo.instrument.detector.image_key_control = numpy.concatenate(
                [
                    self.nx_tomo.instrument.detector.image_key_control[
                        : old_slice.start
                    ],
                    self.nx_tomo.instrument.detector.image_key_control[new_slice],
                    self.nx_tomo.instrument.detector.image_key_control[
                        old_slice.stop :
                    ],
                ]
            )

        # handles detector.data dataset. This one is special because it can contains
        # numpy arrays (raw data), h5py.VirtualSource or DataUrl (or be None)
        det_data = self.nx_tomo.instrument.detector.data
        if det_data is None:
            pass
        elif isinstance(det_data, numpy.ndarray):
            result_nx_tomo.instrument.detector.data = numpy.concatenate(
                [
                    det_data[: old_slice.start],
                    det_data[new_slice],
                    det_data[old_slice.stop :],
                ]
            )
        elif isinstance(det_data, (tuple, list)):
            result_nx_tomo.instrument.detector.data = numpy.concatenate(
                [
                    self._get_detector_data_sub_section(slice(0, old_slice.start, 1)),
                    self._get_detector_data_sub_section(new_slice),
                    self._get_detector_data_sub_section(
                        slice(old_slice.stop, n_frames + 1, 1)
                    ),
                ]
            ).tolist()
        else:
            raise TypeError(
                f"instrument.detector.data must be a numpy array or a VirtualSource or a DataUrl. Not {type(det_data)}"
            )
        return result_nx_tomo

    def _get_detector_data_sub_section(self, section: slice) -> tuple:
        """
        return a tuple of DataUrl or h5py.VirtualSource fitting the slice requested
        """
        det_data = self.nx_tomo.instrument.detector.data
        res = []
        if section.start == section.stop:
            return ()

        def get_elmt_shape(elmt: Union[h5py.VirtualSource, DataUrl]) -> tuple:
            if isinstance(elmt, h5py.VirtualSource):
                return elmt.shape
            elif isinstance(elmt, DataUrl):
                with DatasetReader(elmt) as dataset:
                    return dataset.shape
            else:
                raise TypeError(
                    f"elmt must be a DataUrl or h5py.VirtualSource. Not {type(elmt)}"
                )

        def get_elmt_nb_frame(elmt: Union[h5py.VirtualSource, DataUrl]) -> int:
            shape = get_elmt_shape(elmt)
            if len(shape) == 3:
                return shape[0]
            elif len(shape) == 2:
                return 1
            else:
                raise ValueError(f"virtualSource: {elmt} is not 2D or 3D")

        def construct_slices_elmt_list() -> dict:
            "create a dictionary with slice as key and DataUrl or h5py.VirtualSource as value"
            slices_elmts = []

            current_index = 0
            for elmt in det_data:
                n_frame = get_elmt_nb_frame(elmt)
                slice_ = slice(current_index, current_index + n_frame, 1)
                slices_elmts.append([slice_, elmt])
                current_index += n_frame
            return slices_elmts

        def intersect(slice_1, slice_2):
            """check if the two slices intersect"""
            assert isinstance(slice_1, slice) and slice_1.step == 1
            assert isinstance(slice_2, slice) and slice_2.step == 1
            return slice_1.start < slice_2.stop and slice_1.stop > slice_2.start

        def select(
            elmt: Union[h5py.VirtualSource, DataUrl], region: slice
        ) -> Union[h5py.VirtualSource, DataUrl]:
            """select a region on the elmt.
            Can return at most the elmt itself or a region of it"""
            elmt_n_frame = get_elmt_nb_frame(elmt)
            assert elmt_n_frame != 0
            clamp_region = slice(
                max(0, region.start),
                min(elmt_n_frame, region.stop),
                1,
            )
            assert clamp_region.start != clamp_region.stop

            if isinstance(elmt, h5py.VirtualSource):
                frame_dims = elmt.shape[-2], elmt.shape[-1]
                n_frames = clamp_region.stop - clamp_region.start
                assert n_frames > 0
                shape = (n_frames, frame_dims[0], frame_dims[1])
                vs = h5py.VirtualSource(
                    path_or_dataset=elmt.path,
                    name=elmt.name,
                    shape=shape,
                )
                vs.sel = selection.select(elmt.shape, clamp_region)
                return vs
            else:
                if elmt.data_slice() is None:
                    data_slice = clamp_region
                elif isinstance(elmt.data_slice(), slice):
                    if elmt.data_slice.step not in (1, None):
                        raise ValueError("DataUrl with step !=1 are not handled")
                    else:
                        data_slice = slice(
                            elmt.data_slice.start + clamp_region.start,
                            elmt.data_slice.start + clamp_region.stop,
                            1,
                        )
                else:
                    raise TypeError(
                        f"data_slice is expected to be None or a slice. Not {type(elmt.data_slice())}"
                    )
                return DataUrl(
                    file_path=elmt.file_path(),
                    data_path=elmt.data_path(),
                    scheme=elmt.scheme(),
                    data_slice=data_slice,
                )

        for slice_raw_data, elmt in construct_slices_elmt_list():
            if intersect(section, slice_raw_data):
                res.append(
                    select(
                        elmt,
                        slice(
                            section.start - slice_raw_data.start,
                            section.stop - slice_raw_data.start,
                            1,
                        ),
                    )
                )
        return tuple(res)

    def get_invalid_datasets(self) -> dict:
        """
        return a dict of invalid dataset compare to the instrument.detector.data dataset.
        Key is the location ? path to the invalid dataset. Value is the reason of the failure.
        """
        invalid_datasets = {}
        n_frames = self._get_n_frames()

        # check rotation_angle
        if self.nx_tomo.sample.rotation_angle is not None:
            n_rotation_angles = len(self.nx_tomo.sample.rotation_angle)
            if n_rotation_angles != n_frames:
                invalid_datasets[
                    "sample/rotation_angle"
                ] = f"{n_rotation_angles} angles found when {n_frames} expected"

        # check image_key_control (force to have the same number as image_key already so only check one)
        if self.nx_tomo.instrument.detector.image_key_control is not None:
            n_image_key_control = len(
                self.nx_tomo.instrument.detector.image_key_control
            )
            if n_image_key_control != n_frames:
                invalid_datasets[
                    "instrument/detector/image_key_control"
                ] = f"{n_image_key_control} image_key_control values found when {n_frames} expected"

        # check x_translation
        if self.nx_tomo.sample.x_translation.value is not None:
            n_x_translation = len(self.nx_tomo.sample.x_translation.value)
            if n_x_translation != n_frames:
                invalid_datasets[
                    "sample/x_translation"
                ] = f"{n_x_translation} x translations found when {n_frames} expected"

        # check y_translation
        if self.nx_tomo.sample.y_translation.value is not None:
            n_y_translation = len(self.nx_tomo.sample.y_translation.value)
            if n_y_translation != n_frames:
                invalid_datasets[
                    "sample/y_translation"
                ] = f"{n_y_translation} y translations found when {n_frames} expected"

        # check z_translation
        if self.nx_tomo.sample.z_translation.value is not None:
            n_z_translation = len(self.nx_tomo.sample.z_translation.value)
            if n_z_translation != n_frames:
                invalid_datasets[
                    "sample/z_translation"
                ] = f"{n_z_translation} z translations found when {n_frames} expected"

        return invalid_datasets

    def _get_n_frames(self) -> Optional[int]:
        dataset = self.nx_tomo.instrument.detector.data
        if dataset is None:
            return None
        elif isinstance(dataset, numpy.ndarray):
            if not dataset.ndim == 3:
                raise ValueError(
                    f"nx_tomo.instrument.detector.data is expected to be 3D and not {dataset.ndim}D."
                )
            else:
                return dataset.shape[0]
        elif isinstance(dataset, (list, tuple)):
            n_frames = 0
            for dataset_elmt in dataset:
                if isinstance(dataset_elmt, h5py.VirtualSource):
                    shape = dataset_elmt.shape
                    if len(shape) == 3:
                        n_frames += dataset_elmt.shape[0]
                    elif len(shape) == 2:
                        n_frames += 1
                    else:
                        raise ValueError(
                            f"h5py.VirtualSource shape is expected to be 2D (single frame) or 3D. Not {len(shape)}D."
                        )
                elif isinstance(dataset_elmt, DataUrl):
                    data = get_data(dataset_elmt)
                    if not isinstance(data, numpy.ndarray):
                        raise TypeError(
                            f"url: {dataset_elmt.path()} is not pointing to an array"
                        )
                    elif data.ndim == 2:
                        n_frames += 1
                    elif data.ndim == 3:
                        n_frames += data.shape[0]
                    else:
                        raise ValueError(
                            f"url: {dataset_elmt.path()} is expected to be 2D or 3D. Not {dataset_elmt.ndim} D"
                        )
                else:
                    raise TypeError(
                        f"elements of {type(dataset)} must be h5py.VirtualSource) or silx.io.url.DataUrl and not {type(dataset_elmt)}"
                    )
            return n_frames
        else:
            raise TypeError(
                f"nx_tomo.instrument.detector.data type ({type(dataset)}) is not handled"
            )
