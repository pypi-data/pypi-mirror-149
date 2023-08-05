"""MLI module of official Python client for Driverless AI."""

import json
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import TYPE_CHECKING
from typing import Union

import toml

from driverlessai import _core
from driverlessai import _datasets
from driverlessai import _experiments
from driverlessai import _recipes
from driverlessai import _utils


if TYPE_CHECKING:
    import fsspec  # noqa F401


class Interpretation(_utils.ServerJob):
    """Interact with a MLI interpretation on the Driverless AI server."""

    def __init__(
        self,
        client: "_core.Client",
        key: str,
        update_method: Callable[[str], Any],
        url_method: Callable[["Interpretation"], str],
    ) -> None:
        # super() calls _update() which relies on _update_method()
        self._update_method = update_method
        super().__init__(client=client, key=key)
        self._artifacts: Optional[InterpretationArtifacts] = None
        self._dataset: Optional[_datasets.Dataset] = None
        self._experiment: Optional[_experiments.Experiment] = None
        self._settings: Optional[Dict[str, Any]] = None
        self._url = url_method(self)

    @property
    def artifacts(self) -> "InterpretationArtifacts":
        """Interact with artifacts that are created when the
        interpretation completes."""
        if not self._artifacts:
            self._artifacts = InterpretationArtifacts(
                self._client, self._get_raw_info()
            )
        return self._artifacts

    @property
    def creation_timestamp(self) -> float:
        """Creation timestamp in seconds since the epoch (POSIX timestamp)."""
        return self._get_raw_info().created

    @property
    def dataset(self) -> Optional[_datasets.Dataset]:
        """Dataset for the interpretation."""
        if not self._dataset:
            if hasattr(self._get_raw_info().entity.parameters, "dataset"):
                try:
                    self._dataset = self._client.datasets.get(
                        self._get_raw_info().entity.parameters.dataset.key
                    )
                except self._client._server_module.protocol.RemoteError:
                    # assuming a key error means deleted dataset, if not the error
                    # will still propagate to the user else where
                    self._dataset = (
                        self._get_raw_info().entity.parameters.dataset.dump()
                    )
            else:
                # timeseries sometimes doesn't have dataset attribute
                try:
                    self._dataset = self.experiment.datasets["train_dataset"]
                except self._client._server_module.protocol.RemoteError:
                    # assuming a key error means deleted dataset, if not the error
                    # will still propagate to the user else where
                    self._dataset = None
        return self._dataset

    @property
    def experiment(self) -> Optional[_experiments.Experiment]:
        """Experiment for the interpretation."""
        if not self._experiment:
            try:
                self._experiment = self._client.experiments.get(
                    self._get_raw_info().entity.parameters.dai_model.key
                )
            except self._client._server_module.protocol.RemoteError:
                # assuming a key error means deleted experiment, if not the error
                # will still propagate to the user else where
                self._experiment = None
        return self._experiment

    @property
    def run_duration(self) -> Optional[float]:
        """Run duration in seconds."""
        self._update()
        try:
            return self._get_raw_info().entity.training_duration
        except AttributeError:
            print("Run duration not available for some time series interpretations.")
            return None

    @property
    def settings(self) -> Dict[str, Any]:
        """Interpretation settings."""
        if not _utils.is_server_version_less_than(self._client, "1.9.1"):
            raise RuntimeError(
                "Settings cannot be retrieved from server versions >= 1.9.1."
            )
        if not self._settings:
            self._settings = self._client.mli._parse_server_settings(
                self._get_raw_info().entity.parameters.dump()
            )
        return self._settings

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'> {self.key} {self.name}"

    def __str__(self) -> str:
        return f"{self.name} ({self.key})"

    def _update(self) -> None:
        self._set_raw_info(self._update_method(self.key))
        self._set_name(self._get_raw_info().entity.description)

    def delete(self) -> None:
        """Delete MLI interpretation on Driverless AI server."""
        key = self.key
        self._client._backend.delete_interpretation(key)
        print("Driverless AI Server reported interpretation {key} deleted.")

    def gui(self) -> _utils.Hyperlink:
        """Get full URL for the interpretation's page on the Driverless AI server."""
        return _utils.Hyperlink(self._url)

    def rename(self, name: str) -> "Interpretation":
        """Change interpretation display name.

        Args:
            name: new display name
        """
        self._client._backend.update_mli_description(self.key, name)
        self._update()
        return self

    def result(self, silent: bool = False) -> "Interpretation":
        """Wait for job to complete, then return an Interpretation object."""
        self._wait(silent)
        return self


class InterpretationArtifacts:
    """Interact with files created by a MLI interpretation on the
    Driverless AI server."""

    def __init__(self, client: "_core.Client", info: Any) -> None:
        self._client = client
        self._paths = {
            "log": getattr(info.entity, "log_file_path", ""),
            "lime": getattr(info.entity, "lime_rc_csv_path", ""),
            "shapley_transformed_features": getattr(
                info.entity, "shapley_rc_csv_path", ""
            ),
            "shapley_original_features": getattr(
                info.entity, "shapley_orig_rc_csv_path", ""
            ),
            "python_pipeline": getattr(info.entity, "scoring_package_path", ""),
        }

    @property
    def file_paths(self) -> Dict[str, str]:
        """Paths to artifact files on the server."""
        return self._paths

    def download(
        self,
        only: Union[str, List[str]] = None,
        dst_dir: str = ".",
        file_system: Optional["fsspec.spec.AbstractFileSystem"] = None,
        overwrite: bool = False,
    ) -> Dict[str, str]:
        """Download interpretation artifacts from the Driverless AI server. Returns
        a dictionary of relative paths for the downloaded artifacts.

        Args:
            only: specify specific artifacts to download, use
                ``interpretation.artifacts.list()`` to see the available
                artifacts on the Driverless AI server
            dst_dir: directory where interpretation artifacts will be saved
            file_system: FSSPEC based file system to download to,
                instead of local file system
            overwrite: overwrite existing files
        """
        dst_paths = {}
        if isinstance(only, str):
            only = [only]
        if only is None:
            only = self.list()
        for k in only:
            path = self._paths.get(k)
            if path:
                dst_paths[k] = self._client._download(
                    server_path=path,
                    dst_dir=dst_dir,
                    file_system=file_system,
                    overwrite=overwrite,
                )
            else:
                print(f"'{k}' does not exist on the Driverless AI server.")
        return dst_paths

    def list(self) -> List[str]:
        """List of interpretation artifacts that exist on the Driverless AI server."""
        return [k for k, v in self._paths.items() if v]


class InterpretationMethods:
    """Methods for retrieving different interpretation types on the
    Driverless AI server."""

    def __init__(
        self,
        client: "_core.Client",
        list_method: Callable[[int, int], Any],
        update_method: Callable[[str], Any],
        url_method: Callable[[Interpretation], str],
    ):
        self._client = client
        self._list = list_method
        self._update = update_method
        self._url_method = url_method

    def _lazy_get(self, key: str) -> "Interpretation":
        """Initialize an Interpretation object but don't request information
        from the server (possible for interpretation key to not exist on server).
        Useful for populating lists without making a bunch of network calls.

        Args:
            key: Driverless AI server's unique ID for the MLI interpretation
        """
        return Interpretation(self._client, key, self._update, self._url_method)

    def get(self, key: str) -> "Interpretation":
        """Get an Interpretation object corresponding to a MLI interpretation
        on the Driverless AI server.

        Args:
            key: Driverless AI server's unique ID for the MLI interpretation
        """
        interpretation = self._lazy_get(key)
        interpretation._update()
        return interpretation

    def list(
        self, start_index: int = 0, count: int = None
    ) -> Sequence["Interpretation"]:
        """List of Interpretation objects available to the user.

        Args:
            start_index: index on Driverless AI server of first interpretation to list
            count: max number of interpretations to request from the
                Driverless AI server
        """
        if count:
            data = self._list(start_index, count)
        else:
            page_size = 100
            page_position = start_index
            data = []
            while True:
                page = self._list(page_position, page_size)
                data += page
                if len(page) < page_size:
                    break
                page_position += page_size
        return _utils.ServerObjectList(
            data=data,
            get_method=self._lazy_get,
            item_class_name=Interpretation.__name__,
        )


class IIDMethods(InterpretationMethods):
    pass


class TimeseriesMethods(InterpretationMethods):
    pass


class MLI:
    """Interact with MLI interpretations on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client
        self._default_interpretation_settings = {}
        if hasattr(client._backend, "get_mli_config_options"):
            self._default_interpretation_settings = {
                c.name: c.val for c in client._backend.get_mli_config_options()
            }
        for setting in client._backend.get_all_config_options():
            if "mli" in setting.tags:
                name = setting.name.strip()
                if name.startswith("mli_"):
                    name = name[4:]
                self._default_interpretation_settings[name] = setting.val
        # legacy settings that should still be accepted
        self._default_legacy_interpretation_settings = {
            "sample_num_rows": -1,
            "dt_tree_depth": 3,
            "klime_cluster_col": "",
            "qbin_cols": [],
            "dia_cols": [],
            "pd_features": None,
            "debug_model_errors": False,
            "debug_model_errors_class": "False",
        }
        interpretation_url_path = getattr(
            self._client._backend, "interpretation_url_path", "/#/interpret_next"
        )
        ts_interpretation_url_path = getattr(
            self._client._backend, "ts_interpretation_url_path", "/mli-ts"
        )
        self._iid = IIDMethods(
            client=client,
            list_method=lambda x, y: client._backend.list_interpretations(x, y).items,
            update_method=client._backend.get_interpretation_job,
            url_method=lambda x: (
                f"{self._client.server.address}"
                f"{interpretation_url_path}"
                f"?interpret_key={x.key}"
            ),
        )
        self._timeseries = TimeseriesMethods(
            client=client,
            list_method=client._backend.list_interpret_timeseries,
            update_method=client._backend.get_interpret_timeseries_job,
            url_method=lambda x: (
                f"{self._client.server.address}"
                f"{ts_interpretation_url_path}"
                f"?model={x._get_raw_info().entity.parameters.dai_model.key}"
                f"&interpret_key={x.key}"
            ),
        )
        # convert setting name from key to value
        self._setting_for_server_dict = {
            "target_column": "target_col",
            "prediction_column": "prediction_col",
            "weight_column": "weight_col",
            "drop_columns": "drop_cols",
            "klime_cluster_column": "klime_cluster_col",
            "dia_columns": "dia_cols",
            "qbin_columns": "qbin_cols",
        }
        self._setting_for_api_dict = {
            v: k for k, v in self._setting_for_server_dict.items()
        }

    @property
    def iid(self) -> IIDMethods:
        """Retrieve IID interpretations."""
        return self._iid

    @property
    def timeseries(self) -> TimeseriesMethods:
        """Retrieve timeseries interpretations."""
        return self._timeseries

    def _common_dai_explainer_params(
        self,
        experiment_key: str,
        target_column: str,
        dataset_key: str,
        validation_dataset_key: str = "",
        test_dataset_key: str = "",
        **kwargs: Any,
    ) -> Any:
        return self._client._server_module.messages.CommonDaiExplainerParameters(
            common_params=self._client._server_module.CommonExplainerParameters(
                target_col=target_column,
                weight_col=kwargs.get("weight_col", ""),
                prediction_col=kwargs.get("prediction_col", ""),
                drop_cols=kwargs.get("drop_cols", []),
                sample_num_rows=kwargs.get("sample_num_rows", -1),
            ),
            model=self._client._server_module.ModelReference(experiment_key),
            dataset=self._client._server_module.DatasetReference(dataset_key),
            validset=self._client._server_module.DatasetReference(
                validation_dataset_key
            ),
            testset=self._client._server_module.DatasetReference(test_dataset_key),
            use_raw_features=kwargs["use_raw_features"],
            config_overrides=kwargs["config_overrides"],
            sequential_execution=True,
            debug_model_errors=kwargs.get("debug_model_errors", False),
            debug_model_errors_class=kwargs.get("debug_model_errors_class", "False"),
        )

    def _create_iid_interpretation_async(
        self,
        experiment: Optional[_experiments.Experiment] = None,
        explainers: Optional[List[_recipes.ExplainerRecipe]] = None,
        dataset: Optional[_datasets.Dataset] = None,
        **kwargs: Any,
    ) -> str:
        if experiment and not dataset:
            dataset_key = experiment.datasets["train_dataset"].key
            experiment_key = experiment.key
            target_column = experiment.settings["target_column"]
        elif experiment and dataset:
            dataset_key = dataset.key
            experiment_key = experiment.key
            target_column = experiment.settings["target_column"]
        elif not experiment and dataset:
            dataset_key = dataset.key
            experiment_key = ""
            target_column = kwargs.get("target_col", None)
        else:
            raise ValueError("Must provide an experiment or dataset to run MLI.")
        interpret_params = self._client._server_module.InterpretParameters(
            dai_model=self._client._server_module.ModelReference(experiment_key),
            dataset=self._client._server_module.DatasetReference(dataset_key),
            testset=self._client._server_module.DatasetReference(""),  # timeseries only
            target_col=target_column,
            prediction_col=kwargs.get("prediction_col", ""),
            weight_col=kwargs.get("weight_col", ""),
            drop_cols=kwargs.get("drop_cols", []),
            # expert settings
            lime_method=kwargs["lime_method"],
            use_raw_features=kwargs["use_raw_features"],
            sample=kwargs["sample"],
            dt_tree_depth=kwargs.get("dt_tree_depth", 3),
            vars_to_pdp=kwargs["vars_to_pdp"],
            nfolds=kwargs["nfolds"],
            qbin_count=kwargs["qbin_count"],
            sample_num_rows=kwargs.get("sample_num_rows", -1),
            klime_cluster_col=kwargs.get("klime_cluster_col", ""),
            dia_cols=kwargs.get("dia_cols", []),
            qbin_cols=kwargs.get("qbin_cols", []),
            debug_model_errors=kwargs.get("debug_model_errors", False),
            debug_model_errors_class=kwargs.get("debug_model_errors_class", "False"),
            config_overrides=kwargs["config_overrides"],
        )
        if not explainers:
            return self._client._backend.run_interpretation(interpret_params)
        else:
            params = self._common_dai_explainer_params(
                experiment_key=experiment_key,
                target_column=target_column,
                dataset_key=dataset_key,
                **kwargs,
            )
            return self._client._backend.run_interpretation_with_explainers(
                explainers=[
                    self._client._server_module.messages.Explainer(
                        e.id, json.dumps(e.settings)
                    )
                    for e in explainers
                ],
                params=params,
                interpret_params=interpret_params,
                display_name="",
            ).mli_key

    def _create_timeseries_interpretation_async(
        self,
        experiment: _experiments.Experiment,
        explainers: Optional[List[_recipes.ExplainerRecipe]] = None,
        dataset: Optional[_datasets.Dataset] = None,
        test_dataset: Optional[_datasets.Dataset] = None,
        **kwargs: Any,
    ) -> str:
        dataset_key = experiment.datasets["train_dataset"].key
        experiment_key = experiment.key
        target_column = experiment.settings["target_column"]
        if dataset:
            dataset_key = dataset.key
        if test_dataset:
            test_dataset_key = test_dataset.key
        else:
            test_dataset_key = (
                experiment.datasets["test_dataset"].key
                if experiment.datasets["test_dataset"]
                else ""
            )
        interpret_params = self._client._server_module.InterpretParameters(
            dataset=self._client._server_module.ModelReference(dataset_key),
            dai_model=self._client._server_module.ModelReference(experiment_key),
            testset=self._client._server_module.DatasetReference(test_dataset_key),
            target_col=target_column,
            use_raw_features=None,
            prediction_col=None,
            weight_col=None,
            drop_cols=None,
            klime_cluster_col=None,
            nfolds=None,
            sample=None,
            qbin_cols=None,
            qbin_count=None,
            lime_method=None,
            dt_tree_depth=None,
            vars_to_pdp=None,
            dia_cols=None,
            debug_model_errors=False,
            debug_model_errors_class="",
            sample_num_rows=kwargs.get("sample_num_rows", -1),
            config_overrides="",
        )
        if not explainers:
            return self._client._backend.run_interpret_timeseries(interpret_params)
        else:
            params = self._common_dai_explainer_params(
                experiment_key=experiment_key,
                target_column=target_column,
                dataset_key=dataset_key,
                test_dataset_key=test_dataset_key,
                **kwargs,
            )
            return self._client._backend.run_interpretation_with_explainers(
                explainers=[
                    self._client._server_module.messages.Explainer(
                        e.id, json.dumps(e.settings)
                    )
                    for e in explainers
                ],
                params=params,
                interpret_params=interpret_params,
                display_name="",
            ).mli_key

    def _parse_server_settings(self, server_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Driverless AI server interpretation settings to Python API format."""
        blacklist = ["config_overrides", "dai_model", "dataset", "testset"]
        settings: Dict[str, Any] = {}
        if server_settings.get("testset", None) and server_settings["testset"].get(
            "key", ""
        ):
            try:
                settings["test_dataset"] = self._client.datasets.get(
                    server_settings["testset"]["key"]
                )
            except self._client._server_module.protocol.RemoteError:
                # assuming a key error means deleted dataset, if not the error
                # will still propagate to the user else where
                settings["test_dataset"] = server_settings["testset"]
        for key, value in server_settings.items():
            if (
                key not in blacklist
                and value not in [None, "", [], -1]
                and value != self._default_interpretation_settings.get(key)
            ):
                settings[self._setting_for_api_dict.get(key, key)] = value
        if "target_column" not in settings and server_settings["dai_model"]["key"]:
            settings["target_column"] = self._client.experiments.get(
                server_settings["dai_model"]["key"]
            ).settings["target_column"]
        return settings

    def create(
        self,
        experiment: Optional[_experiments.Experiment] = None,
        dataset: Optional[_datasets.Dataset] = None,
        name: Optional[str] = None,
        force: bool = False,
        **kwargs: Any,
    ) -> "Interpretation":
        """Create a MLI interpretation on the Driverless AI server and return
        a Interpretation object corresponding to the created interpretation.

        Args:
            experiment: experiment to interpret, will use training dataset if
                ``dataset`` not specified
            dataset: dataset to use for interpretation
                (if dataset includes target and prediction columns, then an
                experiment is not needed)
            name: display name for the interpretation
            force: create new interpretation even if interpretation with same
                name already exists

        Keyword Args:
            explainers (List[ExplainerRecipe]): list of explainer recipe objects
            test_dataset (Dataset): Dataset object (timeseries only)
            target_column (str): name of column in ``dataset``
            prediction_column (str): name of column in ``dataset``
            weight_column (str): name of column in ``dataset``
            drop_columns (List[str]): names of columns in ``dataset``

        .. note::
            Any expert setting can also be passed as a ``kwarg``.
            To search possible expert settings for your server version,
            use ``mli.search_expert_settings(search_term)``.
        """
        return self.create_async(experiment, dataset, name, force, **kwargs).result()

    def create_async(
        self,
        experiment: Optional[_experiments.Experiment] = None,
        dataset: Optional[_datasets.Dataset] = None,
        name: Optional[str] = None,
        force: bool = False,
        **kwargs: Any,
    ) -> "Interpretation":
        """Launch creation of a MLI interpretation on the Driverless AI server
        and return an Interpretation object to track the status.

        Args:
            experiment: experiment to interpret, will use training dataset if
                ``dataset`` not specified
            dataset: dataset to use for interpretation
                (if dataset includes target and prediction columns, then an
                experiment is not needed)
            name: display name for the interpretation
            force: create new interpretation even if interpretation with same
                name already exists

        Keyword Args:
            explainers (List[ExplainerRecipe]): list of explainer recipe objects
                (server versions >= 1.9.1)
            test_dataset (Dataset): Dataset object (timeseries only)
            target_column (str): name of column in ``dataset``
            prediction_column (str): name of column in ``dataset``
            weight_column (str): name of column in ``dataset``
            drop_columns (List[str]): names of columns in ``dataset``

        .. note::
            Any expert setting can also be passed as a ``kwarg``.
            To search possible expert settings for your server version,
            use ``mli.search_expert_settings(search_term)``.
        """
        if not force:
            _utils.error_if_interpretation_exists(self._client, name)
        explainers = kwargs.pop("explainers", None)
        if explainers is not None:
            _utils.check_server_support(
                client=self._client,
                minimum_server_version="1.9.1",
                parameter="explainers",
            )
        test_dataset = kwargs.pop("test_dataset", None)
        config_overrides = toml.loads(kwargs.pop("config_overrides", ""))
        settings: Dict[str, Any] = {
            "prediction_col": "",
            "weight_col": "",
            "drop_cols": [],
        }
        if not _utils.is_server_version_less_than(self._client, "1.10.0"):
            settings.update(self._default_legacy_interpretation_settings)
        settings.update(self._default_interpretation_settings)
        for setting, value in kwargs.items():
            server_setting = self._setting_for_server_dict.get(setting, setting)
            if server_setting not in settings:
                raise RuntimeError(f"'{setting}' MLI setting not recognized.")
            settings[server_setting] = value
        # add any expert settings to config_override that have to be config override
        config_overrides["mli_pd_features"] = kwargs.get(
            "pd_features", settings.get("pd_features", None)
        )
        if experiment:
            experiment_config_overrides = (
                experiment._get_raw_info().entity.parameters.config_overrides
            )
            experiment_config_overrides = toml.loads(experiment_config_overrides)
            experiment_config_overrides.update(config_overrides)
            config_overrides = experiment_config_overrides
        settings["config_overrides"] = toml.dumps(config_overrides)
        is_timeseries = bool(experiment.settings.get("time_column", ""))
        if is_timeseries and explainers is None:
            key = self._create_timeseries_interpretation_async(
                experiment, explainers, dataset, test_dataset, **settings
            )
            update_method = self.timeseries._update
            url_method = self.timeseries._url_method
        else:
            key = self._create_iid_interpretation_async(
                experiment, explainers, dataset, **settings
            )
            update_method = self.iid._update
            url_method = self.iid._url_method
        interpretation = Interpretation(self._client, key, update_method, url_method)
        if name:
            interpretation.rename(name)
        return interpretation

    def gui(self) -> _utils.Hyperlink:
        """Print full URL for the user's MLI page on Driverless AI server."""
        return _utils.Hyperlink(
            f"{self._client.server.address}{self._client._gui_sep}interpretations"
        )

    def search_expert_settings(
        self, search_term: str, show_description: bool = False
    ) -> None:
        """Search expert settings and print results. Useful when looking for
        kwargs to use when creating interpretations.

        Args:
            search_term: term to search for (case insensitive)
            show_description: include description in results
        """
        if hasattr(self._client._backend, "get_mli_config_options"):
            mli_config_options = self._client._backend.get_mli_config_options()
        else:
            mli_config_options = []
        for c in self._client._backend.get_all_config_options() + mli_config_options:
            if (
                "mli" in c.tags
                and search_term.lower()
                in " ".join([c.name, c.category, c.description, c.comment]).lower()
            ):
                name = c.name
                if name.startswith("mli_"):
                    name = name[4:]
                print(
                    self._setting_for_api_dict.get(name, name),
                    "|",
                    "default_value:",
                    self._default_interpretation_settings[name.strip()],
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
