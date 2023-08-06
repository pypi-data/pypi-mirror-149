from typing import Any
from os.path import join

from xgboost import XGBClassifier, Booster

from . import BaseModel
from deeploy.enums import ModelType


class XGBoostModel(BaseModel):

    __xgboost_model: XGBClassifier

    def __init__(self, model_object: Any, **kwargs) -> None:

        if not issubclass(type(model_object), XGBClassifier) and \
                not issubclass(type(model_object), Booster):
            raise Exception('Not a valid XGBoost class')

        self.__xgboost_model = model_object
        return

    def save(self, local_folder_path: str) -> None:
        self.__xgboost_model.save_model(join(local_folder_path, 'model.bst'))
        return

    def get_model_type(self) -> ModelType:
        return ModelType.XGBOOST
