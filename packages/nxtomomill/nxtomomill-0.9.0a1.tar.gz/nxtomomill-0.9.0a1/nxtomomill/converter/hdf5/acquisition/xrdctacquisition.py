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
module to define a xrd-ct acquisition (made by bliss)
"""

__authors__ = [
    "H. Payno",
]
__license__ = "MIT"
__date__ = "27/11/2020"


from .standardacquisition import StandardAcquisition
from nxtomomill.io.config import TomoHDF5Config
from nxtomomill.io.acquisitionstep import AcquisitionStep
from .utils import has_valid_detector
import h5py
from silx.io.url import DataUrl

try:
    import hdf5plugin  # noqa F401
except ImportError:
    pass
import logging

_logger = logging.getLogger(__name__)


def is_xrdct_entry(node: h5py.Group, detectors_names):
    """
    is the provided h5py Group is an xrd-ct entry ?
    """
    # for now we can try to deduce if the entry is an XRD-CT acquisition
    # by checking if it does not contains scan_number and contains
    # a valid detector
    # maybe we can also use information from the
    # 'detector_name/acq_parameters/saving_directory' where the name of the
    # beamline seems accessible
    if (
        StandardAcquisition._SCAN_NUMBER_PATH not in node
        and "instrument" in node
        and has_valid_detector(node["instrument"], detectors_names=detectors_names)
    ):
        return True
    else:
        return False


class XRDCTAcquisition(StandardAcquisition):
    def __init__(
        self,
        root_url: DataUrl,
        configuration: TomoHDF5Config,
        detector_sel_callback,
        start_index,
        copy_frames: bool = False,
    ):
        """
        Note: for now we are force to provide entry and entry path as both
        can be different. For example when we are browsing the sample
        file entry == entry_path == 1.1 for example.
        Bit for the sample file file entry == 1.1 != entry_path == acquisssXXX_1.1

        :param entry:
        :param file_keys:
        :param scan_titles:
        :param param_already_defined:
        :param raise_error_if_issue:
        :param detector_sel_callback:
        """
        super().__init__(
            root_url=root_url,
            configuration=configuration,
            detector_sel_callback=detector_sel_callback,
            start_index=start_index,
        )
        # for XRD-CT data is contained in the 'acquisition' sequence
        # and we only have projections
        self.register_step(url=root_url, entry_type=AcquisitionStep.PROJECTION)

    @property
    def is_xrd_ct(self):
        return True

    @property
    def require_x_translation(self):
        return False

    @property
    def require_z_translation(self):
        return True

    @property
    def has_diode(self):
        return True

    def is_different_sequence(self, url: DataUrl):
        if not isinstance(url, DataUrl):
            raise TypeError(
                "url is expected to be a DataUrl. This case is " "not managed"
            )

        def get_scan_name(my_str):
            return "".join(my_str.rstrip(".").split(".")[0:-1])

        return self.root_url.file_path() != url.file_path() and get_scan_name(
            self.root_url.data_path()
        ) != get_scan_name(url.data_path())

    def get_axis_scale_types(self):
        """
        Return axis display for the detector data to be used by silx view
        """
        return ["linear", "log"]

    def _write_beam(self, root_node, request_input, input_callback):
        instrument_node = root_node.require_group("instrument")
        instrument_node.require_group("beam")
