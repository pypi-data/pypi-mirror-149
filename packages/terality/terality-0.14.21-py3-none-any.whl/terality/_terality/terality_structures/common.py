import os
from pathlib import Path
from typing import Optional, Dict

from common_client_scheduler import ExportRequest
from terality.exceptions import TeralityClientError

from terality._terality.data_transmitter import S3


def make_export_request(path: str, storage_options: Optional[Dict] = None) -> ExportRequest:
    if not isinstance(path, str):
        raise TeralityClientError("Export methods only support a str path.")

    if path.startswith("s3://"):
        bucket = path[5:].split("/", maxsplit=1)[0]
        aws_region = S3.client().get_bucket_location(Bucket=bucket)["LocationConstraint"]
        # For the us-east-1 region, this call returns None. Let's fix that.
        # Reference: https://github.com/aws/aws-cli/issues/3864 (the same is observed with boto3)
        if aws_region is None:
            aws_region = "us-east-1"
    elif path.startswith("abfs://"):
        aws_region = None
    else:
        # If path is local, convert it to absolute path
        aws_region = None
        path = _make_absolute_path(path)

    return ExportRequest(path=path, aws_region=aws_region, storage_options=storage_options)


def _make_absolute_path(path: str) -> str:
    # pathlib.Path.resolve() fails on windows when path contains an asterix.
    # An asterix is required in the path tail for the `to_parquet_folder` function.
    # It is enough to resolve only the path head and append the tail.

    # Edge case, path=".": fails if we append a "." to the absolute path. We resolve entire path.
    if path == ".":
        return str(Path(path).resolve())

    path_head, path_tail = os.path.split(path)
    return f"{str(Path(path_head).resolve())}/{path_tail}"
