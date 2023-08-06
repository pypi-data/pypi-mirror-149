from functools import partial
import glob
import multiprocessing as mp
import os
from typing import Tuple

import h5py

from ovary_analysis.io.hdf5_io import write_hdf
from ovary_analysis.utils.image import crop_raw_image


def create_follicle_dataset(
    raw_fpath: str,
    segmentation_dir: str,
    output_dir: str,
    min_shape: Tuple[int, int, int],
    mask_raw_im: bool = True
):
    # load the raw image
    with h5py.File(raw_fpath, "r") as f:
        raw_im = f["raw_rescaled"][:]

    # load the ovary segmentation
    raw_fname = os.path.basename(raw_fpath)
    ovary_segmentation_name = raw_fname.replace(".h5", "_segmentation.h5")
    ovary_segmentation_path = os.path.join(segmentation_dir, ovary_segmentation_name)
    with h5py.File(ovary_segmentation_path, "r") as f:
        ovary_segmentation = f["ovary_segmentation_rescaled"][:]

    ovary_mask = ovary_segmentation > 0
    cropped_raw = crop_raw_image(
        raw_im, ovary_mask, min_shape=min_shape, mask_periphery=mask_raw_im
    )

    output_fname = raw_fname.replace("_raw.h5", "_follicles.h5")
    output_fpath = os.path.join(output_dir, output_fname)

    write_hdf(
        pixel_array=cropped_raw,
        fname=output_fpath,
        dataset_name="raw_rescaled",
        compression="gzip"
    )


if __name__ == "__main__":
    RAW_DIR = "/cluster/scratch/kyamauch/full_data_20220301/denoised"
    OVARY_SEGMENTATION_DIR = "/cluster/scratch/kyamauch/full_data_20220301/ovary_segmentation/segmentations"
    OUTPUT_DIR = "/cluster/scratch/kyamauch/full_data_20220301/ovary_segmentation/follicle_segmentation/follicle_datasets"

    MIN_SHAPE = (80, 80, 80)
    MASK_RAW_IM = True

    # get the file names
    raw_file_pattern = os.path.join(RAW_DIR, "*.h5")
    raw_files = glob.glob(raw_file_pattern)

    writer_func = partial(
        create_follicle_dataset,
        segmentation_dir=OVARY_SEGMENTATION_DIR,
        output_dir=OUTPUT_DIR,
        min_shape=MIN_SHAPE,
        mask_raw_im=MIN_SHAPE
    )

    with mp.get_context('spawn').Pool() as pool:
        pool.map(writer_func, raw_files)

