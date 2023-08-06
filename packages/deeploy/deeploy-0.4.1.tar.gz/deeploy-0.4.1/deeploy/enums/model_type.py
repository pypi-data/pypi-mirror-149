from enum import Enum


class ModelType(Enum):
    """Class that contains model types
    """  # noqa
    TENSORFLOW = 0
    PYTORCH = 1
    SKLEARN = 2
    XGBOOST = 3
    ONNX = 4
    TRITON = 5
    CUSTOM = 6
