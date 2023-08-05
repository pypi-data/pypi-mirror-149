from analyticsTestNN1 import helpers
import numpy as np
import pandas as pd


def test_no_null():

    # Simulating how numpy array is extracted from pandas
    np_array = pd.Series([1, 2, 3, '4', 'xyx']).values
    assert not helpers._isnull(np_array)


def test_nan():

    np_array = pd.Series([1, 2, np.nan, '4', 'xyx']).values
    assert helpers._isnull(np_array)


def test_none():

    np_array = pd.Series([1, None, 3, '4', 'xyx']).values
    assert helpers._isnull(np_array)


def test_NaT():

    np_array = pd.Series([1, pd.NaT, 3, '4', 'xyx']).values
    assert not helpers._isnull(np_array)


def test_empty_string():
    '''Testing case where empty string exists, returns True'''

    np_array = pd.Series([1, 2, 3, '', 'xyx']).values
    assert helpers._isnull(np_array)
