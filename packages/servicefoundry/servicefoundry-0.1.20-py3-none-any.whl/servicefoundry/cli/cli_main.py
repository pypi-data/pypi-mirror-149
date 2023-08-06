import rich_click as click

from servicefoundry.cli.version import __version__

from .config import CliConfig
from .const import MAX_WIDTH

click.rich_click.STYLE_ERRORS_SUGGESTION = "blue italic"
click.rich_click.MAX_WIDTH = MAX_WIDTH
click.rich_click.USE_RICH_MARKUP = True

from servicefoundry.cli.commands import (
    get_create_command,
    get_deploy_command,
    get_get_command,
    get_init_command,
    get_list_command,
    get_login_command,
    get_logout_command,
    get_remove_command,
    get_set_command,
)


def create_service_foundry_cli():
    """Generates CLI by combining all subcommands into a main CLI and returns in
    Returns:
        function: main CLI functions will all added sub-commands
    """
    _cli = service_foundry_cli
    _cli.add_command(get_init_command())
    _cli.add_command(get_deploy_command())
    _cli.add_command(get_login_command())
    _cli.add_command(get_get_command())
    _cli.add_command(get_list_command())
    _cli.add_command(get_remove_command())
    _cli.add_command(get_create_command())
    _cli.add_command(get_logout_command())
    _cli.add_command(get_set_command())
    return _cli


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option("--json", is_flag=True)
@click.option("--logs", is_flag=True)
@click.version_option(__version__)
def service_foundry_cli(json, logs):
    """
    Servicefoundry provides an easy way to deploy your code as a web service.

    \b
    To start, login to your truefoundry account with

    \b
    `sfy login`

    \b
    Once logged in, start a new service with

    \b
    `sfy init`
    """
    CliConfig.set("json", json)
    CliConfig.set("logs", logs)
