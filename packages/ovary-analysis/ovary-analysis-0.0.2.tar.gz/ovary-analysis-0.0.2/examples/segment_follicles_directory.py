from functools import partial
import glob
import multiprocessing as mp
import os
from typing import Tuple, Union

import h5py

from ovary_analysis.io.hdf5_io import load_im_from_hdf, write_multi_dataset_hdf
from ovary_analysis.post_process.follicles import post_process_follicles
from ovary_analysis.utils.image import crop_label_image


def segment_follicles(
    prediction_fpath: str,
    raw_im_dir_path: str,
    ovary_segmentation_dir_path: Union[str, os.PathLike],
    output_dir_path: Union[str, os.PathLike],
    prob_threshold: float,
    volume_threshold: float,
    prediction_index: int = 1,
    apply_softmax: bool = True,
    raw_im_key: str = 'raw_rescaled',
    ovary_segmentation_key: str = 'ovary_labels_rescaled',
    prediction_key: str = 'predictions',
    min_shape: Tuple[int, int, int] = (80, 80, 80)
):

    if not os.path.isdir(output_dir_path):
        os.mkdir(output_dir_path)

    # load the raw image
    prediction_fname = os.path.basename(prediction_fpath)
    raw_fname = prediction_fname.replace("_predictions.h5", ".h5")
    raw_im_fpath = os.path.join(raw_im_dir_path, raw_fname)
    with h5py.File(raw_im_fpath, 'r') as f_raw:
        raw_rescaled = f_raw[raw_im_key][:]
        rescaled_attrs = dict(f_raw[raw_im_key].attrs.items())

    # get the ovary segmentation image path
    ovary_segmentation_fname = prediction_fname.replace(
        "_follicles_predictions.h5",
        "_raw_segmentation.h5"
    )
    ovary_segmentation_fpath = os.path.join(ovary_segmentation_dir_path, ovary_segmentation_fname)

    # load the ovary segmentation
    prediction = load_im_from_hdf(
        fpath=prediction_fpath, dataset_key=prediction_key
    )
    ovary_segmentation = load_im_from_hdf(
        fpath=ovary_segmentation_fpath, dataset_key=ovary_segmentation_key
    )
    cropped_ovary_segmentation = crop_label_image(
        label_image=ovary_segmentation,
        ovary_image=ovary_segmentation,
        min_shape=min_shape
    )

    # segment the follicles
    follicles_segmentation = post_process_follicles(
        follicle_prediction=prediction,
        ovary_seg=cropped_ovary_segmentation.astype(bool),
        prob_threshold=prob_threshold,
        volume_threshold=volume_threshold,
        prediction_index=prediction_index,
        apply_softmax=apply_softmax,
    )

    # save the output
    output_fname = os.path.basename(prediction_fpath).replace(
        '_predictions.', '_segmentation.'
    )
    output_fpath = os.path.join(output_dir_path, output_fname)
    rescaled_dataset = {'data': raw_rescaled, 'attrs': rescaled_attrs}
    write_multi_dataset_hdf(
        file_path=output_fpath,
        compression="gzip",
        raw_rescaled=rescaled_dataset,
        follicle_segmentation_rescaled=follicles_segmentation,
        ovary_segmentation_rescaled=cropped_ovary_segmentation
    )

    return output_fpath


if __name__ == "__main__":
    PREDICTIONS_DIR_PATH = "/cluster/scratch/kyamauch/full_data_20220301/follicle_segmentation/predictions"
    RAW_IM_DIR_PATH = "/cluster/scratch/kyamauch/full_data_20220301/follicle_segmentation/follicle_datasets"
    OVARY_SEGMENTATION_DIR_PATH = "/cluster/scratch/kyamauch/full_data_20220301/ovary_segmentation/segmentations"
    OUTPUT_DIR_PATH = "/cluster/scratch/kyamauch/full_data_20220301/follicle_segmentation/segmentations"

    PREDICTIONS_DIR_NAME = 'predictions'
    OUTPUT_DIR_NAME = 'segmentations'
    PROB_THRESHOLD = 0.5
    VOLUME_THRESHOLD = 30
    PREDICTION_INDEX = 1
    APPLY_SOFTMAX = True
    RAW_IM_KEY = 'raw_rescaled'
    FOLLICLES_LABELS_KEY = 'follicle_labels_rescaled'
    OVARY_SEGMENTATION_KEY = 'ovary_labels_rescaled'
    PREDICTIONS_KEY = 'predictions'

    segmentation_function = partial(
        segment_follicles,
        raw_im_dir_path=RAW_IM_DIR_PATH,
        ovary_segmentation_dir_path=OVARY_SEGMENTATION_DIR_PATH,
        output_dir_path=OUTPUT_DIR_PATH,
        prob_threshold=PROB_THRESHOLD,
        volume_threshold=VOLUME_THRESHOLD,
        prediction_index=PREDICTION_INDEX,
        apply_softmax=PREDICTION_INDEX,
        raw_im_key=RAW_IM_KEY,
        follicle_labels_key=FOLLICLES_LABELS_KEY,
        ovary_segmentation_key=OVARY_SEGMENTATION_KEY,
        prediction_key=PREDICTIONS_KEY,
    )

    prediction_paths = glob.glob(os.path.join(PREDICTIONS_DIR_PATH, "*.h5"))

    with mp.get_context('spawn').Pool() as pool:
        pool.map(segmentation_function, prediction_paths)
