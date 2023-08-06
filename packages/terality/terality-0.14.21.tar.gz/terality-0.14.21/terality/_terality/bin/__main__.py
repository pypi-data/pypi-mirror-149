"""Main entry point for the Terality command line interface."""
# Important: we support very old versions of click for compatibility (down to 3.2). Ensure that you're not
# using any recent feature here.
from terality._terality.client import anonymous_client
import click

from common_client_scheduler.responses import CreateUserResponse
from terality._terality.sentry import set_user_for_sentry
from terality._terality.utils.account import (
    has_valid_terality_config_file,
    has_valid_terality_credentials_file,
)
from terality._terality.utils.config import TeralityConfig, TeralityCredentials, ConfigError


@click.group(
    help="This is the Terality command line interface. Documentation is available at https://docs.terality.com.",
    epilog="Terality is currently beta-quality software. For any support question, please write to support@terality.com.",
)
def cli():
    pass


@cli.group(name="account", short_help="Account management utilities.")
def account():
    pass


@account.command(
    name="create",
    short_help="Register a new Terality account.",
    help="Create a free Terality account. We recommend using https://app.terality.com/ instead, as it will provide better account management features. This command may be removed in future Terality versions.",
)
@click.option(
    "--email", prompt="Your email address", confirmation_prompt="Please confirm your email address"
)
@click.option(
    "--full-name", prompt="Your full name (optional)", default="", help="Your full name (optional)."
)
@click.option(
    "--company",
    prompt="Your company name (optional)",
    default="",
    help="Your company name (optional).",
)
@click.option(
    "--skip-configuration", help="Do not create a Terality configuration file.", is_flag=True
)
def account_create(email: str, full_name: str, company: str, skip_configuration: bool):
    click.echo("")
    click.echo(
        "To continue, you must read and accept the Terality Terms of Service, available at https://www.terality.com/terms, and the Terality Privacy Policy, available at https://www.terality.com/privacy."
    )
    click.echo("Enter 'y' to indicate that you accept these terms.")
    click.confirm("Do you accept the Terality Terms of Service?", abort=True, default=True)
    click.confirm("Do you accept the Terality Privacy Policy?", abort=True, default=True)

    click.echo("")
    click.echo("Your account information:")
    click.echo("")
    click.echo(f"Email: {email}")
    if full_name:
        click.echo(f"Full name: {full_name}")
    if company:
        click.echo(f"Company name: {company}")
    click.echo("")

    click.confirm("Confirm and create account?", abort=True, default=True)

    client = anonymous_client()
    res = client.create_user(
        email=email,
        user_accepted_privacy_policy=True,
        user_accepted_terms_of_service=True,
        company=company,
        full_name=full_name,
    )
    if not isinstance(
        res, CreateUserResponse
    ):  # TODO: this validation should be handled at the deserialization level
        raise ValueError(
            f"Unexpected server answer: expected type 'CreateUserResponse', got '{type(res)}'"
        )

    click.echo("")
    click.echo("Congratulations! Your Terality account has been created.")
    click.echo("Your API key is: ")
    click.echo("")
    click.echo("    " + res.api_key)
    click.echo("")
    click.echo(
        "Keep it in a safe place (such as your password manager). If you lose it, please reach out to support@terality.com to renew it."
    )
    click.echo("")

    if not skip_configuration:
        _write_terality_configuration(email, res.api_key)
        click.echo(
            f"Your Terality credentials have been automatically written to {TeralityCredentials.file_path()}. "
            "You can now start using Terality!"
        )

    click.echo("For documentation and resources, go to https://docs.terality.com.")


# TODO: add default from configuration files (show_default and default options in click)
# but this requires cleaning up the config classes beforehand.
@account.command(
    name="configure",
    short_help="Configure this system to use your Terality account",
    help="Create the Terality configuration files on this system. It's recommended not to provide the --api-key flag on the command line, and enter it interactively instead, to avoid leaking it in your shell history.",
)
@click.option(
    "--email",
    prompt="Your email address",
    help="Email address associated with the Terality account.",
)
@click.option("--api-key", prompt="Your Terality API key", help="Terality API key.")
@click.option(
    "--overwrite", help="Overwrite existing configuration files without confirmation.", is_flag=True
)
def account_configure(email: str, api_key: str, overwrite: bool):
    has_config = has_valid_terality_config_file()
    has_credentials = has_valid_terality_credentials_file()

    if has_config:
        _print_warning(
            f"A Terality configuration file is already present at {TeralityConfig.file_path()}."
        )
    if has_credentials:
        _print_warning(
            f"A Terality credentials file is already present at {TeralityCredentials.file_path()}."
        )

    if (has_config or has_credentials) and not overwrite:
        click.confirm(
            "Are you sure you want to overwrite the existing Terality configuration?", abort=True
        )

    config = TeralityConfig()
    credentials = TeralityCredentials(user_id=email, user_password=api_key)
    config.save()
    credentials.save()

    click.echo("Terality account successfully configured on this system.")
    set_user_for_sentry(user_id=email)


@account.command(
    name="info",
    short_help="Display the current Terality configuration.",
    help="Display the Terality configuration on this system.",
)
def account_info():
    try:
        config = TeralityConfig().load()
        config_is_available = True
        config_error_message = None
    except ConfigError as e:
        config = None
        config_is_available = False
        config_error_message = str(e)
    try:
        credentials = TeralityCredentials.load()
        credentials_are_available = True
        credentials_error_message = None
    except ConfigError as e:
        credentials = None
        credentials_are_available = False
        credentials_error_message = str(e)

    if config_error_message is not None:
        _print_warning(config_error_message)
    if credentials_error_message is not None:
        _print_warning(credentials_error_message)

    if not config_is_available or not credentials_are_available:
        click.echo("You can configure your Terality account by running:")
        click.echo("")
        click.echo("    terality account configure")
        click.echo("")
        return

    assert config is not None
    assert credentials is not None
    click.echo("Account")
    click.echo(f"    User email: {credentials.user_id}")
    click.echo("    User API key: <hidden>")
    click.echo("")
    click.echo("Advanced")
    click.echo(
        f"    Configuration files: {TeralityConfig.file_path()}, {TeralityCredentials.file_path()}"
    )
    click.echo(f"    Terality instance (API URL): {config.full_url()}")


def _print_warning(message: str):
    click.echo(click.style("WARNING:", fg="yellow") + " " + message)


def _write_terality_configuration(email: str, api_key: str):
    credentials = TeralityCredentials(user_id=email, user_password=api_key)
    credentials.save()
    config = TeralityConfig()
    config.save()


if __name__ == "__main__":
    cli()
