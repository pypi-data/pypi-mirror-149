from typing import Tuple, Union, List

import numpy as np
from skimage.transform import rescale


def rescale_raw_im(
    raw_im: np.ndarray,
    im_px_size: Tuple[float, float, float],
    target_px_size: Tuple[float, float, float],
) -> np.ndarray:

    scaling_factor = np.divide(im_px_size, target_px_size)
    if np.any(scaling_factor < 1):
        anti_alias = True
    else:
        anti_alias = False
    rescaled_im = rescale(
        raw_im, scaling_factor, anti_aliasing=anti_alias, order=1
    )

    return rescaled_im


def rescale_label_im(
    raw_im: np.ndarray,
    im_px_size: Tuple[float, float, float],
    target_px_size: Tuple[float, float, float],
) -> np.ndarray:

    scaling_factor = np.divide(im_px_size, target_px_size)
    rescaled_im = rescale(raw_im, scaling_factor, order=0)

    return rescaled_im


def pad_label_im(raw_im: np.ndarray, label_im: np.ndarray) -> np.ndarray:
    """Pad a label image to match the shape along the 0th axis
    of the raw image.

    This is a hack to account for the small
    subset of images that have a z dim off by one.

    Parameters
    ----------
    raw_im : np.ndarray
        The raw image. This is the template image.
    label_im : np.ndarray
        This is the image that has its 0th axis padded.

    Returns
    -------
    label_im : np.ndarray
        The padded label image. If no padding is required (i.e., the shape
        of the raw and label images matches), then the original label_im
        is returned.
    """
    if raw_im.shape[0] != label_im.shape[0]:
        n_slices = raw_im.shape[0] - label_im.shape[0]
        assert n_slices > 0
        padding = np.zeros((n_slices, label_im.shape[1], label_im.shape[2]))
        label_im = np.concatenate((label_im, padding), axis=0)
    return label_im


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

    return cropped_image, image.shape, min_indices


def crop_raw_image(
    raw_image, mask_image, min_shape=[80, 80, 80], mask_periphery: bool = True
):
    ovary_mask = mask_image.astype(bool)

    # get the average pixel value and set all non ovary pixels
    if mask_periphery is True:
        mean_px_value = raw_image.mean()
        raw_image[np.logical_not(ovary_mask)] = mean_px_value

    cropped_raw_image, reference_shape, offset = crop_image(
        raw_image, mask_image, min_shape=min_shape
    )

    return cropped_raw_image, reference_shape, offset


def pad_image(image: np.ndarray, reference_shape: Tuple, offsets: Tuple):
    """
    Pad an image to the reference shape and positioned to the given offset.

    Parameters
    ----------
    image : np.ndarray
        Image to be padded
    reference_shape : Tuple
        Shape of the padded array
    offsets : Tuple
        Offset to set the original array into the padded padded output image
    Returns
    -------
    np.ndarray
        Padded image
    """
    # Create an array of zeros with the reference shape
    result = np.zeros(reference_shape)
    # Create a list of slices from offset to offset + shape in each dimension
    insertHere = [
        slice(offsets[dim], offsets[dim] + image.shape[dim])
        for dim in range(image.ndim)
    ]
    # Insert the array in the result at the specified offsets
    result[tuple(insertHere)] = image
    return result


def crop_label_image(label_image, ovary_image, min_shape=[80, 80, 80]):
    ovary_mask = ovary_image.astype(np.bool)
    cropped_label, reference_shape, offset = crop_image(
        label_image, ovary_mask, min_shape=min_shape
    )

    return cropped_label, reference_shape, offset


def pad_im_to_min_size(
    im: np.ndarray, min_size: Union[List[int], np.ndarray] = [80, 80, 80]
) -> np.ndarray:

    min_size = np.asarray(min_size)

    size_diff = np.array(im.shape) - min_size

    if np.all(size_diff >= 0):
        return im
    else:
        # we take negative size_diff because we subtracted min_size from im.shape
        pad_amount = np.clip(-size_diff, a_min=0, a_max=None)
        pad_width = [
            (0, pad_amount[0]),
            (0, pad_amount[1]),
            (0, pad_amount[2]),
        ]
        return np.pad(
            im, pad_width=pad_width, mode='constant', constant_values=0
        )
