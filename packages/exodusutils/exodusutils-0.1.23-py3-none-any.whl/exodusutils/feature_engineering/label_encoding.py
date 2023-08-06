from exodusutils import internal
from exodusutils.exceptions.exceptions import ExodusMethodNotAllowed
import pandas as pd
import numpy as np
from typing import Dict, Optional
from exodusutils.internal.process_unit import ProcessUnit
from sklearn.preprocessing import LabelEncoder
from enum import Enum

class HandleInvalidLabel(str, Enum):
    new_label = "new_label"
    invalid_label = "invalid_label"

class LabelEncoding(ProcessUnit):
    """
    Does label encoding. After fitting, objects of this class would contain a valid `encoders`, which includes \
the `sklearn.preprocessing.LabelEncoder` for each encoded columns.

    To handle unseen labels during `transform`, 2 methods are currently supported:
        - Use a label specifying invalid label (`-1`) to represent them. This is the default behavior.
        - Use an additional label (`len(encoder.classes_)`) to represent them.

    You can change the behavior while initializing this class.
    """
    def __init__(self, target_column_name: str, handle_invalid_label: HandleInvalidLabel = HandleInvalidLabel.invalid_label) -> None:
        self.target_column_name = target_column_name
        self.handle_invalid_label = handle_invalid_label
        self.encoders: Optional[Dict[str, LabelEncoder]] = None

    def fitted(self) -> bool:
        return self.encoders is not None

    def fit(self, df: pd.DataFrame) -> None:
        encoders = dict()
        for name in internal.get_columns(df, object):
            if name != self.target_column_name:
                encoders[name] = LabelEncoder().fit(
                    df.loc[df[name].notnull(), name].astype(str)
                )
        self.encoders = encoders

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.fitted():
            raise ExodusMethodNotAllowed("Has to fit before transform")
        for name, encoder in self.encoders.items():
            df.loc[
                ~df[name].isin(encoder.classes_), name
            ] = np.nan  # unseen values in training data
            df.loc[df[name].notnull(), name] = encoder.transform(
                df.loc[df[name].notnull()][name]
            )
            df.loc[df[name].isna(), name] = (
                -1 if self.handle_invalid_label.value  == HandleInvalidLabel.invalid_label else len(encoder.classes_)
            )  # if it's never seen before, just fill it with `-1`, which means the label is invalid
            df[name] = pd.to_numeric(pd.Series(df[name]), errors="coerce")
        return df

