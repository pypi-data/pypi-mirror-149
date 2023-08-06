from functools import partial

from common_client_scheduler import ObjectStorageKey, ComputationResponse
from terality._terality.encoding import decode

from terality._terality.globals import global_client
from terality.exceptions import TeralityError
from terality_serde import apply_func_on_object_recursively


def replay(bucket: str, key: str):
    """Helper to replay an API call stored in a S3 dump file.

    This function is internal to Terality, and is exposed here to help Terality engineers investigate CI
    and production failures.
    """
    response = global_client().replay(bucket, key)

    if not isinstance(response, ComputationResponse):
        raise TeralityError(
            f"Received unexpected response type (expected ComputationResponse): {response}"
        )

    result = response.result
    result = apply_func_on_object_recursively(
        result, partial(decode, global_client().get_aws_credentials())
    )
    return result


def export_replay_data(bucket: str, key: str) -> ObjectStorageKey:
    """Helper to replay an API call stored in a S3 dump file.

    This function is internal to Terality, and is exposed here to help Terality engineers investigate CI
    and production failures.
    """
    return global_client().export_replay_data(bucket, key)
