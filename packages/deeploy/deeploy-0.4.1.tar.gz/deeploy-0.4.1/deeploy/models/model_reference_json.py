from typing import Optional

from pydantic import BaseModel


class DockerReference(BaseModel):
    image: Optional[str]
    uri: Optional[str]
    port: Optional[int]
    credentialsId: Optional[str]


class BlobReference(BaseModel):
    url: str
    credentialsId: Optional[str]


class ModelReference(BaseModel):
    docker: Optional[DockerReference]
    blob: Optional[BlobReference]


class ModelReferenceJson(BaseModel):
    reference: ModelReference
