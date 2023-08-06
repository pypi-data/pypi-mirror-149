import inspect
from functools import partial

import pandas as pd
from terality._terality.terality_structures import call_pandas_function
from terality_serde import StructType


def __getattr__(attribute: str):
    pd_attr = getattr(pd.api.types, attribute)

    # Send class and module calls to the pandas module
    if inspect.isclass(pd_attr) or inspect.ismodule(pd_attr):
        return pd_attr

    return partial(call_pandas_function, StructType.TOP_LEVEL, None, attribute)
