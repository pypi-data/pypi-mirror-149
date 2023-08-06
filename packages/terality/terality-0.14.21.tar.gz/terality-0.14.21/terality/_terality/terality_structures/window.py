from typing import Set

import pandas as pd
from pandas.core.window import Rolling as PandasRolling
from terality_serde import StructType

from . import ClassMethod, Struct


class ClassMethodRolling(ClassMethod):
    _class_name: str = StructType.ROLLING
    _pandas_class = PandasRolling


class Rolling(Struct, metaclass=ClassMethodRolling):
    """
    A terality.Rolling to handle rolling window calculations.
    This behaves exactly like a pandas.Rolling: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html.
    """

    _pandas_class_instance = pd.DataFrame([0]).rolling(1)
    _indexers: Set[str] = set()
