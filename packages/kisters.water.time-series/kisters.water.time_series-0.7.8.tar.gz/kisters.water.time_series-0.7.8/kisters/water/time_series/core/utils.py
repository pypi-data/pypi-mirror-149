import itertools as it
from typing import Any, Iterable


def _not_none(*args) -> bool:
    """Checks if all args are not None."""
    if any(a is not None for a in args):
        if not all(a is not None for a in args):
            raise AssertionError("Args contain a mixture of None and non-None values.")
        return True
    return False


def valid_ensemble_args(t0, member, dispatch_info=None) -> bool:
    # TODO: relax the requirement that all 3 args should be defined?
    #  maybe just require at least one to be non-None?
    if dispatch_info is None:
        try:
            return _not_none(t0, member)
        except AssertionError:
            raise AssertionError("Provide t0 and member for ensemble time series.")
    else:
        try:
            return _not_none(t0, member, dispatch_info)
        except AssertionError:
            raise AssertionError("Provide t0, dispatch_info and member for ensemble time series.")


def make_iterable(value: Any) -> Iterable:
    """Make an infinite iterable if not iterable or string already."""
    if not isinstance(value, Iterable) or isinstance(value, str):
        return it.repeat(value)
    return value
