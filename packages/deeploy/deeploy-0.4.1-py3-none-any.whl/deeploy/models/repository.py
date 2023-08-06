from typing import Optional

from pydantic import BaseModel

from deeploy.common.functions import to_lower_camel


class Repository(BaseModel):
    id: str
    name: str
    status: int
    is_archived: bool
    workspace_id: str
    is_public: Optional[bool]
    remote_path: str
    created_at: str
    updated_at: str

    class Config:
        alias_generator = to_lower_camel
