import os
import sys
from typing import Optional

from terality._terality.sentry import set_user_for_sentry
from .config import TeralityConfig, TeralityCredentials, ConfigError
from .logger import logger


def has_valid_terality_config_file() -> bool:
    try:
        TeralityConfig.load()
        return True
    except ConfigError:
        return False


def has_valid_terality_credentials_file() -> bool:
    try:
        TeralityCredentials.load()
        return True
    except ConfigError:
        return False


def _has_interactive_input() -> bool:
    try:
        return os.isatty(sys.stdin.fileno())
    except (OSError, ValueError):
        return False


def configure(
    email: Optional[str] = None, api_key: Optional[str] = None, overwrite: bool = True
) -> None:
    """Configure the Terality client.

    If interactive input is available, then the user will be prompted for any argument not provided when
    calling the function. Otherwise, this function will raise a ValueError if required arguments are missing.

    This function signature may change in future releases, as Terality implements other authentication
    mecanisms.

    Side effects:
        Write Terality configuration files. May prompt the user for more information, and log diagnostic
        messages.

    Args:
        email: email address of the user account
        api_key: Terality API key. Can be retrieved from https://app.terality.com.
        overwrite: if False, this function will raise an exception instead of overwriting any existing
            configuration files.
    """
    has_config = has_valid_terality_config_file()
    has_credentials = has_valid_terality_credentials_file()
    has_interactive_input = _has_interactive_input()

    if email is None:
        if has_interactive_input:
            email = input("User email: ")
        else:
            raise ValueError("Missing configuration argument: 'email'.")

    if api_key is None:
        if has_interactive_input:
            api_key = input("API key: ")
        else:
            raise ValueError("Missing configuration argument: 'api_key'.")

    if has_config:
        logger.warning(
            f"A Terality configuration file is already present at {TeralityConfig.file_path()}."
        )
    if has_credentials:
        logger.warning(
            f"A Terality credentials file is already present at {TeralityCredentials.file_path()}."
        )

    if (has_config or has_credentials) and not overwrite:
        raise RuntimeError(
            "Terality credentials are already present on this machine (pass `overwrite = True` to ignore)."
        )

    config = TeralityConfig()
    credentials = TeralityCredentials(user_id=email, user_password=api_key)
    config.save()
    credentials.save()

    logger.info("Terality account successfully configured on this system.")
    set_user_for_sentry(user_id=email)
