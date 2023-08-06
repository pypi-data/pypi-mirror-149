from exodusutils.exceptions.exceptions import ExodusMethodNotAllowed
from typing import List, Optional
from exodusutils import internal
import numpy as np
import pandas as pd
from exodusutils.internal.process_unit import ProcessUnit


class OneHotEncoding(ProcessUnit):
    """
    Does one-hot encoding. If a dummy column that we found during `fit` is not there during `transform`, \
we create the column in the to-be-transformed dataframe, and fill it with `0`.
    """
    def __init__(self, target_column_name: str) -> None:
        self.target_column_name = target_column_name
        self.dummy_columns: Optional[List[str]] = None

    def fitted(self) -> bool:
        return self.dummy_columns is not None

    def fit(self, df: pd.DataFrame) -> None:
        categorical_columns = [c for c in internal.get_columns(df, object) if c != self.target_column_name]
        dummy = pd.get_dummies(df, columns=categorical_columns, dtype=np.int64)
        self.dummy_columns = [col for col in dummy.columns.to_list() if col not in df]

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.fitted():
            raise ExodusMethodNotAllowed("Has to fit before transform")
        categorical_columns = [c for c in internal.get_columns(df, object) if c != self.target_column_name]
        dummy = pd.get_dummies(df, columns=categorical_columns, dtype=np.int64)
        for c in self.dummy_columns:
            if c not in dummy.columns:
                dummy[c] = 0
        return dummy
