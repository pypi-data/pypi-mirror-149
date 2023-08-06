import datetime
import os
from typing import Optional

import h5py
import numpy as np
import pandas as pd
from skimage.morphology import binary_dilation, binary_erosion, cube
from skimage.segmentation import find_boundaries

from ..io.hdf5_io import write_training_data
from ..post_process.ovary import post_process_ovary
from ..utils.time import date_to_datestring


def crop_image(image, mask_image, min_shape=[80, 80, 80]):
    # get the crop extents
    mask_coords = np.argwhere(mask_image)
    min_indices = np.min(mask_coords, axis=0)
    max_indices = np.max(mask_coords, axis=0) + 1

    crop_shape = max_indices - min_indices
    if not np.all(crop_shape >= min_shape):
        # if the crop is smaller than the specified minimum size, expand it
        min_acceptable_indices = min_indices + min_shape
        max_indices[crop_shape < min_shape] = min_acceptable_indices[
            crop_shape < min_shape
        ]

    # get the crop
    cropped_image = image[
        min_indices[0] : max_indices[0],
        min_indices[1] : max_indices[1],
        min_indices[2] : max_indices[2],
    ]

    return cropped_image


def crop_raw_image(
    raw_image, ovary_image, min_shape=[80, 80, 80], mask_periphery: bool = True
):
    ovary_mask = ovary_image.astype(np.bool)

    # get the average pixel value and set all non ovary pixels
    if mask_periphery is True:
        mean_px_value = raw_image.mean()
        raw_image[np.logical_not(ovary_mask)] = mean_px_value

    cropped_raw_image = crop_image(raw_image, ovary_image, min_shape=min_shape)

    return cropped_raw_image


def crop_label_image(label_image, ovary_image, min_shape=[80, 80, 80]):
    ovary_mask = ovary_image.astype(np.bool)
    cropped_label = crop_image(label_image, ovary_mask, min_shape=min_shape)

    return cropped_label


def create_follicle_weights(
    ovary_im: np.ndarray,
    follicles_im: np.ndarray,
    padding_weight: float = 0,
    ovary_weight: float = 0.8,
    follicle_weight: float = 0.8,
    boundary_weight: float = 1,
    follicle_dilation: int = 4,
    follicle_erosion: int = 2,
):
    ovary_mask = ovary_im.astype(np.bool)
    follicles_mask = follicles_im.astype(np.bool)

    weights = np.zeros_like(ovary_mask, dtype=np.float)

    # apply the padding weights
    weights[np.logical_not(ovary_mask)] = padding_weight

    # apply the ovary weights
    weights[ovary_mask] = ovary_weight

    # apply the follicle weights
    weights[follicles_mask] = follicle_weight

    # apply the follicle boundary weights
    dilated_follicles = binary_dilation(
        follicles_mask, selem=cube(follicle_dilation)
    )
    eroded_follicles = binary_erosion(
        follicles_mask, selem=cube(follicle_erosion)
    )
    boundary_mask = np.logical_xor(dilated_follicles, eroded_follicles)
    weights[boundary_mask] = boundary_weight

    return weights


def create_multiclass_labels(follicle_labels: np.ndarray) -> np.ndarray:
    follicles_mask = follicle_labels.astype(bool)
    multiclass_labels = np.zeros_like(follicle_labels, dtype=np.int)
    multiclass_labels[follicles_mask] = 1

    # create periphery region
    follicle_boundaries = find_boundaries(follicles_mask, mode='thick')

    # set labels for periphery
    multiclass_labels[follicle_boundaries] = 2

    multiclass_one_hot = np.stack(
        [follicles_mask, follicle_boundaries]
    ).astype(np.uint8)

    return multiclass_labels, multiclass_one_hot


def create_follicle_dataset(
    ovary_prediction_fname: str,
    ovary_dataset_fname: str,
    output_directory: str,
    patient_id: str,
    cycle_id: str,
    side: str,
    day: datetime.date,
    mask_raw_im: bool = True,
    min_shape=[80, 80, 80],
    raw_name: str = 'raw',
    follicle_name: str = 'follicle_labels',
    ovary_name: str = 'ovary_labels',
    weights_name: str = 'weights',
    threshold: float = 0.5,
    dilation_size: int = 10,
    follicle_dilation: int = 4,
    follicle_erosion: int = 2,
    ovary_weight: float = 0.8,
    follicle_weight: float = 0.8,
    boundary_weight: float = 1,
    multiclass_name: Optional[str] = None,
):

    # load the ovary prediction
    with h5py.File(ovary_prediction_fname) as f_prediction:
        ovary_prediction = f_prediction['predictions'][1, :, :, :]

    with h5py.File(ovary_dataset_fname) as f_ovary:
        raw_im = f_ovary[raw_name][:]
        follicle_im = f_ovary[follicle_name][:]

    # make sure the follicle labels are 0 or 1
    follicle_im[follicle_im > 0] = 1
    follicle_im[follicle_im == 0] = 0

    # create the ovary mask
    ovary_mask = post_process_ovary(
        raw_im=raw_im,
        ovary_prediction=ovary_prediction,
        threshold=threshold,
        dilation_size=dilation_size,
    )

    # crop the data
    cropped_raw = crop_raw_image(
        raw_im, ovary_mask, min_shape=min_shape, mask_periphery=mask_raw_im
    )
    cropped_follicle = crop_label_image(
        follicle_im, ovary_mask, min_shape=min_shape
    )
    cropped_ovary = crop_label_image(
        ovary_mask.copy(), ovary_mask, min_shape=min_shape
    )

    # create the weights image
    weights = create_follicle_weights(
        ovary_im=cropped_ovary,
        follicles_im=cropped_follicle,
        padding_weight=0,
        ovary_weight=ovary_weight,
        follicle_weight=follicle_weight,
        boundary_weight=boundary_weight,
        follicle_dilation=follicle_dilation,
        follicle_erosion=follicle_erosion,
    )

    # create the filename
    date_string = date_to_datestring(day)
    fname = f'{patient_id}_{cycle_id}_{side}_{date_string}_follicles.h5'
    file_path = os.path.join(output_directory, fname)

    if multiclass_name is not None:
        multiclass_im, multiclass_one_hot = create_multiclass_labels(
            cropped_follicle
        )

    else:
        multiclass_im = None
        multiclass_one_hot = None
    # write the data
    write_training_data(
        raw_im=cropped_raw,
        raw_im_path=ovary_dataset_fname,
        follicle_im=cropped_follicle,
        follicle_im_path=ovary_dataset_fname,
        ovary_im=cropped_ovary,
        ovary_im_path=ovary_prediction_fname,
        file_path=file_path,
        raw_name=raw_name,
        follicle_name=follicle_name,
        ovary_name=ovary_name,
        weights_im=weights,
        weights_name=weights_name,
        multiclass_im=multiclass_im,
        multiclass_name=multiclass_name,
        multiclass_one_hot_im=multiclass_one_hot,
        compression='gzip',
    )

    return file_path, True


def batch_create_follicle_dataset(
    dataset_table: pd.DataFrame,
    ovary_datasets_dir: str,
    ovary_predictions_dir: str,
    output_base_dir: str,
    raw_name: str = 'raw',
    follicle_name: str = 'follicle_labels',
    ovary_name: str = 'ovary_labels',
    weights_name: str = 'weights',
    mask_raw_im: bool = True,
    min_shape=[80, 80, 80],
    threshold: float = 0.5,
    dilation_size: int = 10,
    follicle_dilation: int = 4,
    follicle_erosion: int = 2,
    ovary_weight: float = 0.8,
    follicle_weight: float = 0.8,
    boundary_weight: float = 1,
    multiclass_name: Optional[str] = None,
):

    # create the output directories
    group_names = dataset_table['group'].unique()
    for group in group_names:
        os.mkdir(os.path.join(output_base_dir, group))

    file_paths = []
    success = []

    for _, row in dataset_table.iterrows():
        patient_id = row['patient']
        cycle_id = row['cycle']
        side = row['side']
        day = row['day']
        group = row['group']

        if isinstance(day, str):
            date_time_obj = datetime.datetime.strptime(day, '%Y-%m-%d')
            date_string = date_time_obj.strftime('%y%m%d')
        else:
            date_string = day.strftime('%y%m%d')
        filename_base = f'{patient_id}_{cycle_id}_{side}_{date_string}_ovary'

        ovary_prediction_fname = os.path.join(
            ovary_predictions_dir, filename_base + '_predictions.h5'
        )
        ovary_dataset_fname = os.path.join(
            ovary_datasets_dir, group, filename_base + '.h5'
        )
        output_directory = os.path.join(output_base_dir, group)

        file_path, conversion_succeeded = create_follicle_dataset(
            ovary_prediction_fname=ovary_prediction_fname,
            ovary_dataset_fname=ovary_dataset_fname,
            output_directory=output_directory,
            patient_id=patient_id,
            cycle_id=cycle_id,
            side=side,
            day=day,
            raw_name=raw_name,
            follicle_name=follicle_name,
            ovary_name=ovary_name,
            weights_name=weights_name,
            mask_raw_im=mask_raw_im,
            min_shape=min_shape,
            threshold=threshold,
            dilation_size=dilation_size,
            ovary_weight=ovary_weight,
            follicle_weight=follicle_weight,
            boundary_weight=boundary_weight,
            follicle_dilation=follicle_dilation,
            follicle_erosion=follicle_erosion,
            multiclass_name=multiclass_name,
        )

        file_paths.append(file_path)
        success.append(conversion_succeeded)

    dataset_table['follicle_path'] = file_paths
    dataset_table['follicle_conversion_successful'] = success

    return dataset_table
