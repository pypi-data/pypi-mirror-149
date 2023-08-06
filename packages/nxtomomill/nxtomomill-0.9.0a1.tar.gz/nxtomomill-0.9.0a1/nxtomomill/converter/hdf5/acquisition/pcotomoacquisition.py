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
module to define a pcotomo acquistion
"""

__authors__ = [
    "H. Payno",
]
__license__ = "MIT"
__date__ = "08/02/2021"


from silx.utils.proxy import docstring
from nxtomomill.converter.hdf5.acquisition.baseacquisition import EntryReader
from nxtomomill.converter.hdf5.acquisition.standardacquisition import (
    StandardAcquisition,
)
from nxtomomill.io.acquisitionstep import AcquisitionStep
from nxtomomill.io.config import TomoHDF5Config
from silx.io.url import DataUrl
from typing import Optional, Union
import logging
from nxtomomill.nexus.nxtomo import NXtomo
from nxtomomill.utils import ImageKey
from nxtomomill.utils.nxsplitter import _NXtomoDetectorDataSplitter

_logger = logging.getLogger(__name__)


class PCOTomoAcquisition(StandardAcquisition):
    """
    A PCOTomo acquisition is an acquisition that can look like that at bliss side:

    * scan "descritpion", title can be tomo:pcotomo for example
    * Optional scan dark
    * Optional scan flat
    * scan "projections"
    * Optional scan flat

    The scan "projections" contains several "tomo" with a parameter evolving with time like heat or pressure.
    The idea is that we want to split those into several NXtomo.
    Those NXtomo must duplicate dark and flat scans
    For example if scan "projections" contains nb_loop = 2 and nb_loop = 3 we must create nb_loop*nb_loop == 6 NXtomo as output.

    Split of those can are done in postprocessing on the to_NXtomos function
    """

    def __init__(
        self,
        root_url: Union[DataUrl, None],
        configuration: TomoHDF5Config,
        detector_sel_callback,
        start_index,
    ):
        super().__init__(
            root_url=root_url,
            configuration=configuration,
            detector_sel_callback=detector_sel_callback,
            start_index=start_index,
        )
        self._nb_loop = None
        self._nb_tomo = None
        self._entries_to_split = set()  # set of URL as str

    def _preprocess_registered_entries(self):
        # those must be defined before calling super because the super will call then `_preprocess_registered_entry`
        self._nb_loop = None
        self._nb_tomo = None
        self._entries_to_split = set()
        super()._preprocess_registered_entries()

    def _preprocess_registered_entry(self, entry_url, type_):
        super()._preprocess_registered_entry(entry_url=entry_url, type_=type_)
        if type_ is AcquisitionStep.PROJECTION:
            # nb loop parameter must be present only on projection entries
            nb_loop = self.get_nb_loop(entry_url)
            if (
                nb_loop is not None
            ):  # at this moment 02/2022 nb_loop is only defined on projection type
                if self._nb_loop is None or self._nb_loop == nb_loop:
                    self._nb_loop = nb_loop
                    self._entries_to_split.add(entry_url.path())
                else:
                    _logger.error(
                        f"Found entries with a different number of nb_loop: {entry_url.path()}"
                    )
            nb_tomo = self.get_nb_tomo(entry_url)
            if (
                nb_tomo is not None
            ):  # at this moment 02/2022 nb_loop is only defined on projection type
                if self._nb_tomo is None or self._nb_tomo == nb_tomo:
                    self._nb_tomo = nb_tomo
                    self._entries_to_split.add(entry_url.path())
                else:
                    _logger.error(
                        f"Found entries with a different number of _nb_tomo: {entry_url.path()}"
                    )

    def get_nb_loop(self, url) -> Optional[int]:
        with EntryReader(url) as entry:
            if self._NB_LOOP_PATH in entry:
                return entry[self._NB_LOOP_PATH][()]
        return None

    def get_nb_tomo(self, url) -> Optional[int]:
        with EntryReader(url) as entry:
            if self._NB_LOOP_PATH in entry:
                return entry[self._NB_TOMO_PATH][()]
        return None

    def get_expected_nx_tomo(self):
        # the number of expected NXtomo is saved with projection
        # and not with the init title. This is why it but be computed later
        return 0

    @docstring(StandardAcquisition)
    def to_NXtomos(self, request_input, input_callback, check_tomo_n: bool) -> tuple:
        nx_tomos = super().to_NXtomos(request_input, input_callback, check_tomo_n=False)
        results = []

        for nx_tomo in nx_tomos:
            splitter = _NXtomoDetectorDataSplitter(nx_tomo)
            projections_slices = self._get_projections_slices(nx_tomo)
            if len(projections_slices) > 1:
                # insure projections are contiguous otherwise we don't know how to split it.
                # not defined on the current design from bliss. should never happen
                raise ValueError("Expect all projections to be contiguous")
            elif len(projections_slices) == 0:
                raise ValueError("No projection found")
            else:
                results.extend(
                    splitter.split(
                        projections_slices[0],
                        nb_part=(int(self._nb_loop * self._nb_tomo)),
                    )
                )

        if check_tomo_n:
            self.check_tomo_n()

        return tuple(results)

    @staticmethod
    def _get_projections_slices(nx_tomo: NXtomo) -> tuple:
        """Return a tuple of slices for each group of contiguous projections"""
        if nx_tomo.instrument.detector.image_key_control is None:
            return ()

        res = []
        start_pos = -1
        browsing_projection = False
        for i_frame, image_key in enumerate(
            nx_tomo.instrument.detector.image_key_control
        ):
            image_key_value = ImageKey.from_value(image_key)
            if image_key_value is ImageKey.PROJECTION and not browsing_projection:
                browsing_projection = True
                start_pos = i_frame
            elif browsing_projection and image_key_value is not ImageKey.PROJECTION:
                res.append(slice(start_pos, i_frame, 1))
                start_pos = -1
                browsing_projection = False
        else:
            if browsing_projection is True:
                res.append(slice(start_pos, i_frame + 1, 1))
        return tuple(res)
