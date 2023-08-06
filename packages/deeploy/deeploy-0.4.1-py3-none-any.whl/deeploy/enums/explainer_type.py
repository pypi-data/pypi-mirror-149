from enum import Enum


class ExplainerType(Enum):
    """Class that contains explainer types
    """  # noqa
    NO_EXPLAINER = 0
    ANCHOR_TABULAR = 1
    ANCHOR_IMAGES = 2
    ANCHOR_TEXT = 3
    SHAP_KERNEL = 4
    CUSTOM = 5
