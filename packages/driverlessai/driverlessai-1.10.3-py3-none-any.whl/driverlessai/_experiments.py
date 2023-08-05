"""Experiments module of official Python client for Driverless AI."""

import csv
import functools
import io
import time
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import IO
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import TYPE_CHECKING
from typing import Union

import toml

from driverlessai import _core
from driverlessai import _datasets
from driverlessai import _projects
from driverlessai import _recipes
from driverlessai import _utils


if TYPE_CHECKING:
    import fsspec  # noqa F401
    import pandas  # noqa F401


class Experiment(_utils.ServerJob):
    """Interact with an experiment on the Driverless AI server."""

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)
        self._artifacts: Optional[ExperimentArtifacts] = None
        self._datasets: Optional[Dict[str, Optional[_datasets.Dataset]]] = None
        self._log: Optional[ExperimentLog] = None
        self._settings: Optional[Dict[str, Any]] = None

    @property
    def artifacts(self) -> "ExperimentArtifacts":
        """Interact with artifacts that are created when the experiment completes."""
        if not self._artifacts:
            self._artifacts = ExperimentArtifacts(self)
        return self._artifacts

    @property
    def creation_timestamp(self) -> float:
        """Creation timestamp in seconds since the epoch (POSIX timestamp)."""
        return self._get_raw_info().created

    @property
    def datasets(self) -> Dict[str, Optional[_datasets.Dataset]]:
        """Dictionary of ``train_dataset``, ``validation_dataset``, and
        ``test_dataset`` used for the experiment."""
        if not self._datasets:
            train_dataset = self._client.datasets.get(
                self._get_raw_info().entity.parameters.dataset.key
            )
            validation_dataset = None
            test_dataset = None
            if self._get_raw_info().entity.parameters.validset.key:
                validation_dataset = self._client.datasets.get(
                    self._get_raw_info().entity.parameters.validset.key
                )
            if self._get_raw_info().entity.parameters.testset.key:
                test_dataset = self._client.datasets.get(
                    self._get_raw_info().entity.parameters.testset.key
                )
            self._datasets = {
                "train_dataset": train_dataset,
                "validation_dataset": validation_dataset,
                "test_dataset": test_dataset,
            }
        return self._datasets

    @property
    def is_deprecated(self) -> bool:
        """``True`` if experiment was created by an old version of
        Driverless AI and is no longer fully compatible with the current
        server version."""
        return self._get_raw_info().entity.deprecated

    @property
    def log(self) -> "ExperimentLog":
        """Interact with experiment logs."""
        if not self._log:
            self._log = ExperimentLog(self)
        return self._log

    @property
    def run_duration(self) -> Optional[float]:
        """Run duration in seconds."""
        self._update()
        return self._get_raw_info().entity.training_duration

    @property
    def settings(self) -> Dict[str, Any]:
        """Experiment settings."""
        if not self._settings:
            self._settings = self._client.experiments._parse_server_settings(
                self._get_raw_info().entity.parameters.dump()
            )
        return self._settings

    @property
    def size(self) -> int:
        """Size in bytes of all experiment's files on the Driverless AI server."""
        self._update()
        return self._get_raw_info().entity.model_file_size

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'> {self.key} {self.name}"

    def __str__(self) -> str:
        return f"{self.name} ({self.key})"

    def _get_retrain_settings(
        self,
        use_smart_checkpoint: bool = False,
        final_pipeline_only: bool = False,
        final_models_only: bool = False,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        # Get parent experiment settings
        settings: Dict[str, Any] = {**self.datasets, **self.settings}
        # Remove settings that shouldn't be reused
        settings.pop("name", None)
        # Update settings with any new settings
        settings.update(kwargs)
        # Set parent experiment
        settings["parent_experiment"] = self
        if use_smart_checkpoint:
            settings["feature_brain_level"] = 1003
        if final_pipeline_only:
            settings["feature_brain_level"] = 1003
            settings["time"] = 0
        if final_models_only:
            settings["feature_brain_level"] = 1003
            settings["time"] = 0
            settings["brain_add_features_for_new_columns"] = (False,)
            settings["refit_same_best_individual"] = (True,)
            settings["feature_brain_reset_score"] = ("off",)
            settings["force_model_restart_to_defaults"] = False
        return settings

    def _model_ready(func: Callable) -> Callable:  # type: ignore
        @functools.wraps(func)
        def check(self: "Experiment", *args: Any, **kwargs: Any) -> Callable:
            if self.is_complete():
                return func(self, *args, **kwargs)
            raise RuntimeError("Experiment is not complete: " + self.status(verbose=2))

        return check

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_model_job(self.key))
        self._set_name(self._get_raw_info().entity.description)

    def abort(self) -> None:
        """Terminate experiment immediately and only generate logs."""
        if self.is_running():
            return self._client._backend.abort_experiment(self.key)

    def delete(self) -> None:
        """Permanently delete experiment from the Driverless AI server."""
        key = self.key
        self._client._backend.delete_model(key)
        time.sleep(1)  # hack for https://github.com/h2oai/h2oai/issues/14519
        print(f"Driverless AI Server reported experiment {key} deleted.")

    @_model_ready
    def export_dai_file(
        self,
        dst_dir: str = ".",
        dst_file: Optional[str] = None,
        file_system: Optional["fsspec.spec.AbstractFileSystem"] = None,
        overwrite: bool = False,
    ) -> str:
        """Export experiment from Driverless AI server in dai format.

        Args:
            dst_dir: directory where dai file will be saved
            dst_file: name of dai file (overrides default file name)
            file_system: FSSPEC based file system to download to,
                instead of local file system
            overwrite: overwrite existing file
        """
        _utils.check_server_support(
            client=self._client,
            minimum_server_version="1.10.0",
            parameter="export_dai_file",
        )
        job_key = self._client._backend.export_experiment(self.key)
        completed_job = ExperimentExportJob(self._client, job_key).result(silent=True)
        dst_path = self._client._download(
            server_path=completed_job._get_raw_info().experiment_zip_path,
            dst_dir=dst_dir,
            dst_file=dst_file,
            file_system=file_system,
            overwrite=overwrite,
        )
        return dst_path

    def finish(self) -> None:
        """Finish experiment by jumping to final pipeline training and generating
        experiment artifacts.
        """
        if self.is_running():
            return self._client._backend.stop_experiment(self.key)

    def gui(self) -> _utils.Hyperlink:
        """Get full URL for the experiment's page on the Driverless AI server."""
        return _utils.Hyperlink(
            f"{self._client.server.address}{self._client._gui_sep}"
            f"experiment?key={self.key}"
        )

    def metrics(self) -> Dict[str, Union[str, float]]:
        """Return dictionary of experiment scorer metrics and AUC metrics,
        if available.
        """
        self._update()
        metrics = {}
        metrics["scorer"] = self._get_raw_info().entity.score_f_name

        metrics["val_score"] = self._get_raw_info().entity.valid_score
        metrics["val_score_sd"] = self._get_raw_info().entity.valid_score_sd
        metrics["val_roc_auc"] = self._get_raw_info().entity.valid_roc.auc
        metrics["val_pr_auc"] = self._get_raw_info().entity.valid_roc.aucpr

        metrics["test_score"] = self._get_raw_info().entity.test_score
        metrics["test_score_sd"] = self._get_raw_info().entity.test_score_sd
        metrics["test_roc_auc"] = self._get_raw_info().entity.test_roc.auc
        metrics["test_pr_auc"] = self._get_raw_info().entity.test_roc.aucpr

        return metrics

    def notifications(self) -> List[Dict[str, str]]:
        """Return list of experiment notification dictionaries."""
        self._update()
        if hasattr(self._get_raw_info().entity, "warnings"):
            # 1.8 branch
            return [
                {"title": None, "content": n, "priority": None, "created": None}
                for n in self._get_raw_info().entity.warnings
            ]
        notifications = []
        for n in self._client._backend.list_model_notifications(
            self.key, self._get_raw_info().entity.notifications
        ):
            n = n.dump()
            del n["key"]
            notifications.append(n)
        return notifications

    @_model_ready
    def predict(
        self,
        dataset: _datasets.Dataset,
        enable_mojo: bool = True,
        include_columns: Optional[List[str]] = None,
        include_labels: Optional[bool] = None,
        include_raw_outputs: Optional[bool] = None,
        include_shap_values_for_original_features: Optional[bool] = None,
        include_shap_values_for_transformed_features: Optional[bool] = None,
        use_fast_approx_for_shap_values: Optional[bool] = None,
    ) -> "Prediction":
        """Predict on a dataset, then return a Prediction object.

        Args:
            dataset: a Dataset object corresonding to a dataset on the
                Driverless AI server
            enable_mojo: use MOJO (if available) to make predictions
                (server versions >= 1.9.1)
            include_columns: list of columns from the dataset to append to the
                prediction csv
            include_labels: append labels in addition to probabilities for
                classification, ignored for regression (server versions >= 1.10)
            include_raw_outputs: append predictions as margins (in link space)
                to the prediction csv
            include_shap_values_for_original_features: append original feature
                contributions to the prediction csv (server versions >= 1.9.1)
            include_shap_values_for_transformed_features: append transformed
                feature contributions to the prediction csv
            use_fast_approx_for_shap_values: speed up prediction contributions
                with approximation (server versions >= 1.9.1)
        """
        return self.predict_async(
            dataset,
            enable_mojo,
            include_columns,
            include_labels,
            include_raw_outputs,
            include_shap_values_for_original_features,
            include_shap_values_for_transformed_features,
            use_fast_approx_for_shap_values,
        ).result()

    @_model_ready
    def predict_async(
        self,
        dataset: _datasets.Dataset,
        enable_mojo: bool = True,
        include_columns: Optional[List[str]] = None,
        include_labels: Optional[bool] = None,
        include_raw_outputs: Optional[bool] = None,
        include_shap_values_for_original_features: Optional[bool] = None,
        include_shap_values_for_transformed_features: Optional[bool] = None,
        use_fast_approx_for_shap_values: Optional[bool] = None,
    ) -> "PredictionJobs":
        """Launch prediction job on a dataset and return a PredictionJobs object
        to track the status.

        Args:
            dataset: a Dataset object corresonding to a dataset on the
                Driverless AI server
            enable_mojo: use MOJO (if available) to make predictions
                (server versions >= 1.9.1)
            include_columns: list of columns from the dataset to append to the
                prediction csv
            include_labels: append labels in addition to probabilities for
                classification, ignored for regression (server versions >= 1.10)
            include_raw_outputs: append predictions as margins (in link space)
                to the prediction csv
            include_shap_values_for_original_features: append original feature
                contributions to the prediction csv (server versions >= 1.9.1)
            include_shap_values_for_transformed_features: append transformed
                feature contributions to the prediction csv
            use_fast_approx_for_shap_values: speed up prediction contributions
                with approximation (server versions >= 1.9.1)
        """
        if include_columns is None:
            include_columns = []
        if include_labels is not None:
            _utils.check_server_support(
                client=self._client,
                minimum_server_version="1.10.0",
                parameter="include_labels",
            )
        if include_shap_values_for_original_features is not None:
            _utils.check_server_support(
                client=self._client,
                minimum_server_version="1.9.1",
                parameter="include_shap_values_for_original_features",
            )
        if use_fast_approx_for_shap_values is not None:
            _utils.check_server_support(
                client=self._client,
                minimum_server_version="1.9.1",
                parameter="use_fast_approx_for_shap_values",
            )
        # note that `make_prediction` has 4 mutually exclusive options that
        # create different csvs, which is why it has to be called up to 4 times
        keys = []
        # creates csv of probabilities
        keys.append(
            self._client._backend.make_prediction(
                model_key=self.key,
                dataset_key=dataset.key,
                output_margin=False,
                pred_contribs=False,
                pred_contribs_original=False,
                enable_mojo=enable_mojo,
                fast_approx=False,
                fast_approx_contribs=False,
                keep_non_missing_actuals=False,
                include_columns=include_columns,
                pred_labels=include_labels or False,
            )
        )
        if include_raw_outputs:
            # creates csv of raw outputs only
            keys.append(
                self._client._backend.make_prediction(
                    model_key=self.key,
                    dataset_key=dataset.key,
                    output_margin=True,
                    pred_contribs=False,
                    pred_contribs_original=False,
                    enable_mojo=enable_mojo,
                    fast_approx=False,
                    fast_approx_contribs=False,
                    keep_non_missing_actuals=False,
                    include_columns=[],
                    pred_labels=False,
                )
            )
        if include_shap_values_for_original_features:
            # creates csv of SHAP values only
            keys.append(
                self._client._backend.make_prediction(
                    model_key=self.key,
                    dataset_key=dataset.key,
                    output_margin=False,
                    pred_contribs=True,
                    pred_contribs_original=True,
                    enable_mojo=enable_mojo,
                    fast_approx=False,
                    fast_approx_contribs=use_fast_approx_for_shap_values or False,
                    keep_non_missing_actuals=False,
                    include_columns=[],
                    pred_labels=False,
                )
            )
        if include_shap_values_for_transformed_features:
            # creates csv of SHAP values only
            keys.append(
                self._client._backend.make_prediction(
                    model_key=self.key,
                    dataset_key=dataset.key,
                    output_margin=False,
                    pred_contribs=True,
                    pred_contribs_original=False,
                    enable_mojo=enable_mojo,
                    fast_approx=False,
                    fast_approx_contribs=use_fast_approx_for_shap_values or False,
                    keep_non_missing_actuals=False,
                    include_columns=[],
                    pred_labels=False,
                )
            )
        jobs = [PredictionJob(self._client, key, dataset.key, self.key) for key in keys]

        # The user will get a single csv created by concatenating all the above csvs.
        # From the user perspective they are creating a single csv even though
        # multiple csv jobs are spawned. The PredictionJobs object allows the
        # multiple jobs to be interacted with as if they were a single job.
        return PredictionJobs(
            client=self._client,
            jobs=jobs,
            dataset_key=dataset.key,
            experiment_key=self.key,
            include_columns=include_columns,
            include_labels=include_labels,
            include_raw_outputs=include_raw_outputs,
            include_shap_values_for_original_features=(
                include_shap_values_for_original_features
            ),
            include_shap_values_for_transformed_features=(
                include_shap_values_for_transformed_features
            ),
            use_fast_approx_for_shap_values=use_fast_approx_for_shap_values,
        )

    def rename(self, name: str) -> "Experiment":
        """Change experiment display name.

        Args:
            name: new display name
        """
        self._client._backend.update_model_description(self.key, name)
        self._update()
        return self

    def result(self, silent: bool = False) -> "Experiment":
        """Wait for training to complete, then return self.

        Args:
            silent: if True, don't display status updates
        """
        self._wait(silent)
        return self

    def retrain(
        self,
        use_smart_checkpoint: bool = False,
        final_pipeline_only: bool = False,
        final_models_only: bool = False,
        **kwargs: Any,
    ) -> "Experiment":
        """Create a new experiment using the same datasets and settings. Through
        ``kwargs`` it's possible to pass new datasets or overwrite settings.

        Args:
            use_smart_checkpoint: start experiment from last smart checkpoint
            final_pipeline_only: trains final pipeline using smart checkpoint
                if available, otherwise uses default hyperparameters
            final_models_only: trains final pipeline models (but not transformers)
                using smart checkpoint if available, otherwise uses default
                hyperparameters and transformers (overrides `final_pipeline_only`)
            kwargs: datasets and experiment settings as defined in
                ``experiments.create()``
        """
        return self.retrain_async(
            use_smart_checkpoint=use_smart_checkpoint,
            final_pipeline_only=final_pipeline_only,
            final_models_only=final_models_only,
            **kwargs,
        ).result()

    def retrain_async(
        self,
        use_smart_checkpoint: bool = False,
        final_pipeline_only: bool = False,
        final_models_only: bool = False,
        **kwargs: Any,
    ) -> "Experiment":
        """Launch creation of a new experiment using the same datasets and
        settings. Through `kwargs` it's possible to pass new datasets or
        overwrite settings.

        Args:
            use_smart_checkpoint: start experiment from last smart checkpoint
            final_pipeline_only: trains final pipeline using smart checkpoint
                if available, otherwise uses default hyperparameters
            final_models_only: trains final pipeline models (but not transformers)
                using smart checkpoint if available, otherwise uses default
                hyperparameters and transformers (overrides `final_pipeline_only`)
            kwargs: datasets and experiment settings as defined in
                ``experiments.create()``
        """
        settings = self._get_retrain_settings(
            use_smart_checkpoint=use_smart_checkpoint,
            final_pipeline_only=final_pipeline_only,
            final_models_only=final_models_only,
            **kwargs,
        )
        return self._client.experiments.create_async(**settings)

    def summary(self) -> None:
        """Print experiment summary."""
        if not _utils.is_server_job_complete(self._status()):
            print("Experiment is not complete:", self.status(verbose=2))
            return
        summary = (
            f"{getattr(self._get_raw_info(), 'message', '')}\n"
            f"{getattr(self._get_raw_info().entity, 'summary', '')}"
        )
        print(summary.strip())

    def variable_importance(self) -> Union[_utils.Table, None]:
        """Get variable importance in a Table."""
        try:
            variable_importance = self._client._backend.get_variable_importance(
                self.key
            ).dump()
            return _utils.Table(
                [list(x) for x in zip(*variable_importance.values())],
                variable_importance.keys(),
            )
        except self._client._server_module.protocol.RemoteError:
            print("Variable importance not available.")
            return None


class ExperimentArtifacts:
    """Interact with files created by an experiment on the Driverless AI server."""

    def __init__(self, experiment: "Experiment") -> None:
        self._experiment = experiment
        self._paths: Dict[str, str] = {}
        self._prediction_dataset_type = {
            "test_predictions": "test",
            "train_predictions": "train",
            "val_predictions": "valid",
        }

    @property
    def file_paths(self) -> Dict[str, str]:
        """Paths to artifact files on the server."""
        self.list()  # checks if experiment is complete and updates paths
        return self._paths

    def _get_path(self, attr: str, do_timeout: bool = True, timeout: int = 60) -> str:
        path = getattr(self._experiment._get_raw_info().entity, attr)
        if not do_timeout:
            return path
        seconds = 0
        while path == "" and seconds < timeout:
            time.sleep(1)
            seconds += 1
            self._experiment._update()
            path = getattr(self._experiment._get_raw_info().entity, attr)
        return path

    def _model_ready(func: Callable) -> Callable:  # type: ignore
        @functools.wraps(func)
        def check(self: "ExperimentArtifacts", *args: Any, **kwargs: Any) -> Callable:
            if self._experiment.is_complete():
                return func(self, *args, **kwargs)
            raise RuntimeError(
                "Experiment is not complete: " + self._experiment.status(verbose=2)
            )

        return check

    def _update(self) -> None:
        self._experiment._update()
        self._paths["autoreport"] = self._get_path(
            "autoreport_path", self._experiment.settings.get("make_autoreport", False)
        )
        self._paths["autodoc"] = self._paths["autoreport"]
        self._paths["logs"] = self._get_path("log_file_path")
        self._paths["mojo_pipeline"] = self._get_path(
            "mojo_pipeline_path",
            self._experiment.settings.get("make_mojo_pipeline", "off") == "on",
        )
        self._paths["python_pipeline"] = self._get_path(
            "scoring_pipeline_path",
            self._experiment.settings.get("make_python_scoring_pipeline", "off")
            == "on",
        )
        self._paths["summary"] = self._get_path("summary_path")
        self._paths["test_predictions"] = self._get_path("test_predictions_path", False)
        self._paths["train_predictions"] = self._get_path(
            "train_predictions_path", False
        )
        self._paths["val_predictions"] = self._get_path("valid_predictions_path", False)

    @_model_ready
    def create(self, artifact: str) -> None:
        """(Re)build certain artifacts, if possible.

        (re)buildable artifacts:

        - ``'autodoc'``
        - ``'mojo_pipeline'``
        - ``'python_pipeline'``

        Args:
            artifact: name of artifact to (re)build
        """
        if artifact == "python_pipeline":
            print("Building Python scoring pipeline...")
            if not self._experiment._client._backend.build_scoring_pipeline_sync(
                self._experiment.key, force=True
            ).file_path:
                print("Unable to build Python scoring pipeline.")
        if artifact == "mojo_pipeline":
            print("Building MOJO pipeline...")
            if not self._experiment._client._backend.build_mojo_pipeline_sync(
                self._experiment.key, force=True
            ).file_path:
                print("Unable to build MOJO pipeline.")
        if artifact == "autodoc" or artifact == "autoreport":
            print("Generating autodoc...")
            if not self._experiment._client._backend.make_autoreport_sync(
                self._experiment.key, template="", config=""
            ).report_path:
                print("Unable to generate autodoc.")

    @_model_ready
    def download(
        self,
        only: Union[str, List[str]] = None,
        dst_dir: str = ".",
        file_system: Optional["fsspec.spec.AbstractFileSystem"] = None,
        include_columns: Optional[List[str]] = None,
        overwrite: bool = False,
    ) -> Dict[str, str]:
        """Download experiment artifacts from the Driverless AI server. Returns
        a dictionary of relative paths for the downloaded artifacts.

        Args:
            only: specify specific artifacts to download, use
                ``experiment.artifacts.list()`` to see the available
                artifacts on the Driverless AI server
            dst_dir: directory where experiment artifacts will be saved
            file_system: FSSPEC based file system to download to,
                instead of local file system
            include_columns: list of dataset columns to append to prediction csvs
            overwrite: overwrite existing files
        """
        self._update()
        if include_columns is None:
            include_columns = []
        all_dataset_columns: List[str] = sum(
            [getattr(d, "columns", []) for d in self._experiment.datasets.values()],
            [],
        )
        for c in include_columns:
            if c not in all_dataset_columns:
                raise RuntimeError(f"Column '{c}' not found in datasets.")
        dst_paths = {}
        if isinstance(only, str):
            only = [only]
        if only is None:
            only = self.list()
        for artifact in only:
            if include_columns and artifact in self._prediction_dataset_type:
                key = self._experiment._client._backend.download_prediction(
                    self._experiment.key,
                    self._prediction_dataset_type[artifact],
                    include_columns=include_columns,
                )
                while _utils.is_server_job_running(
                    self._experiment._client._backend.get_prediction_job(key).status
                ):
                    time.sleep(1)
                path = self._experiment._client._backend.get_prediction_job(
                    key
                ).entity.predictions_csv_path
            else:
                path = self._paths.get(artifact)
            if not path:
                raise RuntimeError(
                    f"'{artifact}' does not exist on the Driverless AI server."
                )
            dst_paths[artifact] = self._experiment._client._download(
                server_path=path,
                dst_dir=dst_dir,
                file_system=file_system,
                overwrite=overwrite,
            )
        return dst_paths

    @_model_ready
    def export(
        self,
        only: Optional[Union[str, List[str]]] = None,
        include_columns: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Dict[str, str]:
        """Export experiment artifacts from the Driverless AI server. Returns
        a dictionary of relative paths for the exported artifacts.

        Args:
            only: specify specific artifacts to export, use
                ``ex.artifacts.list()`` to see the available
                artifacts on the Driverless AI server
            include_columns: list of dataset columns to append to prediction csvs

        .. note::
            Export location is configured on the Driverless AI server.
        """
        self._update()
        if include_columns is None:
            include_columns = []
        all_dataset_columns: List[str] = sum(
            [getattr(d, "columns", []) for d in self._experiment.datasets.values()],
            [],
        )
        for c in include_columns:
            if c not in all_dataset_columns:
                raise RuntimeError(f"Column '{c}' not found in datasets.")
        export_location = self._experiment._client._backend.list_experiment_artifacts(
            model_key=self._experiment.key,
            storage_destination=kwargs.get("storage_destination", ""),
        ).location
        exported_artifacts = {}
        if isinstance(only, str):
            only = [only]
        if only is None:
            only = self.list()
        for artifact in only:
            if include_columns and artifact in self._prediction_dataset_type:
                key = self._experiment._client._backend.download_prediction(
                    self._experiment.key,
                    self._prediction_dataset_type[artifact],
                    include_columns=include_columns,
                )
                while _utils.is_server_job_running(
                    self._experiment._client._backend.get_prediction_job(key).status
                ):
                    time.sleep(1)
                artifact_path = self._experiment._client._backend.get_prediction_job(
                    key
                ).entity.predictions_csv_path
            else:
                artifact_path = self._paths.get(artifact)
            if not artifact_path:
                raise RuntimeError(
                    f"'{artifact_path}' does not exist on the Driverless AI server."
                )
            artifact_file_name = Path(artifact_path).name
            job_key = self._experiment._client._backend.upload_experiment_artifacts(
                model_key=self._experiment.key,
                user_note=kwargs.get("user_note", ""),
                artifact_path=artifact_path,
                name_override=artifact_file_name,
                repo=kwargs.get("repo", ""),  # deprecated in 1.10.2
                storage_destination=kwargs.get("storage_destination", ""),
                branch=kwargs.get("branch", ""),
                username=kwargs.get("username", ""),
                password=kwargs.get("password", ""),
            )
            _utils.ArtifactExportJob(
                self._experiment._client,
                job_key,
                artifact_path,
                artifact_file_name,
                export_location,
            ).result()
            exported_artifacts[artifact] = str(
                Path(export_location, artifact_file_name)
            )
        return exported_artifacts

    @_model_ready
    def list(self) -> List[str]:
        """List of experiment artifacts that exist on the Driverless AI server."""
        self._update()
        return [k for k, v in self._paths.items() if v and k != "autoreport"]


class ExperimentExportJob(_utils.ServerJob):
    """Monitor creation of experiment export binary on the Driverless AI server."""

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_export_experiment_job(self.key))

    def result(self, silent: bool = False) -> "ExperimentExportJob":
        """Wait for job to complete, then return self.

        Args:
            silent: if True, don't display status updates
        """
        self._wait(silent)
        return self

    def status(self, verbose: int = 0) -> str:
        """Return job status string.

        Args:
            verbose:
                - 0: short description
                - 1: short description with progress percentage
                - 2: detailed description with progress percentage
        """
        status = self._status()
        if verbose == 1:
            return f"{status.message} {self._get_raw_info().progress:.2%}"
        if verbose == 2:
            if status == _utils.JobStatus.FAILED:
                message = " - " + self._get_raw_info().error
            else:
                message = ""  # no message for export jobs
            return f"{status.message} {self._get_raw_info().progress:.2%}{message}"
        return status.message


class ExperimentLog:
    """Interact with experiment logs."""

    def __init__(self, experiment: "Experiment") -> None:
        self._client = experiment._client
        self._experiment = experiment
        self._log_name = "h2oai_experiment_" + experiment.key + ".log"

    def _error_message(self) -> str:
        self._experiment._update()
        error_message = (
            "No logs available for experiment " + self._experiment.name + "."
        )
        return error_message

    def download(
        self,
        archive: bool = True,
        dst_dir: str = ".",
        dst_file: Optional[str] = None,
        file_system: Optional["fsspec.spec.AbstractFileSystem"] = None,
        overwrite: bool = False,
    ) -> str:
        """Download experiment logs from the Driverless AI server.

        Args:
            archive: if available, prefer downloading an archive that contains
                multiple log files and stack traces if any were created
            dst_dir: directory where logs will be saved
            dst_file: name of log file (overrides default file name)
            file_system: FSSPEC based file system to download to,
                instead of local file system
            overwrite: overwrite existing file
        """
        self._experiment._update()
        log_name = self._experiment._get_raw_info().entity.log_file_path
        if log_name == "" or not archive:
            log_name = self._log_name
        return self._client._download(
            server_path=log_name,
            dst_dir=dst_dir,
            dst_file=dst_file,
            file_system=file_system,
            overwrite=overwrite,
        )

    def head(self, num_lines: int = 50) -> None:
        """Print first n lines of experiment log.

        Args:
            num_lines: number of lines to print
        """
        res = self._client._get_file(server_path=self._log_name)
        for line in res.text.rstrip().split("\n")[:num_lines]:
            print(line.strip())

    def tail(self, num_lines: int = 50) -> None:
        """Print last n lines of experiment log.

        Args:
            num_lines: number of lines to print
        """
        res = self._client._get_file(server_path=self._log_name)
        for line in res.text.rstrip().split("\n")[-num_lines:]:
            print(line.strip())


class Experiments:
    """Interact with experiments on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client
        self._default_experiment_settings = {
            setting.name.strip(): setting.val
            for setting in client._backend.get_all_config_options()
        }
        # convert setting name from key to value
        self._setting_for_server_dict = {
            "drop_columns": "cols_to_drop",
            "fold_column": "fold_col",
            "reproducible": "seed",
            "scorer": "score_f_name",
            "target_column": "target_col",
            "time_column": "time_col",
            "weight_column": "weight_col",
            "unavailable_at_prediction_time_columns": (
                "unavailable_columns_at_prediction_time"
            ),
        }
        self._setting_for_api_dict = {
            v: k for k, v in self._setting_for_server_dict.items()
        }

    def _check_api_settings(self, settings: Dict[str, Any]) -> None:
        # check target column exists
        if (
            settings["task"] != "unsupervised"
            and settings["target_column"] not in settings["train_dataset"].columns
        ):
            target_column = settings["target_column"]
            raise ValueError(
                f"Target column '{target_column}' not found in training data."
            )
        # check unsupervised requirements
        if settings["task"] == "unsupervised":
            _utils.check_server_support(
                client=self._client,
                minimum_server_version="1.10.0",
                parameter="task='unsupervised'",
            )
            target_models = settings.get("models", None) or settings.get(
                "included_models", []
            )
            unsupervised_model_names = [
                m.name for m in self._client.recipes.models.list() if m.is_unsupervised
            ]
            # remove Model suffix
            unsupervised_model_names += [
                m[:-5] for m in unsupervised_model_names if m.lower().endswith("model")
            ]
            if len(target_models) != 1 or (
                target_models[0] not in unsupervised_model_names
                and getattr(target_models[0], "name", None)
                not in unsupervised_model_names
            ):
                raise ValueError(
                    "Unsupervised tasks require one unsupervised model to be specified."
                )
        # if custom recipes acceptance jobs are running, wait for them to finish
        if not settings.pop("force_skip_acceptance_tests", False) and hasattr(
            self._client._backend, "_wait_for_custom_recipes_acceptance_tests"
        ):
            self._client._backend._wait_for_custom_recipes_acceptance_tests()

    def _lazy_get(self, key: str) -> "Experiment":
        """Initialize an Experiment object but don't request information from
        the server (possible for experiment key to not exist on server). Useful
        for populating lists without making a bunch of network calls.

        Args:
            key: Driverless AI server's unique ID for the experiment
        """
        return Experiment(self._client, key)

    def _parse_api_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Python API experiment settings to format required by the
        Driverless AI server.
        """
        custom_settings: Dict[str, Any] = {}

        tasks = ["classification", "regression", "unsupervised"]

        not_config_overrides = [
            "train_dataset",  # Reflects 'dataset' in backend
            "resumed_model",
            "target_column",  # Reflects 'target_col' in backend
            "weight_column",  # Reflects 'weight_col' in backend
            "fold_column",  # Reflects 'fold_col' in backend
            "orig_time_col",
            "time_column",  # Reflects 'time_col' in backend
            "is_classification",
            "drop_columns",  # Reflects 'cols_to_drop' in backend
            "validset",
            "testset",
            "enable_gpus",
            "reproducible",  # Reflects 'seed' in backend
            "accuracy",
            "time",
            "interpretability",
            "scorer",  # Reflects 'score_f_name' in backend
            "time_groups_columns",
            # Reflects 'unavailable_columns_at_prediction_time' in backend
            "unavailable_at_prediction_time_columns",
            "time_period_in_seconds",
            "num_prediction_periods",
            "num_gap_periods",
            "is_timeseries",
            "is_image",
            "custom_feature",
        ]

        for setting in [
            "config_overrides",
            "validation_dataset",
            "test_dataset",
            "parent_experiment",
        ]:
            if setting not in settings or settings[setting] is None:
                settings[setting] = ""

        def get_ref(desc: str, obj: Any) -> Tuple[str, Any]:
            if isinstance(obj, str):
                key = obj
            else:
                key = obj.key
            if desc == "train_dataset":
                ref_type = "dataset"
                ref = self._client._server_module.references.DatasetReference(key)
            if desc == "validation_dataset":
                ref_type = "validset"
                ref = self._client._server_module.references.DatasetReference(key)
            if desc == "test_dataset":
                ref_type = "testset"
                ref = self._client._server_module.references.DatasetReference(key)
            if desc == "parent_experiment":
                ref_type = "resumed_model"
                ref = self._client._server_module.references.ModelReference(key)
            return ref_type, ref

        included_models = []
        for m in settings.pop("models", []):
            if isinstance(m, _recipes.ModelRecipe):
                included_models.append(m.name)
            else:
                included_models.append(m)
        if len(included_models) > 0:
            settings.setdefault("included_models", [])
            settings["included_models"] += included_models

        included_transformers = []
        for t in settings.pop("transformers", []):
            if isinstance(t, _recipes.TransformerRecipe):
                included_transformers.append(t.name)
            else:
                included_transformers.append(t)
        if len(included_transformers) > 0:
            settings.setdefault("included_transformers", [])
            settings["included_transformers"] += included_transformers

        custom_settings["is_timeseries"] = False
        custom_settings["is_image"] = "image" in [
            c.data_type for c in settings["train_dataset"].column_summaries()
        ]
        custom_settings["enable_gpus"] = self._client._backend.get_gpu_stats().gpus > 0
        config_overrides = toml.loads(settings["config_overrides"])
        for setting, value in settings.items():
            if setting == "task":
                if value not in tasks:
                    raise ValueError("Please set the task to one of:", tasks)
                custom_settings["is_classification"] = "classification" == value
                if value == "unsupervised":
                    config_overrides["recipe"] = "unsupervised"
            elif setting in [
                "train_dataset",
                "validation_dataset",
                "test_dataset",
                "parent_experiment",
            ]:
                ref_type, ref = get_ref(setting, value)
                custom_settings[ref_type] = ref
            elif setting == "time_column":
                custom_settings[self._setting_for_server_dict[setting]] = value
                custom_settings["is_timeseries"] = value is not None
            elif setting == "scorer":
                if isinstance(value, _recipes.ScorerRecipe):
                    value = value.name
                custom_settings[self._setting_for_server_dict[setting]] = value
            elif setting == "enable_gpus":
                if custom_settings[setting]:  # confirm GPUs are present
                    custom_settings[setting] = value
            elif setting in self._setting_for_server_dict:
                custom_settings[self._setting_for_server_dict[setting]] = value
            elif setting in not_config_overrides:
                custom_settings[setting] = value
            elif setting != "config_overrides":
                if setting not in self._default_experiment_settings:
                    raise RuntimeError(
                        f"'{setting}' experiment setting not recognized."
                    )
                config_overrides[setting] = value
        custom_settings["config_overrides"] = toml.dumps(config_overrides)

        model_parameters = self._client._server_module.messages.ModelParameters(
            dataset=custom_settings["dataset"],
            resumed_model=custom_settings.get(
                "resumed_model", get_ref("parent_experiment", "")
            ),
            target_col=custom_settings["target_col"],
            weight_col=custom_settings.get("weight_col", None),
            fold_col=custom_settings.get("fold_col", None),
            orig_time_col=custom_settings.get(
                "orig_time_col", custom_settings.get("time_col", None)
            ),
            time_col=custom_settings.get("time_col", None),
            is_classification=custom_settings["is_classification"],
            cols_to_drop=custom_settings.get("cols_to_drop", []),
            validset=custom_settings.get("validset", get_ref("validation_dataset", "")),
            testset=custom_settings.get("testset", get_ref("test_dataset", "")),
            enable_gpus=custom_settings.get("enable_gpus", True),
            seed=custom_settings.get("seed", False),
            accuracy=None,
            time=None,
            interpretability=None,
            score_f_name=None,
            time_groups_columns=custom_settings.get("time_groups_columns", None),
            unavailable_columns_at_prediction_time=custom_settings.get(
                "unavailable_columns_at_prediction_time", []
            ),
            time_period_in_seconds=custom_settings.get("time_period_in_seconds", None),
            num_prediction_periods=custom_settings.get("num_prediction_periods", None),
            num_gap_periods=custom_settings.get("num_gap_periods", None),
            is_timeseries=custom_settings.get("is_timeseries", False),
            cols_imputation=custom_settings.get("cols_imputation", []),
            config_overrides=custom_settings.get("config_overrides", None),
            custom_features=[],
            is_image=custom_settings.get("is_image", False),
        )

        server_settings = self._client._backend.get_experiment_tuning_suggestion(
            model_parameters
        ).dump()

        server_settings.update(**custom_settings)

        return server_settings

    def _parse_server_settings(self, server_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Driverless AI server experiment settings to Python API format."""
        blacklist = [
            "is_classification",
            "is_timeseries",
            "is_image",
            "dataset",
            "validset",
            "testset",
            "orig_time_col",
            "resumed_model",
            "config_overrides",
        ]
        if self._client._backend.get_gpu_stats().gpus == 0:
            blacklist.append("enable_gpus")
            blacklist.append("num_gpus_per_experiment")
            blacklist.append("num_gpus_per_model")
        elif server_settings["enable_gpus"]:
            blacklist.append("enable_gpus")
        if not server_settings["seed"]:
            blacklist.append("seed")
        if not server_settings["is_timeseries"]:
            blacklist.append("time_col")

        def supervised_task(server_settings: Dict[str, Any]) -> str:
            if server_settings["is_classification"]:
                return "classification"
            else:
                return "regression"

        settings: Dict[str, Any] = {"task": supervised_task(server_settings)}
        for key, value in server_settings.items():
            if key not in blacklist and value not in [None, "", []]:
                settings[self._setting_for_api_dict.get(key, key)] = value
        settings.update(
            _utils.toml_to_api_settings(
                toml_string=server_settings["config_overrides"],
                default_api_settings=self._default_experiment_settings,
                blacklist=blacklist,
            )
        )
        if settings.get("recipe", None) == "unsupervised":
            settings["target_column"] = None
            settings["task"] = "unsupervised"
        if (
            server_settings["resumed_model"]["key"] != ""
            and server_settings["resumed_model"]["display_name"] != ""
        ):
            settings["parent_experiment"] = self.get(
                server_settings["resumed_model"]["key"]
            )
        for setting_names in [
            ("included_models", "models"),
            ("included_transformers", "transformers"),
        ]:
            if setting_names[0] in settings:
                settings[setting_names[1]] = settings.pop(setting_names[0])
                if isinstance(settings[setting_names[1]], str):
                    settings[setting_names[1]] = settings[setting_names[1]].split(",")

        return settings

    def create(
        self,
        train_dataset: "_datasets.Dataset",
        target_column: Optional[str],
        task: str,
        force: bool = False,
        name: str = None,
        **kwargs: Any,
    ) -> "Experiment":
        """Launch an experiment on the Driverless AI server and wait for it to
        complete before returning.

        Args:
            train_dataset: Dataset object
            target_column: name of column in ``train_dataset``
                (ignored if ``task`` is ``'unsupervised'``)
            task: one of ``'regression'``, ``'classification'``, or ``'unsupervised'``
            force: create new experiment even if experiment with same name
              already exists
            name: display name for experiment

        Keyword Args:
            accuracy (int): accuracy setting [1-10]
            time (int): time setting [1-10]
            interpretability (int): interpretability setting [1-10]
            scorer (Union[str,ScorerRecipe]): metric to optimize for
            models (Union[str,ModelRecipe]): limit experiment to these models
            transformers (Union[str,TransformerRecipe]): limit experiment to
              these transformers
            validation_dataset (Dataset): Dataset object
            test_dataset (Dataset): Dataset object
            weight_column (str): name of column in ``train_dataset``
            fold_column (str): name of column in ``train_dataset``
            time_column (str): name of column in ``train_dataset``,
              containing time ordering for timeseries problems
            time_groups_columns (List[str]): list of column names,
              contributing to time ordering
            unavailable_at_prediction_time_columns (List[str]):
              list of column names, which won't be present at prediction time
              (server versions >= 1.8.1)
            drop_columns (List[str]): list of column names to be dropped
            enable_gpus (bool): allow GPU usage in experiment
            reproducible (bool): set experiment to be reproducible
            time_period_in_seconds (int): the length of the time period in seconds,
              used in timeseries problems
            num_prediction_periods (int): timeseries forecast horizon in time
              period units
            num_gap_periods (int): number of time periods after which
              forecast starts
            config_overrides (str): Driverless AI config overrides in TOML string format

        .. note::
            Any expert setting can also be passed as a ``kwarg``.
            To search possible expert settings for your server version,
            use ``experiments.search_expert_settings(search_term)``.
        """
        return self.create_async(
            train_dataset, target_column, task, force, name, **kwargs
        ).result()

    def create_async(
        self,
        train_dataset: "_datasets.Dataset",
        target_column: Optional[str],
        task: str,
        force: bool = False,
        name: str = None,
        **kwargs: Any,
    ) -> "Experiment":
        """Launch an experiment on the Driverless AI server and return an
        Experiment object to track the experiment status.

        Args:
            train_dataset: Dataset object
            target_column: name of column in ``train_dataset``
                (ignored if ``task`` is ``'unsupervised'``)
            task: one of ``'regression'``, ``'classification'``, or ``'unsupervised'``
            force: create new experiment even if experiment with same name
              already exists
            name: display name for experiment

        Keyword Args:
            accuracy (int): accuracy setting [1-10]
            time (int): time setting [1-10]
            interpretability (int): interpretability setting [1-10]
            scorer (Union[str,ScorerRecipe]): metric to optimize for
            models (Union[str,ModelRecipe]): limit experiment to these models
            transformers (Union[str,TransformerRecipe]): limit experiment to
              these transformers
            validation_dataset (Dataset): Dataset object
            test_dataset (Dataset): Dataset object
            weight_column (str): name of column in ``train_dataset``
            fold_column (str): name of column in ``train_dataset``
            time_column (str): name of column in ``train_dataset``,
              containing time ordering for timeseries problems
            time_groups_columns (List[str]): list of column names,
              contributing to time ordering
            unavailable_at_prediction_time_columns (List[str]):
              list of column names, which won't be present at prediction time
              (server versions >= 1.8.1)
            drop_columns (List[str]): list of column names to be dropped
            enable_gpus (bool): allow GPU usage in experiment
            reproducible (bool): set experiment to be reproducible
            time_period_in_seconds (int): the length of the time period in seconds,
              used in timeseries problems
            num_prediction_periods (int): timeseries forecast horizon in time
              period units
            num_gap_periods (int): number of time periods after which
              forecast starts
            config_overrides (str): Driverless AI config overrides in TOML string format

        .. note::
            Any expert setting can also be passed as a ``kwarg``.
            To search possible expert settings for your server version,
            use ``experiments.search_expert_settings(search_term)``.
        """
        if not force:
            _utils.error_if_experiment_exists(self._client, name)
        kwargs["task"] = task
        kwargs["train_dataset"] = train_dataset
        kwargs["target_column"] = target_column
        self._check_api_settings(kwargs)
        server_settings = self._parse_api_settings(kwargs)
        job_key = self._client._backend.start_experiment(
            self._client._server_module.messages.ModelParameters(**server_settings),
            experiment_name=name,
        )
        job = self.get(job_key)
        print("Experiment launched at:", job.gui())
        return job

    def get(self, key: str) -> "Experiment":
        """Get an Experiment object corresponding to an experiment on the
        Driverless AI server. If the experiment only exists on H2O.ai Storage,
        it will be imported to the server first.

        Args:
            key: Driverless AI server's unique ID for the experiment
        """
        if self._client.server.storage_enabled:
            try:
                storage_key = self._client._backend.import_storage_model(key)
                print("Importing experiment from storage...")
                _utils.StorageImportJob(self._client, storage_key).result()
            except self._client._server_module.protocol.RemoteError as e:
                if not _utils.is_key_error(e):
                    raise
        experiment = self._lazy_get(key)
        experiment._update()
        return experiment

    def gui(self) -> _utils.Hyperlink:
        """Get full URL for the experiments page on the Driverless AI server."""
        return _utils.Hyperlink(
            f"{self._client.server.address}{self._client._gui_sep}experiments"
        )

    def import_dai_file(self, path: str) -> "Experiment":
        """Import a dai file to the Driverless AI server and return a
        corresponding Experiment object."""
        _utils.check_server_support(
            client=self._client,
            minimum_server_version="1.10.0",
            parameter="import_dai_file",
        )
        return self.get(self._client._backend.import_experiment_sync(path))

    def leaderboard(
        self,
        train_dataset: "_datasets.Dataset",
        target_column: Optional[str],
        task: str,
        force: bool = False,
        name: str = None,
        **kwargs: Any,
    ) -> "_projects.Project":
        """Launch an experiment leaderboard on the Driverless AI server and
        return a project object to track experiment statuses. Requires server
        version >= 1.9.0.

        Args:
            train_dataset: Dataset object
            target_column: name of column in ``train_dataset``
                (ignored if ``task`` is ``'unsupervised'``)
            task: one of ``'regression'``, ``'classification'``, or ``'unsupervised'``
            force: create new project even if project with same name
              already exists
            name: display name for project

        Keyword Args:
            accuracy (int): accuracy setting [1-10]
            time (int): time setting [1-10]
            interpretability (int): interpretability setting [1-10]
            scorer (Union[str,ScorerRecipe]): metric to optimize for
            models (Union[str,ModelRecipe]): limit experiment to these models
            transformers (Union[str,TransformerRecipe]): limit experiment to
              these transformers
            validation_dataset (Dataset): Dataset object
            test_dataset (Dataset): Dataset object
            weight_column (str): name of column in ``train_dataset``
            fold_column (str): name of column in ``train_dataset``
            time_column (str): name of column in ``train_dataset``,
              containing time ordering for timeseries problems
            time_groups_columns (List[str]): list of column names,
              contributing to time ordering
            unavailable_at_prediction_time_columns (List[str]):
              list of column names, which won't be present at prediction time
              (server versions >= 1.8.1)
            drop_columns (List[str]): list of column names to be dropped
            enable_gpus (bool): allow GPU usage in experiment
            reproducible (bool): set experiment to be reproducible
            time_period_in_seconds (int): the length of the time period in seconds,
              used in timeseries problems
            num_prediction_periods (int): timeseries forecast horizon in time
              period units
            num_gap_periods (int): number of time periods after which
              forecast starts
            config_overrides (str): Driverless AI config overrides in TOML string format

        .. note::
            Any expert setting can also be passed as a ``kwarg``.
            To search possible expert settings for your server version,
            use ``experiments.search_expert_settings(search_term)``.
        """
        _utils.check_server_support(
            client=self._client,
            minimum_server_version="1.9.0",
            parameter="leaderboard",
        )
        if not force:
            _utils.error_if_project_exists(self._client, name)
        kwargs["task"] = task
        kwargs["train_dataset"] = train_dataset
        kwargs["target_column"] = target_column
        self._check_api_settings(kwargs)
        server_settings = self._parse_api_settings(kwargs)
        project_key = self._client._backend.start_experiment_leaderboard(
            req=self._client._server_module.messages.ModelParameters(**server_settings),
            leaderboard_name=name,
        )
        project = self._client.projects.get(project_key)
        if name:
            project.rename(name)
        print("Leaderboard launched at:", project.gui())
        return project

    def list(self, start_index: int = 0, count: int = None) -> Sequence["Experiment"]:
        """List of Experiment objects available to the user.

        Args:
            start_index: index on Driverless AI server of first experiment in list
            count: number of experiments to request from the Driverless AI server
        """
        if count:
            data = self._client._backend.list_models(start_index, count).models
        else:
            page_size = 100
            page_position = start_index
            data = []
            while True:
                page = self._client._backend.list_models(
                    page_position, page_size
                ).models
                data += page
                if len(page) < page_size:
                    break
                page_position += page_size
        return _utils.ServerObjectList(
            data=data, get_method=self._lazy_get, item_class_name=Experiment.__name__
        )

    def preview(
        self,
        train_dataset: "_datasets.Dataset",
        target_column: Optional[str],
        task: str,
        force: Optional[bool] = None,
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Print a preview of experiment for the given settings.

        Args:
            train_dataset: Dataset object
            target_column: name of column in ``train_dataset``
                (ignored if ``task`` is ``'unsupervised'``)
            task: one of ``'regression'``, ``'classification'``, or ``'unsupervised'``
            force: ignored (``preview`` accepts the same arguments as ``create``)
            name: ignored (``preview`` accepts the same arguments as ``create``)

        Keyword Args:
            accuracy (int): accuracy setting [1-10]
            time (int): time setting [1-10]
            interpretability (int): interpretability setting [1-10]
            scorer (Union[str,ScorerRecipe]): metric to optimize for
            models (Union[str,ModelRecipe]): limit experiment to these models
            transformers (Union[str,TransformerRecipe]): limit experiment to
              these transformers
            validation_dataset (Dataset): Dataset object
            test_dataset (Dataset): Dataset object
            weight_column (str): name of column in ``train_dataset``
            fold_column (str): name of column in ``train_dataset``
            time_column (str): name of column in ``train_dataset``,
              containing time ordering for timeseries problems
            time_groups_columns (List[str]): list of column names,
              contributing to time ordering
            unavailable_at_prediction_time_columns (List[str]):
              list of column names, which won't be present at prediction time
              (server versions >= 1.8.1)
            drop_columns (List[str]): list of column names to be dropped
            enable_gpus (bool): allow GPU usage in experiment
            reproducible (bool): set experiment to be reproducible
            time_period_in_seconds (int): the length of the time period in seconds,
              used in timeseries problems
            num_prediction_periods (int): timeseries forecast horizon in time
              period units
            num_gap_periods (int): number of time periods after which
              forecast starts
            config_overrides (str): Driverless AI config overrides in TOML string format

        .. note::
            Any expert setting can also be passed as a ``kwarg``.
            To search possible expert settings for your server version,
            use ``experiments.search_expert_settings(search_term)``.
        """
        kwargs["task"] = task
        kwargs["train_dataset"] = train_dataset
        kwargs["target_column"] = target_column
        for arg in ["force", "name"]:
            # arg is accepted by create but not needed for preview
            kwargs.pop(arg, None)
        self._check_api_settings(kwargs)
        settings = self._parse_api_settings(kwargs)
        key = self._client._backend.get_experiment_preview(
            self._client._server_module.messages.ModelParameters(**settings)
        )
        while _utils.is_server_job_running(
            self._client._backend.get_experiment_preview_job(key).status
        ):
            time.sleep(1)
        preview = self._client._backend.get_experiment_preview_job(key).entity.lines
        for line in preview:
            print(line)

    def search_expert_settings(
        self, search_term: str, show_description: bool = False
    ) -> None:
        """Search expert settings and print results. Useful when looking for
        kwargs to use when creating experiments.

        Args:
            search_term: term to search for (case insensitive)
            show_description: include description in results
        """
        for c in self._client._backend.get_all_config_options():
            if (
                search_term.lower()
                in " ".join([c.name, c.category, c.description, c.comment]).lower()
            ):
                print(
                    self._setting_for_api_dict.get(c.name, c.name),
                    "|",
                    "default_value:",
                    self._default_experiment_settings[c.name.strip()],
                    end="",
                )
                if show_description:
                    description = c.description.strip()
                    comment = " ".join(
                        [s.strip() for s in c.comment.split("\n")]
                    ).strip()
                    print(" |", description)
                    print(" ", comment)
                print()


class Prediction:
    """Interact with predictions from the Driverless AI server."""

    def __init__(
        self,
        prediction_jobs: List["PredictionJob"],
        included_dataset_columns: List[str],
        includes_labels: bool,
        includes_raw_outputs: bool,
        includes_shap_values_for_original_features: bool,
        includes_shap_values_for_transformed_features: bool,
        used_fast_approx_for_shap_values: bool,
    ) -> None:
        self._client = prediction_jobs[0]._client
        self._file_paths = [
            job._get_raw_info().entity.predictions_csv_path for job in prediction_jobs
        ]
        self._included_dataset_columns = included_dataset_columns
        self._includes_labels = includes_labels
        self._includes_raw_outputs = includes_raw_outputs
        self._includes_shap_values_for_original_features = (
            includes_shap_values_for_original_features
        )
        self._includes_shap_values_for_transformed_features = (
            includes_shap_values_for_transformed_features
        )
        self._keys = prediction_jobs[0].keys
        self._used_fast_approx_for_shap_values = used_fast_approx_for_shap_values

    @property
    def file_paths(self) -> List[str]:
        """Paths to prediction csv files on the server."""
        return self._file_paths

    @property
    def included_dataset_columns(self) -> List[str]:
        """Columns from dataset that are appended to predictions."""
        return self._included_dataset_columns

    @property
    def includes_labels(self) -> bool:
        """Whether classification labels are appended to predictions."""
        return self._includes_labels

    @property
    def includes_raw_outputs(self) -> bool:
        """Whether predictions as margins (in link space) were appended to
        predictions.
        """
        return self._includes_raw_outputs

    @property
    def includes_shap_values_for_original_features(self) -> bool:
        """Whether original feature contributions are appended to predictions
        (server versions >= 1.9.1)."""
        return self._includes_shap_values_for_original_features

    @property
    def includes_shap_values_for_transformed_features(self) -> bool:
        """Whether transformed feature contributions are appended to predictions."""
        return self._includes_shap_values_for_transformed_features

    @property
    def keys(self) -> Dict[str, str]:
        """Dictionary of unique IDs for entities related to the prediction:
        dataset: unique ID of dataset used to make predictions
        experiment: unique ID of experiment used to make predictions
        prediction: unique ID of predictions
        """
        return self._keys

    @property
    def used_fast_approx_for_shap_values(self) -> Optional[bool]:
        """Whether approximation was used to calculate prediction contributions
        (server versions >= 1.9.1)."""
        return self._used_fast_approx_for_shap_values

    def download(
        self,
        dst_dir: str = ".",
        dst_file: Optional[str] = None,
        file_system: Optional["fsspec.spec.AbstractFileSystem"] = None,
        overwrite: bool = False,
    ) -> str:
        """Download csv of predictions.

        Args:
            dst_dir: directory where csv will be saved
            dst_file: name of csv file (overrides default file name)
            file_system: FSSPEC based file system to download to,
                instead of local file system
            overwrite: overwrite existing file
        """
        if len(self.file_paths) == 1:
            return self._client._download(
                server_path=self.file_paths[0],
                dst_dir=dst_dir,
                dst_file=dst_file,
                file_system=file_system,
                overwrite=overwrite,
            )

        if not dst_file:
            dst_file = Path(self.file_paths[0]).name
        dst_path = str(Path(dst_dir, dst_file))

        # concatenate csvs horizontally
        def write_csv(f: IO) -> None:
            csv_writer = csv.writer(f)
            # read in multiple csvs
            texts = [self._client._get_file(p).content for p in self.file_paths]
            csvs = [csv.reader(io.StringIO(t.decode())) for t in texts]
            # unpack and join
            for row_from_each_csv in zip(*csvs):
                row_joined: List[str] = sum(row_from_each_csv, [])
                csv_writer.writerow(row_joined)

        try:
            if file_system is None:
                if overwrite:
                    mode = "w"
                else:
                    mode = "x"
                with open(dst_path, mode) as f:
                    write_csv(f)
                print(f"Downloaded '{dst_path}'")
            else:
                if not overwrite and file_system.exists(dst_path):
                    raise FileExistsError(f"File exists: {dst_path}")
                with file_system.open(dst_path, "w") as f:
                    write_csv(f)
                print(f"Downloaded '{dst_path}' to {file_system}")
        except FileExistsError:
            print(f"{dst_path} already exists. Use `overwrite` to force download.")
            raise

        return dst_path

    def to_pandas(self) -> "pandas.DataFrame":
        """Transfer predictions to a local Pandas DataFrame."""
        import pandas as pd

        # read in multiple csvs
        contents = [self._client._get_file(p).content for p in self.file_paths]
        csvs = [csv.reader(io.StringIO(c.decode())) for c in contents]
        # unpack and join
        rows = []
        for row_from_each_csv in zip(*csvs):
            row_joined: List[str] = sum(row_from_each_csv, [])
            rows.append(row_joined)
        df = pd.DataFrame(columns=rows[0], data=rows[1:])
        df = df.apply(pd.to_numeric, errors="ignore")
        return df


class PredictionJob(_utils.ServerJob):
    """Monitor creation of predictions on the Driverless AI server."""

    def __init__(
        self, client: "_core.Client", key: str, dataset_key: str, experiment_key: str
    ) -> None:
        super().__init__(client=client, key=key)
        self._keys = {
            "dataset": dataset_key,
            "experiment": experiment_key,
            "prediction": key,
        }

    @property
    def keys(self) -> Dict[str, str]:
        """Dictionary of entity unique IDs:
        dataset: unique ID of dataset used to make predictions
        experiment: unique ID of experiment used to make predictions
        prediction: unique ID of predictions
        """
        return self._keys

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_prediction_job(self.key))

    def result(self, silent: bool = False) -> "PredictionJob":
        """Wait for job to complete, then return self.

        Args:
            silent: if True, don't display status updates
        """
        self._wait(silent)
        return self

    def status(self, verbose: int = None) -> str:
        """Return short job status description string."""
        return self._status().message


class PredictionJobs(_utils.ServerJobs):
    """Monitor creation of predictions on the Driverless AI server."""

    def __init__(
        self,
        client: "_core.Client",
        jobs: List[PredictionJob],
        dataset_key: str,
        experiment_key: str,
        include_columns: List[str],
        include_labels: Optional[bool],
        include_raw_outputs: Optional[bool],
        include_shap_values_for_original_features: Optional[bool],
        include_shap_values_for_transformed_features: Optional[bool],
        use_fast_approx_for_shap_values: Optional[bool],
    ) -> None:
        super().__init__(client=client, jobs=jobs)
        self._included_dataset_columns = include_columns
        self._includes_labels = include_labels
        self._includes_raw_outputs = include_raw_outputs
        self._includes_shap_values_for_original_features = (
            include_shap_values_for_original_features
        )
        self._includes_shap_values_for_transformed_features = (
            include_shap_values_for_transformed_features
        )
        self._keys = {
            "dataset": dataset_key,
            "experiment": experiment_key,
            "prediction": jobs[0].key,
        }
        self._used_fast_approx_for_shap_values = use_fast_approx_for_shap_values

    @property
    def included_dataset_columns(self) -> List[str]:
        """Columns from dataset that are appended to predictions."""
        return self._included_dataset_columns

    @property
    def includes_labels(self) -> bool:
        """Whether classification labels are appended to predictions."""
        if self._includes_labels is None:
            return False
        return self._includes_labels

    @property
    def includes_raw_outputs(self) -> bool:
        """Whether predictions as margins (in link space) are appended to
        predictions.
        """
        if self._includes_raw_outputs is None:
            return False
        return self._includes_raw_outputs

    @property
    def includes_shap_values_for_original_features(self) -> bool:
        """Whether original feature contributions are appended to predictions
        (server versions >= 1.9.1)."""
        if self._includes_shap_values_for_original_features is None:
            return False
        return self._includes_shap_values_for_original_features

    @property
    def includes_shap_values_for_transformed_features(self) -> bool:
        """Whether transformed feature contributions are appended to predictions."""
        if self._includes_shap_values_for_transformed_features is None:
            return False
        return self._includes_shap_values_for_transformed_features

    @property
    def keys(self) -> Dict[str, str]:
        """Dictionary of entity unique IDs:
        dataset: unique ID of dataset used to make predictions
        experiment: unique ID of experiment used to make predictions
        prediction: unique ID of predictions
        """
        return self._keys

    @property
    def used_fast_approx_for_shap_values(self) -> Optional[bool]:
        """Whether approximation was used to calculate prediction contributions
        (server versions >= 1.9.1)."""
        return self._used_fast_approx_for_shap_values

    def result(self, silent: bool = False) -> Prediction:
        """Wait for all jobs to complete.

        Args:
            silent: if True, don't display status updates
        """
        status_update = _utils.StatusUpdate()
        if not silent:
            status_update.display(_utils.JobStatus.RUNNING.message)
        jobs = [job.result(silent=True) for job in self.jobs]
        if not silent:
            status_update.display(_utils.JobStatus.COMPLETE.message)
        status_update.end()
        return Prediction(
            prediction_jobs=jobs,
            included_dataset_columns=self.included_dataset_columns,
            includes_labels=self.includes_labels,
            includes_raw_outputs=self.includes_raw_outputs,
            includes_shap_values_for_original_features=(
                self.includes_shap_values_for_original_features
            ),
            includes_shap_values_for_transformed_features=(
                self.includes_shap_values_for_transformed_features
            ),
            used_fast_approx_for_shap_values=self.used_fast_approx_for_shap_values,
        )
