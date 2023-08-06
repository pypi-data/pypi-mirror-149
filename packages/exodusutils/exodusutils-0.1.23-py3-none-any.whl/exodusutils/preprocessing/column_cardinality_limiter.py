from exodusutils.exceptions.exceptions import ExodusMethodNotAllowed
from exodusutils.enums import DataType
from exodusutils.schemas import Column
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from exodusutils.internal.process_unit import ProcessUnit


class ColumnCardinalityLimiter(ProcessUnit):
    """
    Limits the number of distinct labels within one categorical column.

    The default max. cardinality is 30. Any other categorical labels will be turned into the same `\"InvalidLabel\"` label.
    """

    def __init__(self, feature_types: List[Column], target_column_name: str, max_cardinality: int = 30, invalid_label: str = "InvalidLabel") -> None:
        self.feature_types = feature_types
        self.target_column_name = target_column_name
        self.max_cardinality = max_cardinality
        self.invalid_label = invalid_label
        self.cardinalities: Optional[Dict[str, List[str]]] = None

    def fitted(self) -> bool:
        return self.cardinalities is not None

    def fit(self, df: pd.DataFrame) -> None:
        self.cardinalities = {}
        for column_name in [
            c.name
            for c in self.feature_types
            if c.data_type == DataType.string and df[c.name].nunique() > self.max_cardinality
        ]:
            self.cardinalities[column_name] = (
                df[column_name]
                .replace("", np.nan)
                .value_counts()
                .index[:self.max_cardinality]
                .to_list()
            )

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.fitted():
            raise ExodusMethodNotAllowed("Has to fit before transform")
        for column_name, valid_labels in self.cardinalities.items():
            df.loc[
                (~df[column_name].isin(valid_labels)) & (df[column_name].notnull()),
                [column_name],
            ] = self.invalid_label
        return df
