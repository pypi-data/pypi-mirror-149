"""Main file for the package."""
import pandas as pd
import numpy as np


class Ops():
    """Class for making operations on pd.DataFrames."""

    @staticmethod
    def remove_null_values(df: pd.DataFrame) -> pd.DataFrame:
        """Remove all rows containing null values in the dataframe.

        Args:
            df (pd.DataFrame): Dataframe to remove null rows from.

        Returns:
            pd.DataFrame: The input dataframe without any null values.

        Warning:
            The function also matches the following exact strings: ["None", "NaN", "NA", " ", ""]

        Examples:
            >>> df = pd.DataFrame({"A": [1, 2, None], "B": [4, 5, 6]})
            >>> Ops.remove_null_values(df)
                 A  B
            0  1.0  4
            1  2.0  5
        """
        # Regex: (\b = match whole word) (^$ = empty string)
        # Matches "None", "NaN", "NA", " ", ""
        df = df.replace(to_replace=r'\bNone\b|\bNaN\b|\bNA\b| |^$', value=np.nan, regex=True).dropna()

        return df.reset_index(drop=True)

    @staticmethod
    def rotate(df: pd.DataFrame, xx: str, yy: str, scalars: str) -> pd.DataFrame:
        """Remove missing values and rotate the dataframe using the pivot function.

        Args:
            df (pd.DataFrame): Dataframe to rotate.
            xx (str): Column to make frame's new index.
            yy (str): Column to make frame's new columns.
            scalars (str): Column to use for populating he new index.

        Returns:
            pd.DataFrame: reshaped dataframe.

        Examples:
            >>> df = pd.DataFrame({"Year": [2001, 2002, 2002],
            ...                    "Country": ["dk", "gb", "dk"],
            ...                    "SalesAmmount": [10, 20, 10]})
            >>> Ops.rotate(df, xx="Country", yy="Year", scalars="SalesAmmount")
            Year     2001  2002
            Country
            dk       10.0  10.0
            gb        NaN  20.0
        """
        df = Ops.remove_null_values(df=df)
        return df.pivot(index=xx, columns=yy, values=scalars)
