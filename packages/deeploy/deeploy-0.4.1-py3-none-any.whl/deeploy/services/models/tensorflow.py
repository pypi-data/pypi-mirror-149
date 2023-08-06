from typing import Any
from os.path import join

from tensorflow import Module

from . import BaseModel
from deeploy.enums import ModelType


class TensorFlowModel(BaseModel):

    __tensorflow_model: Module

    def __init__(self, model_object: Any, **kwargs) -> None:

        if not issubclass(type(model_object), Module):
            raise Exception('Not a valid TensorFlow class')

        self.__tensorflow_model = model_object
        return

    def save(self, local_folder_path: str) -> None:
        self.__tensorflow_model.save(join(local_folder_path, '1'))
        return

    def get_model_type(self) -> ModelType:
        return ModelType.TENSORFLOW
