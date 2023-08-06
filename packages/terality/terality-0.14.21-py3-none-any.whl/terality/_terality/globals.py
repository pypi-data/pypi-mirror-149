"""This module defines global instances created when importing Terality.

Importing the terality module should have as few side-effects as possible, and they should not
occur outside of the module.
"""
import atexit
import os

import requests

from terality.exceptions import TeralityError
from terality.version import __version__
from .client import (
    TeralityClient,
    client_from_config,
)
from .constants import ENV_PROD, ENV_UNKNOWN
from .utils import logger, TeralityConfig
import logging
from .utils.config import TeralityCredentials, ConfigError
from .sentry import set_up_sentry


def _latest_version_from_pypi() -> str:
    root_package_name = __name__.split(".")[0]
    r = requests.get(f"https://pypi.org/pypi/{root_package_name}/json")
    r.raise_for_status()
    return r.json()["info"]["version"]


def _print_warning_if_not_latest_version() -> None:
    try:
        # Don't perform useless network requests during tests
        if "PYTEST_CURRENT_TEST" in os.environ:
            return
        latest = _latest_version_from_pypi()
        if latest != __version__:
            logger.warning(
                f"You are using version {__version__} of the Terality client, but version {latest} is available. "
                "Consider upgrading your version to get the latest fixes and features."
            )
    except Exception:  # pylint:disable=broad-except  # nosec
        # If any error occurs, don't write a stack trace, just swallow the exception.
        pass


def _configure_logger() -> None:
    # Add configuration to the root logger if not configured.
    # Handlers are added on the root logger instead of the terality logger because it
    # is easier for the advanced user to modify them, and can be considered a reasonable default.
    if len(logging.getLogger().handlers) == 0:
        logging.basicConfig()

    # Logging level is set on the terality logger to not interfere with log messages form other libraries.
    # Logging level is defaulted to INFO to show important messages for first-time users, i.e. caching.
    logger.setLevel(logging.INFO)


def _atexit_delete_session():
    """Try to close the current global session, using a best effort policy. Swallow any Terality exception."""
    try:
        global_client().close_session()
    except TeralityError:
        pass  # nosec: B110 (try_except_pass)


def global_client() -> TeralityClient:
    """Return a preconfigured Terality client.

    If no configuration is available on the system running Terality code, then this client may not be configured.
    In that case, any attempt to call a method on the client will raise an exception.

    This global Terality client is defined in order to hide the existence of a TeralityClient class to
    the user.

    Code in the Terality module can also manually instantiate a TeralityClient with a different
    configuration when required. For instance, an anonymous client (without credentials) can be useful
    for some requests. The `terality._terality.client` moduule contains several helpers to do
    just that.
    """
    return _GLOBAL_CLIENT


def _init_sentry():
    config = TeralityConfig().load(fallback_to_defaults=True)
    environment = ENV_PROD if config.is_production else ENV_UNKNOWN
    try:
        creds = TeralityCredentials.load()
        user_id = creds.user_id
    except ConfigError:
        user_id = None

    set_up_sentry(environment=environment, release=__version__, user_id=user_id)


# Importing the Terality module has some side-effects, defined below.
# This is a consequence of sticking to the pandas API: we can't require the user to manually instantiate a
# "client" class or similar.

_init_sentry()
_print_warning_if_not_latest_version()
_configure_logger()
_GLOBAL_CLIENT = client_from_config()
# Try to replace the _GLOBAL_CLIENT variable with a configured client at module import time.
atexit.register(_atexit_delete_session)
