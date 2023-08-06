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
module to convert from (bliss) .h5 to (nexus tomo compliant) .nx
"""

__authors__ = [
    "H. Payno",
]
__license__ = "MIT"
__date__ = "27/11/2020"


from nxtomomill.converter.hdf5.acquisition.pcotomoacquisition import PCOTomoAcquisition
from nxtomomill.utils.hdf5 import EntryReader
from .acquisition.utils import get_entry_type
from nxtomomill.io.acquisitionstep import AcquisitionStep
from .acquisition.standardacquisition import StandardAcquisition
from .acquisition.zseriesacquisition import (
    ZSeriesBaseAcquisition,
    is_pcotomo_frm_titles,
)
from .acquisition.zseriesacquisition import is_z_series_frm_titles
from .acquisition.zseriesacquisition import is_z_series_frm_z_translation
from .acquisition.xrdctacquisition import XRDCTAcquisition
from .acquisition.xrd3dacquisition import XRD3DAcquisition
from nxtomomill.utils import Format
from silx.utils.deprecation import deprecated
from nxtomomill.io.config import TomoHDF5Config
from nxtomomill.io.framegroup import FrameGroup
from nxtomomill.converter.baseconverter import BaseConverter
from nxtomomill.converter.hdf5.acquisition.baseacquisition import _ask_for_file_removal
from silx.io.url import DataUrl
from tomoscan.io import HDF5File
from typing import Union
from typing import Iterable
import logging
from nxtomomill.plugins import (
    get_plugins_instances_frm_env_var,
    _NXTOMOMILL_PLUGINS_ENV_VAR,
)
import os
import h5py

try:
    import hdf5plugin  # noqa F401
except ImportError:
    pass
# import that should be removed when h5_to_nx will be removed
from nxtomomill.converter.hdf5.utils import H5FileKeys
from nxtomomill.converter.hdf5.utils import H5ScanTitles

from nxtomomill.settings import Tomo

H5_ROT_ANGLE_KEYS = Tomo.H5.ROT_ANGLE_KEYS
H5_VALID_CAMERA_NAMES = Tomo.H5.VALID_CAMERA_NAMES
H5_X_TRANS_KEYS = Tomo.H5.X_TRANS_KEYS
H5_Y_TRANS_KEYS = Tomo.H5.Y_TRANS_KEYS
H5_Z_TRANS_KEYS = Tomo.H5.Z_TRANS_KEYS
H5_ALIGNMENT_TITLES = Tomo.H5.ALIGNMENT_TITLES
H5_ACQ_EXPO_TIME_KEYS = Tomo.H5.ACQ_EXPO_TIME_KEYS
H5_X_PIXEL_SIZE = Tomo.H5.X_PIXEL_SIZE
H5_Y_PIXEL_SIZE = Tomo.H5.Y_PIXEL_SIZE
H5_DARK_TITLES = Tomo.H5.DARK_TITLES
H5_INIT_TITLES = Tomo.H5.INIT_TITLES
H5_PCOTOMO_INIT_TITLES = Tomo.H5.PCOTOMO_INIT_TITLES
H5_ZSERIE_INIT_TITLES = Tomo.H5.ZSERIE_INIT_TITLES
H5_PROJ_TITLES = Tomo.H5.PROJ_TITLES
H5_FLAT_TITLES = Tomo.H5.FLAT_TITLES
H5_REF_TITLES = H5_FLAT_TITLES
H5_Y_ROT_KEY = Tomo.H5.Y_ROT_KEY
H5_DIODE_KEYS = Tomo.H5.DIODE_KEYS

DEFAULT_SCAN_TITLES = H5ScanTitles(
    H5_INIT_TITLES,
    H5_ZSERIE_INIT_TITLES,
    H5_PCOTOMO_INIT_TITLES,
    H5_DARK_TITLES,
    H5_FLAT_TITLES,
    H5_PROJ_TITLES,
    H5_ALIGNMENT_TITLES,
)


DEFAULT_H5_KEYS = H5FileKeys(
    H5_ACQ_EXPO_TIME_KEYS,
    H5_ROT_ANGLE_KEYS,
    H5_VALID_CAMERA_NAMES,
    H5_X_TRANS_KEYS,
    H5_Y_TRANS_KEYS,
    H5_Z_TRANS_KEYS,
    H5_Y_ROT_KEY,
    H5_X_PIXEL_SIZE,
    H5_Y_PIXEL_SIZE,
    H5_DIODE_KEYS,
)


_logger = logging.getLogger(__name__)


class _H5ToNxConverter(BaseConverter):
    """
    Class used to convert a HDF5Config to one or several NXTomoEntry.

    :param configuration: configuration for the translation. such as the
                          input and output file, keys...
    :type configuration: TomoHDF5Config
    :param input_callback: possible callback in case of missing information
    :param progress: progress bar to be updated if provided
    :param detector_sel_callback: callback for the detector selection if any

    Conversion is a two step process:

    step 1: preprocessing
    * insure configuration is valid and that we don't have "unsafe" or
      "opposite" request / rules
    * normalize input URL (complete data_file if not provided)
    * copy some frame group if requested
    * create instances of BaseAcquisition classes that will be used to write
      NXTomo entries
    * handle z series specific case

    step 2: write NXTomo entries to the output file
    """

    def __init__(
        self,
        configuration: TomoHDF5Config,
        input_callback=None,
        progress=None,
        detector_sel_callback=None,
    ):
        if not isinstance(configuration, TomoHDF5Config):
            raise TypeError(
                "configuration should be an instance of HDFConfig"
                " not {}".format(type(configuration))
            )
        self._configuration = configuration
        self._progress = progress
        self._input_callback = input_callback
        self._detector_sel_callback = detector_sel_callback
        self._acquisitions = []
        self._plugins = []
        self._entries_created = []
        self.preprocess()

    @property
    def configuration(self):
        return self._configuration

    @property
    def progress(self):
        return self._progress

    @property
    def input_callback(self):
        return self._input_callback

    @property
    def detector_sel_callback(self):
        return self._detector_sel_callback

    @property
    def plugins(self) -> list:
        return self._plugins

    @plugins.setter
    def plugins(self, plugins: list):
        self._plugins = plugins

    @property
    def entries_created(self) -> tuple:
        """tuple of entries created. Each element is provided as
        (output_file, entry)"""
        return tuple(self._entries_created)

    @property
    def acquisitions(self):
        return self._acquisitions

    def preprocess(self):
        self._preprocess_urls()
        self._check_conversion_is_possible()
        if self.configuration.is_using_titles:
            self._convert_entries_and_sub_entries_to_urls()
            self.build_acquisition_classes_frm_titles()
        else:
            self.configuration.clear_entries_and_subentries()
            self.build_acquisition_classes_frm_urls()
        self._handle_zseries()

    def _handle_zseries(self):
        # for z series we have a "master" acquisition of type
        # ZSeriesBaseAcquisition. But this is used only to build
        # the acquisition sequence. To write we use the z series
        # "sub_acquisitions" which are instances of "StandardAcquisition"
        acquisitions = []
        for acquisition in self.acquisitions:
            if isinstance(acquisition, StandardAcquisition):
                acquisitions.append(acquisition)
            elif isinstance(acquisition, ZSeriesBaseAcquisition):
                acquisitions.extend(acquisition.get_standard_sub_acquisitions())
            else:
                raise TypeError(
                    "Acquisition type {} not handled".format(type(acquisition))
                )
        self._acquisitions = acquisitions

    def convert(self):
        self._entries_created = self.write()
        return self._entries_created

    def build_acquisition_classes_frm_urls(self):
        """
        Build acquisitions classes from the url definition

        :return:
        """
        self.configuration.check_tomo_n = False
        # when building from urls `tomo_n` has no meaning
        if self.configuration.is_using_titles:
            raise ValueError("Configuration specify that titles should be used")
        if self.configuration.format is None:
            _logger.warning("Format is not specify. Use default standard format")
            self.configuration.format = "standard"
        assert self.configuration.output_file is not None, "output_file requested"
        data_frame_grps = self.configuration.data_frame_grps
        # step 0: copy some urls instead if needed
        # update copy parameter
        for frame_grp in data_frame_grps:
            if frame_grp.copy is None:
                frame_grp.copy = self.configuration.default_copy_behavior

        # step 1: if there is no init FrameGroup create an empty one because
        # this is requested
        if len(data_frame_grps) == 0:
            return
        elif data_frame_grps[0].frame_type is not AcquisitionStep.INITIALIZATION:
            data_frame_grps = [
                FrameGroup(frame_type=AcquisitionStep.INITIALIZATION, url=None),
            ]
            data_frame_grps.extend(self.configuration.data_frame_grps)
            self.configuration.data_frame_grps = data_frame_grps

        # step 2: treat FrameGroups
        root_acquisition = None
        start_index = 0
        require_pcotomo_expected_nx_tomo = False
        for frame_grp in data_frame_grps:
            if frame_grp.frame_type is AcquisitionStep.INITIALIZATION:
                current_format = self.configuration.format
                if require_pcotomo_expected_nx_tomo is True:
                    _logger.warning(
                        f"Fail to retrieve expected number of nxtomo for {root_acquisition}"
                    )
                require_pcotomo_expected_nx_tomo = False
                if current_format is Format.STANDARD:
                    from nxtomomill.io.framegroup import filter_acqui_frame_type

                    acqui_projs_fg = filter_acqui_frame_type(
                        init=frame_grp,
                        sequences=self.configuration.data_frame_grps,
                        frame_type=AcquisitionStep.PROJECTION,
                    )
                    acqui_projs_urls = tuple(
                        [acqui_proj.url for acqui_proj in acqui_projs_fg]
                    )

                    if is_z_series_frm_z_translation(
                        acqui_projs_urls, self.configuration
                    ):
                        root_acquisition = ZSeriesBaseAcquisition(
                            root_url=frame_grp.url,
                            configuration=self.configuration,
                            detector_sel_callback=self.detector_sel_callback,
                            start_index=start_index,
                        )
                    elif is_pcotomo_frm_titles(acqui_projs_urls, self.configuration):
                        root_acquisition = PCOTomoAcquisition(
                            root_url=frame_grp.url,
                            configuration=self.configuration,
                            detector_sel_callback=self.detector_sel_callback,
                            start_index=start_index,
                        )
                        start_index += 0
                        # this will be defined with the projections
                        self._require_pcotomo_expected_nx_tomo = True

                    else:
                        root_acquisition = StandardAcquisition(
                            root_url=frame_grp.url,
                            configuration=self.configuration,
                            detector_sel_callback=self.detector_sel_callback,
                            start_index=start_index,
                        )
                        start_index += root_acquisition.get_expected_nx_tomo()
                elif current_format is Format.XRD_CT:
                    root_acquisition = XRDCTAcquisition(
                        root_url=frame_grp.url,
                        configuration=self.configuration,
                        detector_sel_callback=self.detector_sel_callback,
                        copy_frames=frame_grp.copy,
                        start_index=start_index,
                    )
                    start_index += root_acquisition.get_expected_nx_tomo()
                elif current_format is Format.XRD_3D:
                    root_acquisition = XRD3DAcquisition(
                        root_url=frame_grp.url,
                        configuration=self.configuration,
                        detector_sel_callback=self.detector_sel_callback,
                        start_index=start_index,
                    )
                    start_index += root_acquisition.get_expected_nx_tomo()
                else:
                    raise ValueError("Format {} is not handled".format(current_format))
                self.acquisitions.append(root_acquisition)
            else:
                assert (
                    root_acquisition is not None
                ), "processing error. No active root acquisition"
                root_acquisition.register_step(
                    url=frame_grp.url,
                    entry_type=frame_grp.frame_type,
                    copy_frames=frame_grp.copy,
                )

                # in case of z we append an index according to if
                # is already registered or not
                if isinstance(root_acquisition, ZSeriesBaseAcquisition):
                    with EntryReader(frame_grp.url) as entry:
                        z = root_acquisition.get_z(entry)
                        if z not in self._acquisitions:
                            start_index += 1

                if require_pcotomo_expected_nx_tomo:
                    if frame_grp.frame_type is AcquisitionStep.PROJECTION:
                        nb_loop = root_acquisition.get_nb_loop(frame_grp.url)
                        nb_tomo = root_acquisition.get_nb_tomo(frame_grp.url)
                        if nb_loop is not None and nb_tomo is not None:
                            start_index += int(nb_loop) * int(nb_tomo)
                            require_pcotomo_expected_nx_tomo = False

    def build_acquisition_classes_frm_titles(self):
        """
        Build Acquisition classes that will be used for conversion.
        Usually one Acquisition class will be instantiated per node (h5Group)
        to convert.
        """
        # insert missing z entry title in the common entry title
        scan_init_titles = list(self.configuration.init_titles)
        for title in self.configuration.zserie_init_titles:
            if title not in scan_init_titles:
                scan_init_titles.append(title)
        try:
            self.plugins = get_plugins_instances_frm_env_var()
        except Exception as e:
            _logger.info("no plugins loaded. Reason is: `{}`".format(e))
            self.plugins = []
        else:
            _logger.info(
                "Plugin loaded from {}"
                "".format(os.environ[_NXTOMOMILL_PLUGINS_ENV_VAR])
            )

        with HDF5File(self.configuration.input_file, "r") as h5d:

            def sort_fct(node):
                node_to_treat = h5d.get(node, getlink=True)
                if isinstance(node_to_treat, (h5py.ExternalLink, h5py.SoftLink)):
                    return float(node_to_treat.path.split("/")[-1])
                return float(node)

            groups = list(h5d.keys())
            groups.sort(key=sort_fct)
            # step 1: pre processing: group scan together
            if self.progress is not None:
                self.progress.set_name("parse sequences")
                self.progress.set_max_advancement(len(h5d.keys()))
            acquisitions = []
            # TODO: acquisition should refer to an url
            # list of acquisitions. Once process each of those acquisition will
            # create one 'scan'
            current_acquisition = None
            start_index = 0
            require_pcotomo_expected_nx_tomo = False
            for group_name in groups:
                _logger.debug("parse {}".format(group_name))
                entry = h5d[group_name]
                # improve handling of External (this is the case of proposal files)
                if isinstance(h5d.get(group_name, getlink=True), h5py.ExternalLink):
                    external_link = h5d.get(group_name, getlink=True)
                    file_path = external_link.filename
                    data_path = external_link.path
                else:
                    file_path = self.configuration.input_file
                    data_path = entry.name

                url = DataUrl(
                    file_path=file_path,
                    data_path=data_path,
                    scheme="silx",
                    data_slice=None,
                )

                # if necessary try to guess the type
                if self.configuration.format is None:
                    self.configuration.format = "standard"

                entry_type = get_entry_type(url=url, configuration=self.configuration)
                if entry_type is AcquisitionStep.INITIALIZATION:
                    if require_pcotomo_expected_nx_tomo is True:
                        _logger.warning(
                            f"Fail to retrieve expected number of nxtomo for {current_acquisition}"
                        )

                # Handle XRD-CT dataset
                if self.configuration.is_xrdc_ct:
                    if entry_type is AcquisitionStep.INITIALIZATION:
                        current_acquisition = None
                        _logger.warning(
                            "Found several acquisition type "
                            "in the same file. Stop conversion at"
                            " {}".format(url)
                        )
                        break
                    elif (
                        not self._ignore_entry_frm_titles(group_name)
                        and current_acquisition is None
                    ) or (
                        current_acquisition is not None
                        and current_acquisition.is_different_sequence(url)
                    ):
                        current_acquisition = XRDCTAcquisition(
                            root_url=url,
                            configuration=self.configuration,
                            detector_sel_callback=self.detector_sel_callback,
                            start_index=start_index,
                        )
                        start_index += current_acquisition.get_expected_nx_tomo()
                        acquisitions.append(current_acquisition)

                    elif self._ignore_entry_frm_titles(group_name):
                        current_acquisition = None
                    elif not self._ignore_sub_entry(url):
                        current_acquisition.register_step(
                            url=url,
                            entry_type=AcquisitionStep.PROJECTION,
                            copy_frames=self.configuration.default_copy_behavior,
                        )
                    else:
                        _logger.warning("ignore entry {}".format(entry))
                        # Handle 3D - XRD dataset
                elif self.configuration.is_3d_xrd:
                    if entry_type is AcquisitionStep.INITIALIZATION:
                        current_acquisition = None
                        _logger.warning(
                            "Found several acquisition type "
                            "in the same file. Stop conversion at"
                            " {}".format(url)
                        )
                        break
                    elif (
                        not self._ignore_entry_frm_titles(group_name)
                        and current_acquisition is None
                    ):
                        current_acquisition = XRD3DAcquisition(
                            root_url=url,
                            configuration=self.configuration,
                            detector_sel_callback=self.detector_sel_callback,
                            start_index=start_index,
                        )
                        start_index += current_acquisition.get_expected_nx_tomo()
                        acquisitions.append(current_acquisition)
                        current_acquisition.register_step(
                            url=url,
                            entry_type=AcquisitionStep.PROJECTION,
                            copy_frames=self.configuration.default_copy_behavior,
                        )
                    elif self._ignore_entry_frm_titles(group_name):
                        current_acquisition = None
                    elif not self._ignore_sub_entry(url):
                        current_acquisition.register_step(
                            url=url,
                            entry_type=AcquisitionStep.PROJECTION,
                            copy_frames=self.configuration.default_copy_behavior,
                        )
                    else:
                        _logger.warning("ignore entry {}".format(entry))
                # Handle "standard" tomo dataset
                elif entry_type is AcquisitionStep.INITIALIZATION:
                    try:
                        if is_z_series_frm_titles(
                            entry=entry, configuration=self.configuration
                        ):
                            current_acquisition = ZSeriesBaseAcquisition(
                                root_url=url,
                                configuration=self.configuration,
                                detector_sel_callback=self.detector_sel_callback,
                                start_index=start_index,
                            )
                            start_index += current_acquisition.get_expected_nx_tomo()
                        elif is_pcotomo_frm_titles(
                            entry=entry, configuration=self.configuration
                        ):
                            current_acquisition = PCOTomoAcquisition(
                                root_url=url,
                                configuration=self.configuration,
                                detector_sel_callback=self.detector_sel_callback,
                                start_index=start_index,
                            )
                            start_index += 0
                            # this will be defined with the projections
                            self._require_pcotomo_expected_nx_tomo = True
                        else:
                            current_acquisition = StandardAcquisition(
                                root_url=url,
                                configuration=self.configuration,
                                detector_sel_callback=self.detector_sel_callback,
                                start_index=start_index,
                            )
                            start_index += current_acquisition.get_expected_nx_tomo()
                    except Exception as e:
                        if self._ignore_entry_frm_titles(group_name):
                            continue
                        else:
                            raise e
                    if self._ignore_entry_frm_titles(group_name):
                        current_acquisition = None
                        continue

                    acquisitions.append(current_acquisition)
                # continue "standard" tomo dataset handling
                elif current_acquisition is not None and not self._ignore_sub_entry(
                    url
                ):
                    current_acquisition.register_step(
                        url=url,
                        entry_type=entry_type,
                        copy_frames=self.configuration.default_copy_behavior,
                    )
                    # in case of z we append an index according to if
                    # is already registered or not
                    if isinstance(current_acquisition, ZSeriesBaseAcquisition):
                        with EntryReader(url) as entry:
                            z = current_acquisition.get_z(entry)
                            if z not in self._acquisitions:
                                start_index += start_index

                    if require_pcotomo_expected_nx_tomo:
                        if entry_type is AcquisitionStep.PROJECTION:
                            nb_loop = current_acquisition.get_nb_loop(url)
                            nb_tomo = current_acquisition.get_nb_tomo(url)
                            if nb_loop is not None and nb_tomo is not None:
                                start_index += int(nb_loop) * int(nb_tomo)
                                require_pcotomo_expected_nx_tomo = False

                else:
                    _logger.info("ignore entry {}".format(entry))
                if self.progress is not None:
                    self.progress.increase_advancement()

            self._acquisitions = acquisitions

    def _ignore_entry_frm_titles(self, group_name):
        if self.configuration.entries is None:
            return False
        else:
            if not group_name.startswith("/"):
                group_name = "/" + group_name
            for entry in self.configuration.entries:
                if group_name == entry.data_path():
                    return False
            return True

    def _ignore_sub_entry(self, sub_entry_url: Union[None, DataUrl]):
        """
        :return: True if the provided sub_entry should be ignored
        """
        if sub_entry_url is None:
            return False
        if not isinstance(sub_entry_url, DataUrl):
            raise TypeError(
                "sub_entry_url is expected to be a DataUrl not "
                "{}".format(type(sub_entry_url))
            )
        if self.configuration.sub_entries_to_ignore is None:
            return False

        sub_entry_fp = sub_entry_url.file_path()
        sub_entry_dp = sub_entry_url.data_path()
        for entry in self.configuration.sub_entries_to_ignore:
            assert isinstance(entry, DataUrl)
            if entry.file_path() == sub_entry_fp and entry.data_path() == sub_entry_dp:
                return True
        return False

    def write(self):
        res = []

        acq_str = [str(acq) for acq in self.acquisitions]
        acq_str.insert(
            0, f"parsing finished. {len(self.acquisitions)} acquisitions found"
        )
        _logger.debug("\n   - ".join(acq_str))
        if len(self.acquisitions) == 0:
            _logger.warning(
                "No valid acquisitions have been found. Maybe no "
                "init (zserie) titles have been found. You can "
                "provide more."
            )

        if self.progress is not None:
            self.progress.set_name("write sequences")
            self.progress.set_max_advancement(len(self.acquisitions))

        # write nx_tomo per acquisition
        divide_into_sub_files = self.configuration.bam_single_file or not (
            self.configuration.single_file is False and len(self.acquisitions) == 1
        )

        for acquisition in self.acquisitions:
            if self._ignore_sub_entry(acquisition.root_url):
                continue

            try:
                new_entries = acquisition.write_as_nxtomo(
                    shift_entry=acquisition.start_index,
                    input_file_path=self.configuration.input_file,
                    request_input=self.configuration.request_input,
                    input_callback=self.input_callback,
                    plugins=self.plugins,
                    divide_into_sub_files=divide_into_sub_files,
                )
            except Exception as e:
                if self.configuration.raises_error:
                    raise e
                else:
                    _logger.error(
                        "Fails to write %s. Error is %s"
                        % (str(acquisition.root_url), str(e))
                    )
            else:
                res.extend(new_entries)
            if self.progress is not None:
                self.progress.increase_advancement()

        # if we created one file per entry then create a master file with link to those entries
        if self.configuration.single_file is False and divide_into_sub_files:
            _logger.info("create link in %s" % self.configuration.output_file)
            for (en_output_file, entry) in res:
                with HDF5File(self.configuration.output_file, "a") as master_file:
                    link_file = os.path.relpath(
                        en_output_file,
                        os.path.dirname(self.configuration.output_file),
                    )
                    master_file[entry] = h5py.ExternalLink(link_file, entry)

        return tuple(res)

    def _check_conversion_is_possible(self):
        """Insure minimalistic information are provided"""
        if self.configuration.is_using_titles:
            if not os.path.isfile(self.configuration.input_file):
                raise ValueError(
                    "Given input file does not exists: {}"
                    "".format(self.configuration.input_file)
                )
            if not h5py.is_hdf5(self.configuration.input_file):
                raise ValueError("Given input file is not an hdf5 file")

        if self.configuration.input_file == self.configuration.output_file:
            raise ValueError("input and output file are the same")

        output_file = self.configuration.output_file
        dir_name = os.path.dirname(os.path.abspath(output_file))
        if not os.path.exists(dir_name):
            os.makedirs(os.path.dirname(os.path.abspath(output_file)))
        elif os.path.exists(output_file):
            if self.configuration.overwrite is True:
                _logger.warning("{} will be removed".format(output_file))
                _logger.info("remove {}".format(output_file))
                os.remove(output_file)
            elif not _ask_for_file_removal(output_file):
                _logger.info("unable to overwrite {}, exit".format(output_file))
                exit(0)
            else:
                os.remove(output_file)
        if not os.access(dir_name, os.W_OK):
            _logger.error("You don't have rights to write on {}" "".format(dir_name))
            exit(0)

    def _convert_entries_and_sub_entries_to_urls(self):
        if self.configuration.entries is not None:
            urls = self.configuration.entries
            entries = self._upgrade_urls(
                urls=urls, input_file=self.configuration.input_file
            )
            self.configuration.entries = entries
        if self.configuration.sub_entries_to_ignore is not None:
            urls = self.configuration.sub_entries_to_ignore
            entries = self._upgrade_urls(
                urls=urls, input_file=self.configuration.input_file
            )
            self.configuration.sub_entries_to_ignore = entries

    def _preprocess_urls(self):
        """
        Update darks, flats, projections and alignments urls if
        no file path is provided
        """
        self.configuration.data_frame_grps = self._upgrade_frame_grp_urls(
            frame_grps=self.configuration.data_frame_grps,
            input_file=self.configuration.input_file,
        )

    @staticmethod
    def _upgarde_url(url: DataUrl, input_file: str) -> DataUrl:
        if url is not None and url.file_path() in (None, ""):
            if input_file in (None, str):
                raise ValueError(
                    "file_path for url {} is not "
                    "provided and no input_file provided "
                    "either."
                )
            else:
                return DataUrl(
                    file_path=input_file,
                    scheme="silx",
                    data_slice=url.data_slice(),
                    data_path=url.data_path(),
                )
        else:
            return url

    @staticmethod
    def _upgrade_frame_grp_urls(
        frame_grps: tuple, input_file: Union[None, str]
    ) -> tuple:
        """
        Upgrade all Frame Group DataUrl which did not contain a file_path to
         reference the input_file
        """
        if input_file is not None and not h5py.is_hdf5(input_file):
            raise ValueError("{} is not a h5py file".format(input_file))
        for frame_grp in frame_grps:
            frame_grp.url = _H5ToNxConverter._upgarde_url(frame_grp.url, input_file)
        return frame_grps

    @staticmethod
    def _upgrade_urls(urls: tuple, input_file: Union[None, str]) -> tuple:
        """
        Upgrade all DataUrl which did not contain a file_path to reference
        the input_file
        """
        if input_file is not None and not h5py.is_hdf5(input_file):
            raise ValueError("{} is not a h5py file".format(input_file))
        return tuple([_H5ToNxConverter._upgarde_url(url, input_file) for url in urls])


@deprecated(replacement="from_h5_to_nx", since_version="0.5.0")
def h5_to_nx(
    input_file_path: str,
    output_file: str,
    single_file: bool,
    file_extension: Union[str, None],
    ask_before_overwrite: bool = True,
    request_input: bool = False,
    entries: Union[Iterable, None] = None,
    ignore_sub_entries: Union[Iterable, None] = None,
    input_callback=None,
    file_keys=DEFAULT_H5_KEYS,
    scan_titles=DEFAULT_SCAN_TITLES,
    param_already_defined: Union[dict, None] = None,
    is_xrdc_ct: Union[bool, None] = None,
    progress=None,
    raise_error_if_issue=False,
    detector_sel_callback=None,
):
    configuration = TomoHDF5Config()
    configuration.input_file = input_file_path
    configuration.output_file = output_file
    configuration.single_file = single_file
    configuration.file_extension = file_extension
    configuration.overwrite = ask_before_overwrite
    configuration.request_input = request_input
    configuration.entries = entries
    configuration.raises_error = raise_error_if_issue
    configuration.sub_entries_to_ignore = ignore_sub_entries
    if param_already_defined is not None:
        configuration.param_already_defined = param_already_defined
    if is_xrdc_ct is True:
        configuration.format = "xrd-ct"
    elif is_xrdc_ct is False:
        configuration.format = "standard"
    # handle file keys
    configuration.x_trans_keys = file_keys.x_trans_keys
    configuration.y_trans_keys = file_keys.y_trans_keys
    configuration.z_trans_keys = file_keys.z_trans_keys
    configuration.exposition_time_keys = file_keys.acq_expo_time_keys
    configuration.rotation_angle_keys = file_keys.rot_angle_keys
    configuration.valid_camera_names = file_keys.valid_camera_names
    configuration.y_rot_key = file_keys.y_rot_key
    configuration.x_pixel_size_paths = file_keys.x_pixel_size
    configuration.y_pixel_size_paths = file_keys.y_pixel_size
    configuration.diode_keys = file_keys.diode_keys
    # handle titles keys
    configuration.init_titles = scan_titles.init_titles
    configuration.zserie_init_titles = scan_titles.init_zserie_titles
    configuration.pcotomo_init_titles = scan_titles.init_pcotomo_titles
    configuration.dark_titles = scan_titles.dark_titles
    configuration.flat_titles = scan_titles.flat_titles
    configuration.projections_titles = scan_titles.proj_titles
    configuration.alignment_titles = scan_titles.align_titles

    return from_h5_to_nx(
        configuration=configuration,
        input_callback=input_callback,
        progress=progress,
        detector_sel_callback=detector_sel_callback,
    )


def from_h5_to_nx(
    configuration: TomoHDF5Config,
    input_callback=None,
    progress=None,
    detector_sel_callback=None,
):
    """

    :param configuration: configuration for the translation. such as the
                          input and output file, keys...
    :param input_callback: possible callback in case of missing information
    :param progress: progress bar to be updated if provided
    :param detector_sel_callback: callback for the detector selection if any
    """
    converter = _H5ToNxConverter(
        configuration=configuration,
        input_callback=input_callback,
        progress=progress,
        detector_sel_callback=detector_sel_callback,
    )
    return converter.convert()


def get_bliss_tomo_entries(input_file_path: str, configuration: TomoHDF5Config):
    """Util function.
    Return the set of entries at root that match bliss entries.
    Used by tomwer for example.
    Warning: entries can be external links (in the case of the file beeing a proposal file)
    """
    if not isinstance(configuration, TomoHDF5Config):
        raise TypeError("configuration is expected to be a HDF5Config")

    with HDF5File(input_file_path, "r") as h5d:
        acquisitions = []

        for group_name in h5d.keys():
            _logger.debug("parse %s" % group_name)
            entry = h5d[group_name]
            # improve handling of External (this is the case of proposal files)
            if isinstance(h5d.get(group_name, getlink=True), h5py.ExternalLink):
                external_link = h5d.get(group_name, getlink=True)
                file_path = external_link.filename
                data_path = external_link.path
            else:
                file_path = input_file_path
                data_path = entry.name
                if not data_path.startswith("/"):
                    data_path = "/" + data_path
            url = DataUrl(file_path=file_path, data_path=data_path)
            if configuration.is_using_titles:
                # if use title take the ones corresponding to init
                entry_type = get_entry_type(url=url, configuration=configuration)
                if entry_type is AcquisitionStep.INITIALIZATION:
                    acquisitions.append(group_name)
            else:
                # check if the entry fit one of the data_frame_grps
                # with an init status
                possible_url_file_path = [
                    os.path.realpath(url.file_path()),
                    url.file_path(),
                ]
                if configuration.output_file not in ("", None):
                    possible_url_file_path.append(
                        os.path.relpath(
                            url.file_path(), os.path.dirname(configuration.output_file)
                        )
                    )
                for frame_grp in configuration.data_frame_grps:
                    if frame_grp.frame_type is AcquisitionStep.INITIALIZATION:
                        if (
                            frame_grp.url.file_path() in possible_url_file_path
                            and frame_grp.data_path() == url.data_path()
                        ):
                            acquisitions.append(entry.name)

        return acquisitions
