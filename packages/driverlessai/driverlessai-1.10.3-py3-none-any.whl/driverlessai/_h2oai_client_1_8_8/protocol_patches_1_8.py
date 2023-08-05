"""protocol.py patches for server versions 1.8"""

import inspect
import functools
from pathlib import Path
from typing import List

from .messages import *
from .messages_patches_1_8 import ServerObject
from . import references


def ignore_unexpected_kwargs(func):
    @functools.wraps(func)
    def wrapper_ignore_unexpected_kwargs(*args, **kwargs):
        filtered_kwargs = {}
        for k,v in kwargs.items():
            if k in inspect.signature(func).parameters.keys():
                filtered_kwargs[k] = v
        return func(*args, **filtered_kwargs)
    return wrapper_ignore_unexpected_kwargs

def not_supported_by_servers(less_than_version: str, feature: str = "Feature") -> None:
    raise RuntimeError(
        f"{feature} is not supported in Driverless AI server versions < {less_than_version}"
    )

# 1.8.0
def update_dataset_name(self, key: str, new_name: str) -> None:
    import warnings
    warnings.warn(
        "Dataset naming only works upon creation from 'gbq', 'jdbc', 'kdb', or 'snow' data sources in Driverless AI server versions < 1.8.1. "
    )

def list_datasets_with_similar_name(self, name: str) -> List[str]:
    page_size = 100
    page_position = 0
    datasets = []
    while True:
        page = self.list_datasets(page_position, page_size, include_inactive=True).datasets
        # inactive datasets are ignored by `list_datasets_with_similar_name` in servers > 1.8.0 
        # but are needed for proper page length comparison
        datasets.extend(d.name for d in page if d.import_status <= 0)
        if len(page) < page_size:
            break
        page_position += page_size
    return [d for d in datasets if d.endswith(name)]

get_data_recipe_preview = lambda *args: not_supported_by_servers(less_than_version="1.8.1", feature="Modifying datasets")
modify_dataset_by_recipe_file = lambda *args: not_supported_by_servers(less_than_version="1.8.1", feature="Modifying datasets")
modify_dataset_by_recipe_url = lambda *args: not_supported_by_servers(less_than_version="1.8.1", feature="Modifying datasets")

# 1.8.0 - 1.8.2
list_experiment_artifacts = lambda *args: not_supported_by_servers(less_than_version="1.8.3", feature="Exporting artifacts")
upload_experiment_artifacts = lambda *args: not_supported_by_servers(less_than_version="1.8.3", feature="Exporting artifacts")

# 1.8.0 - 1.8.5.1
def create_dataset_from_gbq(self, args: GbqCreateDatasetArgs) -> str:
    """

    """
    filepath = f"gs://{args.bucket_name}/{args.dst}.csv" 
    self.create_bigquery_query(args.dataset_id, filepath, args.query)
    req_ = dict(filepath=filepath)
    res_ = self._request('create_dataset_from_gbq', req_)
    return res_

def create_dataset_from_kdb(self, args: KdbCreateDatasetArgs) -> str:
    """

    """
    req_ = dict(dst=args.dst, query=args.query)
    res_ = self._request('create_dataset_from_kdb', req_)
    return res_

def create_dataset_from_snowflake(self, args: SnowCreateDatasetArgs) -> str:
    """

    """
    filepath = self.create_snowflake_query(args.region, args.database, args.warehouse, args.schema, args.role, args.dst, args.query, args.optional_formatting)
    req_ = dict(filepath=filepath)
    res_ = self._request('create_dataset_from_snow', req_)
    return res_

def create_dataset_from_spark_hive(self, args: HiveCreateDatasetArgs) -> str:
    raise RuntimeError("Hive connector is not supported in Driverless AI server versions < 1.8.6.")

def create_dataset_from_spark_jdbc(self, args: JdbcCreateDatasetArgs) -> str:
    """

    """
    spark_jdbc_config = SparkJDBCConfig(
        options=[],
        database=args.database,
        jarpath=args.jarpath,
        classpath=args.classpath,
        url=args.url
    )
    req_ = dict(dst=args.dst, query=args.query, id_column=args.id_column, jdbc_user=args.jdbc_user, password=args.password, spark_jdbc_config=spark_jdbc_config.dump())
    res_ = self._request('create_dataset_from_spark_jdbc', req_)
    return res_

# 1.8.3 - 1.8.5.1
def fix_export_location(func):
    @functools.wraps(func)
    def fix_export_location_wrapper(*args, **kwargs):
        out = func(*args, **kwargs)
        out.location = str(Path(out.location, out.user, kwargs["model_key"]))
        return out
    return fix_export_location_wrapper

# 1.8
def list_interpretations(self, offset: int, limit: int) -> ServerObject:
    """

    """
    req_ = dict(offset=offset, limit=limit)
    res_ = self._request('list_interpretations', req_)
    return ServerObject(items=[InterpretSummary.load(b_) for b_ in res_])

def list_project_experiments(self, project_key: str) -> ServerObject:
    """

    """
    req_ = dict(project_key=project_key)
    res_ = self._request('get_experiments_for_project', req_)
    return ServerObject(model_summaries=[ModelSummaryWithDiagnostics.load(b_) for b_ in res_])

def list_projects(self, offset: int, limit: int) -> ServerObject:
    """

    """
    req_ = dict(offset=offset, limit=limit)
    res_ = self._request('list_projects', req_)
    return ServerObject(items=[Project.load(b_) for b_ in res_])

def list_visualizations(self, offset: int, limit: int) -> ServerObject:
    """

    """
    req_ = dict(offset=offset, limit=limit)
    res_ = self._request('list_visualizations', req_)
    return ServerObject(items=[AutoVizSummary.load(b_) for b_ in res_])

def run_interpret_timeseries(self, interpret_params: InterpretParameters) -> str:
    """

    """
    settings = (
        "dai_model",
        "testset",
        "sample_num_rows",
        "config_overrides"
    )
    interpret_params_filtered = {k:v for k,v in interpret_params.dump().items() if k in settings} 
    req_ = dict(interpret_timeseries_params=interpret_params_filtered)
    res_ = self._request('run_interpret_timeseries', req_)
    return res_

def run_interpretation(self, interpret_params: InterpretParameters) -> str:
    """

    """
    settings = (
        "dai_model",
        "dataset",
        "target_col",
        "use_raw_features",
        "prediction_col",
        "weight_col",
        "drop_cols",
        "klime_cluster_col",
        "nfolds",
        "sample",
        "sample_num_rows",
        "qbin_cols",
        "qbin_count",
        "lime_method",
        "dt_tree_depth",
        "vars_to_pdp",
        "config_overrides",
        "dia_cols"
    )
    interpret_params_filtered = {k:v for k,v in interpret_params.dump().items() if k in settings} 
    req_ = dict(interpret_params=interpret_params_filtered)
    res_ = self._request('run_interpretation', req_)
    return res_

def get_mli_config_options(self) -> List[ConfigItem]:
    """

    """
    return [
        ConfigItem(
            name="use_raw_features", description="Show interpretation based on the original columns.", 
            comment="", type="bool", val=True, predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        ),
        ConfigItem(
            name="klime_cluster_col", description="Column used to split data into k-LIME clusters.",
            comment="", type="str", val="", predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        ),
        ConfigItem(
            name="nfolds", description="Number of folds used by the surrogate models.",
            comment="", type="int", val=0, predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        ),
        ConfigItem(
            name="sample", description="Whether the training dataset should be sampled down for the interpretation.",
            comment="", type="bool", val=True, predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        ),
        ConfigItem(
            name="sample_num_rows", description="Number of sampled rows.",
            comment="", type="int", val=-1, predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        ),
        ConfigItem(
            name="qbin_cols", description="List of numeric columns to convert to quantile bins (can help fit surrogate models)",
            comment="", type="list", val=[], predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        ),
        ConfigItem(
            name="qbin_count", description="Number of quantile bins for the quantile bin columns.",
            comment="", type="int", val=0, predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        ),
        ConfigItem(
            name="lime_method", description="LIME method type from ['k-LIME', 'LIME_SUP'].",
            comment="", type="str", val="k-LIME", predefined=['k-LIME', 'LIME_SUP'], tags=["mli"], min_=None, max_=None, category="mli"
        ),
        ConfigItem(
            name="dt_tree_depth", description="Max depth of decision tree surrogate model.",
            comment="", type="int", val=3, predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        ),
        ConfigItem(
            name="vars_to_pdp", description="Number of variables to use for DAI PDP based on DAI feature importance and number of variables to use for surrogate Random Forest PDP based on surrogate Random Forest feature importance.",
            comment="", type="int", val=10, predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        ),
        ConfigItem(
            name="dia_cols", description="List of categorical columns to use for disparate impact analysis.",
            comment="", type="list", val=[], predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        )
    ]
