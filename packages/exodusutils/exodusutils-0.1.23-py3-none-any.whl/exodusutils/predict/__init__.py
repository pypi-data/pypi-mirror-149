from typing import Dict

import numpy as np
import pandas as pd

from exodusutils.constants import PREDICTION_COLNAME


def append_predictions(
    df: pd.DataFrame,
    predictions: np.ndarray,
    class_predict_probas: Dict[str, np.ndarray],
) -> pd.DataFrame:
    """
    Append predictions to the dataframe.

    If this is a classification experiment, then supply this method with `class_predict_probas`, a
    mapping from class names to class probabilities.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe
    predictions : np.ndarray
        predictions
    class_predict_probas : Dict[str, np.ndarray]
        class predict probailities

    Returns
    -------
    pd.DataFrame

    """
    df[PREDICTION_COLNAME] = predictions
    for class_name, class_proba in class_predict_probas.items():
        df[class_name] = class_proba
    return df
