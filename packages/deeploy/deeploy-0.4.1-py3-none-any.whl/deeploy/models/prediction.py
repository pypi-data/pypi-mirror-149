from typing import List, Optional, Any

from pydantic import BaseModel


class Prediction(BaseModel):
    pass


class V1Prediction(Prediction):
    predictions: List[Any]


class V2Prediction(Prediction):
    predictions: List[Any]
    featureLabels: Optional[List[str]]
    requestLogId: Optional[str]
    predictionLogIds: Optional[List[str]]
