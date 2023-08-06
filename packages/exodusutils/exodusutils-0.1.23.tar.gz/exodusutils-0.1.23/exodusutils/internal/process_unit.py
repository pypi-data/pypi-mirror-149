import abc
from typing import Optional, Tuple

import pandas as pd


class ProcessUnit(abc.ABC):
    
    def fitted(self) -> bool:
        """Whether this process unit has been fitted or not."""
        raise NotImplementedError

    def fit(self, df: pd.DataFrame) -> None:
        """Fits this processing unit based on the given dataframe.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to fit this processing unit.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforms the given dataframe based on the results stored in this processing unit after calling `fit`.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to transform.

        Returns
        -------
        pd.DataFrame
            The transformed dataframe.

        """
        raise NotImplementedError

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fits this processing unit based on the dataframe, and then transform the dataframe based on the fit results.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to fit this processing unit and transformed.

        Returns
        -------
        pd.DataFrame
            The transformed dataframe.

        """
        self.fit(df)
        return self.transform(df)

    def maybe_transform(
        self, maybeDf: Optional[pd.DataFrame]
    ) -> Optional[pd.DataFrame]:
        """Transforms the input dataframe if it is not a `None`."""
        return None if maybeDf is None else self.transform(maybeDf)

    def run(self, training_df: pd.DataFrame, validation_df: Optional[pd.DataFrame], holdout_df: Optional[pd.DataFrame]) -> Tuple[pd.DataFrame, Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """
        Will do the following:
        - `fit_transform` on the training dataframe.
        - `transform` on the validation dataframe if it is not a `None`.
        - `transform` on the holdout dataframe if it is not a `None`.
        - Return the dataframes.
        """
        training_df = self.fit_transform(training_df)
        validation_df = self.maybe_transform(validation_df)
        holdout_df = self.maybe_transform(holdout_df)
        return training_df, validation_df, holdout_df
