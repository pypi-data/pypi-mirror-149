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
Utils related to bliss-HDF5
"""


from nxtomomill.io.acquisitionstep import AcquisitionStep
from silx.io.utils import h5py_read_dataset
from nxtomomill.io.config import TomoHDF5Config
from silx.io.url import DataUrl
from tomoscan.io import HDF5File
import typing
import h5py

try:
    import hdf5plugin  # noqa F401
except ImportError:
    pass
import logging

_logger = logging.getLogger(__name__)


def has_valid_detector(node, detectors_names):
    """
    :return True if the node looks like a valid nx detector
    """
    for key in node.keys():
        if (
            "NX_class" in node[key].attrs
            and node[key].attrs["NX_class"] == "NXdetector"
        ):
            if detectors_names is None or key in detectors_names:
                return True
    return False


def get_entry_type(
    url: DataUrl, configuration: TomoHDF5Config
) -> typing.Union[None, AcquisitionStep]:
    """
    :return: return the step of the acquisition or None if cannot find it.
    """
    if not isinstance(url, DataUrl):
        raise TypeError("DataUrl is expected. Not {}".format(type(url)))
    if url.data_slice() is not None:
        raise ValueError(
            "url expect to provide a link to bliss scan. Slice " "are not handled"
        )
    with HDF5File(url.file_path(), mode="r") as h5f:
        if url.data_path() not in h5f:
            raise ValueError("Provided path does not exists: {}".format(url))
        entry = h5f[url.data_path()]
        if not isinstance(entry, h5py.Group):
            raise ValueError(
                "Expected path is not related to a h5py.Group "
                "({}) when expect to target a bliss entry."
                "".format(entry)
            )

        try:
            title = h5py_read_dataset(entry["title"])
        except Exception:
            _logger.error("fail to find title for %s, skip this group" % entry.name)
        else:
            init_titles = list(configuration.init_titles)
            init_titles.extend(configuration.zserie_init_titles)
            init_titles.extend(configuration.pcotomo_init_titles)

            step_titles = {
                AcquisitionStep.INITIALIZATION: init_titles,
                AcquisitionStep.DARK: configuration.dark_titles,
                AcquisitionStep.FLAT: configuration.flat_titles,
                AcquisitionStep.PROJECTION: configuration.projections_titles,
                AcquisitionStep.ALIGNMENT: configuration.alignment_titles,
            }

            for step, titles in step_titles.items():
                for title_start in titles:
                    if title.startswith(title_start):
                        return step
            return None


def get_nx_detectors(node: h5py.Group) -> tuple:
    """

    :param h5py.Group node: node to inspect
    :return: tuple of NXdetector (h5py.Group) contained in `node`
             (expected to be the `instrument` group)
    :rtype: tuple
    """
    if not isinstance(node, h5py.Group):
        raise TypeError("node should be an instance of h5py.Group")
    nx_detectors = []
    for _, subnode in node.items():
        if isinstance(subnode, h5py.Group) and "NX_class" in subnode.attrs:
            if subnode.attrs["NX_class"] == "NXdetector":
                if "data" in subnode and hasattr(subnode["data"], "ndim"):
                    if subnode["data"].ndim == 3:
                        nx_detectors.append(subnode)
    nx_detectors = sorted(nx_detectors, key=lambda det: det.name)
    return tuple(nx_detectors)


def guess_nx_detector(node: h5py.Group) -> tuple:
    """
    Try to guess what can be an nx_detector without using the "NXdetector"
    NX_class attribute. Expect to find a 3D dataset named 'data' under
    a subnode
    """
    if not isinstance(node, h5py.Group):
        raise TypeError("node should be an instance of h5py.Group")
    nx_detectors = []
    for _, subnode in node.items():
        if isinstance(subnode, h5py.Group) and "data" in subnode:
            if isinstance(subnode["data"], h5py.Dataset) and subnode["data"].ndim == 3:
                nx_detectors.append(subnode)

    nx_detectors = sorted(nx_detectors, key=lambda det: det.name)
    return tuple(nx_detectors)
