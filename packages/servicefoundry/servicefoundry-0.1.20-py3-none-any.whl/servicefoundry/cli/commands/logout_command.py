import logging

import rich_click as click

from servicefoundry.build import lib
from servicefoundry.cli.util import handle_exception_wrapper

logger = logging.getLogger(__name__)


@click.command()
@handle_exception_wrapper
def logout():
    """
    Logout servicefoundry session
    """
    lib.logout()


def get_logout_command():
    return logout
