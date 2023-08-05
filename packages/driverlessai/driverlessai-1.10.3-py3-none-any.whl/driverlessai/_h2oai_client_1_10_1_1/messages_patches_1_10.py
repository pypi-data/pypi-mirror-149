"""messages.py patches for server versions 1.10"""

from .references import *


class ServerObject:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def dump(self) -> dict:
        d = {k: (v.dump() if hasattr(v, 'dump') else v) for k, v in vars(self).items()}
        return d


# 1.10.0
class GbqCreateDatasetArgs(ServerObject):
    def __init__(self, **kwargs) -> None:
        if kwargs.get("location"):
            raise ValueError(
                "`gbq_location` is only supported in Driverless AI server versions >= 1.10.1."
            )
        kwargs.pop("location", None)
        super().__init__(**kwargs)


# 1.10.0 - 1.10.1.3
class SnowCreateDatasetArgs(ServerObject):
    def __init__(self, **kwargs) -> None:
        if kwargs.get("account"):
            raise ValueError(
                "`snowflake_account` is only supported in Driverless AI server "
                "versions >= 1.10.2."
            )
        kwargs.pop("account", None)
        super().__init__(**kwargs)
