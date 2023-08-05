from functools import partial
import glob
import os
from typing import Optional, Union, List

import numpy as np
from scipy import ndimage
from scipy.special import softmax
from skimage.measure import regionprops_table
from skimage.morphology import binary_dilation, cube

from ..io.hdf5_io import load_im_from_hdf, write_multi_dataset_hdf, load_raw_im


def post_process_ovary(
    ovary_prediction: np.ndarray,
    raw_im: np.ndarray,
    threshold: float = 0.8,
    dilation_size: Optional[int] = None,
    mask_padding: bool = True,
) -> np.ndarray:
    ovary_mask = np.zeros_like(ovary_prediction, dtype=np.bool)

    # mask out the padding region of the image
    if mask_padding is True:
        ovary_prediction[raw_im == 0] = 0
    ovary_mask[ovary_prediction >= threshold] = True

    # filter for the largest object
    ovary_mask = ndimage.binary_fill_holes(ovary_mask)
    ovary_labels = ndimage.label(ovary_mask)[0]
    region_props = regionprops_table(
        ovary_labels, properties=['label', 'area']
    )
    if len(region_props['label']) > 1:
        max_area_ind = np.argmax(region_props['area'])
        max_label = region_props['label'][max_area_ind]
        ovary_mask[ovary_labels != max_label] = False

    # apply the dilation is requested
    if dilation_size is not None:
        ovary_mask = binary_dilation(ovary_mask, selem=cube(dilation_size))

    return ovary_mask


def segment_ovary_from_prediction(
    prediction_path: Union[str, os.PathLike],
    raw_im_path: Union[str, os.PathLike],
    output_dir: Union[str, os.PathLike],
    threshold: float = 0.8,
    apply_sigmoid: bool = False,
    apply_softmax: bool = False,
    prediction_index: int = 0,
    dilation_size: Optional[int] = None,
    mask_padding: bool = True,
    raw_im_key: str = 'raw_rescaled',
    follicle_labels_key: str = 'follicle_labels_rescaled',
    ovary_labels_key: str = 'ovary_labels_rescaled',
    prediction_key: str = 'predictions',
) -> str:
    """Segment an ovary image from CNN predictions.

    Parameters
    ----------
    prediction_path : Union[str, os.PathLike]
        The path to the predictions file.
    raw_im_path : Union[str, os.PathLike]
        The path to the raw image file. This will be the dataset
        the predictions were made from.
    output_dir : Union[str, os.PathLike]
        The path to the directory the segmentation should be saved to.
    threshold : float
        The probability threshold for binarizing the image.
        The default value is 0.8.
    dilation_size : Optional[int]
        The size of the morphological dilation to apply following binarization
        of the probabilities image. If None is give, no dilation is performed.
        The default value is None.
    raw_im_key : str
        The key in the raw_im file to access to the raw image dataset.
        The default value is raw_rescaled.
    follicle_labels_key : str
        The key in the raw_im file to access to the follicle labels dataset.
        The default value is follicle_labels_rescaled.
    ovary_labels_key : str
        The key in the raw_im file to access to the follicle labels dataset.
        The default value is 'ovary_labels_rescaled'
    prediction_key : str
        The key in the raw_im file to access to the follicle labels dataset.
        The default value is 'predictions'

    Returns
    -------
    output_fpath : str
        The path to the resulting segmentation.
    """
    # load the images
    prediction = load_im_from_hdf(
        fpath=prediction_path, dataset_key=prediction_key
    )
    _, _, raw_rescaled, rescaled_attrs = load_raw_im(
        fpath=raw_im_path, rescaled_name=raw_im_key
    )

    if follicle_labels_key is not None:
        follicle_labels = load_im_from_hdf(
            fpath=raw_im_path, dataset_key=follicle_labels_key
        )
    else:
        follicle_labels = None

    if ovary_labels_key is not None:
        ovary_labels = load_im_from_hdf(
            fpath=raw_im_path, dataset_key=ovary_labels_key
        )
    else:
        ovary_labels = None

    if (apply_sigmoid is True) and (apply_softmax is True):
        raise ValueError('apply_sigmoid and apply_softmax cannot both be True')
    elif apply_sigmoid is True:
        prediction = prediction[prediction_index, ...]
        prediction = 1 / (1 + np.exp(-prediction))
    elif apply_softmax is True:
        prediction = softmax(prediction, axis=0)
        prediction = prediction[prediction_index, ...]

    # segment the ovary
    ovary_segmentation = post_process_ovary(
        ovary_prediction=prediction,
        raw_im=raw_rescaled,
        threshold=threshold,
        dilation_size=dilation_size,
        mask_padding=mask_padding,
    )

    # save the segmentation
    output_fname = os.path.basename(prediction_path).replace(
        '_predictions.', '_segmentation.'
    )
    output_fpath = os.path.join(output_dir, output_fname)
    rescaled_dataset = {'data': raw_rescaled, 'attrs': rescaled_attrs}

    if (follicle_labels is not None) and (ovary_labels is not None):
        write_multi_dataset_hdf(
            file_path=output_fpath,
            compression='gzip',
            raw_rescaled=rescaled_dataset,
            follicle_labels_rescaled=follicle_labels,
            ovary_labels_rescaled=ovary_labels,
            ovary_segmentation_rescaled=ovary_segmentation,
        )
    else:
        write_multi_dataset_hdf(
            file_path=output_fpath,
            compression='gzip',
            raw_rescaled=rescaled_dataset,
            ovary_segmentation_rescaled=ovary_segmentation,
        )

    return output_fpath


def segment_ovary_dir(
    dir_path: Union[str, os.PathLike],
    raw_im_dir: Union[str, os.PathLike],
    predictions_subdir: str,
    output_dir_name: Union[str, os.PathLike],
    threshold: float = 0.8,
    apply_sigmoid: bool = False,
    apply_softmax: bool = False,
    prediction_index: int = 0,
    dilation_size: Optional[int] = None,
    mask_padding: bool = True,
    raw_im_key: str = 'raw_rescaled',
    follicle_labels_key: str = 'follicle_labels_rescaled',
    ovary_labels_key: str = 'ovary_labels_rescaled',
    prediction_key: str = 'predictions',
) -> List[str]:
    predictions_dir = os.path.join(dir_path, predictions_subdir)
    predictions_pattern = os.path.join(predictions_dir, '*_predictions.h5')
    prediction_files = glob.glob(predictions_pattern)

    output_dir_fpath = os.path.join(dir_path, output_dir_name)
    if not os.path.isdir(output_dir_fpath):
        os.mkdir(output_dir_fpath)

    segmentation_fpaths = []
    for prediction in prediction_files:
        raw_im_name = os.path.basename(prediction).replace(
            '_predictions.', '.'
        )
        raw_im_path = os.path.join(raw_im_dir, raw_im_name)
        seg_path = segment_ovary_from_prediction(
            prediction_path=prediction,
            raw_im_path=raw_im_path,
            output_dir=output_dir_fpath,
            threshold=threshold,
            dilation_size=dilation_size,
            mask_padding=mask_padding,
            apply_sigmoid=apply_sigmoid,
            apply_softmax=apply_softmax,
            prediction_index=prediction_index,
            raw_im_key=raw_im_key,
            follicle_labels_key=follicle_labels_key,
            ovary_labels_key=ovary_labels_key,
            prediction_key=prediction_key,
        )

        segmentation_fpaths.append(seg_path)

    return segmentation_fpaths


def post_process_ovary_cross_val(
    crossval_dir: Union[str, os.PathLike],
    ovary_datasets_dir: Union[str, os.PathLike],
    predictions_subdir: str,
    output_dir_name: Union[str, os.PathLike],
    threshold: float = 0.8,
    apply_sigmoid: bool = False,
    apply_softmax: bool = False,
    prediction_index: int = 0,
    dilation_size: Optional[int] = None,
    mask_padding: bool = True,
    raw_im_key: str = 'raw_rescaled',
    follicle_labels_key: str = 'follicle_labels_rescaled',
    ovary_labels_key: str = 'ovary_labels_rescaled',
    prediction_key: str = 'predictions',
):
    # get the fold directories
    folder_pattern = os.path.join(crossval_dir, 'fold_*', '')
    fold_candidates = glob.glob(folder_pattern)

    # make sure they are directories
    fold_dirs = [f for f in fold_candidates if os.path.isdir(f)]
    n_fold = len(fold_dirs)
    print(f'processing {n_fold} folds')

    # make the base function
    process_func = partial(
        segment_ovary_dir,
        raw_im_dir=ovary_datasets_dir,
        predictions_subdir=predictions_subdir,
        output_dir_name=output_dir_name,
        threshold=threshold,
        apply_sigmoid=apply_sigmoid,
        apply_softmax=apply_softmax,
        prediction_index=prediction_index,
        dilation_size=dilation_size,
        mask_padding=mask_padding,
        raw_im_key=raw_im_key,
        follicle_labels_key=follicle_labels_key,
        ovary_labels_key=ovary_labels_key,
        prediction_key=prediction_key,
    )

    for folder in fold_dirs:
        process_func(folder)
