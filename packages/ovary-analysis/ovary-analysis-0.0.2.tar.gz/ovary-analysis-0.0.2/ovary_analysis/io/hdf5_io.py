import os
from typing import Any, Dict, Optional, Tuple, Union

import h5py
import numpy as np


def load_raw_im(
    fpath: str, raw_name: str = 'raw', rescaled_name: str = 'raw_rescaled'
) -> Tuple[np.ndarray, Dict[str, Any], np.ndarray, Dict[str, Any]]:

    with h5py.File(fpath, 'r') as f_raw:
        raw_im = f_raw[raw_name][:]
        raw_attrs = dict(f_raw[raw_name].attrs.items())
        rescaled_im = f_raw[rescaled_name][:]
        rescaled_attrs = dict(f_raw[rescaled_name].attrs.items())

    return raw_im, raw_attrs, rescaled_im, rescaled_attrs


def load_im_from_hdf(
    fpath: Union[str, os.PathLike], dataset_key: str
) -> np.ndarray:
    """Load an image from an hdf5 file.

    Parameters
    ----------
    fpath : Union[str, os.PathLike]
        The path to the image file.
    dataset_key : str
        The key to load the data from.

    Returns
    -------
    im : np.ndarray
        The image that was loaded.
    """
    with h5py.File(fpath, 'r') as f:
        im = f[dataset_key][:]
    return im


def write_hdf(
    pixel_array: np.ndarray,
    fname: str,
    attrs: Optional[Dict[str, Any]] = None,
    dataset_name: str = 'image',
    compression: Optional[str] = None,
):
    """Write a pixel array to an hdf5 file

    Parameters
    ----------
    pixel_array : np.ndarray
        The pixel intensity data to write.
    fname : str
        The name of the file to write
    dataset_name : str
        The name for the dataset containing the pixel array.
        The default value is 'image'
    compression : Optional[str]
        The compression filter to apply to the data. Can be "gzip" or None.
        The default value is None.
    """
    with h5py.File(fname, 'w') as f:
        dset = f.create_dataset(
            dataset_name,
            pixel_array.shape,
            dtype=pixel_array.dtype,
            data=pixel_array,
            compression=compression,
        )
        if attrs is not None:
            for k, v in attrs.items():
                dset[k] = v


def write_raw(
    raw_im: np.ndarray,
    raw_px_size: Tuple[float, float, float],
    raw_path: str,
    rescaled_im: np.ndarray,
    rescaled_px_size: Tuple[float, float, float],
    fname: str,
    raw_name: str = 'raw',
    rescaled_name: str = 'raw_rescaled',
    compression: Optional[str] = None,
):
    """Write a pixel array to an hdf5 file

    Parameters
    ----------
    raw_im : np.ndarray
        The raw pixel intensity data to write.
    raw_px_size : Tuple[float, float, float]
        The size of each voxel in the raw image in mm / voxel
    raw_path : str
        The file path to the original raw image
    rescaled_im : np.ndarray
        The rescaled raw pixel intensity data to write.
    rescaled_px_size : Tuple[float, float, float]
        The size of each voxel in the rescaled image in mm / voxel
    fname : str
        The name of the file to write
    raw_name : str
        The name for the dataset containing the raw pixel array.
        The default value is 'raw'
    rescaled_name : str
        The name for the dataset containing the rescaled pixel array.
        The default value is 'raw_rescaled'
    compression : Optional[str]
        The compression filter to apply to the data. Can be "gzip" or None.
        The default value is None.
    """
    with h5py.File(fname, 'w') as f:
        raw = f.create_dataset(
            raw_name,
            raw_im.shape,
            dtype=raw_im.dtype,
            data=raw_im,
            compression=compression,
        )
        raw.attrs['px_size'] = raw_px_size
        raw.attrs['orig_path'] = raw_path

        rescaled = f.create_dataset(
            rescaled_name,
            rescaled_im.shape,
            dtype=rescaled_im.dtype,
            data=rescaled_im,
            compression=compression,
        )
        rescaled.attrs['px_size'] = rescaled_px_size


def write_training_data(
    raw_im: np.ndarray,
    follicle_im: np.ndarray,
    ovary_im: np.ndarray,
    file_path: str,
    raw_name: str = 'raw',
    raw_im_path: str = '',
    follicle_name: str = 'follicle_labels',
    follicle_im_path: str = '',
    ovary_name: str = 'ovary_labels',
    ovary_im_path: str = '',
    weights_im: Optional[np.ndarray] = None,
    weights_name: str = 'weights',
    multiclass_im: Optional[np.ndarray] = None,
    multiclass_name: str = 'multiclass_name',
    multiclass_one_hot_im: Optional[np.ndarray] = None,
    multiclass_one_hot_name: str = 'multiclass_one_hot',
    compression: Optional[str] = None,
):
    """Write a training dataset to an hdf5 file

    Parameters
    ----------
    raw_im : np.ndarray
        The raw image pixel intensity data to write.
    label_im : np.ndarray
        The the labeled image data to write.
    file_path : str
        The name of the file to write
    raw_name : str
        The name for the dataset containing the raw pixel array.
        The default value is 'raw'
    raw_name : str
        The name for the dataset containing the label pixel array.
        The default value is 'labels'
    compression : Optional[str]
        The compression filter to apply to the data. Can be "gzip" or None.
        The default value is None.
    """
    with h5py.File(file_path, 'w') as f:
        # write the image
        raw = f.create_dataset(
            raw_name,
            raw_im.shape,
            dtype=raw_im.dtype,
            data=raw_im,
            compression=compression,
        )
        raw.attrs['path'] = raw_im_path
        # write the labels
        follicles = f.create_dataset(
            follicle_name,
            follicle_im.shape,
            dtype=follicle_im.dtype,
            data=follicle_im,
            compression=compression,
        )
        follicles.attrs['path'] = follicle_im_path
        ovary = f.create_dataset(
            ovary_name,
            ovary_im.shape,
            dtype=ovary_im.dtype,
            data=ovary_im,
            compression=compression,
        )
        ovary.attrs['path'] = ovary_im_path

        if weights_im is not None:
            f.create_dataset(
                weights_name,
                weights_im.shape,
                dtype=weights_im.dtype,
                data=weights_im,
                compression=compression,
            )

        if multiclass_im is not None:
            f.create_dataset(
                multiclass_name,
                multiclass_im.shape,
                dtype=multiclass_im.dtype,
                data=multiclass_im,
                compression=compression,
            )
        if multiclass_one_hot_im is not None:
            f.create_dataset(
                multiclass_one_hot_name,
                multiclass_one_hot_im.shape,
                dtype=multiclass_one_hot_im.dtype,
                data=multiclass_one_hot_im,
                compression=compression,
            )


def _write_dataset_from_array(
    file_handle: h5py.File,
    dataset_name: str,
    dataset_array: np.ndarray,
    compression: str = 'gzip',
):
    file_handle.create_dataset(
        dataset_name,
        dataset_array.shape,
        dtype=dataset_array.dtype,
        data=dataset_array,
        compression=compression,
    )


def _write_dataset_from_dict(
    file_handle: h5py.File,
    dataset_name: str,
    dataset: Dict[str, Any],
    compression: str = 'gzip',
):
    dataset_array = dataset['data']
    dset = file_handle.create_dataset(
        dataset_name,
        dataset_array.shape,
        dtype=dataset_array.dtype,
        data=dataset_array,
        compression=compression,
    )

    dataset_attrs = dataset.get('attrs', None)
    if dataset_attrs is not None:
        for k, v in dataset_attrs.items():
            dset.attrs[k] = v


def write_multi_dataset_hdf(
    file_path: str, compression: str = 'gzip', **kwargs
):
    if len(kwargs) == 0:
        raise ValueError('Must supply at least one dataset as a kwarg')
    with h5py.File(file_path, 'w') as f:
        for k, v in kwargs.items():
            if isinstance(v, np.ndarray):
                _write_dataset_from_array(
                    file_handle=f,
                    dataset_name=k,
                    dataset_array=v,
                    compression=compression,
                )
            else:
                _write_dataset_from_dict(
                    file_handle=f,
                    dataset_name=k,
                    dataset=v,
                    compression=compression,
                )
