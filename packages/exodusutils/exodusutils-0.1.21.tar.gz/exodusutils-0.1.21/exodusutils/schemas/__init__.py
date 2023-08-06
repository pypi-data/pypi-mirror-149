from pydantic import BaseModel

from exodusutils.enums import DataType


class Attribute(BaseModel):
    """A kv pair representing an attribute. Used for feature importances."""

    name: str
    value: float


class Column(BaseModel):
    """Represents a column in the dataframe."""

    name: str
    data_type: DataType

    class Config:
        use_enum_values = True
