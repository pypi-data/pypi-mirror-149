from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

from exodusutils import internal
from exodusutils.enums import DataType
from exodusutils.exceptions import ExodusForbidden, ExodusMethodNotAllowed
from exodusutils.schemas import Column


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


def apply_label_encoders(
    df: pd.DataFrame, encoders: Dict[str, LabelEncoder]
) -> pd.DataFrame:
    """
    Apply label encoders to `df`. If your model makes use of `label_encoding` method during training,
    then during prediction this should be performed on the prediction dataframe.
    """
    df = df.copy()
    for col, encoder in encoders.items():
        df.loc[
            ~df[col].isin(encoder.classes_), [col]
        ] = np.nan  # unseen values in training data
        df.loc[df[col].notnull(), [col]] = encoder.transform(
            df.loc[df[col].notnull()][col]
        )
        df[col] = pd.to_numeric(pd.Series(df[col]), errors="coerce")
    return df


def apply_one_hot_encoding(
    df: pd.DataFrame, categorical_columns_in_training: List[str]
) -> pd.DataFrame:
    """
    Apply one-hot encoding to `df`. If your model makes use of `one_hot_encoding` method during training,
    then during prediction this should be performed on the prediction dataframe.
    """
    categorical_columns_in_testing = internal.get_columns(df, object)
    dummy = pd.get_dummies(df, columns=categorical_columns_in_testing, dtype=np.int64)
    for c in categorical_columns_in_training:
        if c not in categorical_columns_in_testing:
            dummy[c] = 0
    return dummy


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


def impute(df: pd.DataFrame, column: Column, method: str) -> pd.DataFrame:
    """
    Imputes the given column in the dataframe with a specified method.

    Available methods are:
    - "mode": Only supports non-empty columns
    - "mean": Only supports numeric columns
    - "average": Alias of "mean" method
    - "zero": Imputes numeric columns with 0, empty string "" for other types of columns
    - "min"
    - "max"
    - "median": Only supports numeric columns

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe.
    column : Column
        The column to impute.
    method : str
        The imputation method.

    Returns
    -------
    pd.DataFrame
        The imputed dataframe.

    """

    values = pd.Series(df[df[column.name].notna()][column.name])
    if method == "mode":
        mode = values.mode().values.tolist()
        if mode:
            target = mode[0]
        else:
            raise ExodusMethodNotAllowed(
                f"Cannot calculate mode of empty column = {column.name}"
            )
    elif method == "mean" or method == "average":
        if column.data_type == DataType.double:
            target = values.mean()
        else:
            raise ExodusMethodNotAllowed(
                f"Imputing categorical column = {column.name} with method = {method} is not supported"
            )
    elif method == "zero":
        if column.data_type == DataType.double:
            target = 0
        else:
            target = ""
    elif method == "min":
        target = values.min()
    elif method == "max":
        target = values.max()
    elif method == "median":
        if column.data_type == DataType.double:
            target = values.median()
        else:
            raise ExodusMethodNotAllowed(
                f"Imputing categorical column = {column.name} with method = {method} is not supported"
            )
    else:
        raise ExodusMethodNotAllowed(f"Unsupported imputation method = {method}")
    if column.data_type == DataType.double and np.isnan(target):
        raise ExodusForbidden(f"Cannot impute column = {column.name} with np.nan")
    return df.fillna(value={column.name: target})
