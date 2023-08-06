import os
from shutil import copy2
from typing import List, Union

import numpy as np
import pandas as pd


def split_table_into_k_folds(
    df: pd.DataFrame, n_folds: int = 10, random_seed: int = 42
) -> List[pd.DataFrame]:
    """Split a table of datasets into k folds

    Parameters
    ----------
    df : pd.DataFrame
        The table to split.
    n_folds : int
        The number of folds to split the dataframe into.
    random_seed : int
        The seed for the random number generator used to shuffle the datasets.
        The default value is 42.

    Returns
    -------
    split_table : List[pd.DataFrame]
        Each fold of the split dataframe stored in a list.
    """
    shuffled_df = df.sample(frac=1, random_state=random_seed)
    return np.array_split(shuffled_df, n_folds)


def copy_datasets(
    df: pd.DataFrame,
    in_dir: Union[str, os.PathLike],
    out_dir: Union[str, os.PathLike],
    column_name: str = 'dataset_path',
):
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    for _, row in df.iterrows():
        dataset_name = os.path.basename(row[column_name])
        from_path = os.path.join(in_dir, dataset_name)
        to_path = os.path.join(out_dir, dataset_name)
        copy2(from_path, to_path)
