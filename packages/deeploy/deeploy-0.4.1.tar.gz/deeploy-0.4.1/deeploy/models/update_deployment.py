from typing import Optional, Dict, Any, List

from pydantic import BaseModel


class UpdateDeployment(BaseModel):
    """Class that contains the options for updating a model
    """  # noqa
    deployment_id: str
    name: Optional[str]
    kfserving_id: Optional[str]
    status: Any
    commit: Optional[str]
    commit_message: Optional[str]
    contract_path: Optional[str]
    model_type: Optional[Any]
    model_serverless: Optional[bool] = False
    model_instance_type: Optional[str]
    model_cpu_limit: Optional[float]
    model_cpu_request:  Optional[float]
    model_mem_limit: Optional[int]
    model_mem_request: Optional[int]
    explainer_type: Optional[Any]
    explainer_serverless: Optional[bool] = False
    explainer_instance_type: Optional[str]
    explainer_instance_type: Optional[str]
    explainer_cpu_limit: Optional[float]
    explainer_cpu_request:  Optional[float]
    explainer_mem_limit: Optional[int]
    explainer_mem_request: Optional[int]
    prediction_method: Optional[str] = None

    def to_request_body(self) -> Dict:
        request_body = {
            'id': self.deployment_id,
            'name': self.name,
            'kfServingId': self.kfserving_id,
            'status': self.status,
            'commit': self.commit,
            'commitMessage': self.commit_message,
            'contractPath': self.contract_path,
            'modelType': self.model_type,
            'modelServerless': self.model_serverless,
            'modelInstanceType': self.model_instance_type,
            'modelCpuLimit': self.model_cpu_limit,
            'modelCpuRequest': self.model_cpu_request,
            'modelMemLimit': self.model_mem_limit,
            'modelMemRequest': self.model_mem_request,
            'explainerType': self.explainer_type,
            'explainerServerless': self.explainer_serverless,
            'explainerInstanceType': self.explainer_instance_type,
            'explainerCpuLimit': self.explainer_cpu_limit,
            'explainerCpuRequest': self.explainer_cpu_request,
            'explainerMemLimit': self.explainer_mem_limit,
            'explainerMemRequest': self.explainer_mem_request,
            'predictionMethod': self.prediction_method
        }
        request_body = {k: v for k, v in request_body.items()
                        if v is not None}
        return {k: v for k, v in request_body.items() if v is not None and v != {}}


class UpdateDeploymentMetadata(BaseModel):
    """Class that contains the options for updating a model that doesn't require restarting pods
    """  # noqa
    deployment_id: str
    name: Optional[str]
    description: Optional[str]
    owner_id: Optional[str]
    has_example_input: Optional[bool]
    example_input: Optional[List[Any]]
    example_output: Optional[Any]
    input_tensor_size: Optional[str]
    output_tensor_size: Optional[str]

    def to_request_body(self) -> Dict:
        request_body = {
            'id': self.deployment_id,
            'name': self.name,
            'ownerId': self.owner_id,
            'description': self.description,
            'hasExampleInput': self.has_example_input,
            'exampleInput': self.example_input,
            'exampleOutput': self.example_output,
            'inputTensorSize': self.input_tensor_size,
            'outputTensorSize': self.output_tensor_size,
        }
        request_body = {k: v for k, v in request_body.items()
                        if v is not None}
        return {k: v for k, v in request_body.items() if v is not None and v != {}}
