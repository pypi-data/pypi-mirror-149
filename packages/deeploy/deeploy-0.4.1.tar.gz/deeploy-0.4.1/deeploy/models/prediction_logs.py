from pydantic import BaseModel
from typing import List
from deeploy.models import PredictionLog


class PredictionLogs(BaseModel):
    data: List[PredictionLog]
    count: int
