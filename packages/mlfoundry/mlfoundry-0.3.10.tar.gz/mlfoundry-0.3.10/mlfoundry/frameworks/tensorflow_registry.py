import os
import shutil
from pathlib import Path

import mlflow

from mlfoundry.constants import GET_RUN_TMP_FOLDER, RUN_TMP_FOLDER
from mlfoundry.exceptions import MlflowException, MlFoundryException
from mlfoundry.frameworks.base_registry import BaseRegistry
from mlfoundry.run_utils import download_artifact


class TensorflowRegistry(BaseRegistry):
    def log_model(self, python_object, artifact_path: str, **kwargs):
        """
        Log Tensorflow model
        Args:
            python_object : the object to be registered
            artifact_path (str): artifact_path
        """

        model_file_path = Path(os.path.join(RUN_TMP_FOLDER, artifact_path))
        model_file_path.mkdir(exist_ok=True, parents=True)

        try:
            import tensorflow as tf

            TF2 = tf.__version__.startswith("2")
        except ImportError:
            raise ImportError(
                "Tensorflow package is required to use TfSavedModelArtifact."
            )

        if TF2:
            tf.saved_model.save(
                python_object["model"],
                str(model_file_path),
                signatures=python_object["signatures"],
                options=python_object["options"],
            )
        else:
            tf.saved_model.save(
                python_object,
                str(model_file_path),
                signatures=python_object["signatures"],
            )

        mlflow.log_artifacts(model_file_path, artifact_path=artifact_path)
        shutil.rmtree(model_file_path, ignore_errors=False)

    def load_model(self, model_file_path: str, dest_path: str, **kwargs):
        """
        Load Tensorflow model
        """
        if "mlflow_client" not in kwargs.keys():
            raise MlFoundryException("mlflow_client is required")

        if "run_id" not in kwargs.keys():
            raise MlFoundryException("run_id is required")

        mlflow_client = kwargs["mlflow_client"]
        run_id = kwargs["run_id"]

        if dest_path:
            model_file_path = download_artifact(
                mlflow_client, run_id, model_file_path, dest_path
            )
        else:
            raise MlFoundryException(
                "Please provide a location 'dest_path' to save the model"
            )

        GET_RUN_TMP_FOLDER.mkdir(parents=True, exist_ok=True)
        options = kwargs.get("options", None)

        try:
            import tensorflow as tf

            TF2 = tf.__version__.startswith("2")
        except ImportError:
            raise ImportError(
                "Tensorflow package is required to use TfSavedModelArtifact."
            )

        return tf.saved_model.load(model_file_path, options=options)
