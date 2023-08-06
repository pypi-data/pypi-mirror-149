import os
from typing import Tuple

import numpy as np
import open3d as o3d
import pandas as pd
from scipy.spatial import ConvexHull
from skimage.segmentation import flood_fill
from tqdm.auto import tqdm

from ..io.hdf5_io import write_multi_dataset_hdf
from ..io.label_im import load_label_im
from ..utils.image import rescale_label_im
from ..utils.time import date_to_datestring


def generate_mesh(coords: np.ndarray) -> o3d.geometry.TriangleMesh:
    hull = ConvexHull(coords)
    vertices = hull.points[hull.vertices]

    vertex_lookup = {v: i for i, v in enumerate(hull.vertices)}

    faces = np.zeros_like(hull.simplices, dtype=np.int)

    for i, row in enumerate(hull.simplices):
        for j, element in enumerate(row):
            faces[i, j] = vertex_lookup[element]

    verts_o3d = o3d.utility.Vector3dVector(vertices)
    faces_o3d = o3d.utility.Vector3iVector(faces)

    mesh = o3d.geometry.TriangleMesh(vertices=verts_o3d, triangles=faces_o3d)

    return mesh


def mesh_to_binary(
    mesh: o3d.geometry.TriangleMesh, image_shape: Tuple[int, int, int]
) -> np.ndarray:
    assert mesh.is_watertight()

    voxel_grid = o3d.geometry.VoxelGrid.create_from_triangle_mesh(
        mesh, voxel_size=1
    )

    # query all voxels in the bounding box around the mesh
    min_bound = np.floor(voxel_grid.get_min_bound()) - 1
    max_bound = np.ceil(voxel_grid.get_max_bound()) + 1
    z_range = np.arange(min_bound[0], max_bound[0])
    x_range = np.arange(min_bound[1], max_bound[1])
    y_range = np.arange(min_bound[2], max_bound[2])

    all_coords = []
    for z in z_range:
        for x in x_range:
            for y in y_range:
                all_coords.append([z, x, y])

    coords_array = np.asarray(all_coords, dtype=np.int)
    in_mesh = voxel_grid.check_if_included(
        o3d.utility.Vector3dVector(coords_array)
    )
    coords_in_mesh = coords_array[in_mesh]

    # create the binary image
    binary_im = np.zeros(image_shape, dtype=np.int)
    binary_im[
        coords_in_mesh[:, 0], coords_in_mesh[:, 1], coords_in_mesh[:, 2]
    ] = 1

    # fill in the volume
    mesh_centroid = tuple(mesh.get_center().astype(np.int))
    filled_binary_im = flood_fill(binary_im, mesh_centroid, 1)

    return filled_binary_im


def fill_ovary_labels(sparse_ovary_labels: np.ndarray) -> np.ndarray:
    """Fill in sparse ovary labels to create a contiguous volume

    Parameters
    ----------
    sparse_ovary_labels :np.ndarray
        Label image where the outline of the ovary is sparsely labeled
        with non-zero values. All other voxels are 0.

    Returns
    -------
    filled_ovary_labels : np.ndarray
        Label image where all voxels corresponding to the ovary are labeled
    """
    coords = np.argwhere(sparse_ovary_labels)
    mesh = generate_mesh(coords)
    filled_ovary_labels = mesh_to_binary(
        mesh, image_shape=sparse_ovary_labels.shape
    )
    return filled_ovary_labels


def convert_labels(
    row: pd.Series,
    target_px_size: Tuple[float, float, float],
    output_dir: os.PathLike,
) -> os.PathLike:
    """Convert the raw labels to the training format.

    Parameters
    ----------
    row : pd.Series
        The row in the dataset table corresponding to the label image to be converted.
        The row should contain the following columns:
        ['patient', 'cycle', 'side', 'day', 'path_labels']
    target_px_size : Tuple[float, float, float]
        The target voxel size in mm/px. Should be in ZYX order.
    output_dir : os.PathLike
        The path to save the converted file to.

    Returns
    -------
    output_file_path : os.PathLike
        The path the converted file was saved to. The file follows the pattern:
        f'output_dir/{patient_id}_{cycle}_{side}_{date_string}_converted_labels.h5'
    """
    patient_id = row['patient']
    cycle = row['cycle']
    side = row['side']
    day = row['day']
    raw_labels_fpath = row['path_labels']

    label_im = load_label_im(raw_labels_fpath)

    # get the follicle labels
    follicle_labels = label_im[1, :, :, :].astype(np.uint8)
    follicle_labels[follicle_labels > 0] = 1

    # get the ovary labels (saved as contour)
    sparse_ovary_labels = label_im[0, :, :, :]

    # fill in the ovary labels
    filled_ovary_labels = fill_ovary_labels(sparse_ovary_labels).astype(
        np.uint8
    )

    # create the filename
    date_string = date_to_datestring(day)
    output_fname = (
        f'{patient_id}_{cycle}_{side}_{date_string}_converted_labels.h5'
    )

    # rescale the label images
    im_px_size = (row['px_size_z'], row['px_size_x'], row['px_size_y'])
    rescaled_follicle_labels = rescale_label_im(
        follicle_labels, im_px_size=im_px_size, target_px_size=target_px_size
    ).astype(bool)
    rescaled_ovary_labels = rescale_label_im(
        filled_ovary_labels,
        im_px_size=im_px_size,
        target_px_size=target_px_size,
    ).astype(bool)

    # create the dataset dicts for the rescaled labels
    rescaled_follicle_labels_data = {
        'data': rescaled_follicle_labels,
        'attrs': {'px_size': target_px_size},
    }
    rescaled_ovary_labels_data = {
        'data': rescaled_ovary_labels,
        'attrs': {'px_size': target_px_size},
    }

    # save the converted labels
    output_file_path = os.path.join(output_dir, output_fname)
    write_multi_dataset_hdf(
        file_path=output_file_path,
        compression='gzip',
        raw_labels=label_im,
        follicle_labels=follicle_labels,
        ovary_labels=filled_ovary_labels,
        rescaled_follicle_labels=rescaled_follicle_labels_data,
        rescaled_ovary_labels=rescaled_ovary_labels_data,
    )

    return output_file_path


def batch_convert_labels(
    dataset_table: pd.DataFrame,
    target_px_size: Tuple[float, float, float],
    output_dir: os.PathLike,
) -> pd.DataFrame:
    """Convert a batch of label images

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
        The input dataset_table with a `converted_labels_path` added
        containing the path to the converted files.
    """

    file_paths = []
    for i, row in tqdm(dataset_table.iterrows(), total=len(dataset_table)):

        file_path = convert_labels(
            row=row,
            target_px_size=target_px_size,
            output_dir=output_dir,
        )
        file_paths.append(file_path)
    dataset_table['converted_labels_path'] = file_paths

    return dataset_table
