from __future__ import annotations

import os
import warnings
import platform
from dataclasses import dataclass
from functools import partial
from typing import Callable, Optional, Tuple
import pickle
import sys

from ._vendor import cloudpickle

import pandas as pd
from pandas.core.groupby import SeriesGroupBy, DataFrameGroupBy
from terality_serde.struct_types import STRUCT_TYPE_TO_PANDAS_CLASS, StructType

from . import SerdeMixin


# Pandas and numpy methods are likely to be used as callables but are have a specific serialization
# workflow as they are already imported in the worker.
_WORKER_DEPENDENCIES = {"numpy", "pandas"}

with warnings.catch_warnings():
    warnings.filterwarnings(
        "ignore", category=FutureWarning
    )  # Int64Index and Float64Index deprecated in 1.4

    _CLASS_NAME_TO_PANDAS_CLASS = {  # TODO replace "Index" by te.Index.__name__ etc
        "Index": pd.Index,
        "Int64Index": pd.Int64Index,
        "Float64Index": pd.Float64Index,
        "DatetimeIndex": pd.DatetimeIndex,
        "MultiIndex": pd.MultiIndex,
        "Series": pd.Series,
        "DataFrame": pd.DataFrame,
        "SeriesGroupBy": SeriesGroupBy,
        "DataFrameGroupBy": DataFrameGroupBy,
    }


_ALLOW_ARBITRARY_CODE_EXECUTION = False


def enable_arbitrary_code_execution():
    """Enable arbitrary code execution in the current process.

    This allows deserializing callables, which is an operation that can run arbitrary code (and is thus
    unsecure in general, unless run in a secure sandbox).

    This function will fail unless the "TERALITY_ALLOW_ARBITRARY_CODE_EXECUTION" environment variable is
    set to "1".

    Once called, the entire process should be considered tainted (thus, there is no going back).

    Don't call this function unless you understand the consequences :)

    See:
        raise_on_arbitrary_code_execution_attempt: to help catch programming mistakes, you can also
            explicily mark the point after which callable deserialization is not expected. This doesn't
            add anything to the actual security model.

    Example:
        >>> callable_wrapper = CallableWrapper.from_object(lambda x: x + 1)
        >>> enable_arbitrary_code_execution()
        >>> try:
        >>>     callable_wrapper.to_callable_unsafe()
        >>> finally:
        >>>     raise_on_arbitrary_code_execution_attempt()
        >>>
        >>> # from this point, calling callable_wrapper.to_callable_unsafe() again will raise an exception
    """
    global _ALLOW_ARBITRARY_CODE_EXECUTION  # pylint: disable=global-statement
    if os.environ.get("TERALITY_ALLOW_ARBITRARY_CODE_EXECUTION") != "1":
        raise RuntimeError("Can't enable arbitrary code execution in this environment")
    _ALLOW_ARBITRARY_CODE_EXECUTION = True


def raise_on_arbitrary_code_execution_attempt():
    """Disable arbitrary code execution in the current process.

    This function is obviously unsafe: if code execution already occured, nothing guarantees that this function
    will have any meaningful effect.

    It's intended to catch programming mistakes, by marking code sections where callable deserialization
    should not be performed. Against non-malicious input, attempting to deserialize a callable once this
    function has been called will raise an exception.

    See:
        enable_arbitrary_code_execution
    """
    global _ALLOW_ARBITRARY_CODE_EXECUTION  # pylint: disable=global-statement
    _ALLOW_ARBITRARY_CODE_EXECUTION = False


def _convert_terality_method_to_pandas(obj: Callable):
    """
    Need this conversion to apply the pandas function on the worker instead of the terality one.
    Exemple: when calling series.apply(te.isnull) we serde pd.isnull.

    However, this function has no effect regarding UDF using terality functions.
    For this case, the trick is to set sys.modules["terality"] = pd directly
    in the worker.
    """

    if isinstance(obj, partial):
        struct_type, accessor, method_name = obj.args
        if accessor is not None:
            raise ValueError(f"Function {obj} can not be serialized.")
        if struct_type == StructType.GROUPBY_GROUPS:
            raise ValueError("Method of a terality.GroupByGroups can not be serialized.")
        class_type = STRUCT_TYPE_TO_PANDAS_CLASS[struct_type]
    else:
        class_name = obj.__qualname__.split(".")[0]
        class_type = _CLASS_NAME_TO_PANDAS_CLASS[class_name]
        method_name = obj.__name__

    method_to_call = getattr(class_type, method_name)
    return method_to_call


@dataclass
class CallableWrapper(SerdeMixin):
    """Represent a user-supplied callable. THIS OBJECT CAN BE UNSAFE, READ THE DOCS!"""

    pickled_payload: bytes

    # Function name is lost when we wrap a function defined in a worker dependency module, but we need
    # it to detect aggregations functions (e.g. `np.min`) so we can take the path supporting big parts.
    func_full_name: Optional[str] = None

    # Optional in order to keep backwards compatibility. If the client doesn't provide the Python version
    # here, default to the version provided by the client in the request headers.
    python_version: Optional[Tuple[str, str, str]] = None

    @classmethod
    def from_object(cls, obj: Callable) -> CallableWrapper:
        """Serialize the provided callable to a CallableWrapper.

        Internally, this uses the `cloudpickle` package and has the same limitations.

        Deserializing (even without running) such a serialized object can run arbitrary code.
        Only deserialize this in a safe sandboxed environment.
        """
        if isinstance(obj, type):
            # types are callable, but we don't support serializing them in this class
            raise TypeError("'obj' must not be a type")

        func = obj.func if isinstance(obj, partial) else obj
        module_obj = None

        # NOTE: Pickling numpy by value might be buggy, cf TER-563.
        if hasattr(func, "__module__") and func.__module__ is not None:
            module_prefix = func.__module__.split(".")[0]
            if module_prefix in _WORKER_DEPENDENCIES:
                # Wrap the function to avoid incompatibility errors if client package has a different version than
                # worker package. Typically, serializing `pd.to_numeric` in pandas 1.3.5 and deserializing it in 1.2.5
                # would result in an ImportError, as 1.3.5 implementation relies on internals that do not exist in 1.2.5. (cf TER-1741)
                def inner(*args, **kwargs):
                    return func(*args, **kwargs)

                obj = inner
            else:
                if module_prefix == "terality":
                    obj = _convert_terality_method_to_pandas(obj)
                elif func.__module__ not in sys.modules:
                    raise ValueError(
                        f"The provided callable module is '{func.__module__}', but it does not seem to be imported (not present in sys.modules). "
                        "Import this module in this Python session to be able to serialize this callable."
                    )
                else:
                    module_obj = sys.modules[func.__module__]
                    cloudpickle.register_pickle_by_value(module_obj)  # type: ignore

        if hasattr(func, "__module__") and hasattr(func, "__qualname__"):
            func_full_name = func.__module__ + "." + func.__qualname__
        else:
            func_full_name = None

        try:
            return cls(pickled_payload=cloudpickle.dumps(obj), func_full_name=func_full_name, python_version=platform.python_version_tuple())  # type: ignore
        finally:
            if module_obj is not None:
                cloudpickle.unregister_pickle_by_value(module_obj)  # type: ignore

    def to_callable_unsafe(self) -> Callable:
        """Return the deserialized callable. This function can run arbitrary user-supplied code and must only be run in a secure sandbox.

        This function will raise a ValueError if the environment variable "TERALITY_ALLOW_ARBITRARY_CODE_EXECUTION"
        is not set to 1. Don't set this environment variable if you don't understand the consequences :)

        If sys.modules["cloudpickle"] is not defined, this function will populate it.
        """
        if (
            os.environ.get("TERALITY_ALLOW_ARBITRARY_CODE_EXECUTION") != "1"
            or _ALLOW_ARBITRARY_CODE_EXECUTION is not True
        ):
            raise ValueError("Callables can only be deserialized in a secure sandbox.")
        try:
            # Backwards compatibility: some older clients will send values referring to the real cloudpickle
            # module (sys.modules["cloudpickle"]) instead of the vendored one
            # (sys.modules["terality_serde._vendor.cloudpickle"].  Let's allow pickle to use our vendored
            # cloudpickle module when a payload refers to the "cloudpickle" module.
            if "cloudpickle" not in sys.modules:
                # We don't undo this change at the end of the function, as it would make it non-thread safe.
                # Let's hope this global change does not break anything in the application.
                sys.modules["cloudpickle"] = cloudpickle

            return pickle.loads(self.pickled_payload)
        except ModuleNotFoundError as e:
            if "terality._terality" in str(e):
                raise ValueError(
                    "Can not deserialize this function, as it depends on another Terality structure. See https://docs.terality.com/getting-terality/user-guide/.apply-and-passing-callables unsupported cases for more information."
                ) from e
            raise ValueError(
                f"Can not deserialize this function, as it depends on a module not available in Terality's backend: `{str(e)}`. See https://docs.terality.com/getting-terality/user-guide/.apply-and-passing-callables unsupported cases for more information."
            ) from e
