import logging
from typing import Any, Tuple
import os
import shutil
import uuid
import json


from pydantic import parse_obj_as
from git import Repo

from deeploy.services import DeeployService, GitService, ModelWrapper, ExplainerWrapper
from deeploy.models import ClientConfig, Deployment, CreateDeployment, UpdateDeployment, \
    DeployOptions, UpdateOptions, V1Prediction, V2Prediction, ModelReferenceJson, PredictionLog, \
    PredictionLogs, UpdateDeploymentMetadata
from deeploy.enums import ExplainerType, ModelType
from deeploy.common.functions import delete_all_contents_in_directory, directory_exists, \
    directory_empty, file_exists


class Client(object):
    """
    A class for interacting with Deeploy
    """

    __config: ClientConfig

    def __init__(
            self, host: str, workspace_id: str, access_key: str = None, secret_key: str = None,
            deployment_token: str = None, branch_name: str = None) -> None:
        """Initialise the Deeploy client
        Parameters:
            host (str): The host at which Deeploy is located, i.e. deeploy.example.com
            workspace_id (str): The ID of the workspace in which your repository
                is located
            access_key (str): Personal Access Key generated from the Deeploy UI
            secret_key (str): Secret Access Key generated from the Deeploy UI
            token (str): Deployment token generated from the Deeploy UI
            branch_name (str, optional): The banchname on which to commit new models.
                Defaults to the current branchname.
        """

        self.__config = ClientConfig(**{
            'access_key': access_key,
            'secret_key': secret_key,
            'token': deployment_token,
            'host': host,
            'workspace_id': workspace_id,
            'branch_name': branch_name,
            'repository_id': '',
        })

        self.__deeploy_service = DeeployService(
            host,
            workspace_id,
            access_key,
            secret_key,
            deployment_token,
        )

        return

    def deploy(self, options: DeployOptions, local_repository_path: str,
               model: Any = None, explainer: Any = None, model_type: int = None,
               explainer_type: int = None, overwrite: bool = False,
               commit_message: str = None, contract_path: str = "") -> Deployment:
        """Deploy a model on Deeploy
        Parameters:
            model (Any): The class instance of an ML model
            options (DeployOptions): An instance of the deploy options class
                containing the deployment options
            local_repository_path (str): Absolute path to the local git repository
                which is connected to Deeploy
            explainer (Any, optional): The class instance of an optional model explainer
            model_type (int, optional): model type enum from ModelType class
            explainer_type (int, optional): mopel type enum from ExplainerType class
            overwrite (bool, optional): Whether or not to overwrite files that are in the
                'model' and 'explainer' folders in the git folder. Defaults to False
            commit_message (str, optional): Commit message to use
            contract_path (str, optional): Relative repository subpath that contains the
                Deeploy contract to deploy from
        """
        commit = False

        if not (self.__config.access_key and self.__config.secret_key):
            raise Exception('Missing access credentials to create deployment.')

        git_service = GitService(local_repository_path)

        repository_in_workspace, repository_id = self.__is_git_repository_in_workspace(git_service)

        if not repository_in_workspace:
            raise Exception(
                'Repository was not found in the Deeploy workspace. \
                 Make sure you have connected it before.')
        else:
            self.__config.repository_id = repository_id

        logging.info('Pulling from the remote repository...')
        git_service.pull()
        logging.info('Successfully pulled from the remote repository.')

        if options.modelDockerImage:
            model_type = ModelType.CUSTOM
            self.__prepare_model_directory(git_service, local_repository_path, overwrite)
            model_folder = os.path.join(
                local_repository_path, contract_path, 'model')
            shutil.rmtree(model_folder)
            os.mkdir(model_folder)
            self.__create_reference_file(
                model_folder, options.modelBlobReferenceUrl,
                options.modelDockerImage, options.modelDockerPort,
                options.modelDockerCredentialsId, options.modelBlobCredentialsId,
                options.modelDockerUri)
            git_service.add_folder_to_staging(os.path.join(contract_path, 'model'))
        elif options.modelBlobReferenceUrl and model_type:
            model_type = model_type
            self.__prepare_model_directory(git_service, local_repository_path, overwrite)
            model_folder = os.path.join(
                local_repository_path, contract_path, 'model')
            shutil.rmtree(model_folder)
            os.mkdir(model_folder)
            self.__create_reference_file(
                model_folder, options.modelBlobReferenceUrl,
                options.modelDockerImage, options.modelDockerPort,
                options.modelDockerCredentialsId, options.modelBlobCredentialsId,
                options.modelDockerUri)
            git_service.add_folder_to_staging(os.path.join(contract_path, 'model'))
        elif model:
            model_type = self.__process_model(
                model, options, local_repository_path, git_service, overwrite, contract_path).value
        else:
            self.__process_model(
                model, options, local_repository_path, git_service, overwrite, contract_path)
            reference_path = os.path.join(
                local_repository_path, contract_path, 'model', 'reference.json')
            if not os.path.exists(reference_path):
                raise Exception('Missing model reference file in repository.')

            try:
                with open(reference_path) as referenceFile:
                    data = json.load(referenceFile)
                    if 'reference' in data:
                        if "blob" in data['reference']:
                            model_type = model_type
                        elif "docker" in data['reference']:
                            model_type = ModelType.CUSTOM.value
                        else:
                            raise Exception('No information on to be deployed model available.')
                    else:
                        raise Exception('No information on to be deployed model available.')
            except IOError:
                raise Exception('Failed to deploy model from reference.json file.')

        commit_message = '[Deeploy Client] Add new model'

        if explainer:
            explainer_type = self.__process_explainer(
                explainer, local_repository_path, git_service, overwrite, contract_path)
            commit_message += ' and explainer'
        elif options.explainerBlobReferenceUrl or options.explainerDockerImage:
            explainer_type = ExplainerType.CUSTOM
            self.__prepare_explainer_directory(
                git_service, local_repository_path, overwrite, contract_path)
            explainer_folder = os.path.join(
                local_repository_path, contract_path, 'explainer')
            shutil.rmtree(explainer_folder)
            os.mkdir(explainer_folder)
            self.__create_reference_file(
                explainer_folder, options.explainerBlobReferenceUrl,
                options.explainerDockerImage, options.explainerDockerPort,
                options.explainerDockerCredentialsId, options.explainerBlobCredentialsId,
                options.explainerDockerUri)
            git_service.add_folder_to_staging(os.path.join(contract_path, 'explainer'))
            commit_message += ' and explainer'
        else:
            reference_path = os.path.join(
                local_repository_path, contract_path, 'explainer', 'reference.json')

            try:
                with open(reference_path) as referenceFile:
                    data = json.load(referenceFile)
                    if 'reference' in data:
                        if "blob" in data['reference']:
                            explainer_type = explainer_type
                        elif "docker" in data['reference']:
                            explainer_type = ExplainerType.CUSTOM.value
                        else:
                            raise Exception('No information on to be deployed explainer available.')
                    else:
                        raise Exception('No information on to be deployed explainer available.')
            except IOError:
                explainer_type = ExplainerType.NO_EXPLAINER.value

        metadata_path = os.path.join(local_repository_path, contract_path, 'metadata.json')
        self.__prepare_metadata_file(metadata_path, options.feature_labels, overwrite)
        git_service.add_folder_to_staging(os.path.join(contract_path, 'metadata.json'))

        if commit:
            logging.info('Committing and pushing the result to the remote.')
            commit_sha = git_service.commit(commit_message)
            git_service.push()
        else:
            commit_sha = Repo(local_repository_path).head.commit.hexsha

        deployment_options = {
            'name': options.name,
            'description': options.description,
            'repository_id': self.__config.repository_id,
            'example_input': options.example_input,
            'example_output': options.example_output,
            'model_type': model_type,
            'model_serverless': options.model_serverless,
            'model_instance_type': options.model_instance_type,
            'model_cpu_limit': options.model_cpu_limit,
            'model_cpu_request': options.model_cpu_request,
            'model_mem_limit': options.model_mem_limit,
            'model_mem_request': options.model_mem_request,
            'branch_name': git_service.get_current_branch_name(),
            'commit': commit_sha,
            'explainer_type': explainer_type,
            'explainer_serverless': options.explainer_serverless,
            'explainer_instance_type': options.explainer_instance_type,
            'explainer_cpu_limit': options.explainer_cpu_limit,
            'explainer_cpu_request': options.explainer_cpu_request,
            'explainer_mem_limit': options.explainer_mem_limit,
            'explainer_mem_request': options.explainer_mem_request,
            'prediction_method': options.prediction_method,
            'contract_path': contract_path,
        }

        deployment = self.__deeploy_service.create_deployment(
            self.__config.workspace_id, CreateDeployment(**deployment_options))

        return deployment

    def update(self, options: UpdateOptions, local_repository_path: str = None,
               model: Any = None, explainer: Any = None, model_type: int = None,
               explainer_type: int = None, overwrite: bool = False,
               commit: str = None, commit_message: str = None,
               contract_path: str = "") -> Deployment:
        """Update a model on Deeploy
        Parameters:
            model (Any): The class instance of an ML model
            options (UpdateOptions): An instance of the update options class
                containing the update options
            local_repository_path (str): Absolute path to the local git repository
                which is connected to Deeploy
            explainer (Any, optional): The class instance of an optional model explainer
            model_type (int, optional): model type enum from ModelType class
            explainer_type (int, optional): mopel type enum from ExplainerType class
            overwrite (bool, optional): Whether or not to overwrite files that are in the
                'model' and 'explainer' folders in the git folder. Defaults to False
            commit (str, optional): Commit SHA to update to
            commit_message (str, optional): Commit message to use
            contract_path (str, optional): Relative repository subpath that contains the
                Deeploy contract to deploy from
        """
        if not (self.__config.access_key and self.__config.secret_key):
            raise Exception('Missing access credentials to update deployment.')

        if not (self.__deeploy_service.get_deployment(self.__config.workspace_id,
                                                      options.deployment_id)):
            raise Exception(
                'Deployment was not found in the Deeploy workspace. \
                 Make sure the Deployment Id is correct.')

        current_deployment = self.__deeploy_service.get_deployment(
            self.__config.workspace_id, options.deployment_id)

        commit_sha = None

        if (model or explainer):
            if (local_repository_path is None):
                raise Exception(
                    'Local repository path is required to update \
                     the model or explainer.')
            else:
                git_service = GitService(local_repository_path)
                repository_in_workspace, repository_id = \
                    self.__is_git_repository_in_workspace(git_service)

            if not repository_in_workspace:
                raise Exception(
                    'Repository was not found in the Deeploy workspace. \
                     Make sure you have connected it before.')

            self.__config.repository_id = repository_id

            logging.info('Pulling from the remote repository...')
            git_service.pull()
            logging.info('Successfully pulled from the remote repository.')

            if model:
                model_wrapper = self.__process_model(
                    model, options, local_repository_path, git_service, overwrite, contract_path)
                model_type = model_wrapper.get_model_type().value
                commit_message = '[Deeploy Client] Add new model'
            else:
                # TODO: read existing reference.json and check if its a blob url or image
                # if blob url then require model_type else set model_type as custom
                model_type = model_type if model_type else ModelType.CUSTOM.value

            if explainer:
                explainer_wrapper = self.__process_explainer(
                    explainer, git_service, local_repository_path, overwrite, contract_path)
                explainer_type = explainer_wrapper.get_explainer_type().value
                if explainer_type != ExplainerType.NO_EXPLAINER.value:
                    commit_message += ' and explainer'
            else:
                # TODO: read existing reference.json and check if its a blob url or image
                # if blob url then require explainer_type else set explainer_type as custom
                explainer_type = explainer_type if explainer_type else ExplainerType.NO_EXPLAINER.value

            logging.info('Committing and pushing the result to the remote.')
            commit_sha = git_service.commit(commit_message)
            git_service.push()

        if commit:
            commit_sha = commit

        self.__config.repository_id = current_deployment.active_version['repositoryId']

        update_options = {
            'deployment_id': options.deployment_id,
            'name': options.name,
            'description': options.description,
            'repository_id': self.__config.repository_id,
            'example_input': options.example_input,
            'example_output': options.example_output,
            'model_type': model_type,
            'model_serverless': options.model_serverless,
            'model_instance_type': options.model_instance_type,
            'model_cpu_limit': options.model_cpu_limit,
            'model_cpu_request': options.model_cpu_request,
            'model_mem_limit': options.model_mem_limit,
            'model_mem_request': options.model_mem_request,
            'commit': commit_sha,
            'commit_message': commit_message,
            'explainer_type': explainer_type,
            'explainer_serverless': options.explainer_serverless,
            'explainer_instance_type': options.explainer_instance_type,
            'explainer_cpu_limit': options.explainer_cpu_limit,
            'explainer_cpu_request': options.explainer_cpu_request,
            'explainer_mem_limit': options.explainer_mem_limit,
            'explainer_mem_request': options.explainer_mem_request,
            'prediction_method': options.prediction_method,
            'contract_path': contract_path,
        }

        update_options = self.__remove_null_values(update_options)

        if (len(UpdateDeploymentMetadata(**update_options).json()) > 2):
            updated_deployment = self.__deeploy_service.update_deployment_metadata(
                self.__config.workspace_id, UpdateDeploymentMetadata(**update_options))

        if (len(UpdateDeployment(**update_options).json())) > 2:
            updated_deployment = self.__deeploy_service.update_deployment(
                self.__config.workspace_id, UpdateDeployment(**update_options))

        return updated_deployment

    def predict(self, deployment_id: str, request_body: dict) -> V1Prediction or V2Prediction:
        """Make a predict call
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            request_body (dict): Request body with input data for the model
        """

        workspace_id = self.__config.workspace_id
        prediction = self.__deeploy_service.predict(workspace_id, deployment_id, request_body)
        return prediction

    def explain(self, deployment_id: str, request_body: dict, image: bool = False) -> object:
        """Make an explain call
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            request_body (dict): Request body with input data for the model
            image (bool): Return image or not
        """
        workspace_id = self.__config.workspace_id
        explanation = self.__deeploy_service.explain(
            workspace_id, deployment_id, request_body, image)
        return explanation

    def getLogs(self, deployment_id: str) -> PredictionLogs:
        """Retrieve logs
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
        """
        workspace_id = self.__config.workspace_id
        logs = self.__deeploy_service.getLogs(workspace_id, deployment_id)
        return logs

    def getOneLog(self, deployment_id: str, log_id: str) -> PredictionLog:
        """Retrieve one log
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            log_id (str): ID of the log to be retrieved
        """
        workspace_id = self.__config.workspace_id
        log = self.__deeploy_service.getOneLog(workspace_id, deployment_id, log_id)
        return log

    def validate(self, deployment_id: str, log_id: str, validation_input: dict) -> None:
        """Validate a log
        Parameters:
            deployment_id (str): ID of the Deeploy deployment
            log_id (int): ID of the log to be validated
            validation_input: Dict with result, value, and explanation
        """
        workspace_id = self.__config.workspace_id
        self.__deeploy_service.validate(workspace_id, deployment_id,
                                        log_id, validation_input)

    def __are_clientoptions_valid(self, config: ClientConfig) -> bool:
        """Check if the supplied options are valid
        """
        try:
            self.__deeploy_service.get_workspace(config.workspace_id)
        except Exception as e:
            raise e

        return True

    def __is_git_repository_in_workspace(self, git_service: GitService) -> Tuple[bool, str]:
        remote_url = git_service.get_remote_url()
        workspace_id = self.__config.workspace_id

        repositories = self.__deeploy_service.get_repositories(workspace_id)

        correct_repositories = list(
            filter(lambda x: x.remote_path == self.__parse_url_ssh_to_https(remote_url) or
                   x.remote_path == remote_url, repositories))

        if len(correct_repositories) != 0:
            repository_id = correct_repositories[0].id
            return True, repository_id

        return False, None

    def __parse_url_ssh_to_https(self, remote_path: str) -> str or None:
        if (remote_path[:4] != 'git@'):
            path_tokens = remote_path.split('/')
            provider = path_tokens[2]
            user = path_tokens[3]
            path = path_tokens[4:]
            ssh_link = "git@" + provider + ":" + user
            for sub_directory in path:
                ssh_link += "/" + sub_directory
        else:
            ssh_link = None

        return ssh_link

    def __prepare_model_directory(self, git_service: GitService, local_repository_path: str,
                                  contract_path: str, overwrite) -> None:
        model_folder_path = os.path.join(
            local_repository_path, contract_path, 'model')
        if not directory_exists(model_folder_path):
            try:
                os.mkdir(model_folder_path)
            except OSError:
                logging.error("Creation of the directory %s failed" %
                              model_folder_path)
        elif not directory_empty(model_folder_path):
            if not overwrite:
                raise Exception(
                    'The folder %s is not empty. Pass \'overwrite=True\' to overwrite contents.' %
                    model_folder_path)
            delete_all_contents_in_directory(model_folder_path)
            git_service.delete_folder_from_staging('model')
        else:  # folder exists and empty
            pass
        return

    def __prepare_explainer_directory(self, git_service: GitService, local_repository_path: str,
                                      contract_path: str, overwrite) -> None:
        explainer_folder_path = os.path.join(
            local_repository_path, contract_path, 'explainer')
        if not directory_exists(explainer_folder_path):
            try:
                os.mkdir(explainer_folder_path)
            except OSError:
                logging.error("Creation of the directory %s failed" %
                              explainer_folder_path)
        elif not directory_empty(explainer_folder_path):
            if not overwrite:
                raise Exception(
                    'The folder %s is not empty. Pass \'overwrite=True\' to overwrite contents.' %
                    explainer_folder_path)
            delete_all_contents_in_directory(explainer_folder_path)
            git_service.delete_folder_from_staging('explainer')
        else:  # folder exists and empty
            pass
        return

    def __prepare_metadata_file(self, path: str, featureLabels=None,
                                overwrite=False) -> None:
        data = {
            'featureLabels': []
        }

        if featureLabels:
            data['featureLabels'] = featureLabels

        if file_exists(path) and not overwrite:
            pass
        else:
            try:
                with open(path, 'w') as f:
                    json.dump(data, f)
            except OSError:
                logging.error("Creation of the file %s failed" % path)

    def __get_upload_size(self, local_folder_path: str) -> int:
        total_file_sizes = 0
        for root, _, files in os.walk(local_folder_path):
            for single_file in files:
                file_path = os.path.join(root, single_file)
                file_size = os.path.getsize(file_path)
                total_file_sizes += file_size
        return total_file_sizes

    def __upload_folder_to_blob(self, local_repository_path: str, local_folder_path: str) -> str:
        upload_locations = list()
        blob_folder_uuid = str(uuid.uuid4())
        relative_folder_path = os.path.relpath(local_folder_path, local_repository_path)
        for root, _, files in os.walk(local_folder_path):
            for single_file in files:
                relative_file_path = os.path.join(
                    relative_folder_path, os.path.relpath(root, local_folder_path))
                file_path = os.path.join(root, single_file)
                blob_file_location = self.__deeploy_service.upload_blob_file(
                    file_path,
                    relative_file_path,
                    self.__config.workspace_id,
                    self.__config.repository_id,
                    blob_folder_uuid)
                upload_locations.append(blob_file_location)

        partition = upload_locations[0].partition(relative_folder_path)
        blob_folder_path = partition[0] + partition[1]
        return blob_folder_path

    def __remove_null_values(self, d: dict) -> dict:
        def empty(x):
            return x is None or x == {} or x == []

        if not isinstance(d, (dict, list)):
            return d
        elif isinstance(d, list):
            return [v for v in (self.__remove_null_values(v) for v in d) if not empty(v)]
        else:
            return {k: v for k, v in ((k, self.__remove_null_values(v))
                    for k, v in d.items()) if not empty(v)}

    def __create_reference_file(self, local_folder_path: str, blob_storage_link: str = None,
                                docker_image: str = None, docker_image_port: int = None,
                                docker_credentials: str = None, blob_credentials: str = None,
                                docker_uri: str = None) -> None:
        file_path = os.path.join(local_folder_path, 'reference.json')

        reference_json = {
            'reference': {
                'docker': {
                    'image': docker_image,
                    'uri': docker_uri,
                    'credentialsId': docker_credentials,
                    'port': docker_image_port,
                },
                'blob': {
                    'url': blob_storage_link,
                    'credentialsId': blob_credentials,
                },
            },
        }
        reference_json = self.__remove_null_values(reference_json)

        data = parse_obj_as(ModelReferenceJson, reference_json)

        with open(file_path, 'w') as outfile:
            json.dump(data.dict(), outfile)
        return

    def __process_model(self, model, options: DeployOptions or UpdateOptions,
                        local_repository_path: str, git_service: GitService,
                        overwrite: bool, contract_path: str) -> ModelType:
        logging.info('Saving the model to disk...')
        model_folder = os.path.join(
            local_repository_path, contract_path, 'model')
        model_wrapper = None
        if model:
            model_wrapper = ModelWrapper(
                model,
                pytorch_model_file_path=options.pytorch_model_file_path,
                pytorch_torchserve_handler_name=options.pytorch_torchserve_handler_name)
            model_wrapper.save(model_folder)
            self.__prepare_model_directory(
                git_service, local_repository_path, contract_path, overwrite)
            blob_storage_link = self.__upload_folder_to_blob(
                local_repository_path, model_folder)
            shutil.rmtree(model_folder)
            os.mkdir(model_folder)
            self.__create_reference_file(model_folder, blob_storage_link)
            git_service.add_folder_to_staging(os.path.join(contract_path, 'model'))
        return model_wrapper.get_model_type() if model else ModelType.CUSTOM

    def __process_explainer(self, explainer, git_service: GitService,
                            local_repository_path: str, overwrite: bool,
                            contract_path: str) -> ExplainerType:
        logging.info('Saving the explainer to disk...')
        explainer_wrapper = ExplainerWrapper(explainer)
        self.__prepare_explainer_directory(git_service, contract_path, overwrite)
        explainer_folder = os.path.join(
            local_repository_path, contract_path, 'explainer')
        explainer_wrapper.save(explainer_folder)
        blob_storage_link = self.__upload_folder_to_blob(
            local_repository_path, explainer_folder)
        shutil.rmtree(explainer_folder)
        os.mkdir(explainer_folder)
        self.__create_reference_file(explainer_folder, blob_storage_link)
        git_service.add_folder_to_staging(os.path.join(contract_path, 'explainer'))
        return explainer_wrapper
