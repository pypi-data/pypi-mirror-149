from analyticsTestNN1 import analytics
import pandas as pd


def test_rotate_empty():
    '''Test where an empty df is passed to function'''
    df_test = pd.DataFrame(columns=['A', 'B', 'C'])
    result_df = analytics.Ops.rotate(df_test, xx='A', yy='B', scalars='C')

    pd.testing.assert_frame_equal(df_test, result_df)


def test_rotate_example():
    '''Test with the example given'''
    df_test = pd.DataFrame([['a', 'AXA', 13, 'djasd8'],
                            ['b', 'BZB', 123.12000, '7123hy'],
                            ['a', 'CYC', 3.40000, 'h6as7d'],
                            ['a', 'BZB', 4.41332, 'Naisd871a'],
                            ['b', 'AXA', 54.00000, 'dashd77'],
                            ['b', 'CYC', 6.12000, 'mdas7gg']],
                           columns=['A', 'B', 'C', 'D'])

    result_df = analytics.Ops.rotate(df_test, xx='A', yy='B', scalars='C')

    df_expected = pd.DataFrame([[13, 4.41332, 3.40000],
                                [54.00000, 123.12000, 6.12000]],
                               columns=['AXA', 'BZB', 'CYC'],
                               index=['a', 'b'])
    df_expected.index.name = 'A'
    df_expected.columns.name = 'B'

    pd.testing.assert_frame_equal(df_expected, result_df)
