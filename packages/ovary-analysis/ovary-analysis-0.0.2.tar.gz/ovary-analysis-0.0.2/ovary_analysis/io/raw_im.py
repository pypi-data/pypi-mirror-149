from typing import Any, List, Tuple

import numpy as np
from skimage.io import imread
from tifffile import TiffFile


def load_raw_im(raw_im_paths: List[str]) -> np.ndarray:
    """Load a raw image into a numpy array

    Parameters
    ----------
    raw_im_paths : List[str]
        A list of the paths to the z slices for the raw image.
        These should be ordered in ascending z order.

    Returns
    -------
    im_array : np.ndarray
        The image as a numpy array. Ordered ZXY.
    """
    # load the files
    ims = []
    for f in raw_im_paths:
        ims.append(imread(f))
    im_array = np.asarray(ims)
    return im_array


def parse_tiff_metadata(
    fpath: str, tag_name: Any = 270, separator: str = '\r\n'
) -> Tuple[float, float, float, int]:
    # get the metadata
    with TiffFile(fpath) as tif:
        tags = tif.pages[0].tags
        raw_metadata = tags[tag_name].value
    metadata = raw_metadata.split(separator)

    # get the pixel sizes
    px_size_x = _get_metadata_field(metadata, 'Pixel length - X [mm]', float)
    px_size_y = _get_metadata_field(metadata, 'Pixel length - Y [mm]', float)
    px_size_z = _get_metadata_field(metadata, 'Pixel length - Z [mm]', float)

    # get the number of slices
    n_z = _get_metadata_field(metadata, 'Number of Timepoints', int)

    return px_size_x, px_size_y, px_size_z, n_z


def _get_metadata_field(
    metadata: List[str], field_name: str, field_type
) -> Any:
    for field in metadata:
        if field.startswith(field_name):
            split_field = field.split(' ')
            field_value = field_type(split_field[-1])
            break
    return field_value
