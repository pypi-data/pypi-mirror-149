"""AutoViz module of official Python client for Driverless AI."""

from typing import Optional
from typing import Sequence

from driverlessai import _core
from driverlessai import _datasets
from driverlessai import _utils


class AutoViz:
    """Interact with dataset visualizations on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def create(self, dataset: _datasets.Dataset) -> "Visualization":
        """Create a dataset visualization on the Driverless AI server.

        Args:
            dataset: Dataset object
        """
        return self.create_async(dataset).result()

    def create_async(self, dataset: _datasets.Dataset) -> "Visualization":
        """Launch creation of a dataset visualization on the Driverless AI server.

        Args:
            dataset: Dataset object
        """
        key = self._client._backend.get_autoviz(dataset.key, maximum_number_of_plots=50)
        return Visualization(self._client, key)

    def get(self, key: str) -> "Visualization":
        """Get a Visualization object corresponding to a dataset visualization
        on the Driverless AI server.

        Args:
            key: Driverless AI server's unique ID for the visualization
        """
        return Visualization(self._client, key)

    def gui(self) -> _utils.Hyperlink:
        """Get full URL for the AutoViz page on the Driverless AI server."""
        return _utils.Hyperlink(
            f"{self._client.server.address}{self._client._gui_sep}visualizations"
        )

    def list(
        self, start_index: int = 0, count: int = None
    ) -> Sequence["Visualization"]:
        """Return list of dataset Visualization objects.

        Args:
            start_index: index on Driverless AI server of first visualization in list
            count: number of visualizations to request from the Driverless AI server
        """
        if count:
            data = self._client._backend.list_visualizations(start_index, count).items
        else:
            page_size = 100
            page_position = start_index
            data = []
            while True:
                page = self._client._backend.list_visualizations(
                    page_position, page_size
                ).items
                data += page
                if len(page) < page_size:
                    break
                page_position += page_size
        return _utils.ServerObjectList(
            data=data, get_method=self.get, item_class_name=Visualization.__name__
        )


class Visualization(_utils.ServerJob):
    """Interact with a dataset visualization on the Driverless AI server."""

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)
        self._dataset: Optional[_datasets.Dataset] = None

    @property
    def dataset(self) -> _datasets.Dataset:
        """Dataset that was visualized."""
        if self._dataset is None:
            try:
                self._dataset = self._client.datasets.get(
                    self._get_raw_info().dataset.key
                )
            except self._client._server_module.protocol.RemoteError:
                # assuming a key error means deleted dataset, if not the error
                # will still propagate to the user else where
                self._dataset = self._get_raw_info().dataset.dump()
        return self._dataset

    @property
    def is_deprecated(self) -> Optional[bool]:
        """``True`` if visualization was created by an old version of
        Driverless AI and is no longer fully compatible with the current
        server version."""
        return getattr(self._get_raw_info(), "deprecated", None)

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'> {self.key} {self.name}"

    def __str__(self) -> str:
        return f"{self.name} ({self.key})"

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_autoviz_job(self.key))
        self._set_name(self._get_raw_info().name)

    def delete(self) -> None:
        """Permanently delete visualization from the Driverless AI server."""
        key = self.key
        self._client._backend.delete_autoviz_job(key)
        print("Driverless AI Server reported visualization {key} deleted.")

    def gui(self) -> _utils.Hyperlink:
        """Get full URL for the visualization's page on the Driverless AI server."""
        return _utils.Hyperlink(
            f"{self._client.server.address}{self._client._gui_sep}"
            f"auto_viz?&datasetKey={self._get_raw_info().dataset.key}"
            f"&dataset_name={self._get_raw_info().dataset.display_name}"
        )

    def result(self, silent: bool = False) -> "Visualization":
        """Wait for job to complete, then return self.

        Args:
            silent: if True, don't display status updates
        """
        self._wait(silent)
        return self
