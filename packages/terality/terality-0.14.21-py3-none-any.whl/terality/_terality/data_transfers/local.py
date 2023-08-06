import hashlib
import os
from pathlib import Path
from typing import List

from common_client_scheduler import AwsCredentials

from terality._terality import global_client
from terality._terality.progress_bar import data_transfer_progress_bar
from terality.exceptions import TeralityClientError


def upload_local_files(path: str, aws_credentials: AwsCredentials, cache_disabled: bool) -> str:
    """
    Copy files from a local directory to a Terality-owned S3 bucket.

    Args:
        path: path to a single file or a directory. If a directory, all files in the directory will be uploaded.
    """
    try:
        if Path(path).is_file():
            file_checksum = _calculate_file_checksum(path)
            file_size = os.path.getsize(path)
            with data_transfer_progress_bar(total_size=file_size, desc=path) as progress_bar:
                global_client().data_transfer().upload_local_file(
                    aws_credentials,
                    path,
                    f"{file_checksum}/{0}.data",
                    cache_disabled,
                    progress_bar,
                )
            return file_checksum

        paths: List[str] = [str(path_) for path_ in sorted(Path(path).iterdir())]
        folder_checksum = _calculate_folder_checksum(paths)
        total_size = sum(os.path.getsize(path_) for path_ in paths)
        with data_transfer_progress_bar(
            total_size=total_size, desc=f"{path} - files count: {len(paths)}"
        ) as progress_bar:
            for file_num, _ in enumerate(paths):
                global_client().data_transfer().upload_local_file(
                    aws_credentials,
                    paths[file_num],
                    f"{folder_checksum}/{file_num}.data",
                    cache_disabled,
                    progress_bar,
                )
        return folder_checksum
    except FileNotFoundError as e:
        raise TeralityClientError(
            f"File '{path}' could not be found in your local directory, please verify the path. If your file is stored on the cloud, make sure your path starts with 's3://', 'abfs://', or 'az://'.",
        ) from e


def _calculate_file_checksum(file_: str) -> str:
    sha512 = hashlib.sha512()
    with open(file_, "rb") as f:
        for chunk in iter(lambda: f.read(4_194_304), b""):
            sha512.update(chunk)
    return sha512.hexdigest()


def _calculate_folder_checksum(paths: List[str]) -> str:
    folder_checksum = ""
    for path_ in paths:
        file_checksum = _calculate_file_checksum(path_)
        folder_checksum = hashlib.sha512(f"{folder_checksum}{file_checksum}".encode()).hexdigest()
    return folder_checksum
