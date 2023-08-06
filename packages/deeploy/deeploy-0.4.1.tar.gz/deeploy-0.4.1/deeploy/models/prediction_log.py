from pydantic import BaseModel
from typing import Optional, Dict


class PredictionLog(BaseModel):
    id: str
    deploymentId: str
    requestBody: Optional[Dict]
    responseBody: Optional[Dict]
    responseTimeMS: int
    statusCode: int
    createdAt: str
    predictionValidation: Optional[Dict]
