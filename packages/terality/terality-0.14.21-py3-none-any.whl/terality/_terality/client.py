from __future__ import annotations

import base64
import time
from typing import Any, List, Dict, Union, Optional
import threading

from google.protobuf.message import DecodeError

from common_client_scheduler.responses import (
    ExportToAzureBlobStorageResponse,
    CreateUserResponse,
    CreateAnonymousUserResponse,
)
from terality._terality.data_transmitter import DataTransmitter, DataTransmitterS3

from terality.exceptions import TeralityError
from terality._terality.errorreporting import ErrorReporter

from common_client_scheduler.config import (
    SessionInfo,
    SessionInfoLocal,
    SessionInfoType,
    TransferConfig,
    TransferConfigLocal,
)
from common_client_scheduler.requests import (
    FollowUpRequest,
    PandasFunctionRequest,
    ImportFromCloudRequest,
    ExportToCloudRequest,
    StorageService,
    AwsS3PartsExport,
    AzureBlobStoragePartsExport,
    CreateUserRequest,
    AwsPresignedUrlSource,
    ImportFromS3Source,
    AzureBlobSource,
    ImportFromAzureBlobStorageSource,
    AwsS3ObjectPartExportRequest,
    AzureBlobStoragePartExportRequest,
    ObjectStorageKey,
)
from common_client_scheduler.responses import (
    PendingComputationResponse,
    CreateSessionResponse,
    AwsCredentials,
    DataTransferResponse,
    ComputationResponse,
    ImportFromCloudResponse,
    ExportToS3Response,
)
from terality_serde import StructType, IndexType

from .utils.config import CredentialsProvider, TeralityConfig
from .httptransport import HttpTransport


_DEFAULT_PANDAS_OPTIONS = {
    "display": {
        "max_columns": 20,
        "max_colwidth": 50,
        "max_rows": 60,
        "min_rows": 10,
        "show_dimensions": "truncate",
        "width": 80,
        "max_seq_items": 100,
    }
}


class UnconfiguredTeralityClientError(TeralityError):
    pass


class SessionStateError(TeralityError):
    pass


class OptionError(Exception):
    pass


class TeralityClient:  # pylint: disable=too-many-instance-attributes
    """Implement the connectivity with the Terality API.

    This is a stateful class managing authentication and session management. Currently, a single client
    may only have one session active at any given time.

    This client is mostly thread-safe. Several threads can call the `send_request` method concurrently.


    Args:
        http_transport: the underlying HttpTransport used to perform requests.
        auto_session: if True, when no session is currently opened, the TeralityClient will start a new session
            before performing a request.
    """

    # Note: the session management could be split to a separate class, but for now this class
    # is small enough to keep it inline.

    def __init__(self, http_transport: HttpTransport, auto_session: bool = False) -> None:
        self._http_transport = http_transport
        self._session: Optional[SessionInfoType] = None
        self._auto_session = auto_session
        self._credentials_fetcher = _AwsCredentialsFetcher(self)
        self._error_reporter: Optional[ErrorReporter] = None
        self._error_reporter = ErrorReporter(self._http_transport)
        self._data_transfer: DataTransmitter = DataTransmitterS3()
        self._cache_disabled: bool = False
        self._pandas_options: Dict[str, Any] = _DEFAULT_PANDAS_OPTIONS
        self._lock = threading.Lock()

    def set_data_transfer(self, data_transfer: DataTransmitter) -> None:
        """Switch to data transfer implementation (during tests for instance).

        In production use of this class, the default data transfer implementation created by the constructor is enough and there is no need to call this method.
        """
        self._data_transfer = data_transfer

    def cache_disabled(self) -> bool:
        return self._cache_disabled

    def disable_cache(self) -> None:
        self._cache_disabled = True

    def enable_cache(self) -> None:
        self._cache_disabled = False

    def set_pandas_option(self, pat: str, value: Any) -> None:
        # Pattern can contain any number of hierarchies: display.large_repr or display.latex.escape
        with self._lock:
            self._set_option_recursively(pat, value, self._pandas_options)

    def _set_option_recursively(self, pat: str, value: Any, options_dict: Dict[str, Any]) -> None:
        options = pat.split(".")
        if len(options) == 1:
            options_dict[options[0]] = value
        else:
            if options[0] not in options_dict:
                options_dict[options[0]] = {}
            self._set_option_recursively(".".join(options[1:]), value, options_dict[options[0]])

    def get_pandas_option(self, pat: str) -> Any:
        return self._get_option_recursively(pat, self._pandas_options)

    def _get_option_recursively(self, pat: str, options_dict: Dict[str, Any]) -> Any:
        options = pat.split(".")
        try:
            if len(options) == 1:
                return options_dict[options[0]]
            return self._get_option_recursively(".".join(options[1:]), options_dict[options[0]])
        except KeyError as e:
            raise OptionError(f"No such option: {options[0]} exists.") from e

    def get_pandas_options(self) -> Dict[str, Any]:
        return self._pandas_options

    def send_request(self, route: str, payload: Optional[bytes] = None, method="POST") -> bytes:
        with self._lock:
            if self._auto_session and self._session is None:
                self._start_session()

            session_id = self._session.id if self._session is not None else None

        if payload is None:
            payload_b64 = ""
        else:
            payload_b64 = base64.b64encode(payload).decode("utf-8")
        try:
            response_serialized, status_code = self._http_transport.request(
                route,
                payload_b64,
                session_id=session_id,
                method=method,
            )
            # All pending responses should be received with status code 202.
            if status_code == 202:
                response = PendingComputationResponse.parse(response_serialized)
                return self.send_request(
                    "follow_up",
                    FollowUpRequest(function_id=response.pending_computation_id).serialize(),
                )
            return response_serialized
        except Exception as e:
            if self._error_reporter is not None:
                self._error_reporter.report_exception_noexcept(e)
            raise

    def export_replay_data(self, bucket: str, key: str) -> ObjectStorageKey:
        serialized_response = self.send_request(
            "export_replay_data",
            ObjectStorageKey(bucket, key).serialize(),
            method="POST",
        )
        return ObjectStorageKey.parse(serialized_response)

    def replay(self, bucket: str, key: str) -> ComputationResponse:
        serialized_response = self.send_request(
            "replay",
            ObjectStorageKey(bucket, key).serialize(),
            method="POST",
        )
        return ComputationResponse.parse(serialized_response)

    def create_anonymous_user(self) -> CreateAnonymousUserResponse:
        serialized_response = self.send_request(
            "anonymous_users",
            method="POST",
        )
        return CreateAnonymousUserResponse.parse(serialized_response)

    def create_user(
        self,
        email: str,
        user_accepted_privacy_policy: bool,
        user_accepted_terms_of_service: bool,
        company: str,
        full_name: str,
    ) -> CreateUserResponse:
        serialized_response = self.send_request(
            "users/",
            CreateUserRequest(
                email=email,
                user_accepted_privacy_policy=user_accepted_privacy_policy,
                user_accepted_terms_of_service=user_accepted_terms_of_service,
                company=company,
                full_name=full_name,
            ).serialize(),
            method="POST",
        )
        return CreateUserResponse.parse(serialized_response)

    def _export_to_cloud(self, request: ExportToCloudRequest) -> bytes:
        return self.send_request(
            "exports/cloud",
            request.serialize(),
            method="POST",
        )

    def export_to_azure(
        self, parts: List[AzureBlobStoragePartExportRequest]
    ) -> ExportToAzureBlobStorageResponse:
        serialized_response = self._export_to_cloud(
            ExportToCloudRequest(
                service=StorageService.AZURE_BLOB_STORAGE,
                export_request=AzureBlobStoragePartsExport(parts),
            ),
        )
        return ExportToAzureBlobStorageResponse.parse(serialized_response)

    def export_to_s3(
        self, presigned_urls: List[AwsS3ObjectPartExportRequest]
    ) -> ExportToS3Response:
        serialized_response = self._export_to_cloud(
            ExportToCloudRequest(
                service=StorageService.AWS_S3, export_request=AwsS3PartsExport(parts=presigned_urls)
            ),
        )
        return ExportToS3Response.parse(serialized_response)

    def _import_from_cloud(self, request: ImportFromCloudRequest) -> ImportFromCloudResponse:
        serialized_response = self.send_request("imports/cloud", request.serialize(), method="POST")
        return ImportFromCloudResponse.parse(serialized_response)

    def import_from_azure(self, objects: List[AzureBlobSource]) -> ImportFromCloudResponse:
        request = ImportFromCloudRequest(
            service=StorageService.AZURE_BLOB_STORAGE,
            source=ImportFromAzureBlobStorageSource(objects=objects),
        )
        return self._import_from_cloud(request)

    def import_from_s3(
        self, pre_signed_urls: List[AwsPresignedUrlSource]
    ) -> ImportFromCloudResponse:
        request = ImportFromCloudRequest(
            service=StorageService.AWS_S3,
            source=ImportFromS3Source(presigned_urls=pre_signed_urls),
            cache_disabled=self.cache_disabled(),
        )
        return self._import_from_cloud(request)

    def compute_pandas(
        self,
        function_type: Union[StructType, IndexType],
        function_prefix: Optional[str],
        function_name: str,
        args_encoded: str,
        kwargs_encoded: str,
    ) -> ComputationResponse:
        request = PandasFunctionRequest(
            function_type=function_type,
            function_accessor=function_prefix,
            function_name=function_name,
            cache_disabled=self.cache_disabled(),
            pandas_options=self.get_pandas_options(),
            args=args_encoded,
            kwargs=kwargs_encoded,
        )
        serialized_response = self.send_request("compute", request.serialize(), method="POST")
        return ComputationResponse.parse(serialized_response)

    def _start_session(self):
        """Start a session.

        Before processing data, the client must start a session. The data created during the session is bound
        to the session: when the session is closed, the data is garbage collected. Most API calls that deal
        with data processing require an open session.

        Raise:
            SessionStateError: if a session is already in progress
        """
        if self._session is not None:
            raise SessionStateError("A session is already opened on this client.")

        session_serialized, _ = self._http_transport.request("create_session", payload_b64="")
        try:
            session = CreateSessionResponse.parse(session_serialized)
        except DecodeError as e:
            raise RuntimeError("Unexpected server response type, expected SessionInfo.") from e

        if isinstance(session.upload_config, TransferConfigLocal) and isinstance(
            session.download_config, TransferConfigLocal
        ):
            self._session = SessionInfoLocal(
                id=session.id,
                upload_config=session.upload_config,
                download_config=session.download_config,
            )
        elif isinstance(session.upload_config, TransferConfig) and isinstance(
            session.download_config, TransferConfig
        ):
            self._session = SessionInfo(
                id=session.id,
                upload_config=session.upload_config,
                download_config=session.download_config,
            )
        else:
            raise ValueError(
                "Can't create a session with the following transfer config types: upload={type(session.upload_config)} and download={type(session.download_config)}"
            )

    def data_transfer(self) -> DataTransmitter:
        """Return a helper class to perform data transfers.

        A "data transfer" means serialization/deserialization of pandas and numpy structures.
        """
        with self._lock:
            if self._session is None and self._auto_session is True:
                self._start_session()
            self._data_transfer.set_current_session(self._session)
            return self._data_transfer

    def get_aws_credentials(self) -> AwsCredentials:
        """Return AWS credentials that can be used to upload files to the AWS API.

        Don't cache these credentials anywhere as they have a short lifetime. This method already perfoms
        the necessary caching.
        """
        return self._credentials_fetcher.get_credentials()

    def close_session(self):
        """Close the current session, if any.

        If no session is in progress, this method is a no-op.
        """
        with self._lock:
            if self._session is None:
                return

            self._http_transport.request("delete_session", "", session_id=self._session.id)
            self._session = None


def make_client(allow_anonymous=True) -> TeralityClient:
    """Try to read the Terality configuration files, and return a configured TeralityClient from them.

    Args:
        allow_anonymous: if True, allow unauthenticated requests to the API. Anonymous clients don't require
            configuration files (unlike authenticated clients, which will raise exceptions if no
            configuration files are present).

    Raise:
        ConfigError: if the client credentials could not be loaded, and allow_anonymous is False

    See:
        unconfigured_client
    """

    config = TeralityConfig.load(fallback_to_defaults=True)
    credentials_provider = CredentialsProvider(
        init_with_credentials=False, allow_anonymous=allow_anonymous
    )

    http_transport = HttpTransport(
        base_url=config.full_url(),
        request_timeout=config.timeout,
        credentials_provider=credentials_provider,
    )
    return TeralityClient(http_transport, auto_session=not allow_anonymous)


def anonymous_client() -> TeralityClient:
    """Return a Terality client that won't error if no credentials are present.

    See:
        make_client
    """
    return make_client(allow_anonymous=True)


def client_from_config() -> TeralityClient:
    """Return a Terality client that will raise an exception when making a request if no credentials are present.

    See:
        make_client
    """
    return make_client(allow_anonymous=False)


class _AwsCredentialsFetcher:
    """Small utility to lazily fetch temporary AWS credentials from the Terality API.

    `get_credentials` will fetch credentials on the first call, and cache the result.

    Those credentials are used to upload files to Terality-owned S3 buckets.

    This class is thread-safe.
    """

    def __init__(self, client: TeralityClient) -> None:
        self._credentials: Optional[AwsCredentials] = None
        self._credentials_fetched_at = time.monotonic()
        self._client = client
        self._lock = threading.Lock()

    def get_credentials(self) -> AwsCredentials:
        with self._lock:
            if (
                self._credentials is None
                or time.monotonic() > self._credentials_fetched_at + 30 * 60
            ):
                self._fetch_credentials()
            assert self._credentials is not None
            return self._credentials

    def _fetch_credentials(self) -> None:
        res = DataTransferResponse.parse(self._client.send_request("transfers"))
        self._credentials = res.temporary_upload_aws_credentials
        self._credentials_fetched_at = time.monotonic()
