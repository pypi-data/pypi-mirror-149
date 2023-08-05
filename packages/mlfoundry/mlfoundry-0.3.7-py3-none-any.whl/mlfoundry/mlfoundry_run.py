import atexit
import datetime
import json
import logging
import os
import queue
import time
import weakref
from typing import Any, Collection, Dict, Iterable, List, Optional, Union

import mlflow
import numpy as np
import pandas as pd
import whylogs
from mlflow.entities import Metric, Param, RunStatus, RunTag
from mlflow.tracking import MlflowClient

from mlfoundry import amplitude, constants, enums
from mlfoundry.background.interface import Interface
from mlfoundry.background.sender import SenderJob
from mlfoundry.background.system_metrics import SystemMetricsJob
from mlfoundry.dataset import DataSet, TabularDatasetDriver
from mlfoundry.exceptions import MlflowException, MlFoundryException
from mlfoundry.frameworks import get_model_registry
from mlfoundry.git_info import GitInfo
from mlfoundry.internal_namespace import NAMESPACE
from mlfoundry.metrics.v1 import get_metrics_calculator as get_metrics_calculator_v1
from mlfoundry.metrics.v2 import ComputedMetrics
from mlfoundry.metrics.v2 import get_metrics_calculator as get_metrics_calculator_v2
from mlfoundry.run_utils import (
    NumpyEncoder,
    ParamsType,
    log_artifact_blob,
    process_params,
)
from mlfoundry.schema import Schema

logger = logging.getLogger(__name__)


class MlFoundryRun:
    # TODO (nikunjbjj): Seems like these artifact locations are defined in constants.py for loading.
    #  Need to change this.
    S3_MODELS_PATH = "models"
    S3_DATASET_PATH = "datasets"
    S3_STATS_PATH = "stats"
    S3_WHYLOGS_PATH = "whylogs"
    S3_METRICS_PATH = "multi_dimensional_metrics"

    def __init__(
        self, experiment_id: str, run_id: str, log_system_metrics: bool = True
    ):
        self.experiment_id = str(experiment_id)
        mlflow.get_experiment(self.experiment_id)
        self.run_id = run_id
        # TODO (chiragjn): Shouldn't mlflow_client be a protected/private member?
        self.mlflow_client = MlflowClient()
        self._dataset_module: TabularDatasetDriver = TabularDatasetDriver(
            mlflow_client=self.mlflow_client, run_id=run_id
        )
        self.model_uri = "runs:/" + str(self.run_id) + "/" + self.S3_MODELS_PATH
        # TODO (chiragjn): Make a settings module and allow enabling/disabling collection and changing intervals
        if log_system_metrics:
            # Interface and Sender do not belong under this condition but for now we don't need to init them otherwise
            self._interface = Interface(
                run_id=self.run_id,
                event_queue=queue.Queue(),
            )
            self._sender_job = SenderJob(
                interface=self._interface,
                mlflow_client=self.mlflow_client,
                interval=0.0,
            )
            self._system_metrics_job = SystemMetricsJob(
                pid=os.getpid(),
                interface=self._interface,
                num_samples_to_aggregate=15,
                interval=2.0,
            )
        else:
            self._interface = None
            self._sender_job = None
            self._system_metrics_job = None
        self._terminate_called = False
        self._start()

    def __repr__(self) -> str:
        return f"<{type(self).__name__} at 0x{id(self):x}: run_id={self.run_id!r}>"

    def __enter__(self):
        return self

    def _stop_background_jobs(self):
        """
        Stop launched background jobs (system metrics, sender) if any and try to finish them gracefully
        """
        # expect that this function can be called more than once in non-ideal scenarios and defend for it
        if not any([self._interface, self._system_metrics_job, self._sender_job]):
            return

        logger.info(
            f"Shutting down background jobs and syncing data for run with id {self.run_id!r}, "
            f"please don't kill this process..."
        )
        # Stop event producers
        if self._system_metrics_job:
            self._system_metrics_job.stop(timeout=2)
        # Stop accepting more events
        if self._interface:
            self._interface.close()
        # Finish consuming whatever is left
        if self._sender_job:
            try:
                self._sender_job.stop(disable_sleep=True, timeout=10)
            except KeyboardInterrupt:
                # TODO (chiragjn): Separate internal logging and stream to show messages to user
                print(
                    "Ctrl-C interrupt detected, background jobs are still terminating. "
                    "Press Ctrl-C again to stop."
                )
                self._sender_job.stop(disable_sleep=True, timeout=10)
        self._system_metrics_job = None
        self._sender_job = None
        self._interface = None

    def _terminate_run_if_running(self, termination_status: RunStatus):
        if self._terminate_called:
            return

        # Prevent double execution for termination
        self._terminate_called = True

        current_status = None
        try:
            # TODO (chiragjn): This is a network call, should we just cache it on the instance?
            current_status = self.mlflow_client.get_run(self.run_id).info.status
        except Exception as e:
            logger.warning(f"failed to get run status {termination_status} due to {e}")

        try:
            self._stop_background_jobs()
            # we do not need to set any termination status unless the run was in RUNNING state
            if current_status != RunStatus.to_string(RunStatus.RUNNING):
                return
            self.mlflow_client.set_terminated(
                self.run_id, RunStatus.to_string(termination_status)
            )
        except Exception as e:
            logger.warning(
                f"failed to set termination status {termination_status} due to {e}"
            )

    def __exit__(self, exc_type, exc_val, exc_tb):
        status = RunStatus.FINISHED if exc_type is None else RunStatus.FAILED
        self._terminate_run_if_running(status)

    def __del__(self):
        # TODO (chiragjn): Should this be marked as FINISHED or KILLED?
        self._terminate_run_if_running(RunStatus.FINISHED)

    def _start(self):
        def terminate_run_if_running_with_weakref(
            mlf_run_weakref: "weakref.ReferenceType[MlFoundryRun]",
            termination_status: RunStatus,
        ):
            _run = mlf_run_weakref()
            if _run:
                _run._terminate_run_if_running(termination_status)

        atexit.register(
            terminate_run_if_running_with_weakref, weakref.ref(self), RunStatus.FINISHED
        )
        if self._sender_job:
            self._sender_job.start()
        if self._system_metrics_job:
            self._system_metrics_job.start()

    def end(self):
        self._terminate_run_if_running(RunStatus.FINISHED)

    def _add_git_info(self, root_path: Optional[str] = None):
        root_path = root_path or os.getcwd()
        try:
            git_info = GitInfo(root_path)
            tags = [
                RunTag(
                    key=constants.GIT_COMMIT_TAG_NAME,
                    value=git_info.current_commit_sha,
                ),
                RunTag(
                    key=constants.GIT_BRANCH_TAG_NAME,
                    value=git_info.current_branch_name,
                ),
                RunTag(key=constants.GIT_DIRTY_TAG_NAME, value=str(git_info.is_dirty)),
            ]
            remote_url = git_info.remote_url
            if remote_url is not None:
                tags.append(RunTag(key=constants.GIT_REMOTE_URL_NAME, value=remote_url))
            self.mlflow_client.log_batch(run_id=self.run_id, tags=tags)
            log_artifact_blob(
                mlflow_client=self.mlflow_client,
                run_id=self.run_id,
                blob=git_info.diff_patch,
                file_name=constants.PATCH_FILE_NAME,
                artifact_path=constants.PATCH_FILE_ARTIFACT_DIR,
            )
        except Exception as ex:
            # no-blocking
            logger.warning(f"failed to log git info because {ex}")

    def download_artifact(self, path: str, dst_path: Optional[str] = None) -> str:
        """
        Download recursively an artifact file or directory from a run to a local directory if applicable, and
        return a local path for it.

        Args:
            path : Relative source path to the desired artifact.
            dst_path : Absolute path of the local filesystem destination directory to which to download the specified
                artifacts. This directory must already exist. If unspecified, the artifacts will either be downloaded to
                a new uniquely-named directory on the local filesystem or will be returned directly in the case of the
                LocalArtifactRepository.
        Returns:
            str: Local path of desired artifact
        """
        if dst_path is None:
            return self.mlflow_client.download_artifacts(self.run_id, path=path)
        elif os.path.isdir(dst_path):
            return self.mlflow_client.download_artifacts(
                self.run_id, path=path, dst_path=dst_path
            )
        else:
            raise MlFoundryException(
                f"Destination path {dst_path} should be an existing directory."
            )

    def __get_dataset_path(
        self, data_slice: enums.DataSlice, fileformat: enums.FileFormat = None
    ):
        if fileformat:
            return (
                str(self.run_id) + "_" + data_slice.value + "." + str(fileformat.value)
            )  # with extension
        else:
            return str(self.run_id) + "_" + data_slice.value  # without extension

    def log_artifact(self, local_path: str, artifact_path: Optional[str] = None):
        if artifact_path is not None:
            NAMESPACE.validate_namespace_not_used(path=artifact_path)
        if os.path.isfile(local_path):
            self.mlflow_client.log_artifact(
                self.run_id, local_path=local_path, artifact_path=artifact_path
            )
        elif os.path.isdir(local_path):
            self.mlflow_client.log_artifacts(
                self.run_id, local_dir=local_path, artifact_path=artifact_path
            )
        else:
            raise MlFoundryException(
                f"local path {local_path} should be an existing file or directory"
            )

    def log_model(self, model, framework: Union[enums.ModelFramework, str]):
        """logs a model to s3 given a model object along with the framework
        Args:
            model : model object in a particular framework
            framework (str): one of the framework
        Example:
        >> log_model(sklearn_model, ModelFramework.SKLEARN)
        """
        framework = enums.ModelFramework(framework)

        amplitude.track(
            amplitude.Event.LOG_MODEL,
            event_properties={"model_framework": framework.value},
        )
        try:
            artifacts = self.mlflow_client.list_artifacts(self.run_id)
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None

        for artifact in artifacts:
            if MlFoundryRun.S3_MODELS_PATH in artifact.path:
                raise MlFoundryException(f"Model already logged, cannot overwrite")

        # TODO (chiragjn): This is hack to temporarily use the mlflow.fluent API because
        #                  .log_model relies on run_id being stored in mlflow's global run stack
        created_run = None
        try:
            # Add to mlflow.fluent's global stack, hoping no other fluent run is running parallely
            created_run = mlflow.start_run(
                experiment_id=self.experiment_id,
                run_id=self.run_id,
                nested=True,  # necessary to avoid messing with existing run stack
                tags={"modelFramework": framework.value},
            )
            get_model_registry(framework).log_model(
                model, artifact_path=MlFoundryRun.S3_MODELS_PATH
            )
            logger.info("Model logged successfully")
        finally:
            if created_run:
                # Remove from mlflow.fluent's global stack but keeping the run in Running mode
                mlflow.end_run(RunStatus.to_string(RunStatus.RUNNING))

    def log_dataset(
        self,
        dataset_name: str,
        features,
        predictions=None,
        actuals=None,
        only_stats: bool = False,
    ):
        """
        Log a dataset associated with a run. A dataset is a collection of features,
        predictions and actuals. Datasets are uniquely identified by the dataset_name
        under a run. They are immutable, once successfully logged, overwriting it is not allowed.

        Mixed types are not allowed in features, actuals and predictions. However, there can be
        missing data in the form of None, NaN, NA.

        :param dataset_name:    Name of the dataset. Dataset name should only contain letters,
                                numbers, underscores and hyphens.
        :type dataset_name: str
        :param features:        Features associated with this dataset.
                                This should be either pandas DataFrame or should be of a
                                data type which can be convered to a DataFrame.
        :param predictions:     Predictions associated with this dataset and run. This
                                should be either pandas Series or should be of a data type which
                                can be convered to a Series. This is an optional argument.
        :param actuals:         Actuals associated with this dataset and run. This
                                should be either pandas Series or should be of a data type which
                                can be convered to a Series. This is an optional argument.
        :param only_stats:      If True, then the dataset (features, predictions, actuals) is
                                not saved. Only statistics and the dataset schema will be
                                persisted. Default is False.
        :type only_stats: bool
        """
        self._dataset_module.log_dataset(
            dataset_name=dataset_name,
            features=features,
            predictions=predictions,
            actuals=actuals,
            only_stats=only_stats,
        )

    def get_dataset(self, dataset_name: str) -> Optional[DataSet]:
        """
        Returns the features, predictions, actuals associated with the dataset.
        If only_stats was set to True while logging the dataset,
        this will return None.

        :param dataset_name: Name of the dataset.
        :type dataset_name: str
        :rtype: typing.Optional[DataSet]
        """
        return self._dataset_module.get_dataset(dataset_name=dataset_name)

    def log_metrics(self, metric_dict: Dict[str, Any], step: int = 0):
        """Logs the metrics given metric_dict that has metric name as key and metric value as value
        Args:
            metric_dict (dict): metric_dict that has metric name as key and metric value as value
            step (int): step associated with the metrics present in metric_dict
        Examples:
        >> log_metric({'accuracy':0.91, 'f1_score':0.5})
        """
        # not sure about amplitude tracking here.
        # as the user can use this function in training loop
        # amplitude.track(amplitude.Event.LOG_METRICS)

        try:
            # mlfow_client doesn't have log_metrics api, so we have to use log_batch,
            # This is what internally used by mlflow.log_metrics
            timestamp = int(time.time() * 1000)
            metrics_arr = [
                Metric(key, value, timestamp, step=step)
                for key, value in metric_dict.items()
            ]
            if len(metrics_arr) == 0:
                raise MlflowException("Cannot log empty metrics dictionary")

            self.mlflow_client.log_batch(
                run_id=self.run_id, metrics=metrics_arr, params=[], tags=[]
            )
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None

        logger.info("Metrics logged successfully")

    def log_params(self, param_dict: ParamsType):
        """Logs the parameter given param_dict that has param name as key and param value as value
        Args:
            param_dict (dict): param_dict that has param name as key and param value as value
        Examples:
        >> log_params({'learning_rate':0.01, 'n_epochs:10'})

        We can also pass argparse Namspace objects directly

        ```
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("-batch_size", type=int, required=True)
        args = parser.parse_args()
        log_params(args)
        ```
        """
        amplitude.track(amplitude.Event.LOG_PARAMS)

        try:
            # mlfowclient doesnt have log_params api, so we have to use log_batch,
            # This is what internally used by mlflow.log_params
            param_dict = process_params(param_dict)
            params_arr = [Param(key, str(value)) for key, value in param_dict.items()]

            if len(params_arr) == 0:
                raise MlflowException("Cannot log empty params dictionary")

            self.mlflow_client.log_batch(
                run_id=self.run_id, metrics=[], params=params_arr, tags=[]
            )
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None

        logger.info("Parameters logged successfully")

    def set_tags(self, tags: Dict[str, Any]):
        """Logs the given tags. Converts tag values to strings.
        Args:
            tags (dict): string tag name as key and tag value as value
        Examples:
        >> set_tags({'nlp.framework': 'Spark NLP'})
        """
        amplitude.track(amplitude.Event.SET_TAGS)

        try:
            NAMESPACE.validate_namespace_not_used(names=tags.keys())
            tags_arr = [RunTag(key, str(value)) for key, value in tags.items()]
            self.mlflow_client.log_batch(
                run_id=self.run_id, metrics=[], params=[], tags=tags_arr
            )
        except MlflowException as e:
            raise MlFoundryException(e.message) from e
        logger.debug("Set tags successfully")

    def get_tags(self) -> Dict[str, str]:
        amplitude.track(amplitude.Event.GET_TAGS)

        run = self.mlflow_client.get_run(self.run_id)
        return run.data.tags

    def __compute_whylogs_stats(self, df):

        if not isinstance(df, pd.DataFrame):
            raise MlFoundryException(
                f"df is expexted to be pd.DataFrame but got {str(type(df))}"
            )

        profile_file_name = (
            "profile"
            + "_"
            + datetime.datetime.now().strftime(constants.TIME_FORMAT)
            + ".bin"
        )
        session = whylogs.get_or_create_session()
        profile = session.new_profile()
        profile.track_dataframe(df)
        profile.write_protobuf(profile_file_name)

        try:
            self.mlflow_client.set_tag(self.run_id, "whylogs", True)
            self.mlflow_client.log_artifact(
                self.run_id,
                profile_file_name,
                artifact_path=MlFoundryRun.S3_WHYLOGS_PATH,
            )
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None

        if os.path.exists(profile_file_name):
            os.remove(profile_file_name)

    def auto_log_metrics(
        self,
        model_type: enums.ModelType,
        data_slice: enums.DataSlice,
        predictions: Collection[Any],
        actuals: Optional[Collection[Any]] = None,
        class_names: Optional[List[str]] = None,
        prediction_probabilities=None,
    ) -> ComputedMetrics:
        metrics_calculator = get_metrics_calculator_v2(model_type)
        metrics = metrics_calculator.compute_metrics(
            predictions=predictions,
            actuals=actuals,
            prediction_probabilities=prediction_probabilities,
            class_names=class_names,
        )
        metric_path = os.path.join(constants.ALM_ARTIFACT_PATH, data_slice.value)
        log_artifact_blob(
            mlflow_client=self.mlflow_client,
            run_id=self.run_id,
            blob=metrics.json(),
            file_name=constants.ALM_METRICS_FILE_NAME,
            artifact_path=metric_path,
        )
        return metrics

    # TODO (nikunjbjj): This function is too long. Need to be broken into smaller testable modules.
    def log_dataset_stats(
        self,
        df,
        data_slice: enums.DataSlice,
        data_schema: Schema,
        model_type: enums.ModelType,
        shap_values=None,
    ):
        data_slice = enums.DataSlice(data_slice)
        model_type = enums.ModelType(model_type)

        if not isinstance(df, pd.DataFrame):
            raise MlFoundryException(f"Expected pd.DataFrame but got {str(type(df))}")

        if not data_schema.actual_column_name:
            raise MlFoundryException(f"Schema.actual_column_name cannot be None")
        elif not data_schema.prediction_column_name:
            raise MlFoundryException(f"Schema.prediction_column_name cannot be None")
        elif data_schema.feature_column_names is None:
            raise MlFoundryException(f"Schema.feature_column_names cannot be None")
        elif not isinstance(data_schema.feature_column_names, list):
            raise MlFoundryException(
                f"data_schema.feature_column_names should be of type list, "
                f"cannot be {type(data_schema.feature_column_names)}"
            )

        self.__compute_whylogs_stats(df[set(data_schema.feature_column_names)])

        if model_type in [
            enums.ModelType.BINARY_CLASSIFICATION,
            enums.ModelType.MULTICLASS_CLASSIFICATION,
        ]:
            class_names = None
            prediction_col_dtype, actual_col_dtype = (
                df[data_schema.prediction_column_name].dtype,
                df[data_schema.actual_column_name].dtype,
            )
            if prediction_col_dtype == object and actual_col_dtype != object:
                raise MlflowException(
                    "Both predictions column and actual column has to be of same datatype, either string or number"
                )
            elif prediction_col_dtype != object and actual_col_dtype == object:
                raise MlflowException(
                    "Both predictions column and actual column has to be of same datatype, either string or number"
                )
            elif prediction_col_dtype == object and actual_col_dtype == object:
                actual_class_names = df[data_schema.actual_column_name].unique()
                prediction_class_name = df[data_schema.prediction_column_name].unique()
                class_names = sorted(
                    set(actual_class_names) | set(prediction_class_name)
                )
                df[data_schema.actual_column_name] = df[
                    data_schema.actual_column_name
                ].apply(lambda x: class_names.index(x))
                df[data_schema.prediction_column_name] = df[
                    data_schema.prediction_column_name
                ].apply(lambda x: class_names.index(x))

        unique_count_dict = {}
        if model_type in [
            enums.ModelType.BINARY_CLASSIFICATION,
            enums.ModelType.MULTICLASS_CLASSIFICATION,
        ]:
            unique_count_dict[data_schema.prediction_column_name] = np.unique(
                df[data_schema.prediction_column_name].to_list(), return_counts=True
            )
            unique_count_dict[data_schema.actual_column_name] = np.unique(
                df[data_schema.actual_column_name].to_list(), return_counts=True
            )
        elif model_type == enums.ModelType.REGRESSION:
            session = whylogs.get_or_create_session()
            profile = session.new_profile()
            profile.track_dataframe(
                df[[data_schema.actual_column_name, data_schema.prediction_column_name]]
            )
            unique_count_dict[
                constants.ACTUAL_PREDICTION_COUNTS
            ] = profile.flat_summary()["hist"]

        if data_schema.categorical_feature_column_names:
            for feature in data_schema.categorical_feature_column_names:
                unique_count_dict[feature] = np.unique(
                    df[feature].to_list(), return_counts=True
                )

        unique_count_name = "unique_count" + "_" + str(data_slice.value) + ".json"
        constants.RUN_STATS_FOLDER.mkdir(parents=True, exist_ok=True)
        unique_count_path = os.path.join(constants.RUN_STATS_FOLDER, unique_count_name)

        with open(unique_count_path, "w") as fp:
            json.dump(unique_count_dict, fp, cls=NumpyEncoder)

        schema_json_name = "schema" + "_" + str(data_slice.value) + ".json"
        schema_json_path = os.path.join(constants.RUN_STATS_FOLDER, schema_json_name)

        with open(schema_json_path, "w") as outfile:
            json.dump(data_schema.__dict__, outfile)

        # TODO (nikunjbjj): This class name could be referenced before assignment. We need to fix this.
        if (
            model_type
            in [
                enums.ModelType.BINARY_CLASSIFICATION,
                enums.ModelType.MULTICLASS_CLASSIFICATION,
            ]
            and class_names is not None
        ):
            class_names_path = f"class_names_{data_slice.value}.json"
            class_names_path = constants.RUN_STATS_FOLDER / class_names_path
            class_names_dict = {"class_names": class_names}
            with open(class_names_path, "w") as fp:
                json.dump(class_names_dict, fp)

        metrics_class = get_metrics_calculator_v1(model_type)

        if data_schema.prediction_probability_column_name:
            metrics_dict = metrics_class.compute_metrics(
                df[set(data_schema.feature_column_names)],
                df[data_schema.prediction_column_name].to_list(),
                df[data_schema.actual_column_name].to_list(),
                df[data_schema.prediction_probability_column_name].to_list(),
            )
        else:
            metrics_dict = metrics_class.compute_metrics(
                df[set(data_schema.feature_column_names)],
                df[data_schema.prediction_column_name].to_list(),
                df[data_schema.actual_column_name].to_list(),
            )
        # non-multi dimensional metrics
        metrics_dict_with_data_slice = {}

        for key in metrics_dict[constants.NON_MULTI_DIMENSIONAL_METRICS].keys():
            new_key = "pre_computed_" + key + "_" + str(data_slice.value)
            metrics_dict_with_data_slice[new_key] = metrics_dict[
                constants.NON_MULTI_DIMENSIONAL_METRICS
            ][key]

        if shap_values is not None:
            tag_key = "data_stats_and_shap_" + data_slice.value
        else:
            tag_key = "data_stats_" + data_slice.value

        self.mlflow_client.set_tag(self.run_id, "modelType", model_type.value)
        self.mlflow_client.set_tag(self.run_id, tag_key, True)
        self.log_metrics(metrics_dict_with_data_slice)

        constants.RUN_METRICS_FOLDER.mkdir(parents=True, exist_ok=True)
        multi_dimension_metric_file = (
            "pre_computed_"
            + constants.MULTI_DIMENSIONAL_METRICS
            + "_"
            + str(data_slice.value)
            + ".json"
        )
        multi_dimension_metric_file_path = os.path.join(
            constants.RUN_METRICS_FOLDER, multi_dimension_metric_file
        )

        with open(multi_dimension_metric_file_path, "w") as fp:
            json.dump(
                metrics_dict[constants.MULTI_DIMENSIONAL_METRICS], fp, cls=NumpyEncoder
            )

        if model_type == enums.ModelType.TIMESERIES:
            actuals_predictions_filename = (
                "actuals_predictions_" + str(data_slice.value) + ".parquet"
            )
            actuals_predictions_filepath = os.path.join(
                constants.RUN_STATS_FOLDER, actuals_predictions_filename
            )
            df[
                [data_schema.prediction_column_name, data_schema.actual_column_name]
            ].to_parquet(actuals_predictions_filepath)

        try:

            # with self.mlflow_run as run:
            self.mlflow_client.log_artifact(
                self.run_id, unique_count_path, artifact_path=MlFoundryRun.S3_STATS_PATH
            )
            self.mlflow_client.log_artifact(
                self.run_id,
                multi_dimension_metric_file_path,
                artifact_path=MlFoundryRun.S3_METRICS_PATH,
            )
            self.mlflow_client.log_artifact(
                self.run_id, schema_json_path, artifact_path=MlFoundryRun.S3_STATS_PATH
            )
            if (
                model_type
                in [
                    enums.ModelType.BINARY_CLASSIFICATION,
                    enums.ModelType.MULTICLASS_CLASSIFICATION,
                ]
                and class_names is not None
            ):
                self.mlflow_client.log_artifact(
                    self.run_id,
                    class_names_path,
                    artifact_path=MlFoundryRun.S3_STATS_PATH,
                )
            # TODO (nikunjbjj): This class name path and actuals_predictions_filepath could be referenced
            #  before assignment. We need to fix this.
            if model_type == enums.ModelType.TIMESERIES:
                self.mlflow_client.log_artifact(
                    self.run_id,
                    actuals_predictions_filepath,
                    artifact_path=MlFoundryRun.S3_STATS_PATH,
                )
                os.remove(actuals_predictions_filepath)
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None

        os.remove(multi_dimension_metric_file_path)
        os.remove(schema_json_path)
        os.remove(unique_count_path)

        if shap_values is not None:
            self.__log_shap_values(
                df[set(data_schema.feature_column_names)], shap_values, data_slice
            )

        logger.info("Dataset stats have been successfully computed and logged")

    def __log_shap_values(self, df, shap_values: list, data_slice: enums.DataSlice):

        if not isinstance(df, pd.DataFrame):
            raise MlFoundryException(f"Expected pd.DataFrame but got {str(type(df))}")

        artifact_name = str(self.run_id) + "_" + str(data_slice.value) + "_shap.json"
        constants.RUN_STATS_FOLDER.mkdir(parents=True, exist_ok=True)
        filename = os.path.join(constants.RUN_STATS_FOLDER, artifact_name)

        shap_values_dict = {"shap_values": shap_values}

        with open(filename, "w") as fp:
            json.dump(shap_values_dict, fp, cls=NumpyEncoder)

        try:
            self.mlflow_client.log_artifact(
                self.run_id, filename, artifact_path=MlFoundryRun.S3_STATS_PATH
            )
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None

        os.remove(filename)

    def __get_artifact(self, run_id, artifact_name, dest_path):
        try:
            return self.mlflow_client.download_artifacts(
                run_id, artifact_name, dest_path
            )
        except MlflowException as e:
            raise MlFoundryException(e.message).with_traceback(
                e.__traceback__
            ) from None

    def get_metrics(
        self, metric_names: Optional[Iterable[str]] = None
    ) -> Dict[str, List[Metric]]:
        """
        Returns logged metrics.

        Args:
            metric_names: a list of metric names. If not passed,
                          Then returns all metrics logged for the run.
        Returns:
            A dictionary of metric_names and the logger metrics.
            The key is metric name. Value is a list of mlflow.entities.Metric object.
            If a metric has not been used before, value will be an empty list.

        ```
        In [4]: test_run.log_metrics({"loss": 0.6}, step=1)
        2022-02-21 22:32:19.550 INFO    mlfoundry.mlfoundry_run: Metrics logged successfully

        In [5]: test_run.log_metrics({"loss": 0.3}, step=2)
        2022-02-21 22:32:27.191 INFO    mlfoundry.mlfoundry_run: Metrics logged successfully

        In [6]: test_run.get_metrics()
        Out[6]:
        {'loss': [<Metric: key='loss', step=1, timestamp=1645462939544, value=0.6>,
          <Metric: key='loss', step=2, timestamp=1645462947185, value=0.3>]}
        ```
        """

        amplitude.track(amplitude.Event.GET_METRICS)
        run = self.mlflow_client.get_run(self.run_id)
        run_metrics = run.data.metrics

        metric_names = (
            set(metric_names) if metric_names is not None else run_metrics.keys()
        )

        unknown_metrics = metric_names - run_metrics.keys()
        if len(unknown_metrics) > 0:
            logger.warning(f"{unknown_metrics} metrics not present in the run")
        metrics_dict = {metric_name: [] for metric_name in unknown_metrics}
        valid_metrics = metric_names - unknown_metrics
        for metric_name in valid_metrics:
            metrics_dict[metric_name] = self.mlflow_client.get_metric_history(
                self.run_id, metric_name
            )
        return metrics_dict

    def get_params(self):
        # Ending any run that is active to prevent mlflow from throwing error
        amplitude.track(amplitude.Event.GET_PARAMS)
        run = self.mlflow_client.get_run(self.run_id)
        return run.data.params

    def get_model(self, dest_path: str = None, **kwargs):
        amplitude.track(amplitude.Event.GET_MODEL)
        artifacts = self.mlflow_client.list_artifacts(self.run_id)
        model_exists = False
        model_file_path = None
        for artifact in artifacts:
            if MlFoundryRun.S3_MODELS_PATH in artifact.path:
                model_exists = True
                model_file_path = artifact.path
                break

        if not model_exists:
            raise MlFoundryException("Model is not logged")

        run = self.mlflow_client.get_run(self.run_id)
        run_tags = run.data.tags

        framework = enums.ModelFramework(run_tags.get("modelFramework"))

        if framework is None:
            raise MlFoundryException("Invalid Framework found")

        if framework == enums.ModelFramework.TENSORFLOW:
            self.model_uri = model_file_path
        model_framework_class_instance = get_model_registry(framework)
        return model_framework_class_instance.load_model(
            self.model_uri,
            dest_path=dest_path,
            mlflow_client=self.mlflow_client,
            run_id=self.run_id,
            **kwargs,
        )
