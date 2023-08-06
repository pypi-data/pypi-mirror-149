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
module to convert from edf to (nexus tomo compliant) .nx
"""

__authors__ = [
    "H. Payno",
]
__license__ = "MIT"
__date__ = "27/11/2020"


from collections import namedtuple
from typing import Optional
from nxtomomill.io.config.edfconfig import TomoEDFConfig
from nxtomomill.nexus.nxsource import SourceType
from nxtomomill import utils
from nxtomomill.utils import ImageKey
from nxtomomill.converter.version import version as converter_version
from nxtomomill.nexus.utils import create_nx_data_group
from nxtomomill.nexus.utils import link_nxbeam_to_root
from nxtomomill.nexus.nxdetector import FieldOfView
from nxtomomill.settings import Tomo
from silx.utils.deprecation import deprecated
from tomoscan.esrf.utils import get_parameters_frm_par_or_info
from tomoscan.unitsystem.energysystem import EnergySI

try:
    from tomoscan.esrf.scan.edfscan import EDFTomoScan
except ImportError:
    from tomoscan.esrf.edfscan import EDFTomoScan
from tomoscan.unitsystem import metricsystem
from tomoscan.io import HDF5File
import fabio
import numpy
import os
import logging

EDF_MOTOR_POS = Tomo.EDF.MOTOR_POS
EDF_MOTOR_MNE = Tomo.EDF.MOTOR_MNE
EDF_REFS_NAMES = Tomo.EDF.REFS_NAMES
EDF_TO_IGNORE = Tomo.EDF.TO_IGNORE
EDF_ROT_ANGLE = Tomo.EDF.ROT_ANGLE
EDF_DARK_NAMES = Tomo.EDF.DARK_NAMES
EDF_X_TRANS = Tomo.EDF.X_TRANS
EDF_Y_TRANS = Tomo.EDF.Y_TRANS
EDF_Z_TRANS = Tomo.EDF.Z_TRANS

_logger = logging.getLogger(__name__)


EDFFileKeys = namedtuple(
    "EDFFileKeys",
    [
        "motor_pos_keys",
        "motor_mne_keys",
        "rot_angle_keys",
        "x_trans_keys",
        "y_trans_keys",
        "z_trans_keys",
        "to_ignore",
        "dark_names",
        "ref_names",
    ],
)

DEFAULT_EDF_KEYS = EDFFileKeys(
    EDF_MOTOR_POS,
    EDF_MOTOR_MNE,
    EDF_ROT_ANGLE,
    EDF_X_TRANS,
    EDF_Y_TRANS,
    EDF_Z_TRANS,
    EDF_TO_IGNORE,
    EDF_DARK_NAMES,
    EDF_REFS_NAMES,
)


@deprecated(replacement="from_edf_to_nx", since_version="0.9.0")
def edf_to_nx(
    scan: EDFTomoScan,
    output_file: str,
    file_extension: str,
    file_keys: EDFFileKeys = DEFAULT_EDF_KEYS,
    progress=None,
    sample_name: Optional[str] = None,
    title: Optional[str] = None,
    instrument_name: Optional[str] = None,
    source_name: Optional[str] = None,
    source_type: Optional[SourceType] = None,
) -> tuple:
    """
    Convert an edf file to a nexus file.
    For now duplicate data.

    :param scan:
    :param output_file:
    :param file_extension:
    :param file_keys:
    :param progress:
    :param Optional[str] sample_name: name of the sample
    :param Optional[str] title: dataset title
    :param Optional[str] instrument_name: name of the instrument used
    :param Optional[str] source_name: name of the source (most likely ESRF)
    :param Optional[str] source_type: type of the source (most likely "Synchrotron X-ray Source")
    :return: (nexus_file, entry)
    :rtype:tuple
    """
    if not isinstance(scan, EDFTomoScan):
        raise TypeError("scan is expected to be an instance of EDFTomoScan")

    config = TomoEDFConfig()
    config.input_folder = scan.path
    config.dataset_basename = scan.dataset_basename
    config.output_file = output_file
    config.file_extension = file_extension
    config.sample_name = sample_name
    config.title = title
    config.instrument_name = instrument_name
    config.source_name = source_name
    config.source_type = source_type
    # handle file_keys
    config.motor_position_keys = file_keys.motor_pos_keys
    config.motor_mne_keys = file_keys.motor_mne_keys
    config.rotation_angle_keys = file_keys.rot_angle_keys
    config.x_trans_keys = file_keys.x_trans_keys
    config.y_trans_keys = file_keys.y_trans_keys
    config.z_trans_keys = file_keys.z_trans_keys
    config.ignore_file_patterns = file_keys.to_ignore
    config.dark_names = file_keys.dark_names
    config.flat_names = file_keys.ref_names

    return from_edf_to_nx(config, progress=progress)


def from_edf_to_nx(configuration: TomoEDFConfig, progress=None) -> tuple:
    """
    Convert an edf file to a nexus file.
    For now duplicate data.

    :param TomoEDFConfig config: configuration to use to process the data
    :return: (nexus_file, entry)
    :rtype:tuple
    """
    if configuration.input_folder is None:
        raise ValueError("input_folder should be provided")
    if not os.path.isdir(configuration.input_folder):
        raise OSError(f"{configuration.input_folder} is not a valid folder path")

    if configuration.output_file is None:
        raise ValueError("output_file should be provided")

    if configuration.dataset_info_file is not None:
        if not os.path.isfile(configuration.dataset_info_file):
            raise ValueError(f"{configuration.dataset_info_file} is not a file")
        else:
            scan_info = get_parameters_frm_par_or_info(configuration.dataset_info_file)
    else:
        scan_info = None

    scan = EDFTomoScan(
        scan=configuration.input_folder,
        dataset_basename=configuration.dataset_basename,
        scan_info=scan_info,
        # TODO: add n frames ?
    )

    fileout_h5 = utils.get_file_name(
        file_name=configuration.output_file,
        extension=configuration.file_extension,
        check=True,
    )
    _logger.info(f"Output file will be {fileout_h5}")

    output_data_path = "entry"

    DARK_ACCUM_FACT = True
    with HDF5File(fileout_h5, "w") as h5d:
        metadata = []
        proj_urls = scan.get_proj_urls(
            scan=scan.path, dataset_basename=scan.dataset_basename
        )

        for dark_to_find in configuration.dark_names:
            dk_urls = scan.get_darks_url(scan_path=scan.path, prefix=dark_to_find)
            if len(dk_urls) > 0:
                if dark_to_find == "dark":
                    DARK_ACCUM_FACT = False
                break
        if configuration.ignore_file_patterns is None:
            _edf_to_ignore = list()
        else:
            _edf_to_ignore = list(configuration.ignore_file_patterns)

        for refs_to_find in configuration.flat_names:
            if refs_to_find == "ref":
                _edf_to_ignore.append("HST")
            else:
                _edf_to_ignore.remove("HST")

            refs_urls = scan.get_flats_url(
                scan_path=scan.path,
                prefix=refs_to_find,
                ignore=_edf_to_ignore,
                dataset_basename=scan.dataset_basename,
            )
            if len(refs_urls) > 0:
                break

        n_frames = len(proj_urls) + len(refs_urls) + len(dk_urls)

        def getExtraInfo(scan):
            assert isinstance(scan, EDFTomoScan)
            projections_urls = scan.projections
            if len(projections_urls) == 0:
                raise ValueError(
                    f"No projections found in {scan.path} with dataset basename: {configuration.dataset_basename if configuration.dataset_basename is not None else 'Default'} and dataset info file: {configuration.dataset_info_file if configuration.dataset_info_file is not None else 'Default'}. "
                )
            indexes = sorted(projections_urls.keys())
            first_proj_file = projections_urls[indexes[0]]
            fid = fabio.open(first_proj_file.file_path())

            rotangle_index = -1
            xtrans_index = -1
            ytrans_index = -1
            ztrans_index = -1
            frame_type = None

            try:
                if hasattr(fid, "header"):
                    hd = fid.header
                else:
                    hd = fid.getHeader()
                motor_mne_key = _get_valid_key(hd, configuration.motor_mne_keys)
                motors = hd.get(motor_mne_key, "").split(" ")

                rotangle_index = _get_valid_key_index(
                    motors, configuration.rotation_angle_keys
                )
                xtrans_index = _get_valid_key_index(motors, configuration.x_trans_keys)
                ytrans_index = _get_valid_key_index(motors, configuration.y_trans_keys)
                ztrans_index = _get_valid_key_index(motors, configuration.z_trans_keys)

                if hasattr(fid, "bytecode"):
                    frame_type = fid.bytecode
                else:
                    frame_type = fid.getByteCode()
            finally:
                fid.close()
                fid = None

            return frame_type, rotangle_index, xtrans_index, ytrans_index, ztrans_index

        (
            frame_type,
            rot_angle_index,
            x_trans_index,
            y_trans_index,
            z_trans_index,
        ) = getExtraInfo(scan=scan)

        if rot_angle_index == -1 and configuration.force_angle_calculation is False:
            _logger.warning(
                f"Unable to find one of the defined key for rotation in header ({configuration.rotation_angle_keys}). Will force angle calculation"
            )
            configuration.force_angle_calculation = True

        data_dataset = h5d.create_dataset(
            "/entry/instrument/detector/data",
            shape=(n_frames, scan.dim_2, scan.dim_1),
            dtype=frame_type,
        )

        keys_dataset = h5d.create_dataset(
            "/entry/instrument/detector/image_key", shape=(n_frames,), dtype=numpy.int32
        )

        keys_control_dataset = h5d.create_dataset(
            "/entry/instrument/detector/image_key_control",
            shape=(n_frames,),
            dtype=numpy.int32,
        )

        title = configuration.title
        if title is None:
            title = os.path.basename(scan.path)
        h5d["/entry/title"] = title

        sample_name = configuration.sample_name
        if configuration.sample_name is None:
            # try to deduce sample name from scan path.
            try:
                sample_name = os.path.abspath(scan.path).split(os.sep)[-3:]
                sample_name = os.sep.join(sample_name)
            except Exception:
                sample_name = "unknow"
        h5d["/entry/sample/name"] = sample_name
        if configuration.instrument_name is not None:
            instrument_grp = h5d["/entry"].require_group("instrument")
            instrument_grp["name"] = configuration.instrument_name

        if configuration.source_name is not None:
            source_grp = h5d["/entry/instrument"].require_group("source")
            source_grp["name"] = configuration.source_name
        if configuration.source_type is not None:
            source_grp = h5d["/entry/instrument"].require_group("source")
            source_grp["type"] = configuration.source_type.value

        if configuration.force_angle_calculation_endpoint:
            proj_angle = scan.scan_range / (scan.tomo_n - 1)
        else:
            proj_angle = scan.scan_range / scan.tomo_n

        distance = scan.retrieve_information(
            scan=os.path.abspath(scan.path),
            dataset_basename=scan.dataset_basename,
            ref_file=None,
            key="Distance",
            type_=float,
            key_aliases=["distance"],
            scan_info=scan.scan_info,
        )
        if distance is not None:
            h5d["/entry/instrument/detector/distance"] = (
                distance * configuration.distance_unit.value
            )
            h5d["/entry/instrument/detector/distance"].attrs["unit"] = "m"

        pixel_size = scan.retrieve_information(
            scan=os.path.abspath(scan.path),
            dataset_basename=scan.dataset_basename,
            ref_file=None,
            key="PixelSize",
            type_=float,
            key_aliases=["pixelSize"],
            scan_info=scan.scan_info,
        )
        h5d["/entry/instrument/detector/x_pixel_size"] = (
            pixel_size * configuration.pixel_size_unit.value
        )
        h5d["/entry/instrument/detector/x_pixel_size"].attrs["unit"] = "m"
        h5d["/entry/instrument/detector/y_pixel_size"] = (
            pixel_size * configuration.pixel_size_unit.value
        )
        h5d["/entry/instrument/detector/y_pixel_size"].attrs["unit"] = "m"

        energy = scan.retrieve_information(
            scan=os.path.abspath(scan.path),
            dataset_basename=scan.dataset_basename,
            ref_file=None,
            key="Energy",
            type_=float,
            key_aliases=["energy"],
            scan_info=scan.scan_info,
        )
        if energy is not None:
            if configuration.energy_unit != EnergySI.KILOELECTRONVOLT:
                energy = energy * configuration.energy_unit / EnergySI.KILOELECTRONVOLT
            h5d["/entry/instrument/beam/incident_energy"] = energy
            h5d["/entry/instrument/beam/incident_energy"].attrs["unit"] = "keV"

        # rotations values
        rotation_dataset = h5d.create_dataset(
            "/entry/sample/rotation_angle", shape=(n_frames,), dtype=numpy.float32
        )
        h5d["/entry/sample/rotation_angle"].attrs["unit"] = "degree"

        # provision for centering motors
        x_dataset = h5d.create_dataset(
            "/entry/sample/x_translation", shape=(n_frames,), dtype=numpy.float32
        )
        h5d["/entry/sample/x_translation"].attrs["unit"] = "m"
        y_dataset = h5d.create_dataset(
            "/entry/sample/y_translation", shape=(n_frames,), dtype=numpy.float32
        )
        h5d["/entry/sample/y_translation"].attrs["unit"] = "m"
        z_dataset = h5d.create_dataset(
            "/entry/sample/z_translation", shape=(n_frames,), dtype=numpy.float32
        )
        h5d["/entry/sample/z_translation"].attrs["unit"] = "m"

        #  --------->  and now fill all datasets!

        nf = 0

        def read_url(url) -> tuple:
            data_slice = url.data_slice()
            if data_slice is None:
                data_slice = (0,)
            if data_slice is None or len(data_slice) != 1:
                raise ValueError(
                    "Fabio slice expect a single frame, " "but %s found" % data_slice
                )
            index = data_slice[0]
            if not isinstance(index, int):
                raise ValueError(
                    "Fabio slice expect a single integer, " "but %s found" % data_slice
                )

            try:
                fabio_file = fabio.open(url.file_path())
            except Exception:
                _logger.debug(
                    "Error while opening %s with fabio", url.file_path(), exc_info=True
                )
                raise IOError(
                    "Error while opening %s with fabio (use debug"
                    " for more information)" % url.path()
                )

            try:
                if fabio_file.nframes == 1:
                    if index != 0:
                        raise ValueError(
                            "Only a single frame available. Slice %s out of range"
                            % index
                        )
                    data = fabio_file.data
                    header = fabio_file.header
                else:
                    data = fabio_file.getframe(index).data
                    header = fabio_file.getframe(index).header
            except Exception:
                data = None
                header = None
            finally:
                fabio_file.close()
                fabio_file = None
            return data, header

        if progress is not None:
            progress.set_name("write dark")
            progress.reset(len(dk_urls))

        def ignore(file_name):
            for forbid in _edf_to_ignore:
                if forbid in file_name:
                    return True
            return False

        # darks

        # dark in acumulation mode?
        norm_dark = 1.0
        if scan.dark_n > 0 and DARK_ACCUM_FACT is True:
            norm_dark = len(dk_urls) / scan.dark_n
        dk_indexes = sorted(dk_urls.keys())
        if progress is not None:
            progress.reset(len(dk_urls))

        for dk_index in dk_indexes:
            dk_url = dk_urls[dk_index]
            if ignore(os.path.basename(dk_url.file_path())):
                _logger.info("ignore " + dk_url.file_path())
                continue
            data, header = read_url(dk_url)
            metadata.append(header)

            data_dataset[nf, :, :] = data * norm_dark
            keys_dataset[nf] = ImageKey.DARK_FIELD.value
            keys_control_dataset[nf] = ImageKey.DARK_FIELD.value

            motor_pos_key = _get_valid_key(header, configuration.motor_position_keys)
            if motor_pos_key:
                str_mot_val = header[motor_pos_key].split(" ")
                if rot_angle_index == -1 or configuration.force_angle_calculation:
                    rotation_dataset[nf] = 0.0
                else:
                    rotation_dataset[nf] = float(str_mot_val[rot_angle_index])
                if x_trans_index == -1:
                    x_dataset[nf] = 0.0
                else:
                    x_dataset[nf] = (
                        float(str_mot_val[x_trans_index])
                        * metricsystem.millimeter.value
                    )
                if y_trans_index == -1:
                    y_dataset[nf] = 0.0
                else:
                    y_dataset[nf] = (
                        float(str_mot_val[y_trans_index])
                        * metricsystem.millimeter.value
                    )
                if z_trans_index == -1:
                    z_dataset[nf] = 0.0
                else:
                    z_dataset[nf] = (
                        float(str_mot_val[z_trans_index])
                        * metricsystem.millimeter.value
                    )

            nf += 1
            if progress is not None:
                progress.increase_advancement(i=1)

        ref_indexes = sorted(refs_urls.keys())

        ref_projs = []
        for irf in ref_indexes:
            pjnum = int(irf)
            if pjnum not in ref_projs:
                ref_projs.append(pjnum)

        # refs
        def store_refs(
            refIndexes,
            tomoN,
            projnum,
            refUrls,
            nF,
            dataDataset,
            keysDataset,
            keysCDataset,
            xDataset,
            yDataset,
            zDataset,
            rotationDataset,
            raix,
            xtix,
            ytix,
            ztix,
        ):
            nfr = nF
            for ref_index in refIndexes:
                int_rf = int(ref_index)
                test_val = 0
                if int_rf == projnum:
                    refUrl = refUrls[ref_index]
                    if ignore(os.path.basename(refUrl.file_path())):
                        _logger.info("ignore " + refUrl.file_path())
                        continue
                    data, header = read_url(refUrl)
                    metadata.append(header)

                    dataDataset[nfr, :, :] = data + test_val
                    keysDataset[nfr] = ImageKey.FLAT_FIELD.value
                    keysCDataset[nfr] = ImageKey.FLAT_FIELD.value
                    motor_pos_key = _get_valid_key(
                        header, configuration.motor_position_keys
                    )

                    if motor_pos_key in header:
                        str_mot_val = header[motor_pos_key].split(" ")
                        if raix == -1 or configuration.force_angle_calculation:
                            rotationDataset[nfr] = 0.0
                        else:
                            rotationDataset[nfr] = float(str_mot_val[raix])
                        if xtix == -1:
                            xDataset[nfr] = 0.0
                        else:
                            xDataset[nfr] = float(str_mot_val[xtix])
                        if ytix == -1:
                            yDataset[nfr] = 0.0
                        else:
                            yDataset[nfr] = float(str_mot_val[ytix])
                        if ztix == -1:
                            zDataset[nfr] = 0.0
                        else:
                            zDataset[nfr] = float(str_mot_val[ztix])

                    nfr += 1
            return nfr

        # projections
        proj_indexes = sorted(proj_urls.keys())
        if progress is not None:
            progress.set_name("write projections and flats")
            progress.reset(len(proj_indexes))
        nproj = 0
        iref_pj = 0

        alignment_indices = []
        for proj_index in proj_indexes:
            proj_url = proj_urls[proj_index]
            if ignore(os.path.basename(proj_url.file_path())):
                _logger.info("ignore " + proj_url.file_path())
                continue

            # store refs if the ref serial number is = projection number
            if iref_pj < len(ref_projs) and ref_projs[iref_pj] == nproj:
                nf = store_refs(
                    ref_indexes,
                    scan.tomo_n,
                    ref_projs[iref_pj],
                    refs_urls,
                    nf,
                    data_dataset,
                    keys_dataset,
                    keys_control_dataset,
                    x_dataset,
                    y_dataset,
                    z_dataset,
                    rotation_dataset,
                    rot_angle_index,
                    x_trans_index,
                    y_trans_index,
                    z_trans_index,
                )
                iref_pj += 1
            data, header = read_url(proj_url)
            metadata.append(header)

            data_dataset[nf, :, :] = data
            keys_dataset[nf] = ImageKey.PROJECTION.value
            keys_control_dataset[nf] = ImageKey.PROJECTION.value
            if nproj >= scan.tomo_n:
                keys_control_dataset[nf] = ImageKey.ALIGNMENT.value

            motor_pos_key = _get_valid_key(header, configuration.motor_position_keys)
            if motor_pos_key in header:
                str_mot_val = header[motor_pos_key].split(" ")

                # continuous scan - rot angle is unknown. Compute it
                if (
                    configuration.force_angle_calculation is True
                    and nproj < scan.tomo_n
                ):
                    angle = nproj * proj_angle
                    if (
                        scan.scan_range < 0
                        and configuration.angle_calculation_rev_neg_scan_range is False
                    ):
                        angle = scan.scan_range - angle

                    rotation_dataset[nf] = angle
                else:
                    if configuration.force_angle_calculation:
                        # FIXMe: for alignment projection when calculation is force the
                        # angle will always be set to 0.0 when it should be computed.
                        # it would be wiser to compute all the rotation angle at the
                        # end when each frame is tag.
                        rotation_dataset[nf] = 0.0
                        if configuration.force_angle_calculation:
                            alignment_indices.append(nf)
                    else:
                        rotation_dataset[nf] = float(str_mot_val[rot_angle_index])

                if x_trans_index == -1:
                    x_dataset[nf] = 0.0
                else:
                    x_dataset[nf] = float(str_mot_val[x_trans_index])
                if y_trans_index == -1:
                    y_dataset[nf] = 0.0
                else:
                    y_dataset[nf] = float(str_mot_val[y_trans_index])
                if z_trans_index == -1:
                    z_dataset[nf] = 0.0
                else:
                    z_dataset[nf] = float(str_mot_val[z_trans_index])

            nf += 1
            nproj += 1

            if progress is not None:
                progress.increase_advancement(i=1)

        # we need to update alignement angles values. I wanted to avoid to redo all the previous existing processing.
        n_alignment_angles = len(alignment_indices)
        if n_alignment_angles == 3:
            alignments_angles = numpy.linspace(
                scan.scan_range,
                0,
                n_alignment_angles,
                endpoint=(n_alignment_angles % 2) == 0,
            )
            for index, angle in zip(alignment_indices, alignments_angles):
                rotation_dataset[index] = angle

        # store last flat if any remaining in the list
        if iref_pj < len(ref_projs):
            nf = store_refs(
                ref_indexes,
                scan.tomo_n,
                ref_projs[iref_pj],
                refs_urls,
                nf,
                data_dataset,
                keys_dataset,
                keys_control_dataset,
                x_dataset,
                y_dataset,
                z_dataset,
                rotation_dataset,
                rot_angle_index,
                x_trans_index,
                y_trans_index,
                z_trans_index,
            )

        # we can add some more NeXus look and feel
        h5d["/entry"].attrs["NX_class"] = "NXentry"
        h5d["/entry"].attrs["definition"] = "NXtomo"
        h5d["/entry"].attrs["version"] = converter_version()
        h5d["/entry/instrument"].attrs["NX_class"] = "NXinstrument"
        h5d["/entry/instrument/detector"].attrs["NX_class"] = "NXdetector"
        h5d["/entry/instrument/detector/data"].attrs["interpretation"] = "image"
        if configuration.field_of_view is not None:
            field_of_view = configuration.field_of_view
        elif abs(scan.scan_range) == 180:
            field_of_view = "Half"
        elif abs(scan.scan_range) == 360:
            field_of_view = "Full"

        if field_of_view is not None:
            field_of_view = FieldOfView.from_value(field_of_view)
            h5d["/entry/instrument/detector/field_of_view"] = field_of_view.value

        h5d["/entry/sample"].attrs["NX_class"] = "NXsample"
        h5d["/entry/definition"] = "NXtomo"
        source_grp = h5d["/entry/instrument"].get("source", None)
        if source_grp is not None and "NX_class" not in source_grp.attrs:
            source_grp.attrs["NX_class"] = "NXsource"

        h5d.flush()

    for i_meta, meta in enumerate(metadata):
        # save metadata
        from silx.io.dictdump import dicttoh5

        dicttoh5(
            meta,
            fileout_h5,
            h5path=f"/entry/instrument/positioners/{i_meta}",
            update_mode="replace",
            mode="a",
        )

    try:
        create_nx_data_group(
            file_path=fileout_h5,
            entry_path=output_data_path,
            axis_scale=["linear", "linear"],
        )
    except Exception as e:
        _logger.error("Fail to create NXdata group. Reason is {}".format(str(e)))

    # create beam group at root for compatibility
    try:
        link_nxbeam_to_root(file_path=fileout_h5, entry_path=output_data_path)
    except Exception:
        pass

    return fileout_h5, output_data_path


def _get_valid_key(header: dict, keys: tuple) -> Optional[str]:
    """Return the first existing key in header"""
    for key in keys:
        if key in header:
            return key
    else:
        return None


def _get_valid_key_index(motors: list, keys: tuple) -> Optional[int]:
    for key in keys:
        if key in motors:
            return motors.index(key)
    else:
        return -1
