from typing import Any, Dict, List, Optional

from pydantic import BaseModel
from pydantic.fields import Field

from exodusutils.schemas import Attribute
from exodusutils.schemas.scores import CVScores, Scores


class Attributes(BaseModel):
    cv_scores: CVScores
    variable_importance: List[Attribute] = []
    validation_scores: Optional[CVScores] = None
    holdout_scores: Optional[Scores] = None


class TrainRespBody(BaseModel):
    """
    The schema for train response body.
    """

    name: str = Field(description="The name of the model algorithm")
    model_id: str = Field(description="The specified model id")
    hyperparameters: Dict[str, Any] = Field(description="The hyperparameters")
    attributes: Attributes = Field(
        description="The attributes, including CV scores, validation scores, etc."
    )


class PredictRespBody(BaseModel):
    """
    The schema for prediction response body.
    """

    prediction: List[Dict[str, Any]] = Field(description="The prediction response")


class InfoRespBody(BaseModel):
    """
    The schema for info response body.
    """

    name: str = Field(description="Name of the model algorithm")
    description: str = Field(description="Description of the model algorithm")
