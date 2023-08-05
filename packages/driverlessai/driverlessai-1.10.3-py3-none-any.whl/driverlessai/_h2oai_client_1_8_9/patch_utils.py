import inspect
import functools


def ignore_unexpected_kwargs(func):
    @functools.wraps(func)
    def wrapper_ignore_unexpected_kwargs(*args, **kwargs):
        func_params = inspect.signature(func).parameters.keys()
        if "kwargs" in func_params:
            return func(*args, **kwargs)
        filtered_kwargs = {}
        for k,v in kwargs.items():
            if k in func_params:
                filtered_kwargs[k] = v
        return func(*args, **filtered_kwargs)
    return wrapper_ignore_unexpected_kwargs
