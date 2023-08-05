"""Projects module of official Python client for Driverless AI."""

from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence

from driverlessai import _core
from driverlessai import _datasets
from driverlessai import _experiments
from driverlessai import _utils


class Project(_utils.ServerObject):
    """Interact with a project on the Driverless AI server."""

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)
        self._dataset_types = {
            "test_dataset": "Testing",
            "test_datasets": "Testing",
            "train_dataset": "Training",
            "train_datasets": "Training",
            "validation_dataset": "Validation",
            "validation_datasets": "Validation",
        }
        self._datasets: Optional[Dict[str, Sequence[_datasets.Dataset]]] = None
        self._experiments: Optional[_utils.ServerObjectList] = None

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_project(self.key))
        self._set_name(self._get_raw_info().name)
        self._datasets = {
            "test_datasets": _utils.ServerObjectList(
                data=self._client._backend.get_datasets_for_project(
                    project_key=self.key,
                    dataset_type=self._dataset_types["test_dataset"],
                ),
                get_method=self._client.datasets.get,
                item_class_name=_datasets.Dataset.__name__,
            ),
            "train_datasets": _utils.ServerObjectList(
                data=self._client._backend.get_datasets_for_project(
                    project_key=self.key,
                    dataset_type=self._dataset_types["train_dataset"],
                ),
                get_method=self._client.datasets.get,
                item_class_name=_datasets.Dataset.__name__,
            ),
            "validation_datasets": _utils.ServerObjectList(
                data=self._client._backend.get_datasets_for_project(
                    project_key=self.key,
                    dataset_type=self._dataset_types["validation_dataset"],
                ),
                get_method=self._client.datasets.get,
                item_class_name=_datasets.Dataset.__name__,
            ),
        }
        self._experiments = _utils.ServerObjectList(
            data=[
                x.summary
                for x in self._client._backend.list_project_experiments(
                    project_key=self.key
                ).model_summaries
            ],
            get_method=self._client.experiments.get,
            item_class_name=_experiments.Experiment.__name__,
        )

    @property
    def datasets(self) -> Dict[str, Sequence[_datasets.Dataset]]:
        """Datasets linked to the project."""
        self._update()
        return self._datasets

    @property
    def description(self) -> Optional[str]:
        """Project description."""
        return self._get_raw_info().description or None

    @property
    def experiments(self) -> Sequence["_experiments.Experiment"]:
        """Experiments linked to the project."""
        self._update()
        return self._experiments

    @property
    def sharings(self) -> List[Dict[str, Optional[str]]]:
        """Users the project is shared with. Requires server versions >= 1.9.3
        with H2O.ai Storage connected.
        """
        _utils.check_server_support(
            client=self._client,
            minimum_server_version="1.9.3",
            parameter="sharings",
        )
        sharings = []
        for sharing in self._client._backend.list_project_sharings(self.key):
            username = _utils.get_storage_user_name(self._client, sharing.user_id)
            try:
                role = _utils.get_storage_role_name(
                    self._client, sharing.restriction_role_id
                )
            except RuntimeError:
                # Owner role is not listed
                role = None
            sharings.append({"username": username, "role": role})
        return sharings

    def delete(self) -> None:
        """Permanently delete project from the Driverless AI server."""
        key = self.key
        self._client._backend.delete_project(key)
        print(f"Driverless AI Server reported project {key} deleted.")

    def gui(self) -> _utils.Hyperlink:
        """Get full URL for the project's page on the Driverless AI server."""
        return _utils.Hyperlink(
            f"{self._client.server.address}{self._client._gui_sep}"
            f"project?projectKey={self.key}"
        )

    def link_dataset(
        self,
        dataset: _datasets.Dataset,
        dataset_type: str,
        link_associated_experiments: bool = False,
    ) -> "Project":
        """Link a dataset to the project.

        Args:
            dataset: a Dataset object corresonding to a dataset on the
                Driverless AI server
            dataset_type: can be one of: ``'train_dataset(s)'``,
                ``'validation_dataset(s)'``, or ``'test_dataset(s)'``
            link_associated_experiments: also link experiments that used the dataset
                (server versions >= 1.9.1)
        """
        if link_associated_experiments:
            _utils.check_server_support(
                client=self._client,
                minimum_server_version="1.9.1",
                parameter="link_associated_experiments",
            )
        self._client._backend.link_dataset_to_project(
            project_key=self.key,
            dataset_key=dataset.key,
            dataset_type=self._dataset_types[dataset_type],
            link_dataset_experiments=link_associated_experiments,
        )
        self._update()
        return self

    def link_experiment(self, experiment: "_experiments.Experiment") -> "Project":
        """Link an experiment to the project.

        Args:
            experiment: an Experiment object corresonding to a experiment on the
                Driverless AI server
        """
        self._client._backend.link_experiment_to_project(
            project_key=self.key, experiment_key=experiment.key
        )
        self._update()
        return self

    def rename(self, name: str) -> "Project":
        """Change project display name.

        Args:
            name: new display name
        """
        self._client._backend.update_project_name(self.key, name)
        self._update()
        return self

    def redescribe(self, description: str) -> "Project":
        """Change project description. Requires server version >= 1.9.1.

        Args:
            description: new description
        """
        _utils.check_server_support(
            client=self._client,
            minimum_server_version="1.9.1",
            parameter="redescribe",
        )
        self._client._backend.update_project_description(self.key, description)
        self._update()
        return self

    def share(self, username: str, role: str = "Default") -> None:
        """Share a project. Requires server versions >= 1.9.3 with H2O.ai
        Storage connected.

        Args:
            username: Driverless AI username of user to share with
            role: one of "Default" or "Reader"
        """
        _utils.check_server_support(
            client=self._client,
            minimum_server_version="1.9.3",
            parameter="share",
        )
        self._client._backend.share_project(
            project_id=self.key,
            user_id=_utils.get_storage_user_id(self._client, username),
            restriction_role_id=_utils.get_storage_role_id(self._client, role),
        )

    def unlink_dataset(
        self, dataset: _datasets.Dataset, dataset_type: str
    ) -> "Project":
        """Unlink a dataset from the project.

        Args:
            dataset: a Dataset object corresonding to a dataset on the
                Driverless AI server
            dataset_type: can be one of: ``'train_dataset(s)'``,
                ``'validation_dataset(s)'``, or ``'test_dataset(s)'``
        """
        self._client._backend.unlink_dataset_from_project(
            project_key=self.key,
            dataset_key=dataset.key,
            dataset_type=self._dataset_types[dataset_type],
        )
        self._update()
        return self

    def unlink_experiment(self, experiment: "_experiments.Experiment") -> "Project":
        """Unlink an experiment from the project.

        Args:
            experiment: an Experiment object corresonding to a experiment on the
                Driverless AI server
        """
        self._client._backend.unlink_experiment_from_project(
            project_key=self.key, experiment_key=experiment.key
        )
        self._update()
        return self

    def unshare(self, username: str) -> None:
        """Unshare a project. Requires server versions >= 1.9.3 with H2O.ai
        Storage connected.

        Args:
            username: Driverless AI username of user to unshare with
        """
        _utils.check_server_support(
            client=self._client,
            minimum_server_version="1.9.3",
            parameter="unshare",
        )
        for sharing in self._client._backend.list_project_sharings(self.key):
            if (
                username == _utils.get_storage_user_name(self._client, sharing.user_id)
                and sharing.restriction_role_id
            ):
                self._client._backend.unshare_project(
                    project_id=self.key, sharing_id=sharing.id
                )
                return
        raise RuntimeError(f"Project share with '{username}' not found.")


class Projects:
    """Interact with projects on the Driverless AI server."""

    def __init__(self, client: "_core.Client"):
        self._client = client

    def create(
        self, name: str, description: Optional[str] = None, force: bool = False
    ) -> Project:
        """Create a project on the Driverless AI server.

        Args:
            name: display name for project
            description: description of project
            force: create new project even if project with same name already exists
        """
        if not force:
            _utils.error_if_project_exists(self._client, name)
        key = self._client._backend.create_project(name, description)
        return self.get(key)

    def get(self, key: str) -> Project:
        """Get a Project object corresponding to a project on the
        Driverless AI server.

        Args:
            key: Driverless AI server's unique ID for the project
        """
        return Project(self._client, key)

    def gui(self) -> _utils.Hyperlink:
        """Get full URL for the projects page on the Driverless AI server."""
        return _utils.Hyperlink(
            f"{self._client.server.address}{self._client._gui_sep}projects"
        )

    def list(self, start_index: int = 0, count: int = None) -> Sequence["Project"]:
        """List of Project objects available to the user.

        Args:
            start_index: index on Driverless AI server of first project in list
            count: number of projects to request from the Driverless AI server
        """
        if count:
            data = self._client._backend.list_projects(start_index, count).items
        else:
            page_size = 100
            page_position = start_index
            data = []
            while True:
                page = self._client._backend.list_projects(
                    page_position, page_size
                ).items
                data += page
                if len(page) < page_size:
                    break
                page_position += page_size
        return _utils.ServerObjectList(
            data=data, get_method=self.get, item_class_name=Project.__name__
        )
