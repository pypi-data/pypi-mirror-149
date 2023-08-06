from enum import Enum
from exodusutils.enums import DataType
from typing import List, Optional

import pandas as pd
from pydantic import BaseModel
from pydantic.class_validators import validator
from pydantic.fields import Field

from exodusutils import internal
from exodusutils.exceptions.exceptions import ExodusBadRequest
from exodusutils.schemas import Column


class TrainReqBodyBase(BaseModel):
    """
    The base schema for training requests.

    Attributes
    ----------
    training_data : bytes
        The training data as a sequence of bytes.
    feature_types : List[Column]
        The features present in training data.
    target : Column
        The target column. Must be present in `feature_types`.
    folds : int
        Number of folds for this experiment.
    """

    training_data: bytes = Field(description="The training data as a sequence of bytes")
    feature_types: List[Column] = Field(
        default=[], description="The features present in training data"
    )
    target: Column = Field(
        description="The target column. Must be present in feature_types"
    )
    folds: int = Field(
        default=5, ge=2, le=10, description="Number of folds for this experiment"
    )

    @validator("target")
    def check_column(cls, v, values):
        if v not in values.get("feature_types", []):
            raise ExodusBadRequest(
                f"target {v} not found in feature_types {values.get('feature_types', [])}"
            )
        return v

    @validator("feature_types")
    def validate_header(cls, v, values):
        data = values["training_data"]
        header = data.decode("utf-8").split("\n")[0].split(",")
        internal.validate_columns(header, v)
        return v

    def get_feature_names(self) -> List[str]:
        """
        Returns the names of the features.
        """
        return [f.name for f in self.feature_types]

    def get_training_df(self) -> pd.DataFrame:
        """
        Returns the Pandas DataFrame from the bytes in training_data field.
        """
        return internal.get_df(self.training_data, self.feature_types)

    def get_features(self, data_type: DataType) -> List[Column]:
        """
        Returns the features with the specified data type.

        Parameters
        ----------
        data_type : DataType
            The specified data type.

        Returns
        -------
        List[Column]
            The features.

        """
        return [f for f in self.feature_types if f.data_type == data_type]

    def get_feature_names_by_data_type(self, data_type: DataType) -> List[str]:
        """
        Helper function for extracting names for features with a specified type.

        Parameters
        ----------
        data_type : DataType
            The specified data type.

        Returns
        -------
        List[str]
            Names of the features.
        """
        return [f.name for f in self.get_features(data_type)]


class TrainIIDReqBody(TrainReqBodyBase):
    """
    The schema for IID training request body.

    Has the following fields:
    - `feature_types`: a list of `Column`s, which is the name of a feature and the feature's data type.
    - `target`: the target `Column`.
    - `folds`: number of cross validation folds we want to train.
    - `random_seed`: random seed. Optional.

    Get dataframes by calling the following methods:
    - `get_training_df`: returns the training data as a Pandas dataframe.
    - `get_holdout_df`: returns the holdout data as a Pandas dataframe if the field is not a `None`. Otherwise returns a `None`.
    - `get_validation_df`: returns the validation data as a Pandas dataframe if the field is not a `None`. Otherwise returns a `None`.
    """

    random_seed: Optional[int] = Field(
        default=None, description="The random seed for this experiment. Optional."
    )
    validation_data: Optional[bytes] = Field(
        default=None, description="The validation data as a sequence of bytes. Optional"
    )
    holdout_data: Optional[bytes] = Field(
        default=None, description="The holdout data as a sequence of bytes. Optional"
    )
    fold_assignment_column_name: Optional[str] = Field(
        default=None,
        description="The name of the fold assignment column. If not provided, Exodus will cut cross validation folds in a modulo fashion. If this field is defined, it is required to be a valid column in the input dataframe. This column is not included in `feature_types`, and will be discarded during training.",
    )

    @validator("fold_assignment_column_name")
    def validate_fold_column(cls, v, values):
        if v is not None:
            data = values["training_data"]
            header = data.decode("utf-8").split("\n")[0].split(",")
            if v not in header:
                raise ExodusBadRequest(
                    f"fold assignment column = {v} not found in header"
                )
        return v

    class Config:
        schema_extra = {
            "examples": [
                {
                    "training_data": "foo,bar\n0,abc\n1,def\n2,ghi\n3,jkl\n4,mnop\n5,qrs\n",
                    "feature_types": [
                        {"name": "foo", "data_type": "double"},
                        {"name": "bar", "data_type": "string"},
                    ],
                    "target": [{"name": "bar", "data_type": "string"}],
                    "folds": 3,
                    "validation_percentage": 0.2,
                    "holdout_data": "foo,bar\n99,zzz\n",
                }
            ]
        }

    def get_holdout_df(self) -> Optional[pd.DataFrame]:
        """
        Returns the Pandas DataFrame from the bytes in holdout_data field, or `None` if none specified.
        """
        if not self.holdout_data:
            return None
        else:
            return internal.get_df(self.holdout_data, self.feature_types)

    def get_validation_df(self) -> Optional[pd.DataFrame]:
        """
        Returns the Pandas DataFrame from the bytes in holdout_data field, or `None` if none specified.
        """
        if not self.validation_data:
            return None
        else:
            return internal.get_df(self.validation_data, self.feature_types)


class PredictReqBody(BaseModel):
    """
    The schema for prediction request body.
    """

    model_id: str = Field(description="The specified model id")
    data: str = Field(description="The prediction data as JSON")
    threshold: Optional[float] = Field(
        default=None, description="The threshold for classification predictions"
    )
    keep_columns: List[str] = Field(
        default=[], description="The columns to keep in the prediction response"
    )

    def get_prediction_df(self, feature_types: List[Column]) -> pd.DataFrame:
        """
        Returns the Pandas DataFrame from the bytes in data field.

        If the input data contains any column that is not in `feature_types`, that column will be
        dropped from the resulting dataframe.
        """
        valid_columns = [f.name for f in feature_types]
        df = pd.DataFrame(pd.read_json(self.data, orient="records"))
        valid_features = [f for f in feature_types if f.name in df.columns.tolist()]

        # We only want to keep the columns that are specified in `feature_types`
        return df.drop(
            [c for c in df.columns.tolist() if c not in valid_columns], axis=1
        ).pipe(internal.cast_df_types, valid_features)


class MigrateAction(str, Enum):
    """
    Defines the migration action. Could only be either one of `up` and `down`.
    """

    up = "up"
    down = "down"


class MigrateReqBody(BaseModel):
    """
    The schema for migrate request body.
    """

    action: MigrateAction = Field(description="The migration action")

    class Config:
        use_enum_values = True
