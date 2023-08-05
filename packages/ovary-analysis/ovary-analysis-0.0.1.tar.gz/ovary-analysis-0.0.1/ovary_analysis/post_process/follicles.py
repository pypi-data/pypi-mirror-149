import glob
import os
from typing import Union

import h5py
import numpy as np
from scipy import ndimage as ndi
from scipy.special import softmax
from skimage.measure import regionprops_table
from skimage.segmentation import clear_border

from ovary_analysis.io.hdf5_io import (
    load_im_from_hdf,
    write_multi_dataset_hdf,
)
from ovary_analysis.utils.submission_utils import get_fold_directories


def process_follicle_labels(
    follicle_labels: np.ndarray, volume_threshold: float
) -> np.ndarray:
    """Process follicle labels to remove follicles with volumes
    below the specified threshold. Also removes labels touching
    the image border.

    Parameters
    ----------
    follicle_labels : np.ndarray
        The follicle labels as a label image.
    volume_threshold : float
        The minimum follicle volume in voxels.

    Returns
    -------
    follicle_labels : np.ndarray
        The follicle labels with the small and border-touching
        labels removed.
    """
    follicle_mask_clean = remove_small_follicles(
        follicle_mask=follicle_labels, volume_threshold=volume_threshold
    )

    follicle_mask_no_border = clear_border(follicle_mask_clean)
    follicle_labels, _ = ndi.label(follicle_mask_no_border)

    return follicle_labels


def segment_follicles(
    follicle_prediction: np.ndarray,
    ovary_seg: np.ndarray,
    threshold: float,
    prediction_index: int = 1,
) -> np.ndarray:
    """Segment follicles from a prediction image

    Parameters
    ----------
    follicle_prediction : np.ndarray
        The prediction output from the segmentation model.
        Should be ordered CZYX. Where C is the prediction
        class.
    ovary_seg : np.ndarray
        The ovary segmentation image used to remove follicles detected
        outside of the ovary. Should be a binary image.
    threshold : float
        The probability threshold. Probabilities greater than the threshold
        are called as follicle.
    prediction_index : int
        The index in the prediction image corresponding to the follicle
        prediction. The default value is 1.

    Returns
    -------
    follicle_mask : np.ndarray
        The binary mask of the follicle segmentation.
    """
    follicle_prediction = follicle_prediction[prediction_index, ...]
    follicle_mask = np.zeros_like(follicle_prediction, dtype=bool)

    follicle_mask[follicle_prediction >= threshold] = True
    follicle_mask[np.logical_not(ovary_seg)] = False

    return follicle_mask


def remove_small_follicles(
    follicle_mask: np.ndarray, volume_threshold: float
) -> np.ndarray:
    """Remove follicles below a size threshold

    Parameters
    ----------
    follicle_mask : np.ndarray
        The binary mask of the follicle segmentation.
    volume_threshold : float
        The volume threshold below which follicles are discarded.
        The threshold is in voxels.

    Returns
    -------
    clean_follicles : np.ndarray
        The binary mask of the follicle segmentation with small
        follicles removed.
    """
    label_im, _ = ndi.label(follicle_mask)
    rp_table = regionprops_table(label_im, properties=('label', 'area'))

    area_to_remove_mask = rp_table['area'] < volume_threshold
    labels_to_remove = rp_table['label'][area_to_remove_mask]

    clean_follicles = label_im.copy()
    for label_index in labels_to_remove:
        clean_follicles[clean_follicles == label_index] = 0

    return clean_follicles.astype(bool)


def post_process_follicles(
    follicle_prediction: np.ndarray,
    ovary_seg: np.ndarray,
    prob_threshold: float,
    volume_threshold: float,
    prediction_index: int = 1,
    apply_softmax: bool = True,
) -> np.ndarray:
    """Create a segmentation label image from the model prediction.

    Parameters
    ----------
    follicle_prediction : np.ndarray
        The prediction output from the segmentation model.
        Should be ordered CZYX. Where C is the prediction
        class.
    ovary_seg : np.ndarray
        The ovary segmentation image used to remove follicles detected
        outside of the ovary. Should be a binary image.
    prob_threshold : float
        The probability threshold. Probabilities greater than the threshold
        are called as follicle.
    volume_threshold : float
        The volume threshold below which follicles are discarded.
        The threshold is in voxels.
    prediction_index : int
        The index in the prediction image corresponding to the follicle
        prediction. The default value is 1.
    apply_softmax : bool
        Flag set to true if a softmax should be applied along axis 0
        of the follicle_prediction. The default value is True.

    Returns
    -------
    follicle_labels : np.ndarray
        The follicle segmentation label image.
    """
    if apply_softmax is True:
        follicle_prediction = softmax(follicle_prediction, axis=0)

    follicle_seg = segment_follicles(
        follicle_prediction=follicle_prediction,
        ovary_seg=ovary_seg,
        threshold=prob_threshold,
        prediction_index=prediction_index,
    )

    follicle_mask_clean = remove_small_follicles(
        follicle_mask=follicle_seg, volume_threshold=volume_threshold
    )

    follicle_mask_no_border = clear_border(follicle_mask_clean)

    follicle_labels, _ = ndi.label(follicle_mask_no_border)

    return follicle_labels


def segment_follicles_from_prediction(
    prediction_path: Union[str, os.PathLike],
    raw_im_path: Union[str, os.PathLike],
    prob_threshold: float,
    volume_threshold: float,
    output_dir: Union[str, os.PathLike],
    prediction_index: int = 1,
    apply_softmax: bool = True,
    raw_im_key: str = 'raw_rescaled',
    follicle_labels_key: str = 'follicle_labels_rescaled',
    ovary_segmentation_key: str = 'ovary_labels_rescaled',
    prediction_key: str = 'predictions',
) -> str:
    # load the images
    prediction = load_im_from_hdf(
        fpath=prediction_path, dataset_key=prediction_key
    )

    with h5py.File(raw_im_path, 'r') as f_raw:
        raw_rescaled = f_raw[raw_im_key][:]
        rescaled_attrs = dict(f_raw[raw_im_key].attrs.items())

    try:
        follicle_labels = load_im_from_hdf(
            fpath=raw_im_path, dataset_key=follicle_labels_key
        )
        clean_follicle_lables = process_follicle_labels(
            follicle_labels=follicle_labels, volume_threshold=volume_threshold
        )
    except KeyError:
        follicle_labels = None
        clean_follicle_lables = None
    ovary_segmentation = load_im_from_hdf(
        fpath=raw_im_path, dataset_key=ovary_segmentation_key
    )

    # segment the follicles
    follicles_segmentation = post_process_follicles(
        follicle_prediction=prediction,
        ovary_seg=ovary_segmentation.astype(bool),
        prob_threshold=prob_threshold,
        volume_threshold=volume_threshold,
        prediction_index=prediction_index,
        apply_softmax=apply_softmax,
    )

    # save the segmentation
    output_fname = os.path.basename(prediction_path).replace(
        '_predictions.', '_segmentation.'
    )
    output_fpath = os.path.join(output_dir, output_fname)
    rescaled_dataset = {'data': raw_rescaled, 'attrs': rescaled_attrs}
    writer_kwargs = {
        'file_path': output_fpath,
        'compression': 'gzip',
        'raw_rescaled': rescaled_dataset,
        'follicle_segmentation_rescaled': follicles_segmentation,
        'ovary_segmentation_rescaled': ovary_segmentation,
    }
    if clean_follicle_lables is not None:
        writer_kwargs.update(
            {'follicle_labels_rescaled': clean_follicle_lables}
        )
    write_multi_dataset_hdf(**writer_kwargs)

    return output_fpath


def segment_follicles_fold(
    fold_dir_path: Union[str, os.PathLike],
    raw_im_dir_name: Union[str, os.PathLike],
    output_dir_name: Union[str, os.PathLike],
    predictions_dir_name: str,
    prob_threshold: float,
    volume_threshold: float,
    prediction_index: int = 1,
    apply_softmax: bool = True,
    raw_im_key: str = 'raw_rescaled',
    follicle_labels_key: str = 'follicle_labels_rescaled',
    ovary_segmentation_key: str = 'ovary_labels_rescaled',
    prediction_key: str = 'predictions',
):

    output_dir_fpath = os.path.join(fold_dir_path, output_dir_name)
    if not os.path.isdir(output_dir_fpath):
        os.mkdir(output_dir_fpath)

    # get the prediction directory path
    prediction_dir_path = os.path.join(fold_dir_path, predictions_dir_name)

    # get the raw images
    raw_im_dir = os.path.join(fold_dir_path, raw_im_dir_name)
    raw_im_pattern = os.path.join(raw_im_dir, '*.h5')
    raw_im_files = glob.glob(raw_im_pattern)

    segmentation_fpaths = []
    for raw_im_path in raw_im_files:
        prediction_im_name = os.path.basename(raw_im_path).replace(
            '.h5', '_predictions.h5'
        )
        prediction_path = os.path.join(prediction_dir_path, prediction_im_name)

        seg_path = segment_follicles_from_prediction(
            prediction_path=prediction_path,
            raw_im_path=raw_im_path,
            prob_threshold=prob_threshold,
            volume_threshold=volume_threshold,
            output_dir=output_dir_fpath,
            prediction_index=prediction_index,
            apply_softmax=apply_softmax,
            raw_im_key=raw_im_key,
            follicle_labels_key=follicle_labels_key,
            ovary_segmentation_key=ovary_segmentation_key,
            prediction_key=prediction_key,
        )
        segmentation_fpaths.append(seg_path)

    return segmentation_fpaths


def post_process_follicles_cross_val(
    crossval_dir_path: Union[str, os.PathLike],
    fold_dir_pattern: str,
    raw_im_dir_name: Union[str, os.PathLike],
    predictions_dir_name: str,
    output_dir_name: Union[str, os.PathLike],
    prob_threshold: float,
    volume_threshold: float,
    prediction_index: int = 1,
    apply_softmax: bool = True,
    raw_im_key: str = 'raw_rescaled',
    follicle_labels_key: str = 'follicle_labels_rescaled',
    ovary_segmentation_key: str = 'ovary_labels_rescaled',
    prediction_key: str = 'predictions',
):
    fold_directories = get_fold_directories(
        base_dir=crossval_dir_path, fold_dir_pattern=fold_dir_pattern
    )

    for _, fold_directory in fold_directories:
        _ = segment_follicles_fold(
            fold_dir_path=fold_directory,
            raw_im_dir_name=raw_im_dir_name,
            output_dir_name=output_dir_name,
            predictions_dir_name=predictions_dir_name,
            prob_threshold=prob_threshold,
            volume_threshold=volume_threshold,
            prediction_index=prediction_index,
            apply_softmax=apply_softmax,
            raw_im_key=raw_im_key,
            follicle_labels_key=follicle_labels_key,
            ovary_segmentation_key=ovary_segmentation_key,
            prediction_key=prediction_key,
        )
