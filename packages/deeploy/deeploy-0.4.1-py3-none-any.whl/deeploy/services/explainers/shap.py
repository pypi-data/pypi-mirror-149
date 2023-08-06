from typing import Any
from os.path import join

import dill
from shap.explainers.explainer import Explainer

from . import BaseExplainer
from deeploy.enums import ExplainerType


class SHAPExplainer(BaseExplainer):

    __shap_explainer: Explainer

    def __init__(self, explainer_object: Any) -> None:

        if not issubclass(type(explainer_object), Explainer):
            raise Exception('Not a valid SHAP class')

        self.__shap_explainer = explainer_object
        return

    def save(self, local_folder_path: str) -> None:
        with open(join(local_folder_path, 'explainer.dill'), 'wb') as f:
            dill.dump(self.__shap_explainer, f)
        return

    def get_explainer_type(self) -> ExplainerType:
        return ExplainerType.SHAP_KERNEL
