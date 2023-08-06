import datetime
import os
from typing import Optional, Union, Dict, Any

import h5py
import numpy as np
import pandas as pd
from skimage.morphology import binary_dilation, binary_erosion, cube
from skimage.segmentation import find_boundaries

from ..io.hdf5_io import write_training_data

from ..utils.config_utils import (
    _load_and_update_training_config,
    _load_and_update_prediction_config,
)
from ..utils.image import crop_raw_image, crop_label_image

from ..utils.submission_utils import (
    _write_train_script,
    _write_predict_script,
    write_batch_submission_script,
    get_fold_directories,
)
from ..utils.time import date_to_datestring


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


def create_multiclass_labels(
    follicle_labels: np.ndarray, follicle_border_mode: str = 'outer'
) -> np.ndarray:
    follicles_mask = follicle_labels.astype(bool)
    multiclass_labels = np.zeros_like(follicle_labels, dtype=np.int)
    multiclass_labels[follicles_mask] = 1

    # create periphery region
    follicle_boundaries = find_boundaries(
        follicles_mask, mode=follicle_border_mode
    )

    # set labels for periphery
    multiclass_labels[follicle_boundaries] = 2

    multiclass_one_hot = np.stack(
        [follicles_mask, follicle_boundaries]
    ).astype(np.uint8)

    return multiclass_labels, multiclass_one_hot


def create_follicle_dataset(
    ovary_segmentation_fpath: Union[str, os.PathLike],
    ovary_dataset_fname: str,
    output_directory: str,
    patient_id: str,
    cycle_id: str,
    side: str,
    day: datetime.date,
    mask_raw_im: bool = True,
    min_shape=[80, 80, 80],
    raw_name: str = 'raw_rescaled',
    ovary_seg_name: str = 'ovary_segmentation_rescaled',
    follicle_name: str = 'follicle_labels',
    ovary_name: str = 'ovary_labels',
    weights_name: str = 'weights',
    follicle_border_mode: str = 'outer',
    follicle_dilation: int = 4,
    follicle_erosion: int = 2,
    padding_weight: float = 0,
    ovary_weight: float = 0.8,
    follicle_weight: float = 0.8,
    boundary_weight: float = 1,
    multiclass_name: Optional[str] = None,
):

    # load the ovary segmentation
    with h5py.File(ovary_segmentation_fpath) as f_ovary:
        ovary_segmentation = f_ovary[ovary_seg_name][:]
        raw_im = f_ovary[raw_name][:]
        follicle_labels = f_ovary[follicle_name][:]
        _ = f_ovary[ovary_name][:]

    # make sure the follicle labels are 0 or 1
    follicle_labels[follicle_labels > 0] = 1
    follicle_labels[follicle_labels == 0] = 0

    # crop the data
    ovary_mask = ovary_segmentation > 0
    cropped_raw, _, _ = crop_raw_image(
        raw_im, ovary_mask, min_shape=min_shape, mask_periphery=mask_raw_im
    )
    cropped_follicle, _, _ = crop_label_image(
        follicle_labels, ovary_mask, min_shape=min_shape
    )
    cropped_ovary, _, _ = crop_label_image(
        ovary_mask.copy(), ovary_mask, min_shape=min_shape
    )

    # create the weights image
    weights = create_follicle_weights(
        ovary_im=cropped_ovary,
        follicles_im=cropped_follicle,
        padding_weight=padding_weight,
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
            cropped_follicle, follicle_border_mode=follicle_border_mode
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
        ovary_im_path=ovary_segmentation_fpath,
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

    return file_path


def batch_create_follicle_dataset(
    dataset_table: pd.DataFrame,
    ovary_datasets_dir: str,
    ovary_segmentations_dir: str,
    output_base_dir: str,
    raw_name: str = 'raw',
    follicle_name: str = 'follicle_labels',
    ovary_name: str = 'ovary_labels',
    ovary_seg_name: str = 'ovary_segmentation_rescaled',
    weights_name: str = 'weights',
    mask_raw_im: bool = True,
    min_shape=[80, 80, 80],
    follicle_border_mode='outer',
    follicle_dilation: int = 4,
    follicle_erosion: int = 2,
    padding_weight: float = 0,
    ovary_weight: float = 0.8,
    follicle_weight: float = 0.8,
    boundary_weight: float = 1,
    multiclass_name: Optional[str] = None,
):

    # create the output directories
    group_names = dataset_table['group'].unique()
    for group in group_names:
        group_path = os.path.join(output_base_dir, group)
        if not os.path.isdir(group_path):
            os.mkdir(group_path)

    file_paths = []

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

        ovary_segmentation_fpath = os.path.join(
            ovary_segmentations_dir, filename_base + '_segmentation.h5'
        )
        ovary_dataset_fpath = os.path.join(
            ovary_datasets_dir, filename_base + '.h5'
        )
        output_directory = os.path.join(output_base_dir, group)

        file_path = create_follicle_dataset(
            ovary_segmentation_fpath=ovary_segmentation_fpath,
            ovary_dataset_fname=ovary_dataset_fpath,
            output_directory=output_directory,
            patient_id=patient_id,
            cycle_id=cycle_id,
            side=side,
            day=day,
            mask_raw_im=mask_raw_im,
            min_shape=min_shape,
            raw_name=raw_name,
            follicle_name=follicle_name,
            ovary_name=ovary_name,
            ovary_seg_name=ovary_seg_name,
            weights_name=weights_name,
            follicle_border_mode=follicle_border_mode,
            follicle_dilation=follicle_dilation,
            follicle_erosion=follicle_erosion,
            padding_weight=padding_weight,
            ovary_weight=ovary_weight,
            follicle_weight=follicle_weight,
            boundary_weight=boundary_weight,
            multiclass_name=multiclass_name,
        )

        file_paths.append(file_path)

    dataset_table['follicle_path'] = file_paths

    return dataset_table


def create_follicle_datasets_from_fold(
    data_table_name: str,
    fold_dir: Union[str, os.PathLike],
    ovary_seg_dir_name: str,
    ovary_datasets_dir: Union[str, os.PathLike],
    output_base_dir: str,
    raw_name: str = 'raw',
    follicle_name: str = 'follicle_labels',
    ovary_name: str = 'ovary_labels',
    ovary_seg_name: str = 'ovary_segmentation_rescaled',
    weights_name: str = 'weights',
    mask_raw_im: bool = True,
    min_shape=[80, 80, 80],
    follicle_border_mode: str = 'outer',
    follicle_dilation: int = 4,
    follicle_erosion: int = 2,
    padding_weight: float = 0,
    ovary_weight: float = 0.8,
    follicle_weight: float = 0.8,
    boundary_weight: float = 1,
    multiclass_name: Optional[str] = None,
) -> pd.DataFrame:
    # load the dataset table
    dataset_table_fpath = os.path.join(fold_dir, data_table_name)
    dataset_table = pd.read_csv(dataset_table_fpath)

    # get the name of the ovary segmentations directory
    ovary_segmentations_dir = os.path.join(fold_dir, ovary_seg_dir_name)

    # create the follicle datasets
    updated_dataset_table = batch_create_follicle_dataset(
        dataset_table=dataset_table,
        ovary_datasets_dir=ovary_datasets_dir,
        ovary_segmentations_dir=ovary_segmentations_dir,
        output_base_dir=output_base_dir,
        raw_name=raw_name,
        follicle_name=follicle_name,
        ovary_name=ovary_name,
        ovary_seg_name=ovary_seg_name,
        weights_name=weights_name,
        mask_raw_im=mask_raw_im,
        min_shape=min_shape,
        follicle_border_mode=follicle_border_mode,
        follicle_dilation=follicle_dilation,
        follicle_erosion=follicle_erosion,
        padding_weight=padding_weight,
        ovary_weight=ovary_weight,
        follicle_weight=follicle_weight,
        boundary_weight=boundary_weight,
        multiclass_name=multiclass_name,
    )

    return updated_dataset_table


def create_cross_validation_datasets(
    crossval_dir: Union[str, os.PathLike],
    ovary_data_table_name: str,
    follicle_data_table_name: str,
    ovary_seg_dir_name: str,
    ovary_datasets_dir: Union[str, os.PathLike],
    training_config_path: Union[str, os.PathLike],
    training_runner: str,
    training_job_settings: Dict[str, Any],
    prediction_config_path: Union[str, os.PathLike],
    prediction_runner: str,
    prediction_job_settings: Dict[str, Any],
    output_base_dir: str,
    raw_name: str = 'raw',
    follicle_name: str = 'follicle_labels',
    ovary_name: str = 'ovary_labels',
    ovary_seg_name: str = 'ovary_segmentation_rescaled',
    weights_name: str = 'weights',
    mask_raw_im: bool = True,
    min_shape=[80, 80, 80],
    follicle_border_mode: str = 'outer',
    follicle_dilation: int = 4,
    follicle_erosion: int = 2,
    padding_weight: float = 0,
    ovary_weight: float = 0.8,
    follicle_weight: float = 0.8,
    boundary_weight: float = 1,
    multiclass_name: Optional[str] = None,
):
    # get the fold directories
    fold_dirs = get_fold_directories(crossval_dir, 'fold_*')
    n_fold = len(fold_dirs)
    print(f'processing {n_fold} folds')

    training_scripts = []
    prediction_scripts = []
    if not os.path.isdir(output_base_dir):
        os.mkdir(output_base_dir)
    for fold_index, fold in fold_dirs:
        fold_name = os.path.basename(fold)
        fold_dir_path = os.path.join(output_base_dir, fold_name)

        print(fold_dir_path)
        if not os.path.isdir(fold_dir_path):
            os.mkdir(fold_dir_path)

        # create the follicle datasets
        data_table = create_follicle_datasets_from_fold(
            data_table_name=ovary_data_table_name,
            fold_dir=fold,
            ovary_seg_dir_name=ovary_seg_dir_name,
            ovary_datasets_dir=ovary_datasets_dir,
            output_base_dir=fold_dir_path,
            raw_name=raw_name,
            follicle_name=follicle_name,
            ovary_name=ovary_name,
            ovary_seg_name=ovary_seg_name,
            weights_name=weights_name,
            mask_raw_im=mask_raw_im,
            min_shape=min_shape,
            follicle_border_mode=follicle_border_mode,
            follicle_dilation=follicle_dilation,
            follicle_erosion=follicle_erosion,
            padding_weight=padding_weight,
            ovary_weight=ovary_weight,
            follicle_weight=follicle_weight,
            boundary_weight=boundary_weight,
            multiclass_name=multiclass_name,
        )

        # save the datatable
        table_output_fpath = os.path.join(
            fold_dir_path, follicle_data_table_name
        )
        data_table.to_csv(table_output_fpath)

        # setup and save the training files
        checkpoint_dir = os.path.join(fold_dir_path, 'checkpoints')
        train_data_path = os.path.join(fold_dir_path, 'train')
        val_data_path = os.path.join(fold_dir_path, 'val')
        updated_training_config_path = _load_and_update_training_config(
            config_path=training_config_path,
            fold_index=fold_index,
            checkpoint_dir=checkpoint_dir,
            train_file_dir=[train_data_path],
            val_file_dir=[val_data_path],
            config_output_directory=fold_dir_path,
        )
        training_script_path = _write_train_script(
            train_runner=training_runner,
            config_path=updated_training_config_path,
            output_dir=fold_dir_path,
        )
        training_scripts.append(training_script_path)

        # setup and save the prediction config
        test_data_path = os.path.join(fold_dir_path, 'test')
        model_path = os.path.join(checkpoint_dir, 'best_checkpoint.pytorch')
        prediction_output_path = os.path.join(fold_dir_path, 'predictions')
        if not os.path.isdir(prediction_output_path):
            os.mkdir(prediction_output_path)
        updated_prediction_config_path = _load_and_update_prediction_config(
            config_path=prediction_config_path,
            fold_index=fold_index,
            model_path=model_path,
            image_files=[train_data_path, val_data_path, test_data_path],
            prediction_output_directory=prediction_output_path,
            config_output_directory=fold_dir_path,
        )
        prediction_script_path = _write_predict_script(
            predict_runner=prediction_runner,
            config_path=updated_prediction_config_path,
            output_dir=fold_dir_path,
        )
        prediction_scripts.append(prediction_script_path)

        print(f'fold{fold_index} complete')

    print('writing submission scripts')
    # write the training submission scripts
    training_submission_path = os.path.join(
        output_base_dir, 'training_submission_script.sh'
    )
    write_batch_submission_script(
        submission_script_path=training_submission_path,
        runner_scripts=training_scripts,
        job_prefix='training',
        job_settings=training_job_settings,
    )

    # write the prediction submission scripts
    prediction_submission_path = os.path.join(
        output_base_dir, 'prediction_submission_script.sh'
    )
    write_batch_submission_script(
        submission_script_path=prediction_submission_path,
        runner_scripts=prediction_scripts,
        job_prefix='prediction',
        job_settings=prediction_job_settings,
    )

    print('done')
