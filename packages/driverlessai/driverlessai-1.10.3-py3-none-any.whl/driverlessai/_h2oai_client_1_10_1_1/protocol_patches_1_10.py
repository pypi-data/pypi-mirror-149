"""protocol.py patches for server versions 1.10"""

import inspect
import functools

from .messages import *
from .messages_patches_1_10 import ServerObject


def ignore_unexpected_kwargs(func):
    @functools.wraps(func)
    def wrapper_ignore_unexpected_kwargs(*args, **kwargs):
        filtered_kwargs = {}
        for k,v in kwargs.items():
            if k in inspect.signature(func).parameters.keys():
                filtered_kwargs[k] = v
        return func(*args, **filtered_kwargs)
    return wrapper_ignore_unexpected_kwargs
