import pandas as pd
from pandas._testing import assert_frame_equal
import numpy as np
from ovary_analysis.utils import measurement_table


def test_calc_relative_day():
    # Setup
    valid_DataFrame = pd.DataFrame(
        {
            'patient_id': ['A01', 'A01', 'A02', 'A02'],
            'side': ['links', 'links', 'rechts', 'rechts'],
            'cycle': ['z1', 'z1', 'z2', 'z2'],
            'date': ['2017/4/3', '2017/4/5', '2017/5/17', '2017/5/19'],
            'volume': [10, 20, 30, 50],
        }
    )
    valid_DataFrame['date'] = pd.to_datetime(valid_DataFrame['date'])
    valid_DataFrame['day_rel'] = np.nan

    valid_df_rel = pd.DataFrame(
        {
            'patient_id': ['A01', 'A01', 'A02', 'A02'],
            'side': ['links', 'links', 'rechts', 'rechts'],
            'cycle': ['z1', 'z1', 'z2', 'z2'],
            'date': ['2017/4/3', '2017/4/5', '2017/5/17', '2017/5/19'],
            'volume': [10, 20, 30, 50],
            'day_rel': [0, 2, 0, 2],
        }
    )
    valid_df_rel['date'] = pd.to_datetime(valid_df_rel['date'])

    # Exercise
    df_rel = measurement_table.calc_relative_day(valid_DataFrame)

    # Verify
    assert_frame_equal(df_rel, valid_df_rel, check_dtype=False)

    # Cleanup - none necessary


def test_calc_growth():
    # Setup
    df = pd.DataFrame(
        {
            'patient_id': ['A01', 'A01', 'A02', 'A02'],
            'side': ['links', 'links', 'rechts', 'rechts'],
            'cycle': ['z1', 'z1', 'z2', 'z2'],
            'date': ['2017/4/3', '2017/4/5', '2017/5/17', '2017/5/19'],
            'volume': [10, 20, 30, 50],
            'day_rel': [0, 2, 0, 2],
        }
    )

    valid_df = pd.DataFrame(
        {
            'patient_id': ['A01', 'A01', 'A02', 'A02'],
            'side': ['links', 'links', 'rechts', 'rechts'],
            'cycle': ['z1', 'z1', 'z2', 'z2'],
            'date': ['2017/4/3', '2017/4/5', '2017/5/17', '2017/5/19'],
            'volume': [10, 20, 30, 50],
            'day_rel': [0, 2, 0, 2],
            'growth': [0, 10, 0, 20],
        }
    )
    # Exercise
    df1 = measurement_table.calc_growth(df)

    # Verify
    assert_frame_equal(df1, valid_df, check_dtype=False)

    # Cleanup - none necessary


def test_extract_dominant():
    # Setup
    df = pd.DataFrame(
        {
            'patient_id': ['A01', 'A01', 'A02', 'A02'],
            'side': ['links', 'links', 'rechts', 'rechts'],
            'cycle': ['z1', 'z1', 'z2', 'z2'],
            'date': ['2017/4/3', '2017/4/3', '2017/5/17', '2017/5/17'],
            'volume': [10, 20, 30, 50],
            'day_rel': [0, 0, 0, 0],
        }
    )
    valid_df = pd.DataFrame(
        {
            'patient_id': ['A01', 'A02'],
            'side': ['links', 'rechts'],
            'cycle': ['z1', 'z2'],
            'date': ['2017/4/3', '2017/5/17'],
            'volume': [20, 50],
            'day_rel': [0, 0],
            'original_index': [1, 3],
        }
    )

    # Exercise
    df1 = measurement_table.extract_dominant(df, level='cycle')

    # Verify
    assert_frame_equal(df1, valid_df, check_dtype=False, check_like=True)

    # Cleanup - none necessary


def test_voxel_to_mm():
    # Setup
    df = pd.DataFrame({'volume': [2, 5]})
    valid_df = pd.DataFrame({'volume': [0.0077398, 0.019350]})

    # Exercise
    df1 = measurement_table.voxel_to_mm(df)

    # Verify
    assert_frame_equal(
        df1, valid_df, check_dtype=False, check_like=True, check_less_precise=5
    )

    # Cleanup - none necessary


def test_remove_dominant_follicle():
    # Setup
    df = pd.DataFrame(
        {
            'patient_id': ['A01', 'A01', 'A02', 'A02'],
            'side': ['links', 'links', 'rechts', 'rechts'],
            'cycle': ['z1', 'z1', 'z2', 'z2'],
            'date': ['2017/4/3', '2017/4/3', '2017/5/17', '2017/5/17'],
            'volume': [10, 20, 30, 50],
            'day_rel': [0, 0, 0, 0],
        }
    )
    valid_df = pd.DataFrame(
        {
            'patient_id': ['A01', 'A02'],
            'side': ['links', 'rechts'],
            'cycle': ['z1', 'z2'],
            'date': ['2017/4/3', '2017/5/17'],
            'volume': [10, 30],
            'day_rel': [0, 0],
        }
    )
    # Exercise
    df1 = measurement_table.remove_dominant_follicle(df)

    # Verify
    assert_frame_equal(df1, valid_df, check_dtype=False, check_like=True)

    # Cleanup - none necessary


def test_unique_patient():
    # Setup
    df = pd.DataFrame(
        {
            'patient_id': ['A01', 'A01', 'A02', 'A02'],
            'side': ['links', 'links', 'rechts', 'rechts'],
            'cycle': ['z1', 'z1', 'z2', 'z2'],
            'date': ['2017/4/3', '2017/4/3', '2017/5/17', '2017/5/17'],
            'volume': [10, 20, 30, 50],
            'day_rel': [0, 0, 1, 1],
        }
    )
    valid_df = pd.DataFrame(
        {
            'patient_id': ['A01', 'A02'],
            'side': ['links', 'rechts'],
            'cycle': ['z1', 'z2'],
            'date': ['2017/4/3', '2017/5/17'],
            'volume': [20, 50],
            'day_rel': [0, 1],
        }
    )

    # Exercise
    df1 = measurement_table.unique_patient(df)

    # Verify
    assert_frame_equal(df1, valid_df, check_dtype=False, check_like=True)

    # Cleanup - none necessary


def test_calc_domi_relative_day():
    # Setup
    df = pd.DataFrame(
        {
            'patient_id': ['A01', 'A01', 'A01', 'A02', 'A02', 'A02'],
            'side': ['links', 'links', 'links', 'rechts', 'rechts', 'rechts'],
            'cycle': ['z1', 'z1', 'z1', 'z2', 'z2', 'z2'],
            'date': [
                '2017/4/3',
                '2017/4/5',
                '2017/4/5',
                '2017/5/17',
                '2017/5/19',
                '2017/5/21',
            ],
            'volume': [10, 20, 25, 30, 50, 45],
            'day_rel': [0, 2, 2, 0, 2, 4],
        }
    )
    valid_df = pd.DataFrame(
        {
            'patient_id': ['A01', 'A01', 'A01', 'A02', 'A02', 'A02'],
            'side': ['links', 'links', 'links', 'rechts', 'rechts', 'rechts'],
            'cycle': ['z1', 'z1', 'z1', 'z2', 'z2', 'z2'],
            'date': [
                '2017/4/3',
                '2017/4/5',
                '2017/4/5',
                '2017/5/17',
                '2017/5/19',
                '2017/5/21',
            ],
            'volume': [10, 20, 25, 30, 50, 45],
            'day_rel': [0, 2, 2, 0, 2, 4],
            'day_from_peak': [-2, 0, 0, -2, 0, 2],
        }
    )

    # Exercise
    df1 = measurement_table.calc_domi_relative_day(df)

    # Verify
    assert_frame_equal(df1, valid_df, check_dtype=False, check_like=True)


def test_group_sparse():
    # Setup
    df = pd.DataFrame(
        {
            'patient_id': ['A01', 'A01', 'A01', 'B02', 'B02', 'B02'],
            'side': ['links', 'links', 'links', 'rechts', 'rechts', 'rechts'],
            'cycle': ['z1', 'z1', 'z1', 'z2', 'z2', 'z2'],
            'date': [
                '2017/4/3',
                '2017/4/5',
                '2017/4/5',
                '2017/5/17',
                '2017/5/19',
                '2017/5/21',
            ],
            'volume': [10, 20, 25, 30, 50, 45],
            'day_rel': [0, 2, 2, 0, 2, 4],
        }
    )
    valid_df = pd.DataFrame(
        {
            'patient_id': ['A01', 'A01', 'A01', 'B02', 'B02', 'B02'],
            'side': ['links', 'links', 'links', 'rechts', 'rechts', 'rechts'],
            'cycle': ['z1', 'z1', 'z1', 'z2', 'z2', 'z2'],
            'date': [
                '2017/4/3',
                '2017/4/5',
                '2017/4/5',
                '2017/5/17',
                '2017/5/19',
                '2017/5/21',
            ],
            'volume': [10, 20, 25, 30, 50, 45],
            'day_rel': [0, 2, 2, 0, 2, 4],
            'group': ['A', 'A', 'A', 'B', 'B', 'B'],
        }
    )

    # Exercise
    df1 = measurement_table.group_parse(df)

    # Verify
    assert_frame_equal(df1, valid_df, check_dtype=False, check_like=True)
