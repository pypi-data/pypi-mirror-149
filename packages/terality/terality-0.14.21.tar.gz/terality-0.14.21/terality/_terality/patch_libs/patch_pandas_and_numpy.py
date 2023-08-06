from contextlib import contextmanager
from threading import local
from typing import Dict, Callable

import pandas as pd
import numpy as np
import terality as te


# Following class allow terality structures to pass isinstance checks against pandas structures within external libs (TER-1482)
# NOTE: If we want to override constructors, we can do the same trick with inheriting te.DataFrame / etc here.


class MetaclassDataFrameIsInstanceTerality(type):
    def __instancecheck__(cls, instance):
        """
        Allow terality.DataFrame objects to pass isinstance checks against pandas.DataFrame within external packages.
        We use a thread local variable in order to disable this override within terality client modules, even if it has
        been enabled with the override context manager.
        No need to check for DataframeIsInstanceTerality cf https://stackoverflow.com/a/47741064
        """

        if _allow_patching_packages_in_terality_modules():
            return isinstance(instance, (cls.__base__, te.DataFrame))
        return isinstance(instance, cls.__base__)


class DataFrameIsInstanceTerality(pd.DataFrame, metaclass=MetaclassDataFrameIsInstanceTerality):
    pass


class MetaclassSeriesIsInstanceTerality(type):
    def __instancecheck__(cls, instance):
        # No need to check for SeriesIsInstanceTerality cf https://stackoverflow.com/a/47741064
        if _allow_patching_packages_in_terality_modules():
            return isinstance(instance, (cls.__base__, te.Series))
        return isinstance(instance, cls.__base__)


class SeriesIsInstanceTerality(pd.Series, metaclass=MetaclassSeriesIsInstanceTerality):
    pass


class MetaclassIndexIsInstanceTerality(type):
    def __instancecheck__(cls, instance):
        # No need to check for IndexIsInstanceTerality as class match https://stackoverflow.com/a/47741064
        if _allow_patching_packages_in_terality_modules():
            return isinstance(instance, (cls.__base__, te.Index))
        return isinstance(instance, cls.__base__)


class IndexIsInstanceTerality(pd.Index, metaclass=MetaclassIndexIsInstanceTerality):
    pass


class MetaclassNDArrayIsInstanceTerality(type):
    def __instancecheck__(cls, instance):
        # No need to check for NDArrayIsInstanceTerality as class match https://stackoverflow.com/a/47741064
        if _allow_patching_packages_in_terality_modules():
            return isinstance(instance, (cls.__base__, te.NDArray))
        return isinstance(instance, cls.__base__)


class NDArrayIsInstanceTerality(np.ndarray, metaclass=MetaclassNDArrayIsInstanceTerality):
    pass


_pd_functions_to_override = ["isna", "isnull", "notna", "notnull"]
_np_functions_to_override = [
    "mean",
    "median",
    "min",
    "max",
    "percentile",
    "quantile",
    "asarray",
    "isin",
    "concatenate",
    "sort",
    "ravel",
    "histogram",
    "nanmin",
    "nanmax",
]

np_funcs_names_to_internal_names = {
    np_func_name: f"_np_{np_func_name}_" for np_func_name in _np_functions_to_override
}


original_pd_functions: Dict[str, Callable] = {}
original_np_functions: Dict[str, Callable] = {}


# TODO check functools.wraps
def _wrap_pd_or_np_function(func_name: str, func: Callable) -> Callable:
    """
    Wrapper around numpy/pandas top level functions, so that if they are called
    with some terality structures arguments, it is the terality version that is used.
    Note these numpy top level methods are not public, we only use them for overriding purposes.
    """

    def internal_func_running_on_client_on_non_terality_param(*args, **kwargs):
        if not _allow_patching_packages_in_terality_modules():
            return func(*args, **kwargs)

        all_args = list(args) + list(kwargs.values())
        for arg in all_args:
            if isinstance(arg, (te.Index, te.Series, te.DataFrame, te.NDArray)):
                return te.__getattr__(func_name)(*args, **kwargs)
            # Check containers arguments one level deep to handle list/tuple of terality structs (like in `np.concat`)
            if isinstance(arg, (list, tuple)):
                for val in arg:
                    if isinstance(val, (te.Index, te.Series, te.DataFrame, te.NDArray)):
                        return te.__getattr__(func_name)(*args, **kwargs)
        return func(*args, **kwargs)

    return internal_func_running_on_client_on_non_terality_param


thread_local_data = local()


def _allow_patching_packages_in_terality_modules():
    """
    Wrapper to handle the fact that the `allow_patching_packages_in_terality_modules`
    may not have been set yet, which means that `disable_patching_packages_in_terality_modules`
    has never been called, thus the code being executed is not part of terality client module.
    """

    if hasattr(thread_local_data, "allow_patching_packages_in_terality_modules"):
        return thread_local_data.allow_patching_packages_in_terality_modules
    return True


@contextmanager
def disable_patching_packages_in_terality_modules():
    """Allow to easily disable patching mechanism in terality client code.

    When enabling these override mechanisms, we must take care that is has no impact within terality client modules.
    As some monkey patch might use some different threads, we use a thread local variable in order
    to disable overriding within terality client modules.
    For reference, consider the following example to understand why we need this override mechanism:
    - an external lib calls pd.isna(real_numpy_array), pd.isna is replaced by te.isna, and the
      real_numpy_array is converted to a frame and uploaded to terality from the client. During the conversion,
      some pandas/numpy methods are used, like `np.asarray`, which would be replaced by our internal `_np_asarray`,
      which will retry itself to upload its input parameter, and this would finally result in an infinite recursion.

    Note that as of writing, the above example can not happen even with the override enabled, because
    we use pandas/numpy version of top level functions on non-terality structures (for performance reasons).
    However, we could still struggle with similar issues regarding isinstance checks against pandas objects,
    thus we need to disable the override within client code (we disable it for both functions override and
    isinstance checks for consistency).

    This function is the only function setting the value of `thread_local_data.allow_patching_packages_in_terality_modules`
    """
    if _allow_patching_packages_in_terality_modules():
        # The attribute is not set or patching is allowed.
        thread_local_data.allow_patching_packages_in_terality_modules = False
        try:
            yield
        finally:
            thread_local_data.allow_patching_packages_in_terality_modules = True
    else:
        # We are already in a terality client module
        yield


def _override_instancechecks():
    original_pd_functions["DataFrame"] = pd.__dict__["DataFrame"]
    original_pd_functions["Series"] = pd.__dict__["Series"]
    original_pd_functions["Index"] = pd.__dict__["Index"]
    original_np_functions["ndarray"] = np.__dict__["ndarray"]

    pd.__dict__["DataFrame"] = DataFrameIsInstanceTerality
    pd.__dict__["Series"] = SeriesIsInstanceTerality
    pd.__dict__["Index"] = IndexIsInstanceTerality
    np.__dict__["ndarray"] = NDArrayIsInstanceTerality


def _undo_override_instancechecks():
    pd.__dict__["DataFrame"] = original_pd_functions["DataFrame"]
    pd.__dict__["Series"] = original_pd_functions["Series"]
    pd.__dict__["Index"] = original_pd_functions["Index"]
    pd.__dict__["ndarray"] = original_np_functions["ndarray"]


def _override_top_level_functions():
    for pd_func_name in _pd_functions_to_override:
        original_pd_functions[pd_func_name] = pd.__dict__[pd_func_name]
        pd.__dict__[pd_func_name] = _wrap_pd_or_np_function(pd_func_name, pd.__dict__[pd_func_name])

    for np_func_name, np_internal_func_name in np_funcs_names_to_internal_names.items():
        original_np_functions[np_func_name] = np.__dict__[np_func_name]
        np.__dict__[np_func_name] = _wrap_pd_or_np_function(
            np_internal_func_name, np.__dict__[np_func_name]
        )


def _undo_override_top_level_functions():
    for pd_function_name, pd_function_value in original_pd_functions.items():
        pd.__dict__[pd_function_name] = pd_function_value

    for np_function_name, np_function_value in original_np_functions.items():
        np.__dict__[np_function_name] = np_function_value


@contextmanager
def patch_external_packages():
    """Enable the use of terality structures within external packages.

    It is recommended to import the external packages within the context manager, as it may prevent
    of some symbols imported by the external package not to be patched.

    Example:
    with patch_external_packages():
        import seaborn as sb
        sb.boxplot(df_terality)


    It patches numpy/pandas top level methods so external libs use terality version instead of numpy/pandas version.
    For instance, it replaces `pandas.isna` by `terality.isna`.

    It also allows teraliy structures to pass instance checks against pandas structures.
    Basically, `isinstance(df_terality, pandas.DataFrame)` is evaluated to True.

    """

    # NOTE: This feature is not exposed publicly as we only support seaborn.boxplot
    # that should be used with `override_boxplot` instead

    _override_top_level_functions()
    _override_instancechecks()
    try:
        yield
    finally:
        _undo_override_instancechecks()
        _undo_override_top_level_functions()
