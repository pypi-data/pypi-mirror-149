from typing import List
import numpy as np
from exodusutils import internal
from exodusutils.enums import TimeUnit
import pandas as pd
from exodusutils.internal.process_unit import ProcessUnit


class TimeComponentEncoding(ProcessUnit):
    """
    Does time component encoding. The `fit` method does nothing.
    """

    def __init__(self, time_unit: TimeUnit = TimeUnit.hour) -> None:
        self.time_unit = TimeUnit(time_unit)
        self.components: List[str] = []

    def fit(self, df: pd.DataFrame) -> None:
        pass

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.components = []
        for column in internal.get_columns(df, np.datetime64):
            for prefixed_column_name, component in zip(
                internal.prefix_datetime_cols_with_time_components(column),
                internal.get_time_components(df, self.time_unit, column),
            ):
                if component is not None:
                    df[prefixed_column_name] = component
                    self.components.append(prefixed_column_name)
        return df
