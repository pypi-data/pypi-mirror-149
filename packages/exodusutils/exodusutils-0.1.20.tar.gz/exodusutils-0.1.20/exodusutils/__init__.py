__version__ = "0.1.0"

from typing import List

import numpy as np
import pandas as pd
from Levenshtein import distance

from exodusutils.enums import TimeUnit


def closest_string(words: List[str], ref: str) -> str:
    """
    Returns the word in `words` that has the minimum Levenshtein distance from `ref`.
    """
    return sorted(words, key=lambda w: distance(w, ref))[0]


def remove_invalid_targets(df: pd.DataFrame, target: str) -> pd.DataFrame:
    """
    Returns a new dataframe that does not have `NaN` in target column. Does not modify the original dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        df
    target : str
        target

    Returns
    -------
    pd.DataFrame

    """
    return df.loc[df[target].notnull(), :]


def format_datetime_column_with_unit(
    df: pd.DataFrame, datetime_column: str, time_unit: TimeUnit
) -> pd.DataFrame:
    """Turns date column into `str` based on given `time_unit`. Will modify the original `df`."""
    df[datetime_column] = df[datetime_column].apply(lambda t: time_unit.format_datetime(t))
    return df


def are_valid_values(values: List[float]) -> bool:
    """
    Whether there exists a non-`np.nan` value in `values`. Used to test if a fold is useless - \
if all actual values are `np.nan`, then the fold is not usable.

    Parameters
    ----------
    values : List[float]
       The values

    Returns
    -------
    bool

    """
    return not all([np.isnan(x) for x in values])
