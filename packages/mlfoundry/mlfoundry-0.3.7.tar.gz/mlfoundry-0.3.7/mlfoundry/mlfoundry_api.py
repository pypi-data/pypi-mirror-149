"""
# TO independently test this module, you can run the example in the path
python examples/sklearn/iris_train.py

Besides running pytest
"""
import datetime
import logging
import os
import typing
import urllib
from functools import partial

import human_id
import mlflow
import pandas as pd
from mlflow.entities import ViewType
from mlflow.store.artifact.artifact_repository_registry import (
    _artifact_repository_registry,
)
from mlflow.tracking import MlflowClient
from mlflow.tracking._tracking_service.utils import _get_default_host_creds

from mlfoundry import amplitude, constants
from mlfoundry.artifact.truefoundry_artifact_repo import TruefoundryArtifactRepository
from mlfoundry.exceptions import MlflowException, MlFoundryException
from mlfoundry.inference.store import (
    ActualPacket,
    InferencePacket,
    InferenceStoreClient,
    ValueType,
    get_inference_store,
)
from mlfoundry.internal_namespace import NAMESPACE
from mlfoundry.mlfoundry_run import MlFoundryRun
from mlfoundry.session import Session
from mlfoundry.tracking.auth_service import AuthService
from mlfoundry.tracking.truefoundry_rest_store import TruefoundryRestStore

logger = logging.getLogger(__name__)


def init_rest_tracking(tracking_uri: str, api_key: typing.Optional[str]):
    get_cred = partial(_get_default_host_creds, tracking_uri)
    rest_store = TruefoundryRestStore(get_cred)
    auth_service = AuthService()

    session = Session(auth_service=auth_service, tracking_service=rest_store)
    session.init_session(api_key)

    artifact_repository = partial(TruefoundryArtifactRepository, rest_store=rest_store)
    _artifact_repository_registry.register("s3", artifact_repository)


def get_client(
    tracking_uri: typing.Optional[str] = None,
    inference_store_uri: typing.Optional[str] = None,
    disable_analytics: bool = False,
    api_key: typing.Optional[str] = None,
):
    # TODO (chiragjn): Will potentially need to make MlFoundry (and possibly MlFoundryRun) a Singleton instance.
    #                  Since this sets the tracking URI in global namespace, if someone were to call
    #                  get_client again with different tracking uri, the ongoing run's data will start getting
    #                  pushed to another datastore. Or we should not allow passing in tracking URI and just have
    #                  fixed online and offline clients
    amplitude.init(disable_analytics)
    if tracking_uri is None:
        tracking_uri = "file:" + os.path.abspath(constants.MLRUNS_FOLDER_NAME)
    elif tracking_uri.startswith("file:"):
        tracking_uri = os.path.join(tracking_uri, constants.MLRUNS_FOLDER_NAME)
    else:
        init_rest_tracking(tracking_uri=tracking_uri, api_key=api_key)
    amplitude.track(
        amplitude.Event.GET_CLIENT,
        # tracking whether user is using file:// or https://
        event_properties={
            "tracking_scheme": urllib.parse.urlparse(tracking_uri).scheme
        },
    )
    return MlFoundry(tracking_uri, inference_store_uri=inference_store_uri)


class MlFoundry:
    def __init__(
        self,
        tracking_uri: typing.Optional[str] = None,
        inference_store_uri: typing.Optional[str] = None,
    ):
        try:
            mlflow.set_tracking_uri(tracking_uri)
        except MlflowException as e:
            err_msg = (
                f"Could not initialise mlfoundry object. Error details: {e.message}"
            )
            raise MlFoundryException(err_msg) from e

        self.mlflow_client = MlflowClient()
        self.inference_store_client: typing.Optional[InferenceStoreClient] = (
            InferenceStoreClient(lambda: get_inference_store(inference_store_uri))
            if inference_store_uri is not None
            else None
        )

    def _get_or_create_experiment(
        self, experiment_name: str, owner: typing.Optional[str]
    ):
        """
        Creates a experiment and returns the experiment id. This experiment is to be passed into run.
        :param
            experiment_name: A unique experiment name
            owner (Optional: str): owner of the project. If owner is not passed,
                                   the current user will be used as owner. If the given owner
                                   does not have the project, it will be created under
                                   the current user.

        :return: The experiment_id of created experiment

        Example:
        >> create_experiment('experiment-1')
        """

        try:
            experiment = self.mlflow_client.get_experiment_by_name(
                experiment_name, owner_subject_id=owner
            )
            if experiment is not None:
                return experiment.experiment_id
            if not owner:
                logger.info(
                    f"project {experiment_name} does not exist. Creating {experiment_name}."
                )
                return self.mlflow_client.create_experiment(experiment_name)
            else:
                logger.warning(
                    f"project {experiment_name} under owner {owner} does not exist. "
                    "looking for project under current user."
                )
                return self._get_or_create_experiment(
                    experiment_name=experiment_name, owner=None
                )
        except MlflowException as e:
            err_msg = (
                f"Error happened in creating or getting experiment based on experiment name: "
                f"{experiment_name}. Error details: {e.message}"
            )
            raise MlFoundryException(err_msg) from e

    def get_all_projects(self):
        """
        Returns names of all the projects
        """
        amplitude.track(amplitude.Event.GET_ALL_PROJECTS)
        try:
            experiments = self.mlflow_client.list_experiments(view_type=ViewType.ALL)
        except MlflowException as e:
            err_msg = (
                f"Error happened in fetching project names. Error details: {e.message}"
            )
            raise MlFoundryException(err_msg) from e

        projects = []
        for e in experiments:
            # Experiment ID 0 represents default project which we are removing.
            if e.experiment_id != "0":
                projects.append(e.name)

        return projects

    def rename_project(self, old_project_name: str, new_project_name: str):
        """
        Renames a project.
        :param old_project_name: Existing project name
        :param new_project_name: New Project name
        """

        amplitude.track(amplitude.Event.RENAME_PROJECT)
        try:
            experiment_id = self.mlflow_client.get_experiment_by_name(
                old_project_name
            ).experiment_id

            self.mlflow_client.rename_experiment(experiment_id, new_project_name)
        except MlflowException as e:
            err_msg = (
                f"Error happened in renaming project from {old_project_name} to "
                f"{new_project_name}. Error details: {e.message}"
            )
            raise MlFoundryException(err_msg) from e

    def create_run(
        self,
        project_name: str,
        run_name: typing.Optional[str] = None,
        tags: typing.Optional[typing.Dict[str, typing.Any]] = None,
        owner: typing.Optional[str] = None,
        **kwargs,
    ) -> MlFoundryRun:
        """
        Creates a run for the given project_name.Each run will have a unique run_id.
        If run_name is not provided, then a name is generated automatically.

        Args:
            project_name (str): name of a project
            run_name (Optional[str]): name of the run
            tags (Optional: Dict[str, Any]): Tags to associate with this run
            owner (Optional: str): owner of the project. If owner is not passed,
                                   the current user will be used as owner. If the given owner
                                   does not have the project, it will be created under
                                   the current user.
            kwargs: Keyword arguments for MlFoundryRun.__init__
                log_system_metrics (bool): if to automatically collect and log system metrics
        Returns:
            MlFoundryRun: an MlFoundryRun with specified experiment and unique run_id

        Examples:
            >>> import mlfoundry as mlf
            >>> client = mlf.get_client()
            >>> mlf_run = client.create_run(project_name='my_project')
        """

        amplitude.track(amplitude.Event.CREATE_RUN)
        if not run_name:
            run_name = human_id.generate_id(word_count=3)
        if project_name == "" or (not isinstance(project_name, str)):
            raise MlFoundryException(
                f"project_name must be string type and not empty. "
                f"Got {type(project_name)} type with value {project_name}"
            )

        experiment_id = self._get_or_create_experiment(project_name, owner=owner)

        if tags is not None:
            NAMESPACE.validate_namespace_not_used(tags.keys())
        else:
            tags = {}

        run = self.mlflow_client.create_run(experiment_id, name=run_name, tags=tags)
        mlf_run_id = run.info.run_id

        mlf_run = MlFoundryRun(experiment_id, mlf_run_id, **kwargs)
        mlf_run._add_git_info()
        logger.info(f"Run is created with id {mlf_run_id!r} and name {run_name!r}")
        return mlf_run

    def get_run(self, run_id: str) -> MlFoundryRun:
        """Given the run_id returns the Python MlFoundryRun object that is created already.

        Args:
            run_id (str): run_id that was created already.

        Returns:
            MlFoundryRun: returns the run object that was created already.

        Example:
        >> run = get_run(<run_id>)
        """
        amplitude.track(amplitude.Event.GET_RUN)
        if run_id == "" or (not isinstance(run_id, str)):
            raise MlFoundryException(
                f"run_id must be string type and not empty. "
                f"Got {type(run_id)} type with value {run_id}"
            )

        run = self.mlflow_client.get_run(run_id)
        experiment_id = run.info.experiment_id
        return MlFoundryRun(experiment_id, run.info.run_id)

    def get_all_runs(self, project_name: str, owner: typing.Optional[str] = None):
        """Returns all the run that was created by the user under the project project_name
        Args:
            project_name (str): name of the project
            owner (Optional: str): owner of the project. If owner is not passed,
                                   the current user will be used as owner.

        Returns:
            pd.DataFrame: dataframe with two columns- run_id and run_name
        """
        amplitude.track(amplitude.Event.GET_ALL_RUNS)
        if project_name == "" or (not isinstance(project_name, str)):
            raise MlFoundryException(
                f"project_name must be string type and not empty. "
                f"Got {type(project_name)} type with value {project_name}"
            )
        experiment = self.mlflow_client.get_experiment_by_name(
            project_name, owner_subject_id=owner
        )
        if experiment is None:
            return pd.DataFrame(
                columns=[constants.RUN_ID_COL_NAME, constants.RUN_NAME_COL_NAME]
            )

        experiment_id = experiment.experiment_id

        try:
            all_run_infos = self.mlflow_client.list_run_infos(
                experiment_id, run_view_type=ViewType.ALL
            )
        except MlflowException as e:
            err_msg = f"Error happened in while fetching runs for project {project_name}. Error details: {e.message}"
            raise MlFoundryException(err_msg) from e

        runs = []

        for run_info in all_run_infos:
            try:
                run = self.mlflow_client.get_run(run_info.run_id)
                run_name = run.info.name or run.data.tags.get(
                    constants.RUN_NAME_COL_NAME, ""
                )
                runs.append((run_info.run_id, run_name))
            except MlflowException as e:
                logger.warning(
                    f"Could not fetch details of run with run_id {run_info.run_id}. "
                    f"Skipping this one. Error details: {e.message}. "
                )

        return pd.DataFrame(
            runs, columns=[constants.RUN_ID_COL_NAME, constants.RUN_NAME_COL_NAME]
        )

    @staticmethod
    def get_tracking_uri():
        return mlflow.tracking.get_tracking_uri()

    def log_prediction(
        self,
        model_name: str,
        model_version: str,
        inference_id: str,
        features: ValueType,
        predictions: ValueType,
        raw_data: typing.Optional[ValueType] = None,
        actuals: typing.Optional[ValueType] = None,
        occurred_at: typing.Optional[int] = None,
    ):
        if self.inference_store_client is None:
            raise MlFoundryException(
                "Pass inference_store_uri in get_client function to use log_prediction"
            )
        if occurred_at is None:
            occurred_at = datetime.datetime.utcnow()
        elif not isinstance(occurred_at, int):
            raise TypeError("occurred_at should be unix epoch")
        else:
            occurred_at = datetime.datetime.utcfromtimestamp(occurred_at)
        inference_packet = InferencePacket(
            model_name=model_name,
            model_version=model_version,
            features=features,
            predictions=predictions,
            inference_id=inference_id,
            raw_data=raw_data,
            actuals=actuals,
            occurred_at=occurred_at,
        )
        self.inference_store_client.log_predictions([inference_packet])

    def log_actuals(self, model_name: str, inference_id: str, actuals: ValueType):
        if self.inference_store_client is None:
            raise MlFoundryException(
                "Pass inference_store_uri in get_client function to use log_prediction"
            )
        actuals_packet = ActualPacket(
            model_name=model_name, inference_id=inference_id, actuals=actuals
        )
        self.inference_store_client.log_actuals([actuals_packet])
