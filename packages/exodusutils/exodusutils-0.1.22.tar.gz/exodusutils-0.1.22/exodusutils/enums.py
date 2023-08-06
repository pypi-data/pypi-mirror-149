from datetime import datetime
from enum import Enum

from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype
from pydantic.main import BaseModel


class TimeUnit(str, Enum):
    """
    Represents a time unit.
    """

    hour = "hour"
    day = "day"
    month = "month"
    year = "year"

    def to_seasonality(self) -> int:
        """
        How many time units there is in a recurring pattern.

        For example, the seasonality of time unit `Month` would be `12`, since it's 12 months in a year.
        """
        if self.value == TimeUnit.hour:
            return 24
        elif self.value == TimeUnit.day:
            return 7
        elif self.value == TimeUnit.month:
            return 12
        else:
            return 1

    def to_resample_rule(self) -> str:
        """
        Turns the time unit to a string literal, which will then be used by pandas to resample the dataset.
        """
        if self.value == TimeUnit.year:
            return "YS"
        elif self.value == TimeUnit.month:
            return "MS"
        elif self.value == TimeUnit.day:
            return "D"
        else:
            return "H"

    def to_timedelta_unit(self) -> str:
        if self.value == TimeUnit.year:
            return "Y"
        elif self.value == TimeUnit.month:
            return "M"
        elif self.value == TimeUnit.day:
            return "D"
        else:
            return "h"

    def format_datetime(self, date: datetime) -> str:
        """Format a `datetime` based on this time unit.

        Parameters
        ----------
        date : datetime
            The `datetime` object to format.

        Returns
        -------
        The formatted `datetime` object as a `str`.
        """
        if self.value == TimeUnit.year:
            return date.strftime("%Y-01-01")
        elif self.value == TimeUnit.month:
            return date.strftime("%Y-%m-01")
        elif self.value == TimeUnit.day:
            return date.strftime("%Y-%m-%d")
        else:
            return date.strftime("%Y-%m-%dT%H:00:00")

    def to_prediction_format(self) -> str:
        """The corresponding format for parsing the dates in the prediction input data set."""
        if self.value == TimeUnit.hour:
            return "%Y-%m-%d %H:%M:%S"
        else:
            return "%Y-%m-%d"

    def to_last_date_format(self) -> str:
        """The corresponding format for parsing the last date in the training set."""
        if self.value == TimeUnit.hour:
            return "%Y-%m-%dT%H:%M:%S"
        else:
            return "%Y-%m-%d"


class ID(BaseModel):
    value: str


class DataType(str, Enum):
    string = "string"
    double = "double"
    timestamp = "timestamp"
    id = "id"

    def to_type(self):
        if self.value == DataType.string:
            return str
        elif self.value == DataType.double:
            return float
        elif self.value == DataType.timestamp:
            return datetime
        elif self.value == DataType.id:
            return ID
        else:
            raise RuntimeError("unprocessable data type")

    @classmethod
    def from_pandas(cls, arr_or_dtype):
        """
        Converts from Pandas types to our custom `DataType`.

        Can take either an array-ish input, or the pandas column dtype.
        """
        if is_numeric_dtype(arr_or_dtype):
            return cls.double
        elif is_datetime64_any_dtype(arr_or_dtype):
            return cls.timestamp
        else:
            return cls.string


class AlgoType(str, Enum):
    TS = "TS"
    IID = "IID"
