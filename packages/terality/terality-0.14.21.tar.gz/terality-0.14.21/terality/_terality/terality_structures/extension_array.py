import numpy as np
import pandas as pd
from terality_serde import StructType

from . import ClassMethod, Struct


class ClassMethodExtensionArray(ClassMethod):
    _class_name: str = StructType.EXTENSION_ARRAY
    _pandas_class = pd.api.extensions.ExtensionArray


class ExtensionArray(Struct, metaclass=ClassMethodExtensionArray):
    _pandas_class_instance = pd.arrays.PandasArray(values=np.empty(shape=1))
