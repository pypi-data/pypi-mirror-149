from typing import Optional, Any, List

from pydantic import BaseModel


class CreateDeployment(BaseModel):
    """Class that contains the options for creating a deployment
    """  # noqa
    name: str
    description: Optional[str]
    repository_id: Optional[str]
    branch_name: Optional[str]
    commit: Optional[str]
    commit_message: Optional[str]
    contract_path: Optional[str]
    has_example_input: Optional[bool]
    example_input: Optional[List[Any]]
    example_output: Optional[Any]
    input_tensor_size: Optional[str]
    output_tensor_size: Optional[str]
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

    def to_request_body(self):
        return {
            'name': self.name,
            'description': self.description,
            'repositoryId': self.repository_id,
            'exampleInput': self.example_input,
            'exampleOutput': self.example_output,
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
            'branchName': self.branch_name,
            'commit': self.commit,
            'contractPath': self.contract_path,
            'predictionMethod': self.prediction_method
        }
