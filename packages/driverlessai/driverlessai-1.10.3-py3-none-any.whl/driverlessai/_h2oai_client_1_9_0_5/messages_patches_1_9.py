"""messages.py patches for server versions 1.9"""

from .references import *


class ServerObject:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def dump(self) -> dict:
        d = {k: (v.dump() if hasattr(v, 'dump') else v) for k, v in vars(self).items()}
        return d


# 1.9.0 - 1.9.0.6
class ModelParameters(ServerObject):
    """

    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

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


# 1.9.0 - 1.9.2.1
class GbqCreateDatasetArgs_up_to_1_9_2_1(ServerObject):
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


# 1.9.3 - 1.9.x
class GbqCreateDatasetArgs_from_1_9_3(ServerObject):
    def __init__(self, **kwargs) -> None:
        if kwargs.get("location"):
            raise ValueError(
                "`gbq_location` is only supported in Driverless AI server versions >= 1.10.1."
            )
        kwargs.pop("location", None)
        super().__init__(**kwargs)


# 1.9
class SnowCreateDatasetArgs(ServerObject):
    def __init__(self, **kwargs) -> None:
        if kwargs.get("account"):
            raise ValueError(
                "`snowflake_account` is only supported in Driverless AI server "
                "versions >= 1.10.2."
            )
        kwargs.pop("account", None)
        super().__init__(**kwargs)
