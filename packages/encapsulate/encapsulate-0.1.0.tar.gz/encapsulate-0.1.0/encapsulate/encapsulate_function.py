from functools import wraps
from inspect import currentframe
from wsgiref import validate


def encapsulate_function(f, correctness_check):
    def validate_access(self):
        try:
            caller_frame = currentframe().f_back.f_back
            calling_class = type(caller_frame.f_locals.get("self"))
            if not correctness_check(type(self), calling_class):
                raise AttributeError(f"{f.__name__} is not accessible to {calling_class}")
        except AttributeError:
            raise AttributeError(f"{f.__name__} is not accessible from a module context.")

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        validate_access(self)
        return f(self, *args, **kwargs)

    return wrapper
