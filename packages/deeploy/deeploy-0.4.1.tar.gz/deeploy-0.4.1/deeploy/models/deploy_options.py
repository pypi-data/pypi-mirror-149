from typing import Optional, List, Any

from pydantic import BaseModel


class DeployOptions(BaseModel):
    """Class that contains the options for deploying a model
    """  # noqa

    name: str
    """str: name of the deployment"""  # noqa
    model_serverless = False
    """bool, optional: whether to deploy the model in a serverless fashion. Defaults to False"""  # noqa
    model_instance_type: Optional[str]
    """str, optional: The preferred instance type for the model pod.""" # noqa
    model_cpu_limit: Optional[float]
    """float, optional: CPU limit of model pod, in CPUs.""" # noqa
    model_cpu_request:  Optional[float]
    """float, optional: CPU request of model pod, in CPUs.""" # noqa
    model_mem_limit: Optional[int]
    """int, optional: RAM limit of model pod, in Megabytes.""" # noqa
    model_mem_request: Optional[int]
    """int, optional: RAM request of model pod, in Megabytes.""" # noqa
    explainer_serverless = False
    """bool, optional: whether to deploy the model in a serverless fashion. Defaults to False"""  # noqa
    explainer_instance_type: Optional[str]
    """str, optional: The preferred instance type for the model pod.""" # noqa  
    explainer_cpu_limit: Optional[float]
    """float, optional: CPU limit of model pod, in CPUs.""" # noqa
    explainer_cpu_request:  Optional[float]
    """float, optional: CPU request of model pod, in CPUs.""" # noqa
    explainer_mem_limit: Optional[int]
    """int, optional: RAM limit of model pod, in Megabytes.""" # noqa
    explainer_mem_request: Optional[int]
    """int, optional: RAM request of model pod, in Megabytes.""" # noqa
    description: Optional[str]
    """str, optional: the description of the deployment"""  # noqa
    example_input: Optional[List[Any]]
    """List, optional: list of example input parameters for the model"""  # noqa
    example_output: Optional[List[Any]]
    """List, optional: list of example output for the model"""  # noqa
    feature_labels: Optional[List[str]]
    """List, optional: list of feature labels for the explanations"""  # noqa
    pytorch_model_file_path: Optional[str]
    """str, optional: absolute or relative path to the .py file containing the pytorch model class definition"""  # noqa
    pytorch_torchserve_handler_name: Optional[str]
    """str, optional: TorchServe handler name. One of 
        ['image_classifier', 'image_classifier', 'object_detector', 'text_classifier']. 
        See the [TorchServe documentation](https://github.com/pytorch/serve/blob/master/docs/default_handlers.md#torchserve-default-inference-handlers)
        for more info."""  # noqa
    modelDockerImage: Optional[str] = None
    """str: url of the model's docker image"""  # noqa
    modelDockerUri: Optional[str] = None
    """str: docker uri of the model"""  # noqa
    modelDockerPort: Optional[str] = None
    """str: model's docker port to use"""  # noqa
    modelDockerCredentialsId: Optional[str] = None
    """str: credentials id of the model's docker image"""  # noqa
    modelBlobReferenceUrl: Optional[str] = None
    """str: url of the model's blob storage location""" # noqa
    modelBlobCredentialsId: Optional[str] = None
    """str: credentials id of the model's blob storage"""  # noqa
    explainerDockerImage: Optional[str] = None
    """str: url of the explainer's docker image"""  # noqa
    explainerDockerUri: Optional[str] = None
    """str: docker uri of the explainer"""  # noqa
    explainerDockerPort: Optional[str] = None
    """str: explainer's docker port to use"""  # noqa
    explainerDockerCredentialsId: Optional[str] = None
    """str: credentials id of the explainer's docker image"""  # noqa
    explainerBlobReferenceUrl: Optional[str] = None
    """str: url of the explainer's blob storage location""" # noqa
    explainerBlobCredentialsId: Optional[str] = None
    """str: credentials id of the explainer's blob storage"""  # noqa
    prediction_method: Optional[str] = None
    """str: Whether to use predict or predict_proba.""" # noqa
