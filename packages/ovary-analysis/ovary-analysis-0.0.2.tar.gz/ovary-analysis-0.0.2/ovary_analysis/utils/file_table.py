import glob
import os
from typing import Tuple
from tqdm import tqdm

import pandas as pd

from ..io.raw_im import parse_tiff_metadata
from .file_names import (
    calculate_day_offsets,
    is_cycle_folder,
    parse_cycle_folder,
    parse_day_dirs,
    parse_label_file_name,
    parse_z_slice,
    validate_labels_file,
    validate_z_slices,
)


def create_raw_file_table(
    root_dir: str, make_file_table: bool = True
) -> Tuple[
    pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame
]:
    patient_folders = [f.path for f in os.scandir(root_dir) if f.is_dir()]

    day_table_data = []
    file_table_data = []
    bad_cycle_folders = []
    bad_day_folders = []
    bad_z_slices = []

    for patient in tqdm(patient_folders):
        cycle_folders = [
            f.path
            for f in os.scandir(patient)
            if (f.is_dir() and is_cycle_folder(f.path))
        ]
        patient_id = os.path.basename(patient)

        for cycle in tqdm(cycle_folders, leave=False):
            if is_cycle_folder(cycle):
                day_dirs = [f.path for f in os.scandir(cycle) if f.is_dir()]
                cycle_idx, side = parse_cycle_folder(cycle)

                dates, good_day_dirs, bad_day_dirs = parse_day_dirs(day_dirs)
                date_offsets = calculate_day_offsets(dates)

                # save the paths for the day folders that couldn't be parsed
                for bad_date in bad_day_dirs:
                    bad_day_folders.append(
                        {
                            'patient': patient_id,
                            'cycle': cycle_idx,
                            'side': side,
                            'folder_path': bad_date,
                        }
                    )

                for day_path, day_abs, day_rel in tqdm(
                    zip(good_day_dirs, dates, date_offsets), leave=False
                ):
                    image_file_pattern = os.path.join(day_path, '*.tif*')
                    image_files = glob.glob(image_file_pattern)

                    z_slices = []
                    metadata_parsed = False
                    for idx, im_slice in enumerate(image_files):
                        success, z_idx = parse_z_slice(im_slice)
                        if success is True:
                            z_slices.append(z_idx)

                            if metadata_parsed is False:
                                (
                                    px_size_x,
                                    px_size_y,
                                    px_size_z,
                                    n_z,
                                ) = parse_tiff_metadata(im_slice)
                                metadata_parsed = True
                        else:
                            bad_z_slices.append(
                                {
                                    'patient': patient_id,
                                    'cycle': cycle_idx,
                                    'side': side,
                                    'day': day_abs,
                                    'day_rel': day_rel,
                                    'path': day_path,
                                    'file_path': im_slice,
                                }
                            )

                    im_files_valid = validate_z_slices(z_slices)

                    if metadata_parsed is False:
                        px_size_x = 0
                        px_size_y = 0
                        px_size_z = 0
                        n_z = 0

                    day_table_data.append(
                        {
                            'patient': patient_id,
                            'cycle': cycle_idx,
                            'side': side,
                            'day': day_abs,
                            'day_rel': day_rel,
                            'path': day_path,
                            'px_size_x': px_size_x,
                            'px_size_y': px_size_y,
                            'px_size_z': px_size_z,
                            'n_z': n_z,
                            'n_z_files': len(z_slices),
                            'z_slices_valid': im_files_valid,
                        }
                    )

                    if make_file_table:
                        for z, im in zip(z_slices, image_files):
                            file_table_data.append(
                                {
                                    'patient': patient_id,
                                    'cycle': cycle_idx,
                                    'side': side,
                                    'day': day_abs,
                                    'day_rel': day_rel,
                                    'z': z,
                                    'dir_path': day_path,
                                    'im_path': im,
                                }
                            )
            else:
                bad_cycle_folders.append(
                    {'patient': patient_id, 'folder_path': cycle}
                )
    day_table = pd.DataFrame.from_records(day_table_data)
    bad_cycle_table = pd.DataFrame.from_records(bad_cycle_folders)
    bad_day_table = pd.DataFrame.from_records(bad_day_folders)
    bad_z_table = pd.DataFrame.from_records(bad_z_slices)
    if make_file_table:
        file_table = pd.DataFrame.from_records(file_table_data)
    else:
        file_table = None

    return day_table, file_table, bad_cycle_table, bad_day_table, bad_z_table


def create_labels_file_table(root_dir: str) -> pd.DataFrame:
    patient_folders = [f.path for f in os.scandir(root_dir) if f.is_dir()]
    day_table_data = []

    for patient in patient_folders:
        cycle_folders = [
            f.path
            for f in os.scandir(patient)
            if (f.is_dir() and is_cycle_folder(f.path))
        ]
        patient_id = os.path.basename(patient)

        for cycle in cycle_folders:
            cycle_idx, side = parse_cycle_folder(cycle)

            image_file_pattern = os.path.join(cycle, '*.tif*')
            image_files = glob.glob(image_file_pattern)

            for im in image_files:
                day_abs = parse_label_file_name(im)
                file_valid, n_z = validate_labels_file(im)

                day_table_data.append(
                    {
                        'patient': patient_id,
                        'cycle': cycle_idx,
                        'side': side,
                        'day': day_abs,
                        'path': os.path.abspath(im),
                        'n_z': n_z,
                        'file_valid': file_valid,
                    }
                )
    day_table = pd.DataFrame.from_records(day_table_data)
    return day_table
