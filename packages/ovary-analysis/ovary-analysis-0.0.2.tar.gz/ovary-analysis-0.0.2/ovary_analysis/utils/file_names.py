import os
from typing import List, Optional, Tuple
import numpy as np
from skimage import io
import datetime
import warnings


def _validate_patient_id(patient_id: str) -> str:
    """check if patient id is in right format A{number} or B{number}

    Parameters
    ----------
    patient_id: str
        Patient ID

    Returns
    -------
    patient_id: str
        return a str if the format is right, None if the format wrong.
    """
    if (
        patient_id[0] == 'A'
        or patient_id[0] == 'B'
        and patient_id[1:].isdecimal()
    ):
        return patient_id
    else:
        warnings.warn("patient ID format error")
        return None


def _validate_cycle(cycle: str) -> str:
    """check if cycle is in right format z1 or z2

    Parameters
    ----------
    cycle: str
        z1 or z2

    Returns
    -------
    cycle: str
        return a str if the format is right, None if the format wrong.
    """
    if cycle == 'z1' or cycle == 'z2':
        return cycle
    else:
        warnings.warn("cycle format error")
        return None


def _validate_side(side: str) -> str:
    """check if side is in right format links or rechts

    Parameters
    ----------
    side: str
        links or rechts

    Returns
    -------
    side: str
        return a str if the format is right, None if the format wrong.
    """
    if side == 'rechts' or side == 'links':
        return side
    else:
        warnings.warn("side format error")
        return None


def _validate_date(date: str) -> datetime.date:
    """check if date is in right format YYMMDD and transform it in datatime

    Parameters
    ----------
    date: str
        YYMMDD

    Returns
    -------
    date: datetime.date
        return a datetime.date if the format is right, None if the format wrong.
    """
    try:
        date = datetime.datetime.strptime(date, "%y%m%d").date()
        return date
    except Exception as e:
        warnings.warn(str(e))
        return None


def parse_seg_fname(fname: str) -> Tuple[str, str, str, datetime.date]:
    """parse the segmentation of file name

    Parameters
    ----------
    fname: str
        file name in form of <patient_id> _ <cycle> _ <side> _ <date>_raw_follicles.h5

    Returns
    -------
    patientID: str
        ID of patient
    cycle: str
        z1 or z2 cycle
    side: str
        links or rechts (left or right) ovary
    date: datetime.date
        the date when the image is taken in form of YYMMDD
    """

    patient_id = _validate_patient_id(fname.split('_')[0])

    cycle = _validate_cycle(fname.split('_')[1].lower())

    side = _validate_side(fname.split('_')[2].lower())

    date = _validate_date(fname.split('_')[3].lower())

    return patient_id, cycle, side, date


def parse_slice_from_raw_fname(fname: str) -> int:
    f_base_name = os.path.basename(fname).lower()
    z_slice_with_ext = f_base_name.split('_z')[-1]
    z_slice = os.path.splitext(z_slice_with_ext)[0]

    return int(z_slice)


def parse_data_directory_name(path: str) -> Tuple[str, str, str]:
    assert os.path.isdir(path)

    norm_path = os.path.normpath(path)
    folders = norm_path.split(os.sep)

    date = folders[-1].replace('.', '')

    ovary_data = folders[-2].split(' ')
    cycle = ovary_data[0].lower()
    side = ovary_data[1].lower()

    return date, cycle, side


def is_cycle_folder(folder_path: str) -> bool:
    """Verify the directory is a valid cycle folder"""
    folder_name = os.path.basename(folder_path).lower()
    contains_cycle = ('z1' in folder_name) != ('z2' in folder_name)
    contains_side = ('links' in folder_name) != ('rechts' in folder_name)

    if contains_cycle and contains_side:
        return True
    else:
        return False


def parse_cycle_folder(folder_path: str) -> Tuple[str, str]:
    if is_cycle_folder(folder_path):
        folder_name = os.path.basename(folder_path).lower()

        if 'z1' in folder_name:
            cycle = 'z1'
        else:
            cycle = 'z2'
        if 'links' in folder_name:
            side = 'links'
        else:
            side = 'rechts'
    else:
        raise ValueError()

    return cycle, side


def parse_day_dirs(
    day_dirs: List[str],
) -> Tuple[List[datetime.date], List[str]]:
    date_list = []
    good_day_dirs = []
    bad_day_dirs = []
    for d in day_dirs:
        dir_name = os.path.basename(d)
        success, formatted_date = _parse_day(dir_name)
        if success is True:
            date_list.append(formatted_date)
            good_day_dirs.append(d)
        else:
            bad_day_dirs.append(d)
    return date_list, good_day_dirs, bad_day_dirs


def _parse_day(day_dir_name: str) -> Tuple[bool, Optional[datetime.date]]:
    try:
        name_parts = day_dir_name.split('.')
        day = int(name_parts[0])
        month = int(name_parts[1])
        year = 2000 + int(name_parts[2])
        formatted_date = datetime.date(day=day, month=month, year=year)
        success = True
    except (ValueError, TypeError):
        success = False
        formatted_date = None

    return success, formatted_date


def calculate_day_offsets(date_list: List[datetime.date]) -> List[int]:
    first_date = min(date_list)
    offset_list = [
        _calculate_day_offset(d, first_date=first_date) for d in date_list
    ]

    return offset_list


def _calculate_day_offset(
    date: datetime.date, first_date: datetime.date
) -> int:
    date_delta = date - first_date
    offset = date_delta.days
    return offset


def parse_z_slice(fname: str) -> int:
    try:
        f_base_name = os.path.basename(fname).lower()
        z_slice_with_ext = f_base_name.split('_z')[-1]
        z_slice = os.path.splitext(z_slice_with_ext)[0]
        slice_index = int(z_slice)
        success = True
    except (ValueError, IndexError):
        success = False
        slice_index = None

    return success, slice_index


def validate_z_slices(z_slices: List[int]) -> bool:
    sorted_slices = sorted(z_slices)
    z_diff = np.diff(sorted_slices)

    # the z slices should be contiguous and start at 0
    if len(sorted_slices) > 0:
        is_valid = np.all(z_diff == 1) and (sorted_slices[0] == 0)
    else:
        is_valid = False

    return is_valid


def parse_label_file_name(fname: str) -> datetime.date:
    f_base = os.path.basename(fname)
    date_parts = f_base.split(' ')[0].split('.')

    day = int(date_parts[0])
    month = int(date_parts[1])
    year = 2000 + int(date_parts[2])

    return datetime.date(day=day, month=month, year=year)


def validate_labels_file(im_path: str) -> Tuple[bool, int]:
    im = io.imread(im_path)
    im_shape = im.shape

    # there should be two labels channels
    valid_im = im_shape[1] == 2
    n_z = im_shape[0]

    return valid_im, n_z
