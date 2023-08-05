"Datasets module of official Python client for Driverless AI." ""

import ast
import os
import re
import tempfile
import time
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import TYPE_CHECKING
from typing import Union

from driverlessai import _core
from driverlessai import _recipes
from driverlessai import _utils


if TYPE_CHECKING:
    import fsspec  # noqa F401
    import pandas  # noqa F401


class Connectors:
    """Interact with data sources that are enabled on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def list(self) -> List[str]:
        """Return list of data sources enabled on the Driverless AI server.

        Examples::

            dai.connectors.list()
        """
        return self._client._backend.list_allowed_file_systems(0, None)


class DataPreviewJob(_utils.ServerJob):
    """Monitor generation of a data preview on the Driverless AI server."""

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_data_preview_job(self.key))

    def result(self, silent: bool = False) -> "DataPreviewJob":
        """Wait for job to complete, then return self.

        Args:
            silent: if True, don't display status updates
        """
        self._wait(silent)
        return self

    def status(self, verbose: int = None) -> str:
        """Return short job status description string."""
        return self._status().message


class Dataset(_utils.ServerObject):
    """Interact with a dataset on the Driverless AI server.

    Examples::

        # Import the iris dataset
        ds = dai.datasets.create(
                data='s3://h2o-public-test-data/smalldata/iris/iris.csv',
                data_source='s3'
        )

        ds.columns
        ds.data_source
        ds.file_path
        ds.file_size
        ds.key
        ds.name
        ds.shape
    """

    def __init__(self, client: "_core.Client", info: Any) -> None:
        super().__init__(client=client, key=info.entity.key)
        self._columns = [c.name for c in info.entity.columns]
        self._logical_types = {
            "categorical": "cat",
            "date": "date",
            "datetime": "datetime",
            "image": "image",
            "id": "id",
            "numerical": "num",
            "text": "text",
        }
        self._shape = (info.entity.row_count, len(info.entity.columns))
        self._set_name(info.entity.name)
        self._set_raw_info(info)

    @property
    def columns(self) -> List[str]:
        """List of column names."""
        return self._columns

    @property
    def creation_timestamp(self) -> float:
        """Creation timestamp in seconds since the epoch (POSIX timestamp)."""
        return self._get_raw_info().created

    @property
    def data_source(self) -> str:
        """Original source of data."""
        return self._get_raw_info().entity.data_source

    @property
    def file_path(self) -> str:
        """Path to dataset bin file on the server."""
        return self._get_raw_info().entity.bin_file_path

    @property
    def file_size(self) -> int:
        """Size in bytes of dataset bin file on the server."""
        return self._get_raw_info().entity.file_size

    @property
    def shape(self) -> Tuple[int, int]:
        """Dimensions (rows, cols)."""
        return self._shape

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'> {self.key} {self.name}"

    def __str__(self) -> str:
        return f"{self.name} ({self.key})"

    def _create_csv_on_server(self) -> str:
        job = self._client._backend.create_csv_from_dataset(self.key)
        while _utils.is_server_job_running(
            self._client._backend.get_create_csv_job(job).status.status
        ):
            time.sleep(1)
        finished_job = self._client._backend.get_create_csv_job(job)
        if not _utils.is_server_job_complete(finished_job.status.status):
            raise RuntimeError(
                self._client._backend._format_server_error(finished_job.status.error)
            )
        return finished_job.url

    # NOTE get_raw_data is not stable!
    def _get_data(
        self, start: int = 0, num_rows: int = None
    ) -> List[List[Union[bool, float, str]]]:
        """Retrieve data as a list.

        Args:
            start: index of first row to include
            num_rows: number of rows to include
        """
        num_rows = num_rows or self.shape[0]
        return self._client._backend.get_raw_data(self.key, start, num_rows).rows

    def _import_modified_datasets(
        self, recipe_job: _recipes.RecipeJob
    ) -> List["Dataset"]:
        data_files = recipe_job.result(silent=True)._get_raw_info().entity.data_files
        keys = [self._client._backend.create_dataset_from_recipe(f) for f in data_files]
        datasets = [
            DatasetJob(self._client, key, name=key).result(silent=True) for key in keys
        ]
        return datasets

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_dataset_job(self.key))
        self._set_name(self._get_raw_info().entity.name)

    def column_summaries(
        self, columns: List[str] = None
    ) -> "DatasetColumnSummaryCollection":
        """Returns a collection of column summaries.

        The collection can be indexed by number or column name:

        - ``dataset.column_summaries()[0]``
        - ``dataset.column_summaries()[0:3]``
        - ``dataset.column_summaries()['C1']``

        A column summary has the following attributes:

        - ``count``: count of non-missing values
        - ``data_type``: raw data type detected by Driverless AI
          when the data was imported
        - ``datetime_format``: user defined datetime format to be used by Driverless AI
          (see ``dataset.set_datetime_format()``)
        - ``freq``: count of most frequent value
        - ``logical_types``: list of user defined data types to be used by Driverless AI
          (overrides ``data_type``, also see ``dataset.set_logical_types()``)
        - ``max``: maximum value for numeric data
        - ``mean``: mean of values for numeric data
        - ``min``: minimum value for numeric data
        - ``missing``: count of missing values
        - ``name``: column name
        - ``sd``: standard deviation of values for numeric data
        - ``unique``: count of unique values

        Printing the collection or an individual summary displays a histogram
        along with summary information, like so::

            --- C1 ---

             4.3|███████
                |█████████████████
                |██████████
                |████████████████████
                |████████████
                |███████████████████
                |█████████████
                |████
                |████
             7.9|████

            Data Type: real
            Logical Types: ['categorical', 'numerical']
            Datetime Format:
            Count: 150
            Missing: 0
            Mean: 5.84
            SD: 0.828
            Min: 4.3
            Max: 7.9
            Unique: 35
            Freq: 10

        Args:
            columns: list of column names to include in the collection

        Examples::

            # Import the iris dataset
            ds = dai.datasets.create(
                data='s3://h2o-public-test-data/smalldata/iris/iris.csv',
                data_source='s3'
            )

            # print column summary for the first three columns
            print(ds.column_summaries()[0:3])
        """
        return DatasetColumnSummaryCollection(self, columns=columns)

    def delete(self) -> None:
        """Delete dataset on Driverless AI server.

        Examples::

            # Import the iris dataset
            ds = dai.datasets.create(
                data='s3://h2o-public-test-data/smalldata/iris/iris.csv',
                data_source='s3'
            )

            ds.delete()
        """
        key = self.key
        self._client._backend.delete_dataset(key)
        print(f"Driverless AI Server reported dataset {key} deleted.")

    def download(
        self,
        dst_dir: str = ".",
        dst_file: Optional[str] = None,
        file_system: Optional["fsspec.spec.AbstractFileSystem"] = None,
        overwrite: bool = False,
    ) -> str:
        """Download dataset from Driverless AI server as a csv.

        Args:
            dst_dir: directory where csv will be saved
            dst_file: name of csv file (overrides default file name)
            file_system: FSSPEC based file system to download to,
                instead of local file system
            overwrite: overwrite existing file

        Examples::

            # Import the iris dataset
            ds = dai.datasets.create(
                data='s3://h2o-public-test-data/smalldata/iris/iris.csv',
                data_source='s3'
            )

            ds.download()
        """
        # _download adds <address>/files/ to start of all paths
        path = re.sub("^.*?/files/", "", self._create_csv_on_server())
        return self._client._download(
            server_path=path,
            dst_dir=dst_dir,
            dst_file=dst_file,
            file_system=file_system,
            overwrite=overwrite,
        )

    def export(self, **kwargs: Any) -> str:
        """Export dataset csv from the Driverless AI server. Returns
        a relative path for the exported csv.

        .. note::
            Export location is configured on the Driverless AI server.
        """
        self._update()
        model_key = "data_set"
        artifact_path = self._create_csv_on_server()
        artifact_file_name = f"{self.name}.csv"
        export_location = self._client._backend.list_experiment_artifacts(
            model_key=model_key,
            storage_destination=kwargs.get("storage_destination", ""),
        ).location
        job_key = self._client._backend.upload_experiment_artifacts(
            model_key=model_key,
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
            self._client, job_key, artifact_path, artifact_file_name, export_location
        ).result()
        return str(Path(export_location, artifact_file_name))

    def head(self, num_rows: int = 5) -> _utils.Table:
        """Return headers and first n rows of dataset in a Table.

        Args:
            num_rows: number of rows to show

        Examples::

            # Load in the iris dataset
            ds = dai.datasets.create(
                data='s3://h2o-public-test-data/smalldata/iris/iris.csv',
                data_source='s3'
            )

            # Print the headers and first 5 rows
            print(ds.head(num_rows=5))
        """
        data = self._get_data(0, num_rows)
        return _utils.Table(data, self.columns)

    def modify_by_code(
        self, code: str, names: List[str] = None
    ) -> Dict[str, "Dataset"]:
        """Create a dictionary of new datasets from original dataset modified by
        a Python ``code`` string, that is the body of a function where:
            - there is an input variable ``X`` that represents the original dataset
              in the form of a datatable frame (dt.Frame)
            - return type is one of dt.Frame, pd.DataFrame, np.ndarray or a list
              of those

        Args:
            code: Python code that modifies ``X``
            names: optional list of names for the new dataset(s)

        Examples::

            # Import the iris dataset
            ds = dai.datasets.create(
                data='s3://h2o-public-test-data/smalldata/iris/iris.csv',
                data_source='s3'
            )

            # Keep the first 4 columns
            new_dataset = ds.modify_by_code(
                'return X[:, :4]', names=['new_dataset']
            )

            # Split on 4th column
            new_datasets = ds.modify_by_code(
                'return [X[:, :4], X[:, 4:]]',
                names=['new_dataset_1', 'new_dataset_2']
            )

        The dictionary will map the dataset ``names`` to the returned element(s)
        from the Python ``code`` string.
        """
        status_update = _utils.StatusUpdate()
        status_update.display(
            f"{_utils.JobStatus.RUNNING.message} - Modifying '{self.name}' into "
            "new dataset(s)..."
        )
        # Add recipe to server and get path to recipe file on server
        key = self._client._backend.get_data_recipe_preview(
            dataset_key=self.key,
            code=code,
            live_code=code,
            full_recipe_code=None,
            custom_recipe_key=None,
        )
        completed_preview_job = DataPreviewJob(self._client, key).result(silent=True)
        # Modify the dataset with recipe
        key = self._client._backend.modify_dataset_by_recipe_file(
            completed_preview_job._get_raw_info().dataset_key,
            completed_preview_job._get_raw_info().recipe_path,
        )
        completed_recipe_job = _recipes.RecipeJob(self._client, key).result(silent=True)
        # Add the new datasets to DAI
        status_update.display(
            f"{_utils.JobStatus.RUNNING.message} - Importing datasets..."
        )
        datasets = self._import_modified_datasets(completed_recipe_job)
        for i, d in enumerate(datasets):
            d.rename(f"{i + 1}.{self.name}")
        status_update.display(_utils.JobStatus.COMPLETE.message)
        status_update.end()
        if names is not None:
            if len(set(names)) != len(datasets):
                raise ValueError(
                    "Number of unique names doesn't match number of new datasets."
                )
            for i, name in enumerate(names):
                datasets[i].rename(name)
        return {d.name: d for d in datasets}

    def modify_by_code_preview(self, code: str) -> _utils.Table:
        """Get a preview of the dataset modified by a Python ``code`` string,
        where:
            - there exists a variable ``X`` that represents the original dataset
              in the form of a datatable frame (dt.Frame)
            - return type is one of dt.Frame, pd.DataFrame, np.ndarray or a list
              of those (only first element of the list is shown in preview)

        Args:
            code: Python code that modifies ``X``

        Examples::

            # Import the iris dataset
            ds = dai.datasets.create(
                data='s3://h2o-public-test-data/smalldata/iris/iris.csv',
                data_source='s3'
            )

            # Keep first 4 columns
            ds.modify_by_code_preview('return X[:, :4]')
        """
        key = self._client._backend.get_data_recipe_preview(
            dataset_key=self.key,
            code=code,
            live_code=code,
            full_recipe_code=None,
            custom_recipe_key=None,
        )
        completed_job = DataPreviewJob(self._client, key).result()
        return _utils.Table(
            completed_job._get_raw_info().entity.rows[:10],
            completed_job._get_raw_info().entity.headers,
        )

    def modify_by_recipe(
        self, recipe: str, names: List[str] = None
    ) -> Dict[str, "Dataset"]:
        """Create a dictionary of new datasets from original dataset modified by
        a recipe.

        The dictionary will map the dataset ``names`` to the returned element(s)
        from the recipe.

        Args:
            recipe: path to recipe or url for recipe
            names: optional list of names for the new dataset(s)

        Examples::

            # Import the airlines dataset
            ds = dai.datasets.create(
                data='s3://h2o-public-test-data/smalldata/airlines/allyears2k_headers.zip',
                data_source='s3'
            )

            # Modify original dataset with a recipe
            new_ds = ds.modify_by_recipe(
                recipe='https://github.com/h2oai/driverlessai-recipes/blob/rel-1.8.4/data/airlines_multiple.py',
                names=['new_airlines1', 'new_airlines2']
            )
        """
        status_update = _utils.StatusUpdate()
        status_update.display(
            f"{_utils.JobStatus.RUNNING.message} - Modifying '{self.name}' into "
            "new dataset(s)..."
        )
        if re.match("^http[s]?://", recipe):
            key = self._client._backend.modify_dataset_by_recipe_url(self.key, recipe)
        else:
            # Add recipe file to server
            path = self._client._backend.perform_upload(recipe, skip_parse=True)[0]
            key = self._client._backend.modify_dataset_by_recipe_file(self.key, path)
        completed_recipe_job = _recipes.RecipeJob(self._client, key).result(silent=True)
        # Add the new datasets to DAI
        status_update.display(
            f"{_utils.JobStatus.RUNNING.message} - Importing datasets..."
        )
        datasets = self._import_modified_datasets(completed_recipe_job)
        for i, d in enumerate(datasets):
            d.rename(f"{i + 1}.{self.name}")
        status_update.display(_utils.JobStatus.COMPLETE.message)
        status_update.end()
        if names is not None:
            if len(set(names)) != len(datasets):
                raise ValueError(
                    "Number of unique names doesn't match number of new datasets."
                )
            for i, name in enumerate(names):
                datasets[i].rename(name)
        return {d.name: d for d in datasets}

    def rename(self, name: str) -> "Dataset":
        """Change dataset display name.

        Args:
            name: new display name

        Examples::

            # Import the iris dataset
            ds = dai.datasets.create(
                data='s3://h2o-public-test-data/smalldata/iris/iris.csv',
                data_source='s3'
            )
            ds.name

            ds.rename(name='new-iris-name')
            ds.name
        """
        self._client._backend.update_dataset_name(self.key, name)
        self._update()
        return self

    def set_datetime_format(self, columns: Dict[str, str]) -> None:
        """Set datetime format of columns.

        Args:
            columns: dictionary where the key is the column name and
                the value is a valid datetime format

        Examples::

            # Import the Eurodate dataset
            date = dai.datasets.create(
                data='s3://h2o-public-test-data/smalldata/jira/v-11-eurodate.csv',
                data_source='s3'
            )

            # Set the date time format for column ‘ds5'
            date.set_datetime_format({'ds5': '%d-%m-%y %H:%M'})
        """
        for k, v in columns.items():
            if v is None:
                v = ""
            self._client._backend.update_dataset_col_format(self.key, k, v)
        self._update()

    def set_logical_types(self, columns: Dict[str, Union[str, List[str]]]) -> None:
        """Designate columns to have the specified logical types. The logical
        type is mainly used to determine which transformers to try on the
        column's data.

        Possible logical types:

        - ``'categorical'``
        - ``'date'``
        - ``'datetime'``
        - ``'id'``
        - ``'numerical'``
        - ``'text'``

        Args:
            columns: dictionary where the key is the column name and the value
                is the logical type or a list of logical types for the column
                (to unset all logical types use a value of ``None``)

        Example::

            # Import the prostate dataset
            prostate = dai.datasets.create(
                data='s3://h2o-public-test-data/smalldata/prostate/prostate.csv',
                data_source='s3'
            )

            # Set the logical types
            prostate.set_logical_types(
                {'ID': 'id', 'AGE': ['categorical', 'numerical'], 'RACE': None}
            )
        """
        for k, v in columns.items():
            if v is None:
                self._client._backend.update_dataset_col_logical_types(self.key, k, [])
            else:
                if isinstance(v, str):
                    v = [v]
                for lt in v:
                    if lt not in self._logical_types:
                        raise ValueError(
                            "Please use logical types from: "
                            + str(sorted(self._logical_types.keys()))
                        )
                self._client._backend.update_dataset_col_logical_types(
                    self.key, k, [self._logical_types[lt] for lt in v]
                )
        self._update()

    def split_to_train_test(
        self,
        train_size: float = 0.5,
        train_name: str = None,
        test_name: str = None,
        target_column: str = None,
        fold_column: str = None,
        time_column: str = None,
        seed: int = 1234,
    ) -> Dict[str, "Dataset"]:
        """Split a dataset into train/test sets on the Driverless AI server and
        return a dictionary of Dataset objects with the keys
        ``'train_dataset'`` and ``'test_dataset'``.

        Args:
            train_size: proportion of dataset rows to put in the train split
            train_name: name for the train dataset
            test_name: name for the test dataset
            target_column: use stratified sampling to create splits
            fold_column: keep rows belonging to the same group together
            time_column: split rows such that the splits are sequential with
                respect to time
            seed: random seed

        .. note:: Only one of ``target_column``, ``fold_column``, or ``time_column``
            can be passed at a time.

        Examples::

            # Import the iris dataset
            ds = dai.datasets.create(
                data='s3://h2o-public-test-data/smalldata/iris/iris.csv',
                data_source='s3'
            )

            # Split the iris dataset into train/test sets
            ds_split = ds.split_to_train_test(train_size=0.7)
        """
        return self.split_to_train_test_async(
            train_size,
            train_name,
            test_name,
            target_column,
            fold_column,
            time_column,
            seed,
        ).result()

    def split_to_train_test_async(
        self,
        train_size: float = 0.5,
        train_name: str = None,
        test_name: str = None,
        target_column: str = None,
        fold_column: str = None,
        time_column: str = None,
        seed: int = 1234,
    ) -> "DatasetSplitJob":
        """Launch creation of a dataset train/test split on the Driverless AI
        server and return a DatasetSplitJob object to track the status.

        Args:
            train_size: proportion of dataset rows to put in the train split
            train_name: name for the train dataset
            test_name: name for the test dataset
            target_column: use stratified sampling to create splits
            fold_column: keep rows belonging to the same group together
            time_column: split rows such that the splits are sequential with
                respect to time
            seed: random seed

        .. note:: Only one of ``target_column``, ``fold_column``, or ``time_column``
            can be passed at a time.

        Examples::

            # Import the iris dataset
            ds = dai.datasets.create(
                data='s3://h2o-public-test-data/smalldata/iris/iris.csv',
                data_source='s3'
            )

            # Launch the creation of a dataset train/test split on the DAI server
            ds_split = ds.split_to_train_test_async(train_size=0.7)
        """
        cols = [target_column, fold_column, time_column]
        if sum([1 for x in cols if x is not None]) > 1:
            raise ValueError("Only one column argument allowed.")
        # Don't pass names here since certain file extensions in the name
        # (like .csv) cause errors, rename inside DatasetSplitJob instead
        key = self._client._backend.make_dataset_split(
            dataset_key=self.key,
            output_name1=None,
            output_name2=None,
            target=target_column,
            fold_col=fold_column,
            time_col=time_column,
            ratio=train_size,
            seed=seed,
        )
        return DatasetSplitJob(self._client, key, train_name, test_name)

    def tail(self, num_rows: int = 5) -> _utils.Table:
        """Return headers and last n rows of dataset in a Table.

        Args:
            num_rows: number of rows to show

        Examples::

            ds = dai.datasets.create(
                data='s3://h2o-public-test-data/smalldata/iris/iris.csv',
                data_source='s3'
            )

            # Print the headers and last 5 rows
            print(ds.tail(num_rows=5))
        """
        data = self._get_data(self.shape[0] - num_rows, num_rows)
        return _utils.Table(data, self.columns)


class DatasetColumnSummary:
    """Information, statistics, and histogram for column data.

    Printing a summary displays a histogram along with summary information,
    like so::

        --- C1 ---

         4.3|███████
            |█████████████████
            |██████████
            |████████████████████
            |████████████
            |███████████████████
            |█████████████
            |████
            |████
         7.9|████

        Data Type: real
        Logical Types: ['categorical', 'numerical']
        Datetime Format:
        Count: 150
        Missing: 0
        Mean: 5.84
        SD: 0.828
        Min: 4.3
        Max: 7.9
        Unique: 35
        Freq: 10
    """

    def __init__(self, column_summary: Dict[str, Any]) -> None:
        self._column_summary = column_summary

    @property
    def count(self) -> int:
        """Count of non-missing values."""
        return self._column_summary["count"]

    @property
    def data_type(self) -> str:
        """Raw data type detected by Driverless AI when the data was imported."""
        return self._column_summary["data_type"]

    @property
    def datetime_format(self) -> str:
        """User defined datetime format to be used by Driverless AI
        (see ``dataset.set_datetime_format()``)."""
        return self._column_summary["datetime_format"]

    @property
    def freq(self) -> int:
        """Count of most frequent value."""
        return self._column_summary["freq"]

    @property
    def logical_types(self) -> List[str]:
        """List of user defined data types to be used by Driverless AI
        (overrides ``data_type``, also see ``dataset.set_logical_types()``)."""
        return self._column_summary["logical_types"]

    @property
    def max(self) -> Optional[Union[bool, float, int]]:
        """Maximum value for binary/numeric data."""
        return self._column_summary["max"]

    @property
    def mean(self) -> Optional[float]:
        """Mean of values for binary/numeric data."""
        return self._column_summary["mean"]

    @property
    def min(self) -> Optional[Union[bool, float, int]]:
        """Minimum value for binary/numeric data."""
        return self._column_summary["min"]

    @property
    def missing(self) -> int:
        """Count of missing values."""
        return self._column_summary["missing"]

    @property
    def name(self) -> str:
        """Column name."""
        return self._column_summary["name"]

    @property
    def sd(self) -> Optional[float]:
        """Standard deviation of values for binary/numeric data."""
        return self._column_summary["std"]

    @property
    def unique(self) -> int:
        """Count of unique values."""
        return self._column_summary["unique"]

    def __repr__(self) -> str:
        return f"<{self.name} Summary>"

    def __str__(self) -> str:
        s = [
            f"--- {self.name} ---\n",
            f"{self._column_summary['hist']}",
            f"Data Type: {self.data_type}",
            f"Logical Types: {self.logical_types!s}",
            f"Datetime Format: {self.datetime_format}",
            f"Count: {self.count!s}",
            f"Missing: {self.missing!s}",
        ]
        if self.mean not in [None, ""]:
            # mean/sd could be NaN
            s.append(
                f"Mean: {self.mean:{'0.3g' if _utils.is_number(self.mean) else ''}}"
            )
            s.append(f"SD: {self.sd:{'0.3g' if _utils.is_number(self.sd) else ''}}")
        if self.min not in [None, ""]:
            # min/max could be datetime string
            s.append(f"Min: {self.min:{'0.3g' if _utils.is_number(self.min) else ''}}")
            s.append(f"Max: {self.max:{'0.3g' if _utils.is_number(self.max) else ''}}")
        s.append(f"Unique: {self.unique!s}")
        s.append(f"Freq: {self.freq!s}")
        return "\n".join(s)


class DatasetColumnSummaryCollection:
    """Collection for storing and retrieving column summaries.

    The collection can be indexed by number or column name:

    - ``dataset.column_summaries()[0]``
    - ``dataset.column_summaries()[0:3]``
    - ``dataset.column_summaries()['C1']``

    Printing a collection displays a histogram along with summary information
    for all columns contained, like so::

        --- C1 ---

         4.3|███████
            |█████████████████
            |██████████
            |████████████████████
            |████████████
            |███████████████████
            |█████████████
            |████
            |████
         7.9|████

        Data Type: real
        Logical Types: ['categorical', 'numerical']
        Datetime Format:
        Count: 150
        Missing: 0
        Mean: 5.84
        SD: 0.828
        Min: 4.3
        Max: 7.9
        Unique: 35
        Freq: 10

    """

    def __init__(self, dataset: "Dataset", columns: List[str] = None):
        self._columns = columns or dataset.columns
        self._dataset = dataset
        self._update()

    def __getitem__(
        self, columns: Union[int, slice, str, List[str]]
    ) -> Union["DatasetColumnSummary", "DatasetColumnSummaryCollection"]:
        self._update()
        if isinstance(columns, str):
            return DatasetColumnSummary(self._column_summaries[columns])
        elif isinstance(columns, int):
            columns = self._columns[columns]
            return DatasetColumnSummary(self._column_summaries[columns])
        elif isinstance(columns, slice):
            columns = self._columns[columns]
        return DatasetColumnSummaryCollection(self._dataset, columns=columns)

    def __iter__(self) -> Iterable["DatasetColumnSummary"]:
        self._update()
        yield from [
            DatasetColumnSummary(self._column_summaries[c]) for c in self._columns
        ]

    def __repr__(self) -> str:
        string = "<"
        for c in self._columns[:-1]:
            string += "<" + c + " Summary>, "
        string += "<" + self._columns[-1] + " Summary>>"
        return string

    def __str__(self) -> str:
        string = ""
        for c in self._columns:
            string += str(DatasetColumnSummary(self._column_summaries[c])) + "\n"
        return string

    def _create_column_summary_dict(self, column: Any) -> Dict[str, Any]:
        summary = {}
        summary["name"] = column.name
        summary["data_type"] = column.data_type
        summary["logical_types"] = [
            k
            for k, v in self._dataset._logical_types.items()
            if v in column.logical_types
        ]
        summary["datetime_format"] = column.datetime_format
        if column.stats.is_numeric:
            stats = column.stats.numeric.dump()
        else:
            stats = column.stats.non_numeric.dump()
        summary["count"] = stats.get("count", 0)
        summary["missing"] = self._dataset.shape[0] - summary["count"]
        summary["mean"] = stats.get("mean", None)
        summary["std"] = stats.get("std", None)
        summary["min"] = stats.get("min", None)
        summary["max"] = stats.get("max", None)
        summary["unique"] = stats.get("unique")
        summary["freq"] = stats.get("freq")
        summary["hist"] = self._create_histogram_string(column)
        return summary

    def _create_histogram_string(self, column: Any) -> str:
        hist = ""
        block = chr(9608)
        if column.stats.is_numeric:
            ht = column.stats.numeric.hist_ticks
            if not ht:
                return "  N/A\n"
            hc = column.stats.numeric.hist_counts
            ht = [f"{ast.literal_eval(t):0.3g}" for t in ht]
            hc = [round(c / max(hc) * 20) for c in hc]
            max_len = max(len(ht[0]), len(ht[-1])) + 1
            hist += f"{ht[0].rjust(max_len)}|{block * hc[0]}\n"
            for c in hc[1:-1]:
                hist += f"{'|'.rjust(max_len + 1)}{block * c}\n"
            hist += f"{ht[-1].rjust(max_len)}|{block * hc[-1]}\n"
        else:
            ht = column.stats.non_numeric.hist_ticks
            if not ht:
                return "  N/A\n"
            hc = column.stats.non_numeric.hist_counts
            hc = [round(c / max(hc) * 20) for c in hc]
            max_len = max([len(t) for t in ht]) + 1
            for i, c in enumerate(hc):
                hist += f"{ht[i].rjust(max_len)}|{block * c}\n"
        return hist

    def _update(self) -> None:
        self._dataset._update()
        self._column_summaries: Dict[str, Dict[str, Union[float, int, str]]] = {
            c.name: self._create_column_summary_dict(c)
            for c in self._dataset._get_raw_info().entity.columns
            if c.name in self._columns
        }


class DatasetJob(_utils.ServerJob):
    """Monitor creation of a dataset on the Driverless AI server."""

    def __init__(self, client: "_core.Client", key: str, name: str = None) -> None:
        super().__init__(client=client, key=key)
        self._set_name(name)

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_dataset_job(self.key))

    def result(self, silent: bool = False) -> "Dataset":
        """Wait for job to complete, then return a Dataset object.

        Args:
            silent: if True, don't display status updates
        """
        self._wait(silent)
        if self.name:
            self._client._backend.update_dataset_name(self.key, self.name)
        return self._client.datasets.get(self.key)


class Datasets:
    """Interact with datasets on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client
        self._simple_connectors = {
            "azrbs": self._client._backend.create_dataset_from_azr_blob,
            "dtap": self._client._backend.create_dataset_from_dtap,
            "file": self._client._backend.create_dataset_from_file,
            "gcs": self._client._backend.create_dataset_from_gcs,
            "hdfs": self._client._backend.create_dataset_from_hadoop,
            "minio": self._client._backend.create_dataset_from_minio,
            "s3": self._client._backend.create_dataset_from_s3,
        }
        if not _utils.is_server_version_less_than(self._client, "1.10.2"):
            self._simple_connectors[
                "h2o_drive"
            ] = self._client._backend.create_dataset_from_h2o_drive

    def _dataset_create(
        self,
        data: Union[str, "pandas.DataFrame"],
        data_source: str,
        data_source_config: Dict[str, str] = None,
        force: bool = False,
        name: str = None,
    ) -> "DatasetJob":
        if data_source not in self._client.connectors.list():
            raise ValueError(
                "Please use one of the available connectors:",
                self._client.connectors.list(),
            )
        if not force:
            if name:
                _utils.error_if_dataset_exists(self._client, name)
            elif isinstance(data, str):
                # if data is not Pandas DataFrame
                _utils.error_if_dataset_exists(self._client, Path(data).name)
        if data_source in self._simple_connectors:
            key = self._simple_connectors[data_source](data)
        elif data_source == "upload":
            if data.__class__.__name__ == "DataFrame":
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_csv_path = Path(temp_dir, f"DataFrame_{os.urandom(4).hex()}")
                    data.to_csv(temp_csv_path, index=False)  # type: ignore
                    key = self._client._backend.upload_dataset(temp_csv_path)[0]
            else:
                key = self._client._backend.upload_dataset(data)[0]
        elif data_source == "gbq":
            if name is None:
                raise ValueError(
                    "Google Big Query connector requires a `name` argument."
                )
            args = self._client._server_module.messages.GbqCreateDatasetArgs(
                dataset_id=data_source_config["gbq_dataset_name"],
                bucket_name=data_source_config["gbq_bucket_name"],
                dst=name,
                query=data,
                location=data_source_config.get("gbq_location", None),
                project=data_source_config.get("gbq_project", None),
            )
            key = self._client._backend.create_dataset_from_gbq(args)
        elif data_source == "hive":
            if name is None:
                raise ValueError("Hive connector requires a `name` argument.")
            args = self._client._server_module.messages.HiveCreateDatasetArgs(
                dst=name,
                query=data,
                hive_conf_path=data_source_config.get("hive_conf_path", ""),
                keytab_path=data_source_config.get("hive_keytab_path", ""),
                auth_type=data_source_config.get("hive_auth_type", ""),
                principal_user=data_source_config.get("hive_principal_user", ""),
                database=data_source_config.get("hive_default_config", ""),
            )
            key = self._client._backend.create_dataset_from_spark_hive(args)
        elif data_source == "jdbc":
            if name is None:
                raise ValueError("JDBC connector requires a `name` argument.")
            args = self._client._server_module.messages.JdbcCreateDatasetArgs(
                dst=name,
                query=data,
                id_column=data_source_config.get("id_column", ""),
                jdbc_user=data_source_config["jdbc_username"],
                password=data_source_config["jdbc_password"],
                url=data_source_config.get("jdbc_url", ""),
                classpath=data_source_config.get("jdbc_driver", ""),
                jarpath=data_source_config.get("jdbc_jar", ""),
                database=data_source_config.get("jdbc_default_config", ""),
            )
            key = self._client._backend.create_dataset_from_spark_jdbc(args)
        elif data_source == "kdb":
            if name is None:
                raise ValueError("KDB connector requires a `name` argument.")
            args = self._client._server_module.messages.KdbCreateDatasetArgs(
                dst=name, query=data
            )
            key = self._client._backend.create_dataset_from_kdb(args)
        elif data_source == "recipe_file":
            data_file = self._client._backend.upload_custom_recipe_sync(
                data
            ).data_files[0]
            key = self._client._backend.create_dataset_from_recipe(data_file)
        elif data_source == "recipe_url":
            recipe_key = self._client._backend.create_custom_recipe_from_url(data)
            completed_recipe_job = _recipes.RecipeJob(self._client, recipe_key).result(
                silent=True
            )
            data_file = completed_recipe_job._get_raw_info().entity.data_files[0]
            key = self._client._backend.create_dataset_from_recipe(data_file)
        elif data_source == "snow":
            if name is None:
                raise ValueError("Snowflake connector requires a `name` argument.")
            args = self._client._server_module.messages.SnowCreateDatasetArgs(
                region=data_source_config.get("snowflake_region", ""),
                database=data_source_config["snowflake_database"],
                warehouse=data_source_config["snowflake_warehouse"],
                schema=data_source_config["snowflake_schema"],
                role=data_source_config.get("snowflake_role", ""),
                dst=name,
                query=data,
                optional_formatting=data_source_config.get("snowflake_formatting", ""),
                sf_user=data_source_config.get("snowflake_username", ""),
                password=data_source_config.get("snowflake_password", ""),
                account=data_source_config.get("snowflake_account", ""),
            )
            key = self._client._backend.create_dataset_from_snowflake(args)
        return DatasetJob(self._client, key, name)

    def create(
        self,
        data: Union[str, "pandas.DataFrame"],
        data_source: str = "upload",
        data_source_config: Dict[str, str] = None,
        force: bool = False,
        name: str = None,
    ) -> "Dataset":
        """Create a dataset on the Driverless AI server and return a Dataset
        object corresponding to the created dataset.

        Args:
            data: path to data file(s) or folder, a Pandas DataFrame,
                or query string for SQL based data sources
            data_source: name of connector to use for data transfer
                (use ``driverlessai.connectors.list()`` to see configured names)
            data_source_config: dictionary of configuration options for
                advanced connectors
            force: create new dataset even if dataset with same name already exists
            name: dataset name on the Driverless AI server

        Examples::

            ds = dai.datasets.create(
                data='s3://h2o-public-test-data/smalldata/iris/iris.csv',
                data_source='s3'
            )
        """
        return self.create_async(
            data, data_source, data_source_config, force, name
        ).result()

    def create_async(
        self,
        data: Union[str, "pandas.DataFrame"],
        data_source: str = "upload",
        data_source_config: Dict[str, str] = None,
        force: bool = False,
        name: str = None,
    ) -> "DatasetJob":
        """Launch creation of a dataset on the Driverless AI server and return
        a DatasetJob object to track the status.

        Args:
            data: path to data file(s) or folder, a Pandas DataFrame,
                or query string for SQL based data sources
            data_source: name of connector to use for data transfer
                (use ``driverlessai.connectors.list()`` to see configured names)
            data_source_config: dictionary of configuration options for
                advanced connectors
            force: create new dataset even if dataset with same name already exists
            name: dataset name on the Driverless AI server

        Examples::

            ds = dai.datasets.create_async(
                data='s3://h2o-public-test-data/smalldata/iris/iris.csv',
                data_source='s3'
            )
        """
        return self._dataset_create(data, data_source, data_source_config, force, name)

    def get(self, key: str) -> "Dataset":
        """Get a Dataset object corresponding to a dataset on the
        Driverless AI server. If the dataset only exists on H2O.ai Storage,
        it will be imported to the server first.

        Args:
            key: Driverless AI server's unique ID for the dataset

        Examples::

            # Use the UUID of the dataset to retrieve the dataset object
            key = 'e7de8630-dbfb-11ea-9f69-0242ac110002'
            ds = dai.datasets.get(key=key)
        """
        if self._client.server.storage_enabled:
            try:
                storage_key = self._client._backend.import_storage_dataset(key)
                print("Importing dataset from storage...")
                _utils.StorageImportJob(self._client, storage_key).result()
            except self._client._server_module.protocol.RemoteError as e:
                if not _utils.is_key_error(e):
                    raise
        info = self._client._backend.get_dataset_job(key)
        return Dataset(self._client, info)

    def gui(self) -> _utils.Hyperlink:
        """Get full URL for the user's datasets page on Driverless AI server.

        Examples::

            dai.datasets.gui()
        """
        return _utils.Hyperlink(
            f"{self._client.server.address}{self._client._gui_sep}datasets"
        )

    def list(self, start_index: int = 0, count: int = None) -> Sequence["Dataset"]:
        """List of Dataset objects available to the user.

        Args:
            start_index: index on Driverless AI server of first dataset to list
            count: max number of datasets to request from the Driverless AI server

        Examples::

            dai.datasets.list(start_index=10, count=5)
        """
        if count:
            data = self._client._backend.list_datasets(
                start_index, count, include_inactive=False
            ).datasets
        else:
            page_size = 100
            page_position = start_index
            data = []
            while True:
                page = self._client._backend.list_datasets(
                    page_position, page_size, include_inactive=True
                ).datasets
                data.extend(
                    d for d in page if _utils.is_server_job_complete(d.import_status)
                )
                if len(page) < page_size:
                    break
                page_position += page_size
        return _utils.ServerObjectList(
            data=data, get_method=self.get, item_class_name=Dataset.__name__
        )


class DatasetSplitJob(_utils.ServerJob):
    """Monitor splitting of a dataset on the Driverless AI server."""

    def __init__(
        self,
        client: "_core.Client",
        key: str,
        train_name: str = None,
        test_name: str = None,
    ) -> None:
        super().__init__(client=client, key=key)
        self._test_name = test_name
        self._train_name = train_name

    def _update(self) -> None:
        self._set_raw_info(self._client._backend.get_dataset_split_job(self.key))

    def result(self, silent: bool = False) -> Dict[str, "Dataset"]:
        """Wait for job to complete, then return a dictionary of Dataset objects.

        Args:
            silent: if True, don't display status updates
        """
        status_update = _utils.StatusUpdate()
        if not silent:
            status_update.display(_utils.JobStatus.RUNNING.message)
        self._wait(silent=True)
        ds1_key, ds2_key = self._get_raw_info().entity
        ds1 = DatasetJob(self._client, ds1_key, name=self._train_name).result(
            silent=True
        )
        ds2 = DatasetJob(self._client, ds2_key, name=self._test_name).result(
            silent=True
        )
        if not silent:
            status_update.display(_utils.JobStatus.COMPLETE.message)
        status_update.end()
        return {"train_dataset": ds1, "test_dataset": ds2}

    def status(self, verbose: int = None) -> str:
        """Return short job status description string."""
        return self._status().message
