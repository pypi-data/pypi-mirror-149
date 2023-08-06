import inspect
from functools import partial
from typing import Union
from pathlib import Path

import pandas as pd

from common_client_scheduler.read_top_level_functions import (
    read_top_level_functions_to_path_parameter,
)

from common_client_scheduler import UploadRequest, ImportFromCloudRequest
from terality import api

from terality_serde import StructType

from . import call_pandas_function

from ..data_transfers.s3 import _get_import_request_from_s3_path

from terality._terality.patch_libs.patch_pandas_and_numpy import np_funcs_names_to_internal_names
from ..utils.azure import parse_azure_filesystem, test_for_azure_libs
from ...exceptions import TeralityClientError, TeralityError

from terality._terality.globals import global_client
from terality._terality.data_transfers import upload_local_files
from terality._terality.utils import logger

_READ_SQL_LOCAL_CHUNK_SIZE = 100_000


def _get_upload_or_import_request_from_path(
    path: Union[str, Path], storage_options
) -> Union[ImportFromCloudRequest, UploadRequest]:
    """
    Converts the path parameter of the read_* function to either:
    - an UploadRequest, if the path is to a local file
    - an ImportFromCloudRequest, if the path is to a cloud storage (AWS, or Azure).
    """
    path_str = str(path) if isinstance(path, Path) else path
    if path_str.startswith("s3://"):
        parts = path_str[len("s3://") :].split("/", 1)
        if len(parts) != 2:
            raise ValueError(
                f"Invalid S3 path, expected format: 's3://bucket/prefix' (prefix may be the empty string), got: '{path}'."
            )
        return _get_import_request_from_s3_path(s3_bucket=parts[0], s3_key_prefix=parts[1])

    if path_str.startswith("abfs://") or path_str.startswith("az://"):
        test_for_azure_libs()
        from ..data_transfers.azure import get_import_request_from_azure_storage_files

        storage_account_name, container, folder = parse_azure_filesystem(path_str, storage_options)
        return get_import_request_from_azure_storage_files(storage_account_name, container, folder)

    if path_str.startswith("gs://"):
        raise TeralityClientError(
            "Currently, Terality does not support GCP storage. Please use AWS S3 or Azure paths."
        )

    transfer_id = upload_local_files(
        path_str, global_client().get_aws_credentials(), global_client().cache_disabled()
    )
    return UploadRequest(path=path_str, transfer_id=transfer_id)


def _treat_read_job(method_name, *args, **kwargs):
    """Special job to intercept file arguments and upload them to Terality for pd.read_xxx() jobs"""
    storage_options = kwargs.get("storage_options")
    path_parameter_name = read_top_level_functions_to_path_parameter[method_name]
    if path_parameter_name in kwargs:
        kwargs[path_parameter_name] = _get_upload_or_import_request_from_path(
            kwargs[path_parameter_name], storage_options
        )
    else:
        if len(args) == 0:
            raise TypeError(
                f"{method_name}() missing 1 required positional argument: '{path_parameter_name}'"
            )
        path, *others = args
        args = [_get_upload_or_import_request_from_path(path, storage_options)] + others
    return call_pandas_function(StructType.TOP_LEVEL, None, method_name, *args, **kwargs)


_read_sql_supported_method_name_to_pandas_method = {
    "read_sql": pd.read_sql,
    "read_sql_table": pd.read_sql_table,
    "read_sql_query": pd.read_sql_query,
}


def _treat_read_sql_locally(method_name: str, *args, **kwargs):

    te_df_chunks = [
        call_pandas_function(StructType.DATAFRAME, None, "from_pandas", pd_df_chunk)
        # chunksize is chosen arbitrarily
        for pd_df_chunk in _read_sql_supported_method_name_to_pandas_method[method_name](
            chunksize=_READ_SQL_LOCAL_CHUNK_SIZE, *args, **kwargs
        )
    ]

    return call_pandas_function(
        StructType.TOP_LEVEL,
        None,
        "concat",
        te_df_chunks,
    )


def _treat_read_sql_job(method_name: str, *args, **kwargs):
    """
    Handles the read_sql top level functions.
    Checks if the connection parameter is a string, and thus serializable by Terality. If so,
    the query will be sent to the engine to be treated. Otherwise, it will be treated locally,
    by chunks, and the results will be concatenated.
    If the engine fails for connection issues, it falls back to the local implementation.
    """
    if "con" in kwargs:
        conn_parameter = kwargs["con"]
    else:
        if len(args) < 2:
            raise TypeError(f"{method_name}() missing at least 1 required positional argument")
        conn_parameter = args[1]

    if isinstance(conn_parameter, str):
        try:
            # Send the read_sql function to server only if the connection parameter
            # can be serialized, string in this case.
            return call_pandas_function(StructType.TOP_LEVEL, None, method_name, *args, **kwargs)
        except TeralityError:
            logger.warning(
                "read_sql could not be executed on our engine, retrying it locally (this might take some time)..."
            )
    else:
        logger.warning(
            f"read_sql connection parameter of type {type(conn_parameter)} is not serializable. SQL import will be treated locally (this might take some time)..."
        )

    return _treat_read_sql_locally(method_name, *args, **kwargs)


_unsupported_functions_requiring_sql_conn = {
    "to_sql",
}


# Even if for now the `read_xxx` function are the only one to be reimplemented by Terality,
# they have a very specific path in the code.
# Should we add any new top level function in the future, it can be implemented very differently
# than a "read_xxx" function.
# Make this clear by already having two concepts: generic "top level functions" whose only instances
# for now are the read functions.
top_level_functions = list(read_top_level_functions_to_path_parameter)


def get_dynamic_top_level_attribute(attribute: str):  # pylint: disable=too-many-return-statements
    """Return the Terality or pandas module attribute with the given name.

    This function is intended to be the implementation of `__getattr__` (not `__getattribute__`) for the
    Terality module.

    When a user tries to access an attribute on the `terality` module that's not exported through the usual means,
    such as:

    >>> import terality as pd
    >>> df = pd.Something()

    then we use `_get_top_level_attribute` to dynamically resolve the `pd.Something` name.

    Note that data structures such as `pd.DataFrame` are exported in the `__init__` file of the Terality module
    and as such are never resolved through this function. Python only calls `__getattr__` when it can't resolve
    a name otherwise.

    The name resolution logic we use is:
    0. check that the pandas module defines the name. If not, raise an AttributeError
    1. intercept functions that need special client processing (such as read_csv, read_parquet...)
    2. if it's a class in pandas (`pd.Timestamp`), then return the pandas class
    3. if it's a module in pandas (`pd.tseries`), then return the pandas module
    4. otherwise, assume that it's a function, and send it to the Terality API

    In the future, we may implement an allowlist of functions to be locally executed by pandas (it could
    be sent by the server at session creation for instance).
    """

    if attribute == "api":
        return api

    # Check if the attribute is defined by the pandas library. If not, this line will raise an AttributeError.
    try:
        pd_attr = getattr(pd, attribute)
    except AttributeError:
        pd_attr = None
        # To support external libs, we need to override some top level numpy methods by their internal terality version.
        # Check whether the attribute corresponds to a numpy method we internally support, thus not part of pandas API.
        # We do not use standard method names as we do not want to have these methods public.
        if attribute not in np_funcs_names_to_internal_names.values():
            raise

    # Send class and module calls to the pandas module
    if inspect.isclass(pd_attr) or inspect.ismodule(pd_attr):
        return pd_attr

    # Special cases for NaT and NA
    if attribute == "NaT":
        return pd.NaT
    if attribute == "NA":
        return pd.NA

    if attribute in _unsupported_functions_requiring_sql_conn:
        error_msg = f"Function {attribute} is not supported."
        if attribute.startswith("read_"):
            error_msg += (
                " Please reach out to support@terality.com if you’d like us to find a workaround for your use case. "
                "Instead, you can also convert your data into csv or parquet and use te.read_csv or te.read_parquet."
            )
        raise TeralityError(error_msg)

    if attribute in _read_sql_supported_method_name_to_pandas_method:
        return partial(_treat_read_sql_job, attribute)

    # Intercept functions that need special handling (for now, only the "read_xxx" family of functions).
    if attribute in read_top_level_functions_to_path_parameter:
        return partial(_treat_read_job, attribute)

    # Send anything else to the Terality API
    return partial(call_pandas_function, StructType.TOP_LEVEL, None, attribute)
