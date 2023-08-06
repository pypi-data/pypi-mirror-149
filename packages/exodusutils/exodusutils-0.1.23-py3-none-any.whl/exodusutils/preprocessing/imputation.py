from enum import Enum
from typing import Any, Optional
from exodusutils.enums import DataType
from exodusutils.exceptions.exceptions import ExodusForbidden, ExodusMethodNotAllowed
from exodusutils.schemas import Column
import pandas as pd
import numpy as np
from exodusutils.internal.process_unit import ProcessUnit

class Method(str, Enum):
    """
    The currently supported imputation methods.
    """
    mode = "mode"
    mean = "mean"
    average = "average"
    zero = "zero"
    min = "min"
    max = "max"
    median = "median"


class Imputation(ProcessUnit):
    """
    Imputes the given column in the dataframe with a specified method.

    Available methods are:
    - "mode": Only supports non-empty columns
    - "mean": Only supports numeric columns
    - "average": Alias of "mean" method
    - "zero": Imputes numeric columns with 0, empty string "" for other types of columns
    - "min"
    - "max"
    - "median": Only supports numeric columns

    """
    def __init__(self, column: Column, method: Method) -> None:
        self.column = column
        self.method = method
        self.target: Optional[Any] = None

    def fitted(self) -> bool:
        return self.target is not None

    def fit(self, df: pd.DataFrame) -> None:
        values = pd.Series(df[df[self.column.name].notna()][self.column.name])
        if self.method == Method.mode:
            mode = values.mode().values.tolist()
            if mode:
                target = mode[0]
            else:
                raise ExodusMethodNotAllowed(
                    f"Cannot calculate mode of empty column = {self.column.name}"
                )
        elif self.method == Method.mean or self.method == Method.average:
            if self.column.data_type == DataType.double:
                target = values.mean()
            else:
                raise ExodusMethodNotAllowed(
                    f"Imputing categorical column = {self.column.name} with method = {self.method.value} is not supported"
                )
        elif self.method == Method.zero:
            if self.column.data_type == DataType.double:
                target = 0
            else:
                target = ""
        elif self.method == Method.min:
            target = values.min()
        elif self.method == Method.max:
            target = values.max()
        elif self.method == Method.median:
            if self.column.data_type == DataType.double:
                target = values.median()
            else:
                raise ExodusMethodNotAllowed(
                    f"Imputing categorical column = {self.column.name} with method = {self.method.value} is not supported"
                )
        else:
            raise ExodusMethodNotAllowed(f"Unsupported imputation method = {self.method.value}")
        if self.column.data_type == DataType.double and np.isnan(target):
            raise ExodusForbidden(f"Cannot impute column = {self.column.name} with np.nan")
        self.target = target

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.fitted():
            raise ExodusMethodNotAllowed("Has to fit before transform")
        return df.fillna(value={self.column.name: self.target})
