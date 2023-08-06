import inspect

import pandas as pd
from terality.api import types


def __getattr__(attribute: str):

    if attribute == "types":
        return types

    pd_attr = getattr(pd.api, attribute)

    # Send class and module calls to the pandas module
    if inspect.isclass(pd_attr) or inspect.ismodule(pd_attr):
        return pd_attr

    raise AttributeError(f"module pandas.api has no attribute {attribute}.")
