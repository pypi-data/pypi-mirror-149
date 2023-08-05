"""protocol.py patches for server versions 1.9"""

import inspect
import functools
from typing import List

from .messages import *
from .messages_patches_1_9 import ServerObject


def ignore_unexpected_kwargs(func):
    @functools.wraps(func)
    def wrapper_ignore_unexpected_kwargs(*args, **kwargs):
        filtered_kwargs = {}
        for k,v in kwargs.items():
            if k in inspect.signature(func).parameters.keys():
                filtered_kwargs[k] = v
        return func(*args, **filtered_kwargs)
    return wrapper_ignore_unexpected_kwargs

# 1.9.0 - 1.9.0.6
def list_project_experiments(self, project_key: str) -> ServerObject:
    """

    """
    req_ = dict(project_key=project_key)
    res_ = self._request('get_experiments_for_project', req_)
    return ServerObject(model_summaries=[ModelSummaryWithDiagnostics.load(b_) for b_ in res_])

# 1.9
def get_mli_config_options(self) -> List[ConfigItem]:
    """

    """
    return [
        ConfigItem(
            name="sample_num_rows", description="Number of sampled rows.",
            comment="", type="int", val=-1, predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        ),
        ConfigItem(
            name="klime_cluster_col", description="Column used to split data into k-LIME clusters.",
            comment="", type="str", val="", predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        ),
        ConfigItem(
            name="qbin_cols", description="List of numeric columns to convert to quantile bins (can help fit surrogate models)",
            comment="", type="list", val=[], predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        ),
        ConfigItem(
            name="dia_cols", description="List of categorical columns to use for disparate impact analysis.",
            comment="", type="list", val=[], predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        ),
        ConfigItem(
            name="pd_features", description="",
            comment="", type="list", val=[], predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        ),
        ConfigItem(
            name="debug_model_errors", description="Whether to build surrogate models on model residuals as a prediction column (squared residuals for regression and logloss residuals for classification).",
            comment="", type="bool", val=False, predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        ),
        ConfigItem(
            name="debug_model_errors_class", description="Class used to calculate logloss residuals if `debug_model_errors` is `True` and the model is a classification model.",
            comment="", type="str", val="False", predefined=[], tags=["mli"], min_=None, max_=None, category="mli"
        )
    ]
