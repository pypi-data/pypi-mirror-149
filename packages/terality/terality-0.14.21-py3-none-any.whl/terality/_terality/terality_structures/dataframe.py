from typing import Any, Callable, Dict, Optional, List, Sequence, Hashable, Union

import pandas as pd
from terality._terality.patch_libs.plot.plot_accessor import TeralityPlotAccessor
from terality._terality.terality_structures import StructIterator
from pandas.core.accessor import CachedAccessor
from terality.exceptions import TeralityError

from terality_serde import StructType

from . import ClassMethod, Struct
from .common import make_export_request


class ClassMethodDF(ClassMethod):
    _class_name: str = StructType.DATAFRAME
    _pandas_class = pd.DataFrame
    _additional_class_methods = ClassMethod._additional_class_methods | {
        "from_dict",
        "from_records",
    }


class DataFrame(Struct, metaclass=ClassMethodDF):
    """
    A terality DataFrame to handle two-dimensional, size-mutable, and potentially heterogeneous tabular data.
    This behaves exactly like a pandas.DataFrame: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html.

    The most common ways to build a terality DataFrame are the following:

    - reading from a file:
    >>> df = terality.read_csv("path/to/my/file.csv")

    - instantiating from a pandas.DataFrame:
    >>> df = terality.DataFrame(df_pd)

    - using the constructor:
    >>> df = terality.DataFrame({"col1": [0, 1, 2], "col2": ["A", "B", "C"]})
    >>> df
      col1 col2
    0     0    A
    1     1    Berality_structures/dataframe.py
    2     2    C
    """

    _class_name: str = StructType.DATAFRAME
    _pandas_class_instance = pd.DataFrame()
    _additional_methods = Struct._additional_methods | {
        "to_csv_folder",
        "to_parquet_folder",
    }
    _args_to_replace: dict = {
        # "to_csv" : (0, ExportRequest),
        "to_excel": (0, make_export_request)
    }
    _missing_attributes_banned_from_roundtrips = ["sentry_repr"]
    _methods_allowed_to_be_cached: List[str] = [
        "columns",
        "dtypes",
        "axes",
        "attrs",
        "empty",
        "flags",
        "index",
    ]

    def _on_missing_attribute(self, item: str):
        if item in self._missing_attributes_banned_from_roundtrips:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute {item!r}")

        try:
            return self._call_method(None, "df_col_by_attribute_access", item)
        except TeralityError as e:
            if "AttributeError" in e.message:
                raise AttributeError(  # pylint:disable=raise-missing-from
                    f"'{type(self).__name__}' object has no attribute {item!r}"
                )
            raise e  # internal error

    def __iter__(self):
        # Iterating on a `DataFrame` is the same as iterating on its columns.
        # No warning as the number of columns is supposed to be low.
        return StructIterator(self.columns, should_emit_warning=False)

    @property
    def flags(self) -> None:
        raise NotImplementedError("DataFrame.flags is not implemented")

    def to_json(  # pylint: disable=too-many-arguments,too-many-locals
        self,
        path_or_buf: str,
        orient: Optional[str] = None,
        date_format: Optional[str] = None,
        double_precision: int = 10,
        force_ascii: bool = True,
        date_unit: str = "ms",
        default_handler: Optional[Callable[[Any], Union[str, int, float, bool, List, Dict]]] = None,
        lines: bool = False,
        compression: Union[str, Dict] = "infer",
        index: bool = True,
        indent: Optional[int] = None,
        storage_options: Optional[Dict] = None,
    ) -> None:
        export_request = make_export_request(path_or_buf, storage_options)
        return self._call_method(
            None,
            "to_json",
            export_request,
            orient=orient,
            date_format=date_format,
            double_precision=double_precision,
            force_ascii=force_ascii,
            date_unit=date_unit,
            default_handler=default_handler,
            lines=lines,
            compression=compression,
            index=index,
            indent=indent,
            storage_options=storage_options,
        )

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
        Store the DataFrame in several CSV files. Only one of num_files, num_rows_per_file, file_size should be provided.
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

    def to_parquet(
        self,
        path: str,
        engine: str = "auto",
        compression: Optional[str] = "snappy",
        index: Optional[bool] = None,
        partition_cols: Optional[List[str]] = None,
        storage_options: Optional[Dict] = None,
    ):

        return self._call_method(
            None,
            "to_parquet",
            make_export_request(path, storage_options),
            engine=engine,
            compression=compression,
            index=index,
            partition_cols=partition_cols,
            storage_options=storage_options,
        )

    def to_parquet_folder(  # pylint: disable=too-many-arguments
        self,
        path: str,
        num_files: Optional[int] = None,
        num_rows_per_file: Optional[int] = None,
        in_memory_file_size: Optional[int] = None,
        with_leading_zeros: bool = False,
        engine: str = "auto",
        compression: Optional[str] = "snappy",
        index: Optional[bool] = None,
        partition_cols: Optional[List[str]] = None,
        storage_options: Optional[Dict] = None,
    ):
        """
        Store the DataFrame in several parquet files. Only one of num_files, num_rows_per_file, file_size must be provided.
        The number of files to produce is deduced from the parameter filled. By default, use chunks of 1GB.
        The path basename must contain the character *, that will be replaced by file number when producing files.
        If the path contains a non-existing folder, it is created.
        Leading zeros can be added to file numbers so each filename will have the same length.

        NOTE: This method has a specific documentation https://docs.terality.com/getting-terality/api-reference/write-to-multiple-files
        which should be updated if needed.
        """

        return self._call_method(
            None,
            "to_parquet_folder",
            make_export_request(path, storage_options),
            engine=engine,
            compression=compression,
            index=index,
            partition_cols=partition_cols,
            storage_options=storage_options,
            num_files=num_files,
            num_rows_per_file=num_rows_per_file,
            in_memory_file_size=in_memory_file_size,
            with_leading_zeros=with_leading_zeros,
        )

    def to_dict(self, orient: str = "dict", into: type = dict):
        pd_df = self._call_method(None, "to_pandas")
        return pd_df.to_dict(orient=orient, into=into)

    def info(
        self,
        verbose: Optional[bool] = None,
        max_cols: Optional[int] = None,
        memory_usage: Optional[Union[bool, str]] = None,
        null_counts: Optional[bool] = None,
    ):

        info = self._call_method(
            None,
            "info",
            verbose=verbose,
            max_cols=max_cols,
            memory_usage=memory_usage,
            null_counts=null_counts,
        )
        print(info)

    @classmethod
    def from_pandas(cls, df: pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("DataFrame.from_pandas only accepts a pandas DataFrame parameter.")

        return cls._call(None, "from_pandas", df)

    def items(self):
        # NOTE: If a day we support a huge number of columns, we should retrieve items by batches from server.
        list_of_col_name_and_series = self._call_method(None, "items")
        return iter(list_of_col_name_and_series)

    # Use the same pattern than pandas to provide pot accessor
    plot = CachedAccessor("plot", TeralityPlotAccessor)
