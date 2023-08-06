from typing import List, Optional

import pandas as pd
from pydantic import BaseModel

from exodusutils import internal
from exodusutils.exceptions.exceptions import ExodusMethodNotAllowed


class SplitFrames(BaseModel):
    """
    A collection of dataframes. The validation frame and test frame are optional.
    """

    train: pd.DataFrame
    validation: Optional[pd.DataFrame]
    test: Optional[pd.DataFrame]

    class Config:
        arbitrary_types_allowed = True


class CVFrames(BaseModel):
    """
    A list of `TrainFrames`. User should not initialize this class directly, instead they should \
use the classmethod `iid`.
    """

    splits: List[SplitFrames]

    @classmethod
    def iid(
        cls,
        df: pd.DataFrame,
        nfolds: int,
        validation_df: Optional[pd.DataFrame] = None,
        fold_assignment_column_name: Optional[str] = None,
    ):
        """
        Create CV frames for an IID experiment.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to split to CV frames.
        nfolds : int
            Number of folds.
        validation_df : Optional[pd.DataFrame]
            The dataframe for validation. Optional.
        fold_assignment_column_name : Optional[str]
            If defined, fold will be cut according to it.

        Returns
        -------
        CVFrames
        """
        splits = []

        if fold_assignment_column_name is None:
            name: str = "FOLD_COLUMN"
            df = internal.append_fold_column(df, name, nfolds)
        else:
            if fold_assignment_column_name not in df.columns:
                raise ExodusMethodNotAllowed(
                    f"Fold column {fold_assignment_column_name} not found in dataframe"
                )
            name = fold_assignment_column_name

        for fold in range(nfolds):
            train = internal.select_and_drop_fold_column(df, name, fold, test=False)
            test = internal.select_and_drop_fold_column(df, name, fold, test=True)
            splits.append(SplitFrames(train=train, validation=validation_df, test=test))
        return cls(splits=splits)
