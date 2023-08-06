import functools
import zipfile

import rich_click as click
from questionary import Choice
from requests.exceptions import ConnectionError
from rich.padding import Padding
from rich.panel import Panel

from servicefoundry.build.console import console

from ..build.exceptions import BadRequestException, ConfigurationException
from .const import IS_DEBUG


def handle_exception(exception):
    if isinstance(exception, BadRequestException):
        print_error(
            f"[cyan bold]status_code[/] {exception.status_code}\n"
            f"[cyan bold]message[/]     {exception.message}"
        )
    elif isinstance(exception, ConnectionError):
        print_error(f"Couldn't connect to Servicefoundry.")
    elif isinstance(exception, ConfigurationException):
        print_error(f"[cyan bold]message[/]     {exception.message}")
    else:
        if IS_DEBUG:
            console.print_exception()
        else:
            console.print(exception)


def handle_exception_wrapper(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            handle_exception(e)

    return inner


def print_error(message):
    text = Padding(message, (0, 1))
    console.print(
        Panel(
            text,
            border_style="red",
            title="Command failed",
            title_align="left",
            width=click.rich_click.MAX_WIDTH,
        )
    )


def print_message(message):
    text = Padding(message, (0, 1))
    console.print(
        Panel(
            text,
            border_style="cyan",
            title="Success",
            title_align="left",
            width=click.rich_click.MAX_WIDTH,
        )
    )


def unzip_package(path_to_package, destination):
    with zipfile.ZipFile(path_to_package, "r") as zip_ref:
        zip_ref.extractall(destination)


def get_space_choices(client):
    spaces = client.list_workspace()
    space_choices = [
        Choice(title=space["name"], value=space)
        for space in spaces
        if space["status"] == "CREATE_SPACE_SUCCEEDED"
    ]
    return space_choices
