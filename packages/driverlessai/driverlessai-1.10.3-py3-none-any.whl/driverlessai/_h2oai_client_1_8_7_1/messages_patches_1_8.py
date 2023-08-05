"""messages.py patches for server versions 1.8"""

from .references import *


class ServerObject:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def dump(self) -> dict:
        d = {k: (v.dump() if hasattr(v, 'dump') else v) for k, v in vars(self).items()}
        return d


# 1.8.0 - 1.8.5.1
class HiveCreateDatasetArgs(ServerObject):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class JdbcCreateDatasetArgs(ServerObject):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class KdbCreateDatasetArgs(ServerObject):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
 

# 1.8.0 - 1.8.6.3
class SnowCreateDatasetArgs_up_to_1_8_6_3(ServerObject):
    def __init__(self, **kwargs) -> None:
        if kwargs.get("sf_user") or kwargs.get("password"):
            raise ValueError(
                "`snowflake_username` and `snowflake_password` are only "
                "supported in Driverless AI server versions >= 1.8.7. "
                "For other Driverless AI server versions, credentials "
                "must be specified in config.toml."
            )
        kwargs.pop("sf_user", None)
        kwargs.pop("password", None)
        if kwargs.get("account"):
            raise ValueError(
                "`snowflake_account` is only supported in Driverless AI server "
                "versions >= 1.10.2."
            )
        kwargs.pop("account", None)
        super().__init__(**kwargs)


# 1.8.7 - 
class SnowCreateDatasetArgs_from_1_8_7(ServerObject):
    def __init__(self, **kwargs) -> None:
        if kwargs.get("account"):
            raise ValueError(
                "`snowflake_account` is only supported in Driverless AI server "
                "versions >= 1.10.2."
            )
        kwargs.pop("account", None)
        super().__init__(**kwargs)


# 1.8
class GbqCreateDatasetArgs(ServerObject):
    def __init__(self, **kwargs) -> None:
        if kwargs.get("location"):
            raise ValueError(
                "`gbq_location` is only supported in Driverless AI server versions >= 1.10.1."
            )
        kwargs.pop("location", None)
        if kwargs.get("project"):
            raise ValueError(
                "`gbq_project` is only supported in Driverless AI server versions >= 1.9.3."
            )
        kwargs.pop("project", None)
        super().__init__(**kwargs)


class InterpretParameters(ServerObject):
    """

    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def clone(self) -> 'InterpretParameters':
        return InterpretParameters(self.dai_model, self.dataset, self.target_col, self.prediction_col, self.use_raw_features, self.nfolds, self.klime_cluster_col, self.weight_col, self.drop_cols, self.sample, self.sample_num_rows, self.qbin_cols, self.qbin_count, self.lime_method, self.dt_tree_depth, self.config_overrides, self.vars_to_pdp, self.dia_cols)

    @staticmethod
    def load(d: dict) -> 'InterpretParameters':
        d['dai_model'] = ModelReference.load(d['dai_model'])
        d['dataset'] = DatasetReference.load(d['dataset'])
        return InterpretParameters(**d)


class ModelParameters(ServerObject):
    """

    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if hasattr(self, "is_image"):
            del self.is_image

    @staticmethod
    def load(d: dict) -> 'ModelParameters':
        if 'dataset' in d:
            d['dataset'] = DatasetReference.load(d['dataset'])
        if 'resumed_model' in d:
            d['resumed_model'] = ModelReference.load(d['resumed_model'])
        if 'validset' in d:
            d['validset'] = DatasetReference.load(d['validset'])
        if 'testset' in d:
            d['testset'] = DatasetReference.load(d['testset'])
        if 'cols_imputation' in d:
            d['cols_imputation'] = [ColumnImputation.load(a) for a in d['cols_imputation']]
        return ModelParameters(**d)
