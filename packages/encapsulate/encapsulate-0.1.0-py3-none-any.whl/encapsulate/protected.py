from .encapsulate_function import encapsulate_function
from .private import are_same_types


def _correctness_check(my_type, caller_type):
    return are_same_types(my_type, caller_type) or issubclass(caller_type, my_type)


def protected(f):
    """Only allows the decorated function to be called from the same class or a subclass."""
    return encapsulate_function(f, _correctness_check)
