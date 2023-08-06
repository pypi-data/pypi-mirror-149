from typing import Any
from os.path import join, exists
import os
import subprocess

from torch.nn import Module
from torch import save

from . import BaseModel
from deeploy.enums import ModelType
from deeploy.common import PYTORCH_CONFIG_FILE


class PyTorchModel(BaseModel):

    __pytorch_model: Module
    __model_file_path: str
    __handler_file_path: str = None

    def __init__(self, model_object: Any, pytorch_model_file_path: str,
                 pytorch_torchserve_handler_name: str = 'image_classifier', **kwargs) -> None:

        if not issubclass(type(model_object), Module):
            raise Exception('Not a valid PyTorch class')

        if not exists(pytorch_model_file_path):
            raise Exception('The Pytorch model file does not exist')

        if not (pytorch_model_file_path.endswith('.py') or
                pytorch_model_file_path.endswith('.ipynb')):
            raise Exception(
                'The Pytorch model file is not a supported file type. Use .py or .ipynb')

        self.__pytorch_model = model_object
        self.__model_file_path = pytorch_model_file_path
        self.__handler_name = pytorch_torchserve_handler_name
        return

    def save(self, local_folder_path: str) -> None:
        serialized_model_path = join(os.getcwd(), 'model.pt')
        mar_folder_path = join(local_folder_path, 'model-store')
        save(self.__pytorch_model.state_dict(), serialized_model_path)

        mar_command = "torch-model-archiver --model-name model --version 1.0 --serialized-file %s \
            --export-path %s" % (serialized_model_path, mar_folder_path)

        if self.__model_file_path.endswith('.py'):
            mar_command += " --model-file %s" % self.__model_file_path

        elif self.__model_file_path.endswith('.ipynb'):
            convert_command = "ipython nbconvert --to script %s" % self.__model_file_path

            ipy_process = subprocess.Popen(
                convert_command.split(), stdout=subprocess.PIPE)
            _, error = ipy_process.communicate()
            if error:
                raise Exception(error)

            mar_command += " --model-file %s" % self.__model_file_path.replace(
                '.ipynb', '.py')

        mar_command += " --handler %s" % self.__handler_name

        if not os.path.exists(mar_folder_path):
            os.makedirs(mar_folder_path)

        mar_process = subprocess.Popen(
            mar_command.split(), stdout=subprocess.PIPE)
        _, error = mar_process.communicate()
        if error:
            raise Exception(error)
        mar_process.wait()

        config_folder_path = join(local_folder_path, 'config')
        if not os.path.exists(config_folder_path):
            os.makedirs(config_folder_path)

        config_file_path = join(config_folder_path, 'config.properties')
        with open(config_file_path, "w+") as config_file:
            config_file.write(PYTORCH_CONFIG_FILE)

        return

    def get_model_type(self) -> ModelType:
        return ModelType.PYTORCH
