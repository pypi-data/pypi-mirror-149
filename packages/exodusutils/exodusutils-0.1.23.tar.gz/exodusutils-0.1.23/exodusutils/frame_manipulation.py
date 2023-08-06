from typing import List, Optional

import numpy as np
import pandas as pd

from exodusutils import internal


def to_numeric_features_df(df: pd.DataFrame, target: str) -> pd.DataFrame:
    """
    Extracts the numeric features from the dataframe, and returns them as a new dataframe.

    The numeric features include:
        - Columns declared with `data_type == DataType.double` in `feature_types`
        - The encoded columns (i.e. the dummy columns in one-hot encoding, or the
                columns that have been label encoded)

    This is the `X` dataframe used in TPOT.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe.
    target : str
        Target column name.

    Returns
    -------
    The numeric features as a dataframe.
    """
    return pd.DataFrame(df[internal.get_numeric_features(df, target)])


def remove_invalid_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes the invalid values from the dataframe, and resets the index.

    The invalid values are:
    - `float("nan")` or `np.nan` in numeric columns
    - `""` in other types of columns
    """
    return pd.DataFrame(df.replace("", np.nan).dropna()).reset_index(drop=True)


def remove_datetime_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes all columns of dtype `datetime64`.
    """
    return pd.DataFrame(df.drop(internal.get_columns(df, np.datetime64), axis=1))


def fill_nan_with_mode(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Fills the `NaN` cells in each numeric column with the most frequent value (aka `mode`) of that column.

    This is used to create labels for the previously unseen values in a label encoded categorical column.

    Parameters
    ----------
    df : DataFrame
        The dataframe to fill.
    columns : List[str]
        The names of the label encoded columns to fill.

    Returns
    -------
    DataFrame
        The dataframe with no `NaN` cell.
    """
    value = {col: internal.get_column_mode(df[col]) for col in columns}
    return df.fillna(value=value)


def drop_blank(df: pd.DataFrame, target_column_name: Optional[str]) -> pd.DataFrame:
    """
    Drops the blank rows from the dataframe. If target column name is given, then all rows with `np.nan` or `\"\"` \
in the target column will be discarded. Otherwise only rows with all `np.nan` or `\"\"` will be discarded.

    Parameters
    ----------
    df : DataFrame
        The dataframe to manipulate on.
    target_column_name : Optional[str]
        The target column name. Optional.

    Returns
    -------
    DataFrame
        The dataframe without blank rows.
    """
    if target_column_name is not None:
        df[target_column_name] = df[target_column_name].replace(
            "", np.nan
        )
        dropped = df.dropna(subset=[target_column_name])
    else:
        dropped = pd.DataFrame(df.replace("", np.nan).dropna(how="all"))
    return dropped.reset_index(drop=True)

