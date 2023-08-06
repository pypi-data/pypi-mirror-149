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
module to define a tomography z-series acquisition (made by bliss)
"""

__authors__ = [
    "H. Payno",
]
__license__ = "MIT"
__date__ = "27/11/2020"


from .baseacquisition import BaseAcquisition
from .baseacquisition import EntryReader
from .standardacquisition import StandardAcquisition
from nxtomomill.io.config import TomoHDF5Config
from silx.io.utils import h5py_read_dataset
from silx.utils.proxy import docstring
from typing import Iterable
import numpy
import h5py
from silx.io.url import DataUrl

try:
    import hdf5plugin  # noqa F401
except ImportError:
    pass


def is_z_series_frm_titles(entry: h5py.Group, configuration: TomoHDF5Config) -> bool:
    """
    is the provided h5py Group is tomography z series acquisition.
    the entry should be an 'initialization' entry. We will look on
    z_title_entries to know if this is a z entry or not
    """
    try:
        title = h5py_read_dataset(entry["title"])
    except Exception:
        return False
    else:
        return title in configuration.zserie_init_titles


def is_pcotomo_frm_titles(entry: h5py.Group, configuration: TomoHDF5Config) -> bool:
    """
    if the provided h5py.Group must be consider as an "initialization" entry/scan of a pcotomo acquistion
    """
    try:
        title = h5py_read_dataset(entry["title"])
    except Exception:
        return False
    else:
        return title in configuration.pcotomo_init_titles


def is_z_series_frm_z_translation(
    projection_urls: Iterable, configuration: TomoHDF5Config
):
    """

    :param Iterable projection_urls: list of DataUrl pointing to projection
                                     nodes.
    :return: True if the set of projections should be considered as a zserie
    """
    z_values = set()
    for url in projection_urls:
        with EntryReader(url) as entry:
            z_values_tmp, _ = BaseAcquisition.get_z_translation_frm(
                entry, n_frame=None, configuration=configuration
            )
            if z_values_tmp is not None:
                if isinstance(z_values_tmp, Iterable):
                    z_values.update(z_values_tmp)
                else:
                    z_values.add(z_values_tmp)
    return len(z_values) > 1


class ZSeriesBaseAcquisition(BaseAcquisition):
    """
    A 'z serie acquisition' is considered as a serie of _StandardAcquisition.
    Registered scan can be split according to z_translation value.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._acquisitions = {}
        """key is z value and value is _StandardAcquisition"""

    def get_expected_nx_tomo(self):
        return 1

    def get_standard_sub_acquisitions(self) -> tuple:
        """
        Return the tuple of all :class:`.StandardAcquisition` composing
        _acquisitions
        """
        return tuple(self._acquisitions.values())

    def get_z(self, entry):
        if not isinstance(entry, h5py.Group):
            raise TypeError("entry: expected h5py.Group")
        z_array = self._get_z_translation(entry, n_frame=None)[0]
        if z_array is None:
            raise ValueError("No z found for scan {}".format(entry.name))
        if isinstance(z_array, (numpy.ndarray, tuple, list)):
            z_array = set(z_array)
        else:
            z_array = set((z_array,))

        # might need an epsilon here ?
        if len(z_array) > 1:
            raise ValueError("More than one value of z found for {}".format(entry.name))
        else:
            return z_array.pop()

    @docstring(BaseAcquisition.register_step)
    def register_step(
        self, url: DataUrl, entry_type, copy_frames: bool = False
    ) -> None:
        """

        :param url:
        """
        with EntryReader(url) as entry:
            z = self.get_z(entry)
        if z not in self._acquisitions:
            self._acquisitions[z] = StandardAcquisition(
                root_url=url,
                configuration=self.configuration,
                detector_sel_callback=self._detector_sel_callback,
                start_index=self.start_index + len(self._acquisitions),
            )
        self._acquisitions[z].register_step(
            url=url, entry_type=entry_type, copy_frames=copy_frames
        )

    @property
    def require_x_translation(self):
        return True

    @property
    def require_z_translation(self):
        return True

    @property
    def is_xrd_ct(self):
        return False

    @docstring(BaseAcquisition)
    def is_different_sequence(self, entry):
        return True
