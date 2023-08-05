from .encapsulate_function import encapsulate_function


def _correctness_check(my_type, caller_type):
    return are_same_types(my_type, caller_type)


def are_same_types(my_type, caller_type):
    return my_type == caller_type


def private(f):
    """Only allows the decorated function to be called from the same class."""
    return encapsulate_function(f, _correctness_check)
