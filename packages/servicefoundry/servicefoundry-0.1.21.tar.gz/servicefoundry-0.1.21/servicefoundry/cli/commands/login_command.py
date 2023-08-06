import logging

import rich_click as click

from servicefoundry.build import lib
from servicefoundry.build.console import console
from servicefoundry.build.lib.messages import PROMPT_POST_LOGIN
from servicefoundry.cli.util import handle_exception_wrapper

logger = logging.getLogger(__name__)


@click.command()
@handle_exception_wrapper
def login():
    """
    Login to servicefoundry

    \b
    Once logged in, you can initiate a new service with `sfy init`
    and deploy the service with `sfy deploy .`
    """
    # TODO (chiragjn): Add support for non interactive login with API key.
    #                  It is supported indirectly as we always look for `SERVICE_FOUNDRY_API_KEY`
    #                  in the environment
    lib.login(non_interactive=False)
    console.print(PROMPT_POST_LOGIN)


def get_login_command():
    return login
