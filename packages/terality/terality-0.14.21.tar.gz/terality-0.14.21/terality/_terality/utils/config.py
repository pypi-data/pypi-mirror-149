from dataclasses import dataclass
import os
from typing import Optional, Type, TypeVar

from abc import ABC
from pathlib import Path
from typing import ClassVar, Tuple
from json import JSONDecodeError

from pydantic import (
    BaseModel,
    BaseSettings,
    Field,
    ValidationError,
)  # pylint: disable=no-name-in-module


class _Paths(BaseSettings):
    terality_home: Path = Field(Path.home() / ".terality", env="TERALITY_HOME")


T = TypeVar("T", bound="BaseConfig")


class ConfigError(Exception):
    """Could not read a Terality configuration file.

    The string representation of instances of this exception (str(e)) is a user-facing, actionable message.
    """


class BaseConfig(BaseModel, ABC):
    """Base abstract class for configuration objects that can be stored in configuration files."""

    _rel_path: ClassVar[str]  # path to the configuration file relative to `$TERALITY_HOME`
    _permissions: ClassVar[int] = 0o644  # rw-r--r--

    @classmethod
    def file_path(cls) -> Path:
        return _Paths().terality_home / cls._rel_path

    @classmethod
    def load(cls: Type[T], fallback_to_defaults: bool = False) -> T:
        """Load the configuration object from the underlying file.

        Args:
            fallback_to_defaults: if True, return a default configuration file when the file does
                not already exists, or if any error occurs when reading it

        Return:
            a configuration object

        Raise:
            Exception: if the file can not be found (when fallback_to_defaults is False)
        """
        file_path = cls.file_path()
        try:
            return cls.parse_file(file_path)
        except ValidationError as e:
            if fallback_to_defaults:
                return cls()
            raise ConfigError(
                "Could not read a Terality configuration file: "
                f"{cls.file_path()} contains invalid values. "
                "Please configure the Terality client (more info at https://docs.terality.com)."
            ) from e
        except JSONDecodeError as e:
            if fallback_to_defaults:
                return cls()
            raise ConfigError(
                "Could not read a Terality configuration file: "
                f"{cls.file_path()} does not contain valid JSON. "
                "Please configure the Terality client (more info at https://docs.terality.com)."
            ) from e
        except PermissionError as e:
            if fallback_to_defaults:
                return cls()
            raise ConfigError(
                "Could not read a Terality configuration file: "
                f"permission denied when reading {cls.file_path()}. "
                "Grant the current user permissions to read this file."
            ) from e

        except FileNotFoundError as e:
            if fallback_to_defaults:
                return cls()
            raise ConfigError(
                "Could not read a Terality configuration file: "
                f"{cls.file_path()} does not exist. "
                "Please configure the Terality client (more info at https://docs.terality.com)."
            ) from e

    def save(self) -> None:
        file_path = self.file_path()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(
            os.open(file_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode=self._permissions),
            "w",
        ) as f:
            f.write(self.json(indent=4))


class TeralityCredentials(BaseConfig):
    """User authentication information."""

    _rel_path: ClassVar[str] = "credentials.json"
    _permissions: ClassVar[int] = 0o600  # rw-------
    user_id: str  # Client-facing user ID (probably an email). Note that the "server user ID" is different.
    user_password: str  # API key or similar


_PRODUCTION_URL = "api.terality2.com/v1"


class TeralityConfig(BaseConfig):
    """Generic configuration related to the Terality API.

    The default values are suitable for the production SaaS environment.
    """

    _rel_path: ClassVar[str] = "config.json"
    version: str = "1"
    url: str = _PRODUCTION_URL
    use_https: bool = True
    timeout: Tuple[int, int] = (3, 35)  # The server has a max 30s timeout on responses.

    # Legacy - the URL parameter should contain everything, but we don't want to invalidate all
    # existing configuration files, nor (for now) deal with multiple configuration versions.
    def full_url(self):
        prefix = "https" if self.use_https else "http"
        return f"{prefix}://{self.url}"

    @property
    def is_production(self) -> bool:
        return self.url == _PRODUCTION_URL


@dataclass
class AuthCredentials:
    user: str
    password: str


class CredentialsProvider:
    """Load and return Terality credentials.

    For now, only return credentials loaded from a configuration file. Later on, we may implement other
    credentials loading strategies.

    Args:
        init_with_credentials: if True, refresh credentials when the instance is created.
        allow_anonymous: if True, this class won't raise a ConfigError when credentials can't be loaded,
            and will instead return None when credentials are requested.
    """

    def __init__(self, init_with_credentials: bool = False, allow_anonymous: bool = False):
        self._auth_credentials: Optional[AuthCredentials] = None
        self._allow_anonymous = allow_anonymous
        if init_with_credentials:
            self.refresh_credentials()

    def get_credentials(self, refresh: bool = False) -> Optional[AuthCredentials]:
        """Return Terality user credentials.

        Credentials will be loaded from the environment or configuration files if:
        * no credentials are currently loaded; or
        * refresh is set to True.
        Otherwise, the currently loaded credentials will be returned.

        Args:
            refresh: if True, credentials will be reloaded before being returned (as per `refresh_credentials`)

        Return:
            credentials, or None if no credentials could be loaded from the enviroment or configuration files

        Raise:
            ConfigError: if refresh = True but no credentials could be found
        """
        if refresh or self._auth_credentials is None:
            self.refresh_credentials()
        return self._auth_credentials

    def refresh_credentials(self) -> None:
        """Refresh the credentials provided by this instance.

        Raise:
            ConfigError: if no credentials could be found and `allow_anonymous` was set False on this instance.
        """
        try:
            config = TeralityCredentials.load()
            self._auth_credentials = AuthCredentials(
                user=config.user_id, password=config.user_password
            )
            return None
        except ConfigError:
            self._auth_credentials = None
            if self._allow_anonymous:
                return None
            raise
