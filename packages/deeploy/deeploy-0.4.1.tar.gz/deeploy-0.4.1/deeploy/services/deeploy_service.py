import base64
from typing import List

import requests
from pydantic import parse_obj_as

from deeploy.models import Deployment, Repository, CreateDeployment, Workspace, \
    V1Prediction, V2Prediction, PredictionLog, PredictionLogs, UpdateDeployment, \
    UpdateDeploymentMetadata
from deeploy.enums import PredictionVersion, AuthType


class DeeployService(object):
    """
    A class for interacting with the Deeploy API
    """

    def __init__(
            self, host: str, workspace_id: str, access_key: str = None, secret_key: str = None,
            token: str = None, insecure=False) -> None:
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__token = token
        self.__workspace_id = workspace_id
        self.__host = 'http://api.%s' % host if insecure else 'https://api.%s' % host

        if (access_key and secret_key) or token:
            if (access_key and secret_key) and not self.__keys_are_valid():
                raise Exception('Access keys are not valid.')
        else:
            raise Exception('Missing authentication data.')
        return

    def get_repositories(self, workspace_id: str) -> List[Repository]:
        url = '%s/v2/workspaces/%s/repositories' % (
            self.__host, workspace_id)
        params = {
            'isArchived': False,
        }

        repositories_response = requests.get(
            url, params=params, auth=(self.__access_key, self.__secret_key))

        repositories = parse_obj_as(
            List[Repository], repositories_response.json())

        return repositories

    def get_repository(self, workspace_id: str, repository_id: str) -> Repository:
        url = '%s/v2/workspaces/%s/repositories/%s' % (
            self.__host, workspace_id, repository_id)

        repository_response = requests.get(
            url, auth=(self.__access_key, self.__secret_key))
        if not self.__request_is_successful(repository_response):
            raise Exception('Repository does not exist in the workspace.')

        repository = parse_obj_as(Repository, repository_response.json())

        return repository

    def get_deployment(
            self, workspace_id: str, deployment_id: str,
            withExamples: bool = False) -> Deployment:
        url = '%s/v2/workspaces/%s/deployments/%s' % (self.__host, workspace_id, deployment_id)
        params = {
            'withExamples': withExamples,
        }
        deployment_response = requests.get(
            url, params=params, auth=(self.__access_key, self.__secret_key))
        if not self.__request_is_successful(deployment_response):
            raise Exception('Failed to retrieve the deployment: %s' %
                            str(deployment_response.json()))

        deployment = parse_obj_as(
            Deployment, deployment_response.json())

        return deployment

    def create_deployment(self, workspace_id: str, deployment: CreateDeployment) -> Deployment:
        url = '%s/v2/workspaces/%s/deployments' % (self.__host, workspace_id)
        data = deployment.to_request_body()

        deployment_response = requests.post(
            url, json=data, auth=(self.__access_key, self.__secret_key))
        if not self.__request_is_successful(deployment_response):
            raise Exception('Failed to create the deployment: %s' % str(deployment_response.json()))

        deployment = parse_obj_as(
            Deployment, deployment_response.json())

        return deployment

    def update_deployment(self, workspace_id: str, update: UpdateDeployment) -> Deployment:
        url = '%s/v2/workspaces/%s/deployments/%s' % (self.__host,
                                                      workspace_id,
                                                      update.deployment_id)
        data = update.to_request_body()

        deployment_response = requests.patch(
            url, json=data, auth=(self.__access_key, self.__secret_key))
        if not self.__request_is_successful(deployment_response):
            raise Exception('Failed to update the deployment: %s' % str(deployment_response.json()))

        deployment = parse_obj_as(
            Deployment, deployment_response.json())

        return deployment

    def update_deployment_metadata(self, workspace_id: str,
                                   update: UpdateDeploymentMetadata) -> Deployment:
        url = '%s/v2/workspaces/%s/deployments/%s/metadata' % (self.__host,
                                                               workspace_id,
                                                               update.deployment_id)
        data = update.to_request_body()

        deployment_response = requests.patch(
            url, json=data, auth=(self.__access_key, self.__secret_key))
        if not self.__request_is_successful(deployment_response):
            raise Exception('Failed to update the deployment: %s' % str(deployment_response.json()))

        deployment = parse_obj_as(
            Deployment, deployment_response.json()['data'])

        return deployment

    def get_workspace(self, workspace_id: str) -> Workspace:
        url = '%s/v2/workspaces/%s' % (self.__host, workspace_id)

        workspace_response = requests.get(
            url, auth=(self.__access_key, self.__secret_key))
        if not self.__request_is_successful(workspace_response):
            raise Exception('Workspace does not exist.')

        workspace = parse_obj_as(Workspace, workspace_response.json())

        return workspace

    def upload_blob_file(
            self, local_file_path: str, relative_folder_path: str, workspace_id: str,
            repository_id: str, uuid: str) -> str:
        url = '%s/v2/workspaces/%s/repositories/%s/upload' % (
            self.__host, workspace_id, repository_id)
        params = {
            'commitSha': uuid,
            'folderPath': relative_folder_path,
        }
        files = {'file': open(local_file_path, 'rb')}
        r = requests.post(url, files=files, params=params,
                          auth=(self.__access_key, self.__secret_key))

        blob_storage_path = r.json()['data']['referencePath']
        return blob_storage_path

    def predict(self, workspace_id: str, deployment_id: str,
                request_body: dict) -> V1Prediction or V2Prediction:
        url = '%s/v2/workspaces/%s/deployments/%s/predict' % (
            self.__host, workspace_id, deployment_id)

        prediction_response = requests.post(
            url, json=request_body, headers=self.__get_auth_header(AuthType.ALL))

        if not self.__request_is_successful(prediction_response):
            raise Exception('Failed to call predictive model.')
        prediction = self.__parse_prediction(prediction_response)
        return prediction

    def explain(self, workspace_id: str, deployment_id: str, request_body: dict,
                image: bool = False) -> object:
        url = '%s/v2/workspaces/%s/deployments/%s/explain' % (
            self.__host, workspace_id, deployment_id)
        params = {
            'image': str(image).lower(),
        }

        explanation_response = requests.post(
            url, json=request_body, params=params, headers=self.__get_auth_header(AuthType.ALL))

        if not self.__request_is_successful(explanation_response):
            raise Exception('Failed to call explainer model.')
        explanation = explanation_response.json()
        return explanation

    def getOneLog(self, workspace_id: str, deployment_id: str, log_id: str) -> PredictionLog:
        url = '%s/v2/workspaces/%s/deployments/%s/logs/%s' % (
            self.__host, workspace_id, deployment_id, log_id)
        params = {
            'logId': log_id
        }

        log_response = requests.get(
            url, params=params, headers=self.__get_auth_header(AuthType.ALL))

        if not self.__request_is_successful(log_response):
            raise Exception('Failed to get log %s.' % log_id)

        log = parse_obj_as(PredictionLog, log_response.json())
        return log

    def getLogs(self, workspace_id: str, deployment_id: str) -> PredictionLogs:
        url = '%s/v2/workspaces/%s/deployments/%s/logs' % (self.__host,
                                                           workspace_id,
                                                           deployment_id)

        logs_response = requests.get(
            url, headers=self.__get_auth_header(AuthType.ALL))

        if not self.__request_is_successful(logs_response):
            raise Exception('Failed to get logs.')
        logs = parse_obj_as(PredictionLogs, logs_response.json())
        return logs

    def validate(self, workspace_id: str, deployment_id: str, log_id: str,
                 validation_input: dict) -> None:
        url = "%s/v2/workspaces/%s/deployments/%s/logs/%s/validations" % (
            self.__host, workspace_id, deployment_id, log_id)

        if ((validation_input['result'] == 0) and ('value' in validation_input)):
            raise Exception('An overrule value can not be provided when confirming the inference.')

        validation_response = requests.post(
            url, json=validation_input,
            headers=self.__get_auth_header(AuthType.TOKEN))
        if not self.__request_is_successful(validation_response):
            if validation_response.status_code == 409:
                raise Exception('Log has already been validated.')
            elif validation_response.status_code == 401:
                raise Exception('No permission to perform this action.')
            else:
                raise Exception('Failed to request validation.')

    def __keys_are_valid(self) -> bool:
        host_for_testing = '%s/v2/workspaces' % self.__host

        workspaces_response = requests.get(
            host_for_testing, auth=(self.__access_key, self.__secret_key))
        if self.__request_is_successful(workspaces_response):
            return True
        return False

    def __token_is_valid(self, workspace_id, deployment_id) -> bool:
        host_for_testing = '%s/v2/workspaces/%s/deployments/%s/logs' % (
            self.__host, workspace_id, deployment_id)
        headers = {'Authorization': 'Bearer ' + self.__token}
        logs_response = requests.get(
            host_for_testing, headers=headers)
        if self.__request_is_successful(logs_response):
            return True
        return False

    def __request_is_successful(self, request: requests.Response) -> bool:
        if str(request.status_code)[0] == '2':
            return True
        return False

    def __check_prediction_version(self, prediction_response: dict) -> PredictionVersion:
        if len(prediction_response.json()) > 1:
            return PredictionVersion.V2
        else:
            return PredictionVersion.V1

    def __parse_prediction(self, prediction_response: dict) -> V1Prediction or V2Prediction:
        if self.__check_prediction_version(prediction_response) == PredictionVersion.V1:
            prediction = parse_obj_as(
                V1Prediction, prediction_response.json())
        else:
            prediction = parse_obj_as(
                V2Prediction, prediction_response.json())
        return prediction

    def __get_auth_header(self, supported_auth: AuthType):
        if (self.__access_key and self.__secret_key) and \
                (supported_auth == AuthType.BASIC or supported_auth == AuthType.ALL):
            credentials = self.__access_key + ":" + self.__secret_key
            b64Val = base64.b64encode(credentials.encode()).decode()
            header = {'Authorization': 'Basic %s' % b64Val}
        elif (self.__token) and \
                (supported_auth == AuthType.TOKEN or supported_auth == AuthType.ALL):
            header = {'Authorization': 'Bearer ' + self.__token}
        elif (self.__access_key and self.__secret_key) and \
                not (supported_auth == AuthType.BASIC or supported_auth == AuthType.ALL):
            raise Exception('This function currently does not support Basic authentication.')
        else:
            raise Exception('This function currently does not support Token authentication.')

        return header
