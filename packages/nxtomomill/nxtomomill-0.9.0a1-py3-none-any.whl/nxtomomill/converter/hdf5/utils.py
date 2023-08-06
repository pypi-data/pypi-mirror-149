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

from collections import namedtuple


H5FileKeys = namedtuple(
    "H5FileKeys",
    [
        "acq_expo_time_keys",
        "rot_angle_keys",
        "valid_camera_names",
        "x_trans_keys",
        "y_trans_keys",
        "z_trans_keys",
        "y_rot_key",
        "x_pixel_size",
        "y_pixel_size",
        "diode_keys",
    ],
)


H5ScanTitles = namedtuple(
    "H5ScanTitles",
    [
        "init_titles",
        "init_zserie_titles",
        "init_pcotomo_titles",
        "dark_titles",
        "flat_titles",
        "proj_titles",
        "align_titles",
    ],
)
