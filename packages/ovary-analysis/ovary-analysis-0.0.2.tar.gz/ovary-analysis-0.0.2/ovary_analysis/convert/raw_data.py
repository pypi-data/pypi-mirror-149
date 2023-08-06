import glob
import os
from typing import Tuple, Union

import pandas as pd
from skimage.util import img_as_ubyte
from tqdm.auto import tqdm

from ..io.hdf5_io import write_raw
from ..io.raw_im import load_raw_im
from ..utils.file_names import parse_z_slice
from ..utils.image import rescale_raw_im
from ..utils.time import date_to_datestring


def convert_raw_dataset(
    row: pd.Series,
    output_dir: str,
    target_px_size: Tuple[float, float, float],
    im_path_key: str = 'path_im',
    n_z_key: str = 'n_z_im',
) -> dict:
    patient_id = row['patient']
    cycle_id = row['cycle']
    side = row['side']
    day = row['day']
    raw_data_path = row[im_path_key]
    n_z = row[n_z_key]
    im_px_size = (row['px_size_z'], row['px_size_x'], row['px_size_y'])

    image_file_pattern = os.path.join(raw_data_path, '*.tif*')
    image_files = glob.glob(image_file_pattern)

    z_slices = []
    good_im_paths = []
    for im_slice in image_files:
        success, z_idx = parse_z_slice(im_slice)
        if success is True:
            z_slices.append(z_idx)
            good_im_paths.append(im_slice)
    assert len(z_slices) == n_z
    image_files_sorted = [f for _, f in sorted(zip(z_slices, good_im_paths))]
    raw_im = load_raw_im(image_files_sorted)

    # rescale image
    rescaled_im = img_as_ubyte(
        rescale_raw_im(raw_im, im_px_size, target_px_size)
    )

    date_string = date_to_datestring(day)
    filename_base = f'{patient_id}_{cycle_id}_{side}_{date_string}_raw.h5'
    file_path = os.path.join(output_dir, filename_base)

    write_raw(
        raw_im=raw_im,
        raw_px_size=im_px_size,
        raw_path=raw_data_path,
        rescaled_im=rescaled_im,
        rescaled_px_size=target_px_size,
        fname=file_path,
        raw_name='raw',
        rescaled_name='raw_rescaled',
        compression='gzip',
    )

    success = True

    result = {
        'patient': patient_id,
        'cycle': cycle_id,
        'side': side,
        'day': day,
        'path': raw_data_path,
        'converted_path': file_path,
        'rescaled_px_size_x': target_px_size[1],
        'rescaled_px_size_y': target_px_size[2],
        'rescaled_px_size_z': target_px_size[0],
        'success': success,
    }
    return result


def batch_convert_raw(
    dataset_table: pd.DataFrame,
    target_px_size: Tuple[float, float, float],
    output_dir: Union[str, os.PathLike],
) -> pd.DataFrame:
    """Convert a batch of raw images

    Parameters
    ----------
    dataset_table : pd.DataFrame
        The table of label images to convert. Must contain columns:
        'patient', 'cycle', 'side', 'day', 'path_labels'
    target_px_size : Tuple[float, float, float]
        The target voxel size in mm/px. Should be in ZYX order.
    output_dir : os.PathLike
        The path to the directory to save the converted files to.

    Returns
    -------
    dataset_table : pd.DataFrame
        The input dataset_table with a `converted_raw_im_path` added
        containing the path to the converted files.
    """

    file_paths = []
    for i, row in tqdm(dataset_table.iterrows(), total=len(dataset_table)):

        file_path = convert_raw_dataset(
            row=row, output_dir=output_dir, target_px_size=target_px_size
        )
        file_paths.append(file_path)
    dataset_table['converted_im_path'] = file_paths

    return dataset_table
