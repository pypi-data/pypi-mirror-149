import os
from typing import Union, Dict, Any, List
import warnings

import h5py
import numpy as np
import pandas as pd
from skimage.morphology import binary_dilation, cube, binary_erosion
from sklearn.model_selection import train_test_split
from tqdm.auto import tqdm

from .training_utils import copy_datasets, split_table_into_k_folds
from ..io.hdf5_io import load_raw_im, write_multi_dataset_hdf
from ..post_process.follicles import remove_small_follicles
from ..utils.config_utils import (
    _load_and_update_training_config,
    _load_and_update_prediction_config,
)
from ..utils.image import pad_label_im, pad_im_to_min_size
from ..utils.submission_utils import (
    _write_predict_script,
    _write_train_script,
    _write_submission_script,
)
from ..utils.time import date_to_datestring


def create_ovary_training_dataset(
    row: pd.Series,
    raw_im_dir: Union[str, os.PathLike],
    label_im_dir: Union[str, os.PathLike],
    output_dir: Union[str, os.PathLike],
    raw_im_name: str = 'raw',
    min_follicle_volume: int = 0,
    follicle_labels_name: str = 'rescaled_follicle_labels',
    ovary_labels_name: str = 'rescaled_ovary_labels',
    min_im_size: List[int] = [80, 80, 80],
    padding_weight: float = 0,
    muscle_weight: float = 0.9,
    ovary_weight: float = 0.9,
    follicle_weight: float = 1,
    boundary_weight: float = 1,
) -> str:
    """Create a training/validation dataset for the ovary segmentation

    Parameters
    ----------
    row : pd.Series
        The row in the file table to create the ovary dataset from.
    raw_im_dir : Union[str, os.PathLike]
        The path to the directory containing the converted raw images.
    label_im_dir : Union[str, os.PathLike]
        The path to the directory containing the converted label images
    output_dir : Union[str, os.PathLike]
        The path to the directory to save the ovary datasets to.
    raw_im_name : str
        The dataset key in the raw image file containig the raw image.
        The rescaled raw image will be accessed from raw_im_name + 'rescaled'
    min_follicle_volume : int
        The minimum number of voxels a follicle needs to have in the label image
        to pass QC. All follicles <= min_follicle_volume are remove. The default
        value is 0.
    follicle_labels_name : str
        The dataset key in the label image file for the rescaled follicle labels.
        The default value is 'rescaled_follicle_labels'.
    ovary_labels_name : str
        The dataset key in the label image file for the rescaled ovary labels.
        The default value is 'rescaled_ovary_labels'.
    min_im_size : List[int]
        The minimum shape for images. This ensures you will be able ot create
        at least one tile. Images with smaller shape are padded with zeros.

    Returns
    -------
    dataset_path : str
        The path to the dataset that was created.
    """
    patient_id = row['patient']
    cycle_id = row['cycle']
    side = row['side']
    date_string = date_to_datestring(row['day'])

    # load the image
    raw_im_fname = os.path.basename(row['converted_im_path'])
    raw_im_fpath = os.path.join(raw_im_dir, raw_im_fname)
    raw_im, raw_attrs, rescaled_im, rescaled_attrs = load_raw_im(
        raw_im_fpath, raw_name=raw_im_name
    )

    # load the labels
    labels_fname = os.path.basename(row['converted_labels_path'])
    labels_fpath = os.path.join(label_im_dir, labels_fname)
    with h5py.File(labels_fpath, 'r') as f_labels:
        follicle_labels = f_labels[follicle_labels_name][:]
        ovary_labels = f_labels[ovary_labels_name][:]

    # we have some label images that are missing a z slice
    # so we have to fix this as a special case
    follicle_labels = pad_label_im(rescaled_im, follicle_labels)
    ovary_labels = pad_label_im(rescaled_im, ovary_labels)

    # apply padding to make sure we meet our minimum tile size
    rescaled_im = pad_im_to_min_size(rescaled_im, min_size=min_im_size)
    ovary_labels = pad_im_to_min_size(ovary_labels, min_size=min_im_size)
    follicle_labels = pad_im_to_min_size(follicle_labels, min_size=min_im_size)

    follicle_labels[follicle_labels > 0] = 1
    follicle_labels_clean = remove_small_follicles(
        follicle_labels, volume_threshold=min_follicle_volume
    ).astype(np.uint8)

    # padding mask
    padding_mask_rescaled = np.zeros_like(rescaled_im, dtype=bool)
    padding_mask_rescaled[rescaled_im == 0] = True

    # create the weights image
    weights = create_ovary_weights(
        padding_im=padding_mask_rescaled,
        ovary_im=ovary_labels,
        follicles_im=follicle_labels_clean,
        padding_weight=padding_weight,
        muscle_weight=muscle_weight,
        ovary_weight=ovary_weight,
        follicle_weight=follicle_weight,
        boundary_weight=boundary_weight,
    )

    fname = f'{patient_id}_{cycle_id}_{side}_{date_string}_ovary.h5'
    file_path = os.path.join(output_dir, fname)

    raw_dataset = {'data': raw_im, 'attrs': raw_attrs}
    rescaled_dataset = {'data': rescaled_im, 'attrs': rescaled_attrs}

    write_multi_dataset_hdf(
        file_path=file_path,
        compression='gzip',
        raw=raw_dataset,
        raw_rescaled=rescaled_dataset,
        follicle_labels_rescaled=follicle_labels_clean,
        ovary_labels_rescaled=ovary_labels,
        weights_rescaled=weights,
    )

    return file_path


def batch_convert_ovary_datasets(
    dataset_table: pd.DataFrame,
    raw_im_dir: Union[str, os.PathLike],
    label_im_dir: Union[str, os.PathLike],
    output_dir: Union[str, os.PathLike],
    raw_im_name: str = 'raw',
    min_follicle_volume: int = 0,
    min_im_size: List[int] = [80, 80, 80],
    padding_weight: float = 0,
    muscle_weight: float = 0.9,
    ovary_weight: float = 0.9,
    follicle_weight: float = 1,
    boundary_weight: float = 1,
    follicle_labels_name: str = 'rescaled_follicle_labels',
    ovary_labels_name: str = 'rescaled_ovary_labels',
    dataset_path_name: str = 'dataset_path',
) -> pd.DataFrame:

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    file_paths = []
    for i, row in tqdm(dataset_table.iterrows(), total=len(dataset_table)):

        file_path = create_ovary_training_dataset(
            row=row,
            raw_im_dir=raw_im_dir,
            label_im_dir=label_im_dir,
            output_dir=output_dir,
            raw_im_name=raw_im_name,
            min_follicle_volume=min_follicle_volume,
            follicle_labels_name=follicle_labels_name,
            ovary_labels_name=ovary_labels_name,
            min_im_size=min_im_size,
            padding_weight=padding_weight,
            muscle_weight=muscle_weight,
            ovary_weight=ovary_weight,
            follicle_weight=follicle_weight,
            boundary_weight=boundary_weight,
        )
        file_paths.append(file_path)
    dataset_table[dataset_path_name] = file_paths

    return dataset_table


def split_and_create_ovary_dataset(
    dataset_table: pd.DataFrame,
    raw_im_dir: str,
    output_base_dir: str,
    train_frac: float = 0.8,
    val_frac: float = 0.1,
    test_frac: float = 0.1,
) -> pd.DataFrame:
    assert (train_frac + val_frac + test_frac) == 1

    split_1 = train_frac
    split_2 = train_frac + val_frac

    # split the dataset
    train, validate, test = np.split(
        dataset_table.sample(frac=1, random_state=0),
        [int(split_1 * len(dataset_table)), int(split_2 * len(dataset_table))],
    )

    # create the training data
    train_dir = os.path.join(output_base_dir, 'train')
    os.mkdir(train_dir)
    train_output = batch_convert_ovary_datasets(
        dataset_table=train,
        raw_im_dir=raw_im_dir,
        output_dir=train_dir,
    )
    train_output['group'] = 'train'

    # create the validation data
    val_dir = os.path.join(output_base_dir, 'val')
    os.mkdir(val_dir)
    val_output = batch_convert_ovary_datasets(
        dataset_table=validate,
        raw_im_dir=raw_im_dir,
        output_dir=val_dir,
    )
    val_output['group'] = 'val'

    # create the test data
    test_dir = os.path.join(output_base_dir, 'test')
    os.mkdir(test_dir)
    test_output = batch_convert_ovary_datasets(
        dataset_table=test, raw_im_dir=raw_im_dir, output_dir=test_dir
    )
    test_output['group'] = 'test'

    output_df = pd.concat([train_output, val_output, test_output])

    return output_df


def create_ovary_weights(
    padding_im: np.ndarray,
    ovary_im: np.ndarray,
    follicles_im: np.ndarray,
    padding_weight: float = 0,
    muscle_weight: float = 0.9,
    ovary_weight: float = 0.9,
    follicle_weight: float = 1,
    boundary_weight: float = 1,
):
    padding_mask = padding_im.astype(np.bool)
    ovary_mask = ovary_im.astype(np.bool)
    follicles_mask = follicles_im.astype(np.bool)

    weights = np.zeros_like(ovary_mask, dtype=np.float)

    # apply the padding weights
    weights[padding_mask] = padding_weight

    # apply the muscle weights
    weights[np.logical_not(padding_mask)] = muscle_weight

    # apply the ovary weights
    weights[ovary_mask] = ovary_weight

    # apply the follicle weights
    weights[follicles_mask] = follicle_weight

    # apply the follicle boundary weights
    dilated_ovary = binary_dilation(ovary_mask, selem=cube(6))
    eroded_ovary = binary_erosion(ovary_mask, selem=cube(2))
    boundary_mask = np.logical_xor(dilated_ovary, eroded_ovary)
    weights[boundary_mask] = boundary_weight

    return weights


def create_cross_validation(
    data_table_path: Union[str, os.PathLike],
    dataset_dir: Union[str, os.PathLike],
    training_config_path: Union[str, os.PathLike],
    training_runner: str,
    training_job_settings: Dict[str, Any],
    prediction_config_path: Union[str, os.PathLike],
    prediction_runner: str,
    prediction_job_settings: Dict[str, Any],
    output_dir: Union[str, os.PathLike],
    df_output_fname: Union[str, os.PathLike],
    n_folds: int = 10,
    frac_train: float = 0.89,
    random_seed: int = 0,
):
    """Create the folders for a ovary cross validation experiment

    Parameters
    ----------
    data_table_path : Union[str, os.PathLike]
        The path to the dataset table to split.
    dataset_dir : Union[str, os.PathLike]
        The path to the folder containing the datasets to split
    training_config_path : Union[str, os.PathLike]
        The path to the training config that will be updated and stored in the
    training_runner : str
        The command to call the training runner. This us generally a bash
        or python script.
    training_job_settings : Dict[str, Any]
        The settings for each job that will be submitted for training the model.
        Must have the following keys: n_cpus, mem_per_cpu, n_gpus job_time
    prediction_config_path : Union[str, os.PathLike]
        The path to the training config that will be updated and stored in the
    prediction_runner : str
        The command to call the predict runner. This us generally a bash
        or python script.
    prediction_job_settings : Dict[str, Any]
        The settings for each job that will be submitted for predictions.
        Must have the following keys: n_cpus, mem_per_cpu, n_gpus job_time
    output_dir : Union[str, os.PathLike]
        The path to the directory to save the cross validation datasets to
    df_output_fname : Union[str, os.PathLike]
        The name of the final dataset table. This will be saved in the output_dir.
    n_folds : int
        The number of folds to split the data into. This will
    frac_train : float
        The fraction of the training portion of the fold to use for training. The
        rest is used for validation.
    random_seed : float
        The value for the random seed. The random number generator is used for
        splitting the data.
    """

    # load the dataframe
    df = pd.read_csv(data_table_path)
    n_datasets = len(df)
    print(f'table loaded, {n_datasets} found')

    # split the data into k partitions
    split_df = split_table_into_k_folds(df, n_folds, random_seed)

    training_scripts = []
    prediction_scripts = []
    for i in range(n_folds):
        print(f'starting fold {i}')
        train_val = split_df.copy()

        # get the test dataset
        test = split_df[i]
        del train_val[i]

        # split the train_val set
        train_val_df = pd.concat(train_val)
        frac_val = 1 - frac_train
        train, val = train_test_split(
            train_val_df, test_size=frac_val, random_state=random_seed
        )

        with warnings.catch_warnings():
            # set the group in the dataframes. We ignore the
            # SettingWithCopyWarning, as we do not intend
            # to propagate the change to the original df
            warnings.simplefilter("ignore")
            test['group'] = 'test'
            train['group'] = 'train'
            val['group'] = 'val'

        # make the folder for the group
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        fold_dir_path = os.path.join(output_dir, f'fold_{i}')
        if not os.path.isdir(fold_dir_path):
            os.mkdir(fold_dir_path)

        # copy the test data
        test_data_path = os.path.join(fold_dir_path, 'test')
        copy_datasets(test, dataset_dir, test_data_path)

        # copy the train data
        train_data_path = os.path.join(fold_dir_path, 'train')
        copy_datasets(train, dataset_dir, train_data_path)

        # copy the val data
        val_data_path = os.path.join(fold_dir_path, 'val')
        copy_datasets(val, dataset_dir, val_data_path)

        print(f'fold {i} data copied')
        # recombine the dataframes and save
        fold_df = pd.concat([test, val, train])
        fold_df.to_csv(os.path.join(fold_dir_path, df_output_fname))

        # setup and save the training config
        checkpoint_dir = os.path.join(fold_dir_path, 'checkpoints')
        updated_training_config_path = _load_and_update_training_config(
            config_path=training_config_path,
            fold_index=i,
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
        model_path = os.path.join(checkpoint_dir, 'best_checkpoint.pytorch')
        prediction_output_path = os.path.join(fold_dir_path, 'predictions')
        if not os.path.isdir(prediction_output_path):
            os.mkdir(prediction_output_path)
        updated_prediction_config_path = _load_and_update_prediction_config(
            config_path=prediction_config_path,
            fold_index=i,
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

        print(f'fold{i} complete')

    print('writing submission scripts')
    training_submission_path = os.path.join(
        output_dir, 'training_submission_script.sh'
    )
    training_job_settings.update(
        {
            'runner_paths': training_scripts,
            'job_prefix': 'training',
            'script_path': training_submission_path,
        }
    )
    _write_submission_script(**training_job_settings)

    prediction_submission_path = os.path.join(
        output_dir, 'prediction_submission_script.sh'
    )
    prediction_job_settings.update(
        {
            'runner_paths': prediction_scripts,
            'job_prefix': 'prediction',
            'script_path': prediction_submission_path,
        }
    )
    _write_submission_script(**prediction_job_settings)

    print('done')
