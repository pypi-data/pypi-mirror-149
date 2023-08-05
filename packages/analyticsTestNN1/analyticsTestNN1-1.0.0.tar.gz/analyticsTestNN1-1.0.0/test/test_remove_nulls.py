from analyticsTestNN1 import analytics
import pandas as pd
import numpy as np


def test_remove_null_values_empty():
    '''Test where an empty df is passed to function'''
    df_test = pd.DataFrame()
    result_df = analytics.Ops.remove_null_values(df_test)

    pd.testing.assert_frame_equal(df_test, result_df)


def test_remove_null_values_no_nulls():
    '''Test where no nulls in df'''
    df_test = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                           columns=['A', 'B', 'C'])
    result_df = analytics.Ops.remove_null_values(df_test)

    pd.testing.assert_frame_equal(df_test, result_df)


def test_remove_null_values_one_nan():
    '''Test where df contains a single nan value'''
    df_test = pd.DataFrame([[1, np.nan, 3], [4, 5, 6]],
                           columns=['A', 'B', 'C'])

    # Drop first row containing nan value
    df_expected = df_test.iloc[1:]
    result_df = analytics.Ops.remove_null_values(df_test)

    pd.testing.assert_frame_equal(df_expected, result_df)


def test_remove_null_values_one_None():
    '''Test where df contains a single None value'''
    df_test = pd.DataFrame([['a', 'b', 'c'], ['d', 'e', 'f'], [4, 5, None]],
                           columns=['A', 'B', 'C'])

    # Drop last row containing None value
    df_expected = df_test.iloc[:-1]
    result_df = analytics.Ops.remove_null_values(df_test)

    pd.testing.assert_frame_equal(df_expected, result_df)


def test_remove_null_values_all_rows():
    '''Test where df contains a null value in each row'''
    df_test = pd.DataFrame([[np.nan, 'b'], [np.nan, 'f'], [5, None]],
                           columns=['A', 'B'])

    result_df = analytics.Ops.remove_null_values(df_test)

    assert result_df.empty


def test_remove_null_values_given_example():
    '''Test for the given example in exercise3.py'''
    df_test = pd.DataFrame([['a', 'AXA', 13, 'djasd8'],
                            ['b', 'BZB', 123.12000, '7123hy'],
                            ['a', 'CYC', 3.40000, 'h6as7d'],
                            ['a', 'BZB', 4.41332, 'Naisd871a'],
                            ['b', 'AXA', 54.00000, 'dashd77'],
                            ['b', 'CYC', 6.12000, 'mdas7gg'],
                            ['b', None, 612.10000, 'masf7gg'],
                            ['a', 'AXA', np.nan, 'jdasd765ad']],
                           columns=['A', 'B', 'C', 'D'])

    result_df = analytics.Ops.remove_null_values(df_test)

    df_expected = pd.DataFrame([['a', 'AXA', 13, 'djasd8'],
                                ['b', 'BZB', 123.12000, '7123hy'],
                                ['a', 'CYC', 3.40000, 'h6as7d'],
                                ['a', 'BZB', 4.41332, 'Naisd871a'],
                                ['b', 'AXA', 54.00000, 'dashd77'],
                                ['b', 'CYC', 6.12000, 'mdas7gg']],
                               columns=['A', 'B', 'C', 'D'])

    assert df_expected.equals(result_df)
