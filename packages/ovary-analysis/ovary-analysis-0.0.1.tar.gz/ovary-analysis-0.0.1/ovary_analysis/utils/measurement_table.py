import pandas as pd
import numpy as np
from ovary_analysis.utils.file_names import calculate_day_offsets


def date_csv_to_df(csv_dir: str) -> pd.DataFrame:
    """import csv file to pandas dataframe
    and assign datetime dtype to column date

    Parameters
    ----------
    csv_dir: str
        directory of the csv file

    Returns
    -------
    raw_data: pandas dataframe
        dataframe with follicle info from each images

    """
    raw_data = pd.read_csv(csv_dir)
    raw_data['date'] = pd.to_datetime(raw_data['date'])
    return raw_data


def calc_relative_day(df: pd.DataFrame) -> pd.DataFrame:
    """calculate the relative days of each patients in each cycles

    Parameters
    ----------
    df: pandas Dataframe
        dataframe with follicle info from each images

    Returns
    -------
    df: pandas Dataframe
        add relative days info to the original dataframe

    """
    df['day_rel'] = np.nan
    z1 = df.loc[df['cycle'] == 'z1']
    z2 = df.loc[df['cycle'] == 'z2']
    z1_patient_id = z1['patient_id'].unique().tolist()
    z2_patient_id = z2['patient_id'].unique().tolist()

    for id1 in z1_patient_id:
        z1_links = (
            df['date']
            .loc[
                (df['cycle'] == 'z1')
                & (df['patient_id'] == id1)
                & (df['side'] == 'links')
            ]
            .tolist()
        )

        if len(z1_links) > 0:
            rel_days_links = calculate_day_offsets(z1_links)
            df['day_rel'].loc[
                (df['cycle'] == 'z1')
                & (df['side'] == 'links')
                & (df['patient_id'] == id1)
            ] = rel_days_links

        z1_rechts = (
            df['date']
            .loc[
                (df['cycle'] == 'z1')
                & (df['patient_id'] == id1)
                & (df['side'] == 'rechts')
            ]
            .tolist()
        )
        if len(z1_rechts) > 0:
            rel_days_rechts = calculate_day_offsets(z1_rechts)
            df['day_rel'].loc[
                (df['cycle'] == 'z1')
                & (df['side'] == 'rechts')
                & (df['patient_id'] == id1)
            ] = rel_days_rechts

    for id2 in z2_patient_id:
        z2_links = (
            df['date']
            .loc[
                (df['cycle'] == 'z2')
                & (df['patient_id'] == id2)
                & (df['side'] == 'links')
            ]
            .tolist()
        )

        if len(z2_links) > 0:
            rel_days_links = calculate_day_offsets(z2_links)
            df['day_rel'].loc[
                (df['cycle'] == 'z2')
                & (df['side'] == 'links')
                & (df['patient_id'] == id2)
            ] = rel_days_links

        z2_rechts = (
            df['date']
            .loc[
                (df['cycle'] == 'z2')
                & (df['patient_id'] == id2)
                & (df['side'] == 'rechts')
            ]
            .tolist()
        )

        if len(z2_rechts) > 0:
            rel_days_rechts = calculate_day_offsets(z2_rechts)
            df['day_rel'].loc[
                (df['cycle'] == 'z2')
                & (df['side'] == 'rechts')
                & (df['patient_id'] == id2)
            ] = rel_days_rechts

    return df


def process_fol_csv(csv_dir: str):
    """import csv file and calculate relative days

    Parameters
    ----------
    csv_dir: str
        directory of the csv file

    Returns
    -------
    df: pandas Dataframe
        add relative days info to the imported dataframe

    """
    df = date_csv_to_df(csv_dir)
    print(df.info())
    df = voxel_to_mm(df)
    df = calc_relative_day(df).sort_values(
        by=['patient_id', 'cycle', 'side', 'day_rel']
    )
    return df


def remove_dominant_follicle(df: pd.DataFrame) -> pd.DataFrame:
    """drop the dominant follicle of each patients on each relative day

    Parameters
    ----------
    df: pandas Dataframe
        dataframe with follicle info from each images

    Returns
    -------
    df: pandas Dataframe
        dataframe with follicle info from each images but exclude dominant follicles

    """
    cycles = df['cycle'].unique().tolist()
    day_rel = df['day_rel'].unique().tolist()
    patient_id = df['patient_id'].unique().tolist()

    for c in cycles:
        for day in day_rel:
            for patient in patient_id:
                try:
                    domi = df.loc[
                        (df['cycle'] == c)
                        & (df['day_rel'] == day)
                        & (df['patient_id'] == patient)
                    ]
                    ind = domi['volume'].idxmax()
                    df = df.drop(ind)
                except ValueError:
                    None
    return df.sort_values(
        by=['patient_id', 'cycle', 'side', 'day_rel'], ignore_index=True
    )


def unique_patient(
    df: pd.DataFrame, keep='last', level='day_rel'
) -> pd.DataFrame:
    """Determine which datasets each patient ID has. This function checks for days, sides, and cycles.

    Parameters
    ----------
    df: pandas dataframe
        follicle data include side, cycle, patient_id and relative day

    Returns
    -------
    df_unique: pandas dataframe
        follicle data in which no duplicate patient id on each relative day.

    """
    df = df.sort_values(
        by=['patient_id', 'cycle', 'side', 'day_rel'], ignore_index=True
    )
    if level == 'day_rel':
        df_unique = df.drop_duplicates(
            subset=['side', 'cycle', 'day_rel', 'patient_id'], keep=keep
        )
    elif level == 'cycle':
        df_unique = df.drop_duplicates(
            subset=['side', 'cycle', 'patient_id'], keep=keep
        )
    return df_unique.sort_values(
        by=['patient_id', 'cycle', 'side', 'day_rel'], ignore_index=True
    )


def extract_dominant(df: pd.DataFrame, level: str = 'day_rel') -> pd.DataFrame:
    """pick out the dominant follicle of each patients with respect to relative day or cycle

    Parameters
    ----------
    df: pandas Dataframe
        dataframe with follicle info from each images

    Returns
    -------
    dominant_df: pandas Dataframe
        dataframe with dominant follicle info of each patients with respect to relative day or cycle

    """
    dominant_df = pd.DataFrame()
    sides = ['links', 'rechts']
    cycles = df['cycle'].unique().tolist()
    day_rel = df['day_rel'].unique().tolist()
    patient_id = df['patient_id'].unique().tolist()
    if level == 'day_rel':
        for c in cycles:
            for day in day_rel:
                for patient in patient_id:
                    for side in sides:
                        try:
                            domi = df.loc[
                                (df['cycle'] == c)
                                & (df['day_rel'] == day)
                                & (df['patient_id'] == patient)
                                & (df['side'] == side)
                            ]
                            ind = domi['volume'].idxmax()
                            dominant_df = dominant_df.append(domi.loc[ind])
                        except ValueError:
                            None
    elif level == 'cycle':
        for c in cycles:
            for patient in patient_id:
                for side in sides:
                    try:
                        domi = df.loc[
                            (df['cycle'] == c)
                            & (df['patient_id'] == patient)
                            & (df['side'] == side)
                        ]
                        ind = domi['volume'].idxmax()
                        temp_domi = domi.loc[ind]
                        temp_domi['original_index'] = ind
                        dominant_df = dominant_df.append(temp_domi)
                    except ValueError:
                        None
    return dominant_df.sort_values(
        by=['patient_id', 'cycle', 'side', 'day_rel'], ignore_index=True
    )


def voxel_to_mm(df: pd.DataFrame) -> pd.DataFrame:
    """unit conversion from voxel to mm^3

    Parameters
    ----------
    df: pandas dataframe
        follicle data which record volume in voxel

    Returns
    -------
    df: pandas dataframe
        follicle data which record volume in mm^3

    """
    df['volume'] = df['volume'].map(lambda x: x * pow(0.157, 3))
    return df


def calc_growth(df: pd.DataFrame) -> pd.DataFrame:
    """calculate the growth of only dominant follicle from one side of ovary of one patient.
        input dataframe should includes only data from dominant follicles

    Parameters
    ----------
    df: pandas dataframe
        follicle data, information such as patient_id, relative days, cycle, side and volume is needed.

    Returns
    -------
    df: pandas dataframe
        add one column named growth to data frame which contains info about the growth of follicle size at each time points.

    """
    df = df.sort_values(by=['patient_id', 'cycle', 'side', 'day_rel'])
    sides = ['links', 'rechts']
    cycles = ['z1', 'z2']
    temp_df_growth = pd.DataFrame()
    for cycle in cycles:
        id_list = df['patient_id'].loc[df['cycle'] == cycle].unique().tolist()
        for patient in id_list:
            for side in sides:
                cycle_volume_df = df.loc[
                    (df['patient_id'] == patient)
                    & (df['cycle'] == cycle)
                    & (df['side'] == side)
                ]
                cycle_volume_df = cycle_volume_df.sort_values(
                    by=['day_rel'], ignore_index=True
                )
                cycle_volume_df['growth'] = np.nan
                if len(cycle_volume_df) > 0:
                    growth_array = np.array([0])
                    if len(cycle_volume_df) > 1:
                        growth_array = np.append(
                            growth_array, np.diff(cycle_volume_df['volume'])
                        )
                    cycle_volume_df['growth'].loc[
                        (cycle_volume_df['patient_id'] == patient)
                        & (cycle_volume_df['cycle'] == cycle)
                        & (cycle_volume_df['side'] == side)
                    ] = growth_array

                    temp_df_growth = temp_df_growth.append(
                        cycle_volume_df[
                            [
                                'patient_id',
                                'cycle',
                                'side',
                                'day_rel',
                                'growth',
                            ]
                        ]
                    )
    df = pd.merge(
        df, temp_df_growth, on=['patient_id', 'cycle', 'side', 'day_rel']
    )
    return df


def calc_domi_relative_day(df: pd.DataFrame) -> pd.DataFrame:
    """calculate the day relative to the day the largest dominant follicle occurred on
    for a given cycle and one side of ovary

    Parameters
    ----------
    df: pandas dataframe
        follicle data, information such as patient_id, relative days, cycle, side and volume is needed.

    Returns
    -------
    df: pandas dataframe
        add one column named domi_day_rel to data frame which contains info about
        the day relative to the day the largest dominant follicle occurred on.

    """
    df['day_from_peak'] = np.nan
    domi_cycle = extract_dominant(df, level='cycle')
    sides = ['links', 'rechts']
    cycles = df['cycle'].unique().tolist()
    patient_id = df['patient_id'].unique().tolist()
    for c in cycles:
        for patient in patient_id:
            for side in sides:
                try:
                    domi_cycle_day = (
                        domi_cycle['day_rel']
                        .loc[
                            (domi_cycle['cycle'] == c)
                            & (domi_cycle['patient_id'] == patient)
                            & (domi_cycle['side'] == side)
                        ]
                        .tolist()
                    )

                    df['day_from_peak'].loc[
                        (df['cycle'] == c)
                        & (df['patient_id'] == patient)
                        & (df['side'] == side)
                    ] = (
                        df['day_rel'].loc[
                            (df['cycle'] == c)
                            & (df['patient_id'] == patient)
                            & (df['side'] == side)
                        ]
                        - domi_cycle_day[0]
                    )
                except IndexError:
                    None
    return df


def group_parse(df: pd.DataFrame) -> pd.DataFrame:
    """parse patient_id adn create a column called growth comprised of "A" or "B"

    Parameters
    ----------
    df: pandas dataframe
        follicle data, information such as patient_id is needed

    Returns
    -------
    df: pandas dataframe
        orignal dataframe with new column called group

    """
    patient_id_list = df['patient_id'].tolist()
    group_list = [patient[0] for patient in patient_id_list]
    df['group'] = group_list
    return df
