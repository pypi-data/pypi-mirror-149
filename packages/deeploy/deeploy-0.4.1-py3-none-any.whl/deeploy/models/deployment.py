from typing import Optional, List, Any, Dict

from pydantic import BaseModel

from deeploy.common.functions import to_lower_camel


class Deployment(BaseModel):
    name: str
    active_version: Optional[Dict]
    workspace_id: str
    description: Optional[str]
    example_input: Optional[List[Any]]
    example_output: Optional[List[Any]]
    status: int
    owner_id: str
    kf_serving_id: Optional[str]
    public_url: Optional[str]
    id: str
    created_at: str
    updated_at: str

    class Config:
        alias_generator = to_lower_camel
