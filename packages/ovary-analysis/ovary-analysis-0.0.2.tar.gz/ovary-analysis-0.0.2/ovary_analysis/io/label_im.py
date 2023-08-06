import os

import numpy as np
from skimage.io import imread


def load_label_im(label_path: os.PathLike) -> np.ndarray:
    """Load a label image (tif) into a numpy array

    Parameters
    ----------
    label_path : os.PathLike
        Path to the label image. Should be a tif.
        The labels file is assumed to be in ZCXY order.

    Returns
    -------
    im_array : np.ndarray
        The label image as a numpy array. Ordered CZXY.
    """
    im = imread(label_path)
    im_array = np.swapaxes(im, 1, 0)

    return im_array
