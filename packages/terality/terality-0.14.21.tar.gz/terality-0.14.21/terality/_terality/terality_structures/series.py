from typing import Optional, Sequence, Hashable, Union, List, Dict

import pandas as pd
from pandas.core.accessor import CachedAccessor
from terality_serde import StructType

from . import ClassMethod, Struct
from .common import make_export_request
from .structure import StructIterator
from terality._terality.patch_libs.plot.plot_accessor import TeralityPlotAccessor


class ClassMethodSeries(ClassMethod):
    _class_name: StructType = StructType.SERIES
    _pandas_class = pd.Series
    _additional_class_methods = ClassMethod._additional_class_methods | {
        "random",
        "random_integers",
    }


class Series(Struct, metaclass=ClassMethodSeries):
    """
    A terality.Series to handle one-dimensional data with axis labels.
    This behaves exactly like a pandas.Series : https://pandas.pydata.org/docs/reference/api/pandas.Series.html.

    The most common ways to build a terality Series are the following :

    - selecting a column of a terality DataFrame :
    >>> df = terality.DataFrame({"A": ["x", "y", "z"]})
    >>> df["A"]
    0    x
    1    y
    2    z
    Name: A, dtype: object

    - instantiating from a pandas.Series:
    >>> series_pd = pandas.Series(["x", "y", "z"], name="A")
    >>> series = terality.Series(series_pd)
    0    x
    1    y
    2    z
    Name: A, dtype: object

    - using the constructor:
    >>> series = terality.Series(["x", "y", "z"], name="A")
    >>> series
    0    x
    1    y
    2    z
    Name: A, dtype: object
    """

    _pandas_class_instance = pd.Series(dtype="float64")
    _accessors = {"str", "dt"}
    _additional_methods = Struct._additional_methods | {"get_range_auto", "random"}

    def __iter__(self):
        return StructIterator(self)

    def to_csv(  # pylint: disable=too-many-arguments, too-many-locals
        self,
        path_or_buf: str,
        sep: str = ",",
        na_rep: str = "",
        float_format: Optional[str] = None,
        columns: Optional[Sequence[Optional[Hashable]]] = None,
        header: Union[bool, List[str]] = True,
        index: bool = True,
        index_label: Optional[Union[str, Sequence, bool]] = None,
        mode: str = "w",
        encoding: Optional[str] = None,
        compression: Union[str, dict] = "infer",
        quoting: Optional[int] = None,
        quotechar: str = '"',
        line_terminator: Optional[str] = None,
        chunksize: Optional[int] = None,
        date_format: Optional[str] = None,
        doublequote: bool = True,
        escapechar: Optional[str] = None,
        decimal: str = ".",
        errors: str = "strict",
        storage_options: Optional[Dict] = None,
    ) -> Optional[str]:
        export_request = make_export_request(path_or_buf, storage_options)
        return self._call_method(
            None,
            "to_csv",
            export_request,
            sep=sep,
            na_rep=na_rep,
            float_format=float_format,
            columns=columns,
            header=header,
            index=index,
            index_label=index_label,
            mode=mode,
            encoding=encoding,
            compression=compression,
            quoting=quoting,
            quotechar=quotechar,
            line_terminator=line_terminator,
            chunksize=chunksize,
            date_format=date_format,
            doublequote=doublequote,
            escapechar=escapechar,
            decimal=decimal,
            errors=errors,
            storage_options=storage_options,
        )

    def to_csv_folder(  # pylint: disable=too-many-arguments, too-many-locals
        self,
        path_or_buf: str,
        num_files: Optional[int] = None,
        num_rows_per_file: Optional[int] = None,
        in_memory_file_size: Optional[int] = None,
        with_leading_zeros: bool = False,
        sep: str = ",",
        na_rep: str = "",
        float_format: Optional[str] = None,
        columns: Optional[Sequence[Optional[Hashable]]] = None,
        header: Union[bool, List[str]] = True,
        index: bool = True,
        index_label: Optional[Union[str, Sequence, bool]] = None,
        mode: str = "w",
        encoding: Optional[str] = None,
        compression: Union[str, dict] = "infer",
        quoting: Optional[int] = None,
        quotechar: str = '"',
        line_terminator: Optional[str] = None,
        chunksize: Optional[int] = None,
        date_format: Optional[str] = None,
        doublequote: bool = True,
        escapechar: Optional[str] = None,
        decimal: str = ".",
        errors: str = "strict",
        storage_options: Optional[Dict] = None,
    ) -> Optional[str]:
        """
        Store the DataFrame in several CSV files. Only one of num_files, num_rows_per_file, file_size must be provided.
        The number of files to produce is deduced from the parameter filled. By default, use chunks of 1GB.
        The path basename must contain the character *, that will be replaced by file number when producing files.
        If the path contains a non-existing folder, it is created.
        Leading zeros can be added to file numbers so each filename will have the same length.

        NOTE: This method has a specific documentation https://docs.terality.com/getting-terality/api-reference/write-to-multiple-files
        which should be updated if needed.
        """

        export_request = make_export_request(path_or_buf, storage_options)
        return self._call_method(
            None,
            "to_csv_folder",
            export_request,
            num_files=num_files,
            num_rows_per_file=num_rows_per_file,
            in_memory_file_size=in_memory_file_size,
            with_leading_zeros=with_leading_zeros,
            sep=sep,
            na_rep=na_rep,
            float_format=float_format,
            columns=columns,
            header=header,
            index=index,
            index_label=index_label,
            mode=mode,
            encoding=encoding,
            compression=compression,
            quoting=quoting,
            quotechar=quotechar,
            line_terminator=line_terminator,
            chunksize=chunksize,
            date_format=date_format,
            doublequote=doublequote,
            escapechar=escapechar,
            decimal=decimal,
            errors=errors,
            storage_options=storage_options,
        )

    @property
    def flags(self):
        raise NotImplementedError("Series.flags is not implemented")

    def to_dict(self, into: type = dict):
        pd_series = self._call_method(None, "to_pandas")
        return pd_series.to_dict(into=into)

    def to_list(self):
        pd_series = self._call_method(None, "to_pandas")
        return pd_series.to_list()

    def tolist(self):
        return self.to_list()

    @classmethod
    def from_pandas(cls, series: pd.Series):
        if not isinstance(series, pd.Series):
            raise TypeError("Series.from_pandas only accepts a pandas Series parameter.")

        return cls._call(None, "from_pandas", series)

    # Use the same pattern than pandas to provide pot accessor
    plot = CachedAccessor("plot", TeralityPlotAccessor)
