'''
This module contains helper functions that simplify the code in analytics.py
'''
import numpy as np


def _isnull(row: np.ndarray) -> bool:
    '''
    Returns True if given numpy array contains a null value 
    Null value of form:
        i. nan (np.NaN)
        ii. None
        iii. ""
    '''
    for val in row:
        if val:
            if isinstance(val, float):
                if np.isnan(val):
                    return True
        else:
            return True
    return False
