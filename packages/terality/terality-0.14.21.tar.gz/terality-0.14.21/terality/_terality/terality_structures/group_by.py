from pandas.core import groupby
from terality._terality.terality_structures import StructIterator
from terality.exceptions import TeralityError
from terality_serde import StructType

from . import ClassMethod, Struct


class ClassMethodGroupBySeries(ClassMethod):
    _class_name: str = StructType.SERIES_GROUPBY
    # noinspection PyUnresolvedReferences
    _pandas_class = groupby.SeriesGroupBy


class SeriesGroupBy(Struct, metaclass=ClassMethodGroupBySeries):
    """
    A terality.SeriesGroupBy that behaves exactly as a pandas.SeriesGroupBy.
    https://pandas.pydata.org/docs/reference/api/pandas.Series.groupby.html
    """

    # noinspection PyUnresolvedReferences
    _pandas_class_instance = groupby.SeriesGroupBy
    _additional_methods = Struct._additional_methods | {"sum", "mean"}


class ClassMethodGroupByDF(ClassMethod):
    _class_name: str = StructType.DATAFRAME_GROUPBY
    # noinspection PyUnresolvedReferences
    _pandas_class = groupby.DataFrameGroupBy


class DataFrameGroupBy(Struct, metaclass=ClassMethodGroupByDF):
    """
    A terality.DataFrameGroupBy that behaves exactly as a pandas.DataFrameGroupBy.
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
    """

    # noinspection PyUnresolvedReferences
    _pandas_class_instance = groupby.DataFrameGroupBy
    _additional_methods = Struct._additional_methods | {"sum", "mean"}
    _missing_attributes_banned_from_roundtrips = ["sentry_repr"]

    def _on_missing_attribute(self, item: str):
        if item in self._missing_attributes_banned_from_roundtrips:
            raise AttributeError(f"'{type(self).__name__}' has no attribute {item!r}")

        try:
            return self._call_method(None, "df_groupby_attribute_access", item)
        except TeralityError as e:
            if "AttributeError" in e.message:
                raise AttributeError(  # pylint:disable=raise-missing-from
                    f"'{type(self).__name__}' object has no attribute {item!r}"
                )
            raise e  # internal error


class ClassMethodGroupByGroups(ClassMethod):
    _class_name: str = StructType.GROUPBY_GROUPS
    # noinspection PyUnresolvedReferences
    _pandas_class = None


class GroupByGroups(Struct, metaclass=ClassMethodGroupByGroups):
    """
    A structure to represent groups, obtained from a obj.groupby().groups.
    https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.GroupBy.groups.html
    This structure avoid retrieving all groups within the user RAM, and allows iteration by batches.
    """

    # Add dict methods to raise a proper error message.
    _additional_methods = {"get_range_auto"} | set(dir(dict))

    def __iter__(self):
        return StructIterator(self)
