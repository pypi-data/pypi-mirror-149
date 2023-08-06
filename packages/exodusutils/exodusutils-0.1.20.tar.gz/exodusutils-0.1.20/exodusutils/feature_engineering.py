from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

from exodusutils import internal
from exodusutils.enums import DataType, TimeUnit
from exodusutils.schemas import Column


def one_hot_encoding(
    training_df: pd.DataFrame, holdout_df: Optional[pd.DataFrame]
) -> Tuple[pd.DataFrame, Optional[pd.DataFrame], List[str]]:
    """
    Performs one-hot encoding. If the experiment contains a holdout data frame, pass it to this method \
so that the newly created encoded columns are identical between holdout and training.

    You should choose either `one_hot_encoding` or `label_encoding` for feature engineering.

    Parameters
    ----------
    training_df : pd.DataFrame
        The training dataframe.
    holdout_df : Optional[pd.DataFrame]
        The holdout dataframe. Optional.

    Returns
    -------
    Tuple[pd.DataFrame, Optional[pd.DataFrame], List[str]]
        The encoded training dataframe, the encoded holdout dataframe, and the newly created encoded column names.

    """
    merged = (
        internal.merge_training_holdout(training_df, holdout_df)
        if holdout_df is not None
        else training_df
    )
    categorical_columns = internal.get_columns(training_df, object)

    dummy = pd.get_dummies(merged, columns=categorical_columns, dtype=np.int64)
    dummy_columns = [col for col in dummy.columns.to_list() if col not in merged]
    return *internal.split_to_training_and_holdout(dummy), dummy_columns


def label_encoding(
    training_df: pd.DataFrame, holdout_df: Optional[pd.DataFrame]
) -> Tuple[pd.DataFrame, Optional[pd.DataFrame], Dict[str, LabelEncoder]]:
    """
    Performs label encoding. If the experiment contains a holdout data frame, pass it to this method \
so that the newly created encoded columns are identical between holdout and training.

    This method will modify the original dataframe.

    You should choose either `one_hot_encoding` or `label_encoding` for feature engineering.

    Parameters
    ----------
    training_df : pd.DataFrame
        The training dataframe.
    holdout_df : Optional[pd.DataFrame]
        The holdout dataframe. Optional.

    Returns
    -------
    Tuple[pd.DataFrame, Optional[pd.DataFrame], List[str]]
        The encoded training dataframe, the encoded holdout dataframe, and a mapping from encoded column \
names to label encoders.

    """

    df = (
        internal.merge_training_holdout(training_df, holdout_df)
        if holdout_df is not None
        else training_df
    )
    categorical_columns = internal.get_columns(training_df, object)
    encoders = dict()
    for col in categorical_columns:
        encoder = LabelEncoder()
        df.loc[df[col].notnull(), [col]] = encoder.fit_transform(
            df.loc[df[col].notnull()].astype(str)[
                col
            ]  # we only want a column instead of an actual df
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")
        encoders[col] = encoder
    return *internal.split_to_training_and_holdout(df), encoders


def time_component_encoding(
    df: pd.DataFrame, time_unit: TimeUnit = TimeUnit.hour
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Appends the time component columns to the dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe
    time_unit : TimeUnit
        The time unit

    Returns
    -------
    The modified `df` with new time components, and the names of the new time component columns.
    """
    # Make sure it is actually a `TimeUnit`...
    time_unit = TimeUnit(time_unit)
    component_columns = []
    for column in internal.get_columns(df, np.datetime64):
        for prefixed_column_name, component in zip(
            internal.prefix_datetime_cols_with_time_components(column),
            internal.get_time_components(df, time_unit, column),
        ):
            if component is not None:
                df[prefixed_column_name] = component
                component_columns.append(prefixed_column_name)
    return df, component_columns


def get_time_component_features(df: pd.DataFrame) -> List[Column]:
    """
    Returns the time component features as `Column`s that are converted from the datetime columns in `df`.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe

    Returns
    -------
    The list of time component features.

    """
    return [
        Column(name=comp, data_type=DataType.string)
        for c in internal.get_columns(df, np.datetime64)
        for comp in internal.prefix_datetime_cols_with_time_components(c)
        if comp in df.columns
    ]
