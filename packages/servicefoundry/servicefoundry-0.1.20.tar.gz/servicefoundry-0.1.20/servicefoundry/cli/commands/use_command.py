import logging

import questionary
import rich_click as click

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.console import console
from servicefoundry.build.util import set_cluster_in_context, set_workspace_in_context
from servicefoundry.cli.util import get_space_choices, handle_exception_wrapper

logger = logging.getLogger(__name__)


@click.group(name="use")
def use_command():
    """
    Set default workspace

    \b
    Supported resources:
    - workspace
    - cluster
    """
    pass


def attempt_set_cluster():
    tfs_client = ServiceFoundryServiceClient.get_client()
    clusters = tfs_client.list_cluster()
    if len(clusters) == 1:
        cluster = clusters[0]
    else:
        raise NotImplementedError("Could not set cluster.")
    set_cluster_in_context(tfs_client, cluster)
    return cluster


@click.command(name="cluster")
@handle_exception_wrapper
def use_cluster():
    attempt_set_cluster()


@click.command(name="workspace")
@click.argument("workspace_name", required=False)
@handle_exception_wrapper
def use_workspace(workspace_name=None):
    cluster = attempt_set_cluster()
    tfs_client = ServiceFoundryServiceClient.get_client()
    if workspace_name:
        spaces = tfs_client.get_workspace_by_name(
            workspace_name=workspace_name, cluster_id=cluster["id"]
        )
        if len(spaces) > 1:
            raise Exception(
                "Error: More than one workspace found with the same name. Please contact truefoundry admin."
            )
        elif not spaces:
            raise Exception(
                f"No workspace with name {workspace_name!r} found in current cluster ({cluster['id']}).\n"
                f"Use `sfy list workspace` to see available workspaces OR "
                f"`sfy use workspace` to pick one interactively",
            )
        space = spaces[0]
    else:
        spaces = tfs_client.list_workspace()
        if not spaces:
            raise Exception(
                "No workspaces found. Create one using `sfy create workspace <workspace-name>`"
            )
        elif len(spaces) == 1:
            space = spaces[0]
        else:
            space_choices = get_space_choices(tfs_client)
            space = questionary.select(
                "Choose your workspace", choices=space_choices
            ).ask()
    console.print(f"Setting {space['name']!r} as the default workspace")
    set_workspace_in_context(tfs_client, space)


def get_set_command():
    use_command.add_command(use_cluster)
    use_command.add_command(use_workspace)
    return use_command
