import glob
import os
from typing import List, Union, Tuple

import h5py
import numpy as np
import pandas as pd
import umetrics
from scipy.special import softmax
from skimage.measure import regionprops_table

from ..io.hdf5_io import load_im_from_hdf
from .follicles import post_process_follicles, process_follicle_labels
from .ovary import post_process_ovary
from ..utils.submission_utils import get_fold_directories


def _calc_effective_diameter(volumes: np.ndarray) -> np.ndarray:
    """Calculate the effective diameter of an object from
    its volume.

    Parameters
    ----------
    volumes : np.ndarray
        The array of image volumes to calculate the diameters from.

    Returns
    -------
    diameters : np.ndarray
        The calculated diameters. These are index matched
        to volumes.
    """
    return 2 * np.power(volumes * 0.75 / np.pi, 1 / 3)


def _classify_diameters(diameters: np.ndarray) -> List[str]:
    # classify the follicles
    follicle_class = []
    for d in diameters:
        if d < 2:
            follicle_class.append('<2')
        elif (d >= 2) and (d < 5):
            follicle_class.append('2-5')
        elif (d >= 5) and (d <= 10):
            follicle_class.append('5-10')
        elif d > 10:
            follicle_class.append('>10')
        else:
            raise ValueError('bad follicle diameter')
    return follicle_class


def _classify_labels(
    label_im: np.ndarray,
    indices: Union[List[int], np.ndarray],
    voxel_size_mm3: float,
) -> pd.DataFrame:
    """Classify objects by their effective diameter. The classes
    are <2, 2-5, 5-10, and >10 mm.


    Parameters
    ----------
    label_im : np.ndarray
        The label image from which to calculate properties.
    indices : List[int]
        The label indices to classify.
    voxel_size_mm3 : float
        The volume of one voxel in the label_im in mm^3


    Returns
    -------
    follicle_class_table : pd.DataFrame
        The table containing the class for each follicle. The follicle has
        the following columns:
            label: the label value in the prediction image.
            volume_px: the volume of the object in voxels
            volume_mm3: the volume of the object in mm^3
            diameter_mm: the calculated effective diameter in mm
            follicle_class: the class of the follicle (<2, 2-5, 5-10, >10)
    """
    rp_table = regionprops_table(label_im, properties=('label', 'area'))

    areas_to_measure = []
    indices = [i for i in indices if i != 0]
    labels_list = list(rp_table['label'])
    for label_list_index in indices:
        label_index = labels_list.index(label_list_index)
        areas_to_measure.append(rp_table['area'][label_index])
    areas_to_measure = np.asarray(areas_to_measure)

    # calculate the follicle volume/diameter
    areas_mm = voxel_size_mm3 * areas_to_measure
    diameters = _calc_effective_diameter(areas_mm)
    follicle_class = _classify_diameters(diameters)

    follicle_class_table = pd.DataFrame(
        {
            'label': indices,
            'volume_px': areas_to_measure,
            'volume_mm3': areas_mm,
            'diameter_mm': diameters,
            'follicle_class': follicle_class,
        }
    )
    return follicle_class_table


def quantify_performance(
    ref_im: np.ndarray,
    pred_im: np.ndarray,
    im_path: str,
    voxel_size_mm3: float,
    iou_threshold: float = 0.5,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Measure the precision and recall of an image segmentation.

    Parameters
    ----------
    ref_im : np.ndarray
        The ground truth reference image. Must be a label image.
    pred_im: np.ndarray
        The predicted segmentation. Must be a label image.
    im_path : str
        The file path of the prediction image.
    voxel_size_mm3 : float
        The volume of a voxel im mm^3.
    iou_threshold : float
        The minimum intersection over union value for a candidate match
        to be considered a true positive. Default value is 0.5.

    Returns
    -------
    metrics_table : pd.DataFrame
        The table of classification for each follicle. This table
        has columns:
            label: the label value in the prediction image
            volume_px: the volume of the object in voxels
            volume_mm3: the volume of the object in mm^3
            diameter_mm: the calculated effective diameter in mm
            follicle_class: the class of the follicle (<2, 2-5, 5-10, >10)
            file_path: the path to the prediction file
            iou_thresh: the IOU threshold used for calling true positives
    true_positive_table : pd.DataFrame
        The table of true positive label pairs (ref and prediction).
        The table has columns:
            label_ref: the label value in the reference image
            label_pred: the label value in the predicted image
            file_path: the path to the prediction file
            iou_thresh: the IOU threshold used for calling true positives
    """
    result = umetrics.calculate(
        ref_im, pred_im, strict=True, iou_threshold=iou_threshold
    )

    # get the true positive labels for the pred im
    tp_labels = [r[1] for r in result.true_positives]

    tp_table = _classify_labels(
        label_im=pred_im, indices=tp_labels, voxel_size_mm3=voxel_size_mm3
    )
    tp_table['seg_class'] = 'tp'

    # get the false positive data
    fp_labels = result.false_positives
    fp_table = _classify_labels(
        label_im=pred_im, indices=fp_labels, voxel_size_mm3=voxel_size_mm3
    )
    fp_table['seg_class'] = 'fp'

    # get the false negative data
    fn_labels = result.false_negatives
    fn_table = _classify_labels(
        label_im=ref_im, indices=fn_labels, voxel_size_mm3=voxel_size_mm3
    )
    fn_table['seg_class'] = 'fn'

    # get the split follicles
    split_ref_indices = []
    split_pred_indices = []
    for ref_index, pred_indices in result.split_errors:
        split_ref_indices.append(ref_index)
        split_pred_indices += pred_indices
    split_ref_table = _classify_labels(
        label_im=ref_im,
        indices=split_ref_indices,
        voxel_size_mm3=voxel_size_mm3,
    )
    split_ref_table['seg_class'] = 'split_ref'
    split_pred_table = _classify_labels(
        label_im=pred_im,
        indices=split_pred_indices,
        voxel_size_mm3=voxel_size_mm3,
    )
    split_pred_table['seg_class'] = 'split_pred'

    # get the merged follicles
    merge_ref_indices = []
    merge_pred_indices = []
    for pred_index, ref_indices in result.merge_errors:
        merge_ref_indices += ref_indices
        merge_pred_indices.append(pred_index)
    merge_ref_table = _classify_labels(
        label_im=ref_im,
        indices=merge_ref_indices,
        voxel_size_mm3=voxel_size_mm3,
    )
    merge_ref_table['seg_class'] = 'merge_ref'
    merge_pred_table = _classify_labels(
        label_im=pred_im,
        indices=merge_pred_indices,
        voxel_size_mm3=voxel_size_mm3,
    )
    merge_pred_table['seg_class'] = 'merge_pred'

    # get the ref labels not matching
    # all_ref_labels = np.unique(ref_im)
    # fn_labels = result.false_negatives
    # tp_ref_labels = [r[0] for r in result.true_positives]
    # un_ref_labels = [
    #     l for l in all_ref_labels if not (l in tp_ref_labels) and not (l in fn_labels)
    # ]
    # un_ref_table = _classify_labels(
    #     label_im=ref_im,
    #     indices=un_ref_labels,
    #     voxel_size_mm3=voxel_size_mm3
    #
    # )
    # un_ref_table['seg_class'] = 'unassigned_ref'
    #
    # # get the pred labels not matching
    all_pred_labels = np.unique(pred_im)
    un_pred_labels = [
        label_index
        for label_index in all_pred_labels
        if not (label_index in tp_labels)
        and not (label_index in fp_labels)
        and not (label_index in merge_pred_indices)
    ]
    un_pred_table = _classify_labels(
        label_im=pred_im, indices=un_pred_labels, voxel_size_mm3=voxel_size_mm3
    )
    un_pred_table['seg_class'] = 'unassigned_pred'

    # make sure all labels accounted for
    ref_labels = set(np.unique(ref_im))
    tp_ref_labels = [r[0] for r in result.true_positives]
    found_ref_labels = set.union(
        set(tp_ref_labels),
        set(fn_labels),
        set(split_ref_indices),
        set(merge_ref_indices),
        {0},
    )
    try:
        assert ref_labels == found_ref_labels
    except AssertionError:
        print(f'ref: {ref_labels}\nfound ref: {found_ref_labels}')

    pred_labels = set(np.unique(pred_im))
    found_pred_labels = set.union(
        set(tp_labels),
        set(fp_labels),
        set(split_pred_indices),
        set(merge_pred_indices),
        set(un_pred_labels),
        {0},
    )
    try:
        assert pred_labels == found_pred_labels
    except AssertionError:
        print(f'pred: {pred_labels}\nfound pred: {found_pred_labels}')

    # concatenate into single table
    metrics_table = pd.concat(
        [
            tp_table,
            fp_table,
            fn_table,
            split_ref_table,
            split_pred_table,
            merge_ref_table,
            merge_pred_table,
            un_pred_table,
        ]
    )
    metrics_table['file_path'] = im_path
    metrics_table['iou_thresh'] = iou_threshold

    # create the table of true positives
    true_positive_table = pd.DataFrame(
        {
            'label_ref': tp_ref_labels,
            'label_pred': tp_labels,
        }
    )
    true_positive_table['file_path'] = im_path
    true_positive_table['iou_thresh'] = iou_threshold

    return metrics_table, true_positive_table


def calculate_segmentation_performance(
    metrics_table: pd.DataFrame,
) -> Tuple[float, float]:
    """Calculate precision and recall for a set of predictions.

    Parameters
    ----------
    metrics_table : pd.DataFrame
        The table of tp/fp results from a set of segmentations

    Returns
    -------
    recall : float
        The recall, TP / (TP + FN)
    precision : float
        The precision, TP / (TP + FP)
    """
    value_counts = metrics_table['seg_class'].value_counts()

    try:
        n_tp = value_counts['tp']
    except KeyError:
        n_tp = 0

    try:
        n_fn = value_counts['fn']
    except KeyError:
        n_fn = 0

    try:
        n_fp = value_counts['fp']
    except KeyError:
        n_fp = 0

    try:
        n_unassigned_pred = value_counts['unassigned_pred']
    except KeyError:
        n_unassigned_pred = 0

    try:
        n_unassigned_ref = value_counts['unassigned_ref']
    except KeyError:
        n_unassigned_ref = 0

    try:
        recall = n_tp / (n_tp + n_fn + n_unassigned_ref)
        precision = n_tp / (n_tp + n_fp + n_unassigned_pred)
    except ZeroDivisionError:
        recall = np.nan
        precision = np.nan

    return recall, precision


def calculate_segmentation_performance_by_class(
    metrics_table: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate the segmentation performance for each follicle class
    in the data set.

    The supported follicle classes are <2, 2-5, 5-10, and >10 mm diameters.

    Parameters
    ----------
    metrics_table : pd.DataFrame
        The table of segmentation results for the dataset. Must have a 'follicle_class'
        column and a seg_class column.

    Returns
    -------
    seg_performance_table : pd.DataFrame
        The resulting prediction and recall for each class.
    """
    small_fol_metrics = metrics_table.loc[
        metrics_table['follicle_class'] == '<2'
    ]
    small_r, small_p = calculate_segmentation_performance(small_fol_metrics)

    small_ant_fol_metrics = metrics_table.loc[
        metrics_table['follicle_class'] == '2-5'
    ]
    small_ant_r, small_ant_p = calculate_segmentation_performance(
        small_ant_fol_metrics
    )

    med_fol_metrics = metrics_table.loc[
        metrics_table['follicle_class'] == '5-10'
    ]
    med_r, med_p = calculate_segmentation_performance(med_fol_metrics)

    large_fol_metrics = metrics_table.loc[
        metrics_table['follicle_class'] == '>10'
    ]
    large_r, large_p = calculate_segmentation_performance(large_fol_metrics)

    seg_performance_table = pd.DataFrame(
        {
            'recall_<2': [small_r],
            'precision_<2': [small_p],
            'recall_2-5': [small_ant_r],
            'precision_2-5': [small_ant_p],
            'recall_5-10': [med_r],
            'precision_5-10': [med_p],
            'recall_>10': [large_r],
            'precision_>10': [large_p],
        }
    )
    return seg_performance_table


def quantify_performance_from_folder(
    prob_thresholds: List[float],
    iou_thresh: float,
    volume_threshold: float,
    voxel_size_mm3: float,
    predictions_dir: str,
    prediction_index: int,
    ref_dir: str,
    ref_file_pattern: str = '*.h5',
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Quantify segmentation performance

    Parameters
    ----------
    prob_thresholds
    iou_thresh
    volume_threshold
    voxel_size_mm3
    predictions_dir
    prediction_index
    ref_dir
    ref_file_pattern

    Returns
    -------

    """
    all_ref_fnames = glob.glob(os.path.join(ref_dir, ref_file_pattern))

    all_metrics_data = []
    all_true_positives = []
    for raw_fpath in all_ref_fnames:
        prediction_fname = os.path.basename(raw_fpath).replace(
            '.h5', '_predictions.h5'
        )
        prediction_fpath = os.path.join(predictions_dir, prediction_fname)
        with h5py.File(prediction_fpath, 'r') as f_pred:
            prediction_im = f_pred['predictions'][:]

        with h5py.File(raw_fpath, 'r') as f_raw:
            follicle_labels = f_raw['follicle_labels_rescaled'][:]
            ovary_labels = f_raw['ovary_labels_rescaled'][:]

        follicle_labels_clean = process_follicle_labels(
            follicle_labels=follicle_labels, volume_threshold=volume_threshold
        )

        metrics = []
        true_positives = []
        for thresh in prob_thresholds:
            follicle_seg = post_process_follicles(
                follicle_prediction=prediction_im,
                ovary_seg=ovary_labels,
                prob_threshold=thresh,
                volume_threshold=volume_threshold,
                prediction_index=prediction_index,
            )

            metrics_table, tp_table = quantify_performance(
                ref_im=follicle_labels_clean,
                pred_im=follicle_seg,
                im_path=prediction_fpath,
                voxel_size_mm3=voxel_size_mm3,
                iou_threshold=iou_thresh,
            )
            metrics_table['prob_threshold'] = thresh
            metrics.append(metrics_table)

            tp_table['prob_threshold'] = thresh
            true_positives.append(tp_table)

        image_metrics = pd.concat(metrics)
        all_metrics_data.append(image_metrics)

        all_true_positives.append(pd.concat(true_positives))

    all_metrics = pd.concat(all_metrics_data)
    all_tp_table = pd.concat(all_true_positives)

    all_seg_metrics = []

    for thresh in prob_thresholds:
        thresh_metrics = all_metrics.loc[
            all_metrics['prob_threshold'] == thresh
        ]

        seg_metrics = calculate_segmentation_performance_by_class(
            thresh_metrics
        )
        seg_metrics['prob_threshold'] = thresh

        all_seg_metrics.append(seg_metrics)

    seg_metrics = pd.concat(all_seg_metrics)

    return all_metrics, all_tp_table, seg_metrics


def quantify_performance_from_crossval(
    crossval_dir: str,
    fold_dir_pattern: str,
    prob_thresholds: List[float],
    iou_thresh: float,
    volume_threshold: float,
    voxel_size_mm3: float,
    predictions_dir_name: str,
    prediction_index: int,
    ref_dir_name: str,
    ref_file_pattern: str = '*.h5',
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    fold_directories = get_fold_directories(
        base_dir=crossval_dir, fold_dir_pattern=fold_dir_pattern
    )
    performance_tables = []
    tp_tables = []
    seg_metrics_tables = []

    for fold_index, fold_directory in fold_directories:
        ref_dir_path = os.path.join(fold_directory, ref_dir_name)
        prediction_dir_path = os.path.join(
            fold_directory, predictions_dir_name
        )

        (
            fold_performance_metrics,
            fold_tp_table,
            fold_seg_metrics,
        ) = quantify_performance_from_folder(
            prob_thresholds=prob_thresholds,
            iou_thresh=iou_thresh,
            volume_threshold=volume_threshold,
            voxel_size_mm3=voxel_size_mm3,
            predictions_dir=prediction_dir_path,
            prediction_index=prediction_index,
            ref_dir=ref_dir_path,
            ref_file_pattern=ref_file_pattern,
        )

        # add the fold index and path
        fold_performance_metrics['fold_index'] = fold_index
        fold_performance_metrics['fold_path'] = fold_directory
        fold_tp_table['fold_index'] = fold_index
        fold_tp_table['fold_path'] = fold_directory
        fold_seg_metrics['fold_index'] = fold_index
        fold_seg_metrics['fold_path'] = fold_directory

        performance_tables.append(fold_performance_metrics)
        tp_tables.append(fold_tp_table)
        seg_metrics_tables.append(fold_seg_metrics)

    return (
        pd.concat(performance_tables, ignore_index=True),
        pd.concat(tp_tables, ignore_index=True),
        pd.concat(seg_metrics_tables, ignore_index=True),
    )


def measure_iou(
    mask_reference: np.ndarray, mask_prediction: np.ndarray
) -> float:
    """Calculate the intersection over union of a segmentation.

    Parameters
    ----------
    mask_reference : np.ndarray
        The reference segmentation.
    mask_prediction : np.ndarray
        The predicted segmentation.

    Returns
    -------
    iou : float
        The intersection over union.
    """
    intersection = np.logical_and(mask_reference, mask_prediction)
    union = np.logical_or(mask_reference, mask_prediction)
    return np.sum(intersection) / np.sum(union)


def measure_iou_from_fold(
    fold_dir_path: str,
    ref_dir: str,
    prediction_dir: str,
    thresholds: List[float],
    prediction_index: int = 1,
    apply_softmax: bool = True,
    label_key: str = 'ovary_labels_rescaled',
    prediction_key: str = 'predictions',
) -> pd.DataFrame:
    # get the files in the raw dir
    ref_dir_path = os.path.join(fold_dir_path, ref_dir)
    ref_file_pattern = os.path.join(ref_dir_path, "*.h5")
    ref_files = glob.glob(ref_file_pattern)

    # iterate through the raw dir
    ious = []
    table_thresholds = []
    file_paths = []
    fold_dirs = []
    for ref_fpath in ref_files:
        # load the raw image
        ref_im = load_im_from_hdf(ref_fpath, label_key)

        # load the prediction
        prediction_fname = os.path.basename(ref_fpath).replace(
            ".h5", "_predictions.h5"
        )
        prediction_fpath = os.path.join(
            fold_dir_path, prediction_dir, prediction_fname
        )
        prediction_im = load_im_from_hdf(prediction_fpath, prediction_key)

        if apply_softmax is True:
            prediction_im = softmax(prediction_im, axis=0)
        prediction_im = prediction_im[prediction_index, ...]

        for thresh in thresholds:
            # segment the prediction
            prediction_mask = post_process_ovary(
                ovary_prediction=prediction_im,
                raw_im=None,
                threshold=thresh,
                dilation_size=None,
                mask_padding=False,
            )
            ref_mask = ref_im.astype(bool)

            ious.append(measure_iou(ref_mask, prediction_mask))
            table_thresholds.append(thresh)
            file_paths.append(prediction_fpath)
            fold_dirs.append(fold_dir_path)

    return pd.DataFrame(
        {
            'fold_path': fold_dirs,
            'file_path': file_paths,
            'threshold': table_thresholds,
            'iou': ious,
        }
    )


def measure_iou_from_crossval(
    crossval_dir: str,
    fold_dir_pattern: str,
    ref_dir: str,
    prediction_dir: str,
    thresholds: List[float],
    prediction_index: int = 1,
    apply_softmax: bool = True,
    label_key: str = 'ovary_labels_rescaled',
    prediction_key: str = 'predictions',
) -> pd.DataFrame:
    fold_directories = get_fold_directories(
        base_dir=crossval_dir, fold_dir_pattern=fold_dir_pattern
    )

    measurement_tables = []
    for fold_index, fold_directory in fold_directories:
        measurement_tables.append(
            measure_iou_from_fold(
                fold_dir_path=fold_directory,
                ref_dir=ref_dir,
                prediction_dir=prediction_dir,
                thresholds=thresholds,
                prediction_index=prediction_index,
                apply_softmax=apply_softmax,
                label_key=label_key,
                prediction_key=prediction_key,
            )
        )
    return pd.concat(measurement_tables)
