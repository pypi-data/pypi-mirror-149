import multiprocessing as mp
from functools import partial

import pandas as pd

from ovary_analysis.convert.raw_data import convert_raw_dataset


if __name__ == "__main__":
    IMAGE_TABLE_PATH = '/nas/groups/iber/Projects/IVF/Bicycle_Study/Data/ultrasound_images_h5/image_table_raw_files_20220228.csv'
    OUTPUT_DIRECTORY = '/local0/kevin/ivf/full_data_converted_20220301/converted'
    TARGET_PX_SIZE = (0.157288, 0.157288, 0.157288)
    IM_PATH_KEY = "path"
    N_Z_KEY = "n_z_files"

    # load the image table
    image_table = pd.read_csv(IMAGE_TABLE_PATH)
    image_table_rows = [row for _, row in image_table.iterrows()]

    conversion_function = partial(
        convert_raw_dataset,
        target_px_size=TARGET_PX_SIZE,
        output_dir=OUTPUT_DIRECTORY,
        im_path_key=IM_PATH_KEY,
        n_z_key=N_Z_KEY
    )
    print(f"converting {len(image_table)} images")
    with mp.get_context('spawn').Pool() as pool:
        records = pool.map(conversion_function, image_table_rows)

    # records = []
    # for i, row in enumerate(image_table_rows):
    #     print(i)
    #     records.append(conversion_function(row))
