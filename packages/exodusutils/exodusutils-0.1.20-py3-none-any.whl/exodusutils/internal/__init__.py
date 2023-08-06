import math
from io import BytesIO
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd

from exodusutils.constants import DATETIME_COMPONENTS_PREFIX
from exodusutils.enums import DataType, TimeUnit
from exodusutils.exceptions import ExodusBadRequest
from exodusutils.schemas import Column


def cast_columns(
    df: pd.DataFrame, columns: List[str], target_type: DataType
) -> pd.DataFrame:
    """
    Casts the specified columns to the target `DataType`.
    """
    for col in columns:
        if target_type == DataType.double:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        elif target_type == DataType.timestamp:
            df[col] = pd.to_datetime(pd.Series(df[col]), errors="coerce")
        else:
            df[col] = df[col].fillna("").astype(str)
    return df


def cast_df_types(df: pd.DataFrame, feature_types: List[Column]) -> pd.DataFrame:
    feature_types = [f for f in feature_types if f.name in df.columns]
    numeric_columns = [f.name for f in feature_types if f.data_type == DataType.double]
    datetime_columns = [
        f.name for f in feature_types if f.data_type == DataType.timestamp
    ]
    categorical_columns = [
        f.name
        for f in feature_types
        if f.name not in numeric_columns + datetime_columns
    ]
    return (
        df.pipe(cast_columns, numeric_columns, DataType.double)
        .pipe(cast_columns, datetime_columns, DataType.timestamp)
        .pipe(cast_columns, categorical_columns, DataType.string)
    )


def get_df(data: bytes, feature_types: List[Column]) -> pd.DataFrame:
    return pd.DataFrame(
        pd.read_csv(BytesIO(data), usecols=[f.name for f in feature_types])
    ).pipe(cast_df_types, feature_types)


def prefix_datetime_cols_with_time_components(col: str) -> List[str]:
    """
    Returns a list of str, representing the new time component names

    Parameters
    ----------
    col : str
        a datetime column

    Returns
    -------
    List[str]
        A list of new column names
    """
    return [f"{t}_{col}" for t in DATETIME_COMPONENTS_PREFIX]


def get_time_components(
    df: pd.DataFrame, time_unit: TimeUnit, col: str
) -> List[Optional[pd.Series]]:
    """
    Returns a list of `pd.Series`s, representing the time components for the given column name. \
A time component is a series of `np.int64`.

    Parameters
    ----------
    df : pd.DataFrame
        Original dataframe that features are to be derived from
    time_unit : TimeUnit
        The `smallest` time unit that the new features should include
    col : str
        One of the datetime columns of df

    Returns
    -------
    List of time components.
    """
    # Time components
    dt = df[col].dt
    components = [dt.year]

    # quarter, month and week component
    if time_unit not in {TimeUnit.year}:
        components += [dt.quarter, dt.month, dt.isocalendar().week]
    else:
        components += [None, None, None]

    # weekday and date component
    if time_unit not in {TimeUnit.year, TimeUnit.month}:
        components += [dt.weekday, dt.day]
    else:
        components += [None, None]

    # hour component
    if time_unit not in {TimeUnit.year, TimeUnit.month, TimeUnit.day}:
        components.append(dt.hour)
    else:
        components.append(None)

    return components


def get_columns(df: pd.DataFrame, dtype) -> List[str]:
    return df.select_dtypes(dtype).columns.tolist()


def merge_training_holdout(
    training: pd.DataFrame, holdout: pd.DataFrame
) -> pd.DataFrame:
    holdout["holdout"] = 1
    training["holdout"] = 0
    return pd.concat([training, holdout])


def split_to_training_and_holdout(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
    if "holdout" not in df.columns:
        return df, None
    else:

        def drop_holdout(df: pd.DataFrame, val: int) -> pd.DataFrame:
            return df.loc[df["holdout"] == val, :].drop(columns="holdout")

        return drop_holdout(df, 0), drop_holdout(df, 1)


def get_numeric_features(df: pd.DataFrame, target: str) -> List[str]:
    return [
        f
        for f in get_columns(df, np.float64) + get_columns(df, np.int64)
        if f != target
    ]


def train_validation_split(
    df: pd.DataFrame, validation_percentage: float
) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
    if validation_percentage == 0.0:
        return df, None
    else:
        indexed_validation = df.sample(frac=validation_percentage)
        return df.loc[
            ~df.index.isin(indexed_validation.index)
        ], indexed_validation.reset_index(drop=True)


def sanitize_pred_and_actual(
    pred: np.ndarray, actual: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    if pred.size != actual.size:
        raise ValueError(f"pred.size = {pred.size} != actual.size = {actual.size}")

    if np.issubdtype(actual.dtype, np.number):
        if not np.issubdtype(pred.dtype, np.number):
            raise ValueError(f"actual is number while pred is not")
        pred, actual = [
            np.array(t)
            for t in zip(*[(p, a) for p, a in zip(pred, actual) if not np.isnan(a)])
        ]

    if pred.size == 0:
        raise ValueError("empty fold score")

    return pred, actual


def validate_columns(header: List[str], features: List[Column]) -> None:
    """
    Check if there are any required features in `features` that are missing from the dataframe

    Parameters
    ----------
        header : List[str]
            columns that are present in a dataframe
        features : List[Column]
            `features` is a list of `Column`s that is/was required for training

    Returns
    -------
        None

    Raises
    ------
        HTTPException
            the client is notified that the information supplied is invalid
    """
    for f in features:
        if (
            f.name not in header
        ):  # This means that a required field is missing from the dataframe
            raise ExodusBadRequest(f"column {f.name} is missing from the data")


def get_column_mode(col) -> float:
    """
    Returns the most frequent value of a numeric column, or `0.0` if it is impossible to calculate.

    This is used to create labels for the previously unseen values in a label encoded categorical column.
    """
    mode = col.mode().values
    if len(mode) > 0:
        return (
            0.0 if math.isnan(mode[0]) else mode[0]
        )  # Just take the first one if there are ties
    else:
        return 0.0


def append_fold_column(df: pd.DataFrame, name: str, folds: int) -> pd.DataFrame:
    """Appends the fold column to the incoming dataframe. Will return a new dataframe, and leave the old one unchanged.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe.
    name : str
        Name of the fold column.
    folds : int
        Number of folds we want to cut.

    Returns
    -------
    pd.DataFrame
        The resulting dataframe.

    """
    res = df.copy()
    res[name] = np.array((df.index % folds).astype(int))
    return res


def select_and_drop_fold_column(
    df: pd.DataFrame, name: str, fold: int, test: bool
) -> pd.DataFrame:
    """
    Selects the rows that are in fold range, and then drops the fold column.

    If `test` is `True`, selects the rows with `name` equal to `fold`. Otherwise chooses the ones that are not equal.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe.
    name : str
        Name of fold column.
    fold : int
        The fold to select.
    test : bool
        Whether we are selecting test frame or not.

    Returns
    -------
    pd.DataFrame
        The selected dataframe.

    """
    return (
        df.loc[(df[name] == fold) if test else (df[name] != fold)]
        .reset_index(drop=True)
        .drop(columns=[name])
    )
