import warnings

import numpy as np
import pandas as pd
from pandas.core.groupby import SeriesGroupBy, DataFrameGroupBy
from pandas.core.window import Rolling
from terality_serde import SerializableEnum


# This class needs to be common to client / scheduler / worker.
class IndexType(str, SerializableEnum):
    """
    Technical types names of supported index sub classes.
    """

    INDEX = "index"
    MULTI_INDEX = "multi_index"
    DATETIME_INDEX = "datetime_index"
    INT64_INDEX = "int64_index"
    FLOAT64_INDEX = "float64_index"


class StructType(str, SerializableEnum):
    """
    Technical types names of pandas supported structures, excluding index.
    """

    DATAFRAME = "dataframe"
    SERIES = "series"
    DATAFRAME_GROUPBY = "dataframe_groupby"
    SERIES_GROUPBY = "series_groupby"
    GROUPBY_GROUPS = "groupby_groups"
    NDARRAY = "ndarray"
    EXTENSION_ARRAY = "pandas_array"
    TOP_LEVEL = "top_level"
    ROLLING = "rolling"


with warnings.catch_warnings():
    warnings.filterwarnings(
        "ignore", category=FutureWarning
    )  # Int64Index and Float64Index deprecated in 1.4

    STRUCT_TYPE_TO_PANDAS_CLASS = {
        IndexType.INDEX: pd.Index,
        IndexType.INT64_INDEX: pd.Int64Index,
        IndexType.FLOAT64_INDEX: pd.Float64Index,
        IndexType.DATETIME_INDEX: pd.DatetimeIndex,
        IndexType.MULTI_INDEX: pd.MultiIndex,
        StructType.NDARRAY: np.ndarray,
        StructType.EXTENSION_ARRAY: pd.api.extensions.ExtensionArray,
        StructType.SERIES: pd.Series,
        StructType.DATAFRAME: pd.DataFrame,
        StructType.SERIES_GROUPBY: SeriesGroupBy,
        StructType.DATAFRAME_GROUPBY: DataFrameGroupBy,
        StructType.ROLLING: Rolling,
        StructType.TOP_LEVEL: pd,
    }
