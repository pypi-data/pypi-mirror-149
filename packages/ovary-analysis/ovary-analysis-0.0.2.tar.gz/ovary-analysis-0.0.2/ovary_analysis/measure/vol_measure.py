import multiprocessing as mp
import glob
import os
from functools import partial

import h5py
import numpy as np
import pandas as pd
from scipy import ndimage as ndi
from skimage.measure import regionprops_table

from .measure_utils import binary_mask_to_surface
from ..utils.file_names import parse_seg_fname
from ..utils.submission_utils import get_fold_directories


def measure_surface_area_from_labels(
    label_image: np.ndarray, n_mesh_smoothing_interations: int = 10
) -> pd.DataFrame:
    """Measure the surface measurement of each object in a label image.

    Parameters
    ----------
    label_image : LabelImage
        The label image from which to measure the surface properties.
    n_mesh_smoothing_interations : int
        The number of interations of smooting to perform. Smoothing is
        done by the trimesh laplacian filter:
        https://trimsh.org/trimesh.smoothing.html#trimesh.smoothing.filter_laplacian
        Default value is 50.

    Returns
    -------
    surface_properties_table : LabelMeasurementTable
        The measured surface properties. Each measurement is a column and each
        object is a row.
    """
    if label_image.ndim != 3:
        raise ValueError(
            "measure_surface_properties_from_labels requires a 3D label image"
        )

    all_label_indices = np.unique(label_image)
    surface_areas = []
    labels = []
    for label_index in all_label_indices:
        if label_index == 0:
            # background is assumed to be label 0
            continue
        try:
            label_mask = label_image == label_index
            smoothed_mesh = binary_mask_to_surface(
                label_mask,
                n_mesh_smoothing_interations=n_mesh_smoothing_interations,
            )
            surface_area = smoothed_mesh.area
        except ValueError:
            # if the meshing fails set surface area to 0
            surface_area = 0
        labels.append(label_index)
        surface_areas.append(surface_area)

    surface_properties_table = pd.DataFrame(
        {"label_index": labels, "surface_area": surface_areas}
    )

    return surface_properties_table.set_index("label_index")


def measure_image(
    label_im: np.ndarray, n_mesh_smoothing_interations: int = 10
) -> pd.DataFrame:
    """The volume of the labeled objects.

    Parameters
    ----------
    label_im : str
        directory of labeled three dimensional image
    n_mesh_smoothing_interations : int
        The number of interations of smooting to perform. Smoothing is
        done by the trimesh laplacian filter:
        https://trimsh.org/trimesh.smoothing.html#trimesh.smoothing.filter_laplacian
        Default value is 50.

    Returns
    -------
    df : pandas dataframe
        label of the follicles
        centroid in three dimensional image
        number of pixels included in each labeled objects
    """
    # measure volumes
    props = regionprops_table(
        label_im, properties=("label", "centroid", "area")
    )
    volume_df = pd.DataFrame(props).rename(
        columns={"label": "label_index", "area": "volume"}
    )
    volume_df.set_index("label_index", inplace=True)

    # measure surface area
    surface_area_df = measure_surface_area_from_labels(
        label_image=label_im,
        n_mesh_smoothing_interations=n_mesh_smoothing_interations,
    )

    return pd.concat((volume_df, surface_area_df), axis=1).reset_index()


def process_image(
    file_path: str, follicles_key: str = 'follicle_segmentation_rescaled'
) -> pd.DataFrame:
    """This function takes a file path, loads the image and passes it to the measurement function(s).
    It then returns the dataframe with the measured properties.

    Parameters
    ----------
    file_path : str
        directory of images

    Returns
    -------
    df : pandas dataframe
        dataframe includes filename, label, centroid, and volume from one image
    """
    file_name = os.path.split(file_path)[1]
    file_name = file_name.replace(".h5", "")

    with h5py.File(file_path, "r") as f_raw:
        follicle_labels = f_raw[follicles_key][:]
        label_im, _ = ndi.label(follicle_labels)
        df = measure_image(label_im)
        patient_id, cycle, side, date = parse_seg_fname(file_name)
        df["patient_id"] = patient_id
        df["cycle"] = cycle
        df["side"] = side
        df["date"] = date
        df["file_path"] = file_path
        return df


def measure_dir(
    dir_path: str,
    file_pattern: str = "*.h5",
    follicles_key: str = 'follicle_segmentation_rescaled',
) -> pd.DataFrame:
    """measure the volume and centroid (multi-processing) of all images in one path. concat them into one data frame

    Parameters
    ----------
    dir_path : str
        directory of folder with images
    file_pattern : str
        data type of images

    Returns
    -------
    df : pandas dataframe
        dataframe includes filename, label, centroid, and volume from all images
    """

    # walk through the path and get the directory
    datapath = os.path.join(dir_path, file_pattern)

    # glob code to get the list of files
    image_files = glob.glob(datapath)

    process_func = partial(process_image, follicles_key=follicles_key)

    # multiprocessing to map process_image() to the files
    with mp.get_context("spawn").Pool() as pool:
        results = pool.map(process_func, image_files)

    # concatenate the results into a single df
    df = pd.concat(results, ignore_index=True)
    return df


def measure_cross_val(
    cross_val_dir_path: str,
    segmentation_folder_name: str,
    fold_dir_pattern: str = "fold_*",
    file_pattern: str = "*.h5",
    follicles_key: str = 'follicle_segmentation_rescaled',
) -> pd.DataFrame:
    fold_directories = get_fold_directories(
        base_dir=cross_val_dir_path, fold_dir_pattern=fold_dir_pattern
    )
    measurements = []

    for fold_index, fold_directory in fold_directories:
        segmentation_directory_path = os.path.join(
            fold_directory, segmentation_folder_name
        )
        measurement_table = measure_dir(
            dir_path=segmentation_directory_path,
            file_pattern=file_pattern,
            follicles_key=follicles_key,
        )
        measurement_table['fold_index'] = fold_index
        measurement_table['fold_directory'] = fold_directory
        measurements.append(measurement_table)

    return pd.concat(measurements, ignore_index=True)
