from . import BaseModel
from deeploy.enums import ModelType


class ONNXModel(BaseModel):
    # TODO
    def save(self, local_folder_path: str) -> None:
        return

    def get_model_type(self) -> ModelType:
        return ModelType.ONNX
