'''This file contains required class and methods for exercise 2'''
import pandas as pd
from analyticsTestNN1 import helpers


class Ops:
    '''This class provides methods to to be used in exercise 3 on DataFrames'''

    @staticmethod
    def remove_null_values(data: pd.DataFrame) -> pd.DataFrame:
        '''
        Removes rows that contain a null value.
        A null value (in the context of this func) is one of the following:
            i. nan (np.NaN)
            ii. None
            iii. ""

        Args:
            data (pd.DataFrame) : The pandas dataframe

        Returns:
            pd.DataFrame : a dataframe without null values

        Note: Can be implemented using pandas functions:

            return data.dropna()

            or

            return data[data.apply(lambda x: not pd.isnull(x).any(), axis = 1)]
        '''
        if data.empty:
            return data

        boolean_vals = []
        for row in data.values:
            boolean_vals.append(not helpers._isnull(row))
        return data[boolean_vals]

    @staticmethod
    def rotate(
        data: pd.DataFrame,
        xx: str, yy: str,
            scalars: str) -> pd.DataFrame:
        '''
        Implements the pivot functionality of the pandas DataFrames

        Args:
            data (pd.DataFrame): The pandas dataframe to be rotated
            xx (str) : The column to be the x-axis of rotated dataframe
            yy (str) : The column to be the y-axis of rotated dataframe
            scalars(str) : The column that will populate the dataframe

        Returns:
            pd.DataFrame : The rotated (pivoted) dataframe

        Raises:
            Exception: ValueError Index contains duplicate entires

        Note: Can be implemented using pandas functions:

            return data.pivot(index=xx, columns=yy, values=scalars)
        '''

        data = Ops.remove_null_values(data)

        if data.empty:
            return data

        dict_of_dicts = {}

        # Iterate over each row and unpack values
        for _, (x, y, z) in data[[xx, yy, scalars]].iterrows():

            if y in dict_of_dicts:
                # if x is already a key, then there are duplicate values
                if x in dict_of_dicts[y]:
                    raise ValueError("Value Error: \
                        Index contains duplicate entries")
                else:
                    dict_of_dicts[y][x] = z
            else:
                dict_of_dicts[y] = {}
                dict_of_dicts[y][x] = z

        return_df = pd.DataFrame(data=dict_of_dicts)
        return_df.index.name = xx
        return_df.columns.name = yy
        return return_df
