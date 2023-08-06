from typing import Any, List
import inspect

from deeploy.enums import ExplainerType
from deeploy.services.explainers import BaseExplainer


class ExplainerWrapper:

    __explainer_helper: BaseExplainer

    def __init__(self, explainer_object: Any) -> None:

        self.__explainer_helper = self.__get_explainer_helper(explainer_object)
        return

    def save(self, local_folder_path: str) -> None:
        self.__explainer_helper.save(local_folder_path)
        return

    def get_explainer_type(self) -> ExplainerType:
        return self.__explainer_helper.get_explainer_type()

    def __get_explainer_type(self, model_object: Any) -> ExplainerType:

        base_classes = list(map(lambda x: x.__module__ + '.' +
                                x.__name__, inspect.getmro(type(model_object))))

        if self.__is_alibi_anchor_text(base_classes):
            return ExplainerType.ANCHOR_TEXT
        if self.__is_alibi_anchor_images(base_classes):
            return ExplainerType.ANCHOR_IMAGES
        if self.__is_alibi_anchor_tabular(base_classes):
            return ExplainerType.ANCHOR_TABULAR
        if self.__is_shap_kernel(base_classes):
            return ExplainerType.SHAP_KERNEL

        raise NotImplementedError(
            'This explainer type is not implemented by Deeploy')

    def __get_explainer_helper(self, explainer_object) -> BaseExplainer:

        explainer_type = self.__get_explainer_type(explainer_object)

        # only import the helper class when it is needed
        if explainer_type == ExplainerType.ANCHOR_TEXT or \
                explainer_type == ExplainerType.ANCHOR_IMAGES or \
                explainer_type == ExplainerType.ANCHOR_TABULAR:
            from deeploy.services.explainers.alibi import AlibiExplainer
            return AlibiExplainer(explainer_object)
        if explainer_type == ExplainerType.SHAP_KERNEL:
            from deeploy.services.explainers.shap import SHAPExplainer
            return SHAPExplainer(explainer_object)

    def __is_alibi_anchor_text(self, base_classes: List[str]) -> bool:
        return 'alibi.explainers.anchor_text.AnchorText' in base_classes

    def __is_alibi_anchor_images(self, base_classes: List[str]) -> bool:
        return 'alibi.explainers.anchor_image.AnchorImage' in base_classes

    def __is_alibi_anchor_tabular(self, base_classes: List[str]) -> bool:
        return 'alibi.explainers.anchor_tabular.AnchorTabular' in base_classes

    def __is_shap_kernel(self, base_classes: List[str]) -> bool:
        return 'shap.explainers.kernel.KernelExplainer' in base_classes
