import logging

import questionary
import rich_click as click
from rich import print_json

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.cli.config import CliConfig
from servicefoundry.cli.const import (
    ENABLE_AUTHORIZE_COMMANDS,
    ENABLE_CLUSTER_COMMANDS,
    ENABLE_SECRETS_COMMANDS,
)
from servicefoundry.cli.util import handle_exception_wrapper

logger = logging.getLogger(__name__)

WORKSPACE_DISPLAY_FIELDS = [
    "id",
    "name",
    "namespace",
    "status",
    "clusterId",
    "createdBy",
    "createdAt",
    "updatedAt",
]
DEPLOYMENT_DISPLAY_FIELDS = [
    "id",
    "serviceId",
    "domain",
    "deployedBy",
    "createdAt",
    "updatedAt",
]


@click.group(name="remove")
def remove_command():
    # TODO (chiragjn): Figure out a way to update supported resources based on ENABLE_* flags
    """
    Servicefoundry remove entity by id

    \b
    Supported resources:
    - workspace
    - service
    """
    pass


@click.command(name="cluster", help="remove cluster")
@click.argument("cluster_id")
@handle_exception_wrapper
def remove_cluster(cluster_id):
    tfs_client = ServiceFoundryServiceClient.get_client()
    confirm = questionary.confirm(
        default=False,
        auto_enter=False,
        message=f"Are you sure you want to remove cluster {cluster_id!r}?",
    ).ask()
    if confirm:
        tfs_client.remove_cluster(cluster_id)
        # Remove workspace and cluster from context
        ctx_cluster = tfs_client.session.get_cluster()
        if ctx_cluster and ctx_cluster["id"] == cluster_id:
            tfs_client.session.set_workspace(None)
            tfs_client.session.set_cluster(None)
            tfs_client.session.save_session()
    else:
        raise Exception("Aborted!")


@click.command(name="workspace", help="remove workspace")
@click.argument("workspace_name")
@click.option(
    "--cluster_id",
    type=click.STRING,
    help="cluster id to delete the workspace from",
)
@handle_exception_wrapper
def remove_workspace(workspace_name, cluster_id):
    tfs_client = ServiceFoundryServiceClient.get_client()
    if not cluster_id:
        cluster = tfs_client.session.get_cluster()
        if not cluster:
            raise Exception(
                "cluster_id is neither passed in as option, nor set in context. "
                "Use `sfy use cluster` to pick a cluster context and then rerun this command"
            )
        cluster_id = cluster["id"]
    spaces = tfs_client.get_workspace_by_name(
        workspace_name=workspace_name, cluster_id=cluster_id
    )
    if len(spaces) > 1:
        raise Exception(
            "Error: More than one workspace found with the same name. Please contact truefoundry admin."
        )
    elif not spaces:
        raise Exception(
            f"No workspace with name {workspace_name!r} found in current cluster ({cluster_id}).\n"
            f"Use `sfy list workspace` to see available workspaces OR "
            f"`sfy use workspace` to pick one interactively",
        )
    space = spaces[0]
    workspace_id = space["id"]
    confirm = questionary.confirm(
        default=False,
        auto_enter=False,
        message=f"Are you sure you want to remove workspace {workspace_name!r}?",
    ).ask()
    if confirm:
        response = tfs_client.remove_workspace(workspace_id)
        # Remove workspace from context if we removed it
        ctx_workspace = tfs_client.session.get_workspace()
        if ctx_workspace and ctx_workspace["id"] == workspace_id:
            tfs_client.session.set_workspace(None)
            tfs_client.session.save_session()
    else:
        raise Exception("Aborted!")
    if not CliConfig.get("json"):
        tfs_client.tail_logs(response["pipelinerun"]["name"], wait=True)
    else:
        print_json(data=response)


@click.command(name="service", help="remove service")
@click.argument("service_id")
@handle_exception_wrapper
def remove_service(service_id):
    confirm = questionary.confirm(
        default=False,
        auto_enter=False,
        message=f"Are you sure you want to remove service {service_id!r}?",
    ).ask()
    if confirm:
        tfs_client = ServiceFoundryServiceClient.get_client()
        deployment = tfs_client.remove_service(service_id)
        tfs_client.tail_logs(deployment["runId"])
    else:
        raise Exception("Aborted!")


@click.command(name="secret-group", help="remove secret-group")
@click.argument("secret_group_id")
@handle_exception_wrapper
def remove_secret_group(secret_group_id):
    confirm = questionary.confirm(
        default=False,
        auto_enter=False,
        message=f"Are you sure you want to remove secret group {secret_group_id!r}?",
    ).ask()
    if confirm:
        tfs_client = ServiceFoundryServiceClient.get_client()
        response = tfs_client.delete_secret_group(secret_group_id)
        print_json(data=response)
    else:
        raise Exception("Aborted!")


@click.command(name="secret", help="remove secret")
@click.argument("secret_id")
@handle_exception_wrapper
def remove_secret(secret_id):
    confirm = questionary.confirm(
        default=False,
        auto_enter=False,
        message=f"Are you sure you want to remove secret {secret_id!r}?",
    ).ask()
    if confirm:
        tfs_client = ServiceFoundryServiceClient.get_client()
        response = tfs_client.delete_secret(secret_id)
        print_json(data=response)
    else:
        raise Exception("Aborted!")


@click.command(name="auth", help="remove authorization")
@click.argument("authorization_id")
@handle_exception_wrapper
def remove_auth(authorization_id):
    confirm = questionary.confirm(
        default=False,
        auto_enter=False,
        message=f"Are you sure you want to remove authorization {authorization_id!r}?",
    ).ask()
    if confirm:
        tfs_client = ServiceFoundryServiceClient.get_client()
        response = tfs_client.delete_authorization(authorization_id)
        print_json(data=response)
    else:
        raise Exception("Aborted!")


def get_remove_command():
    remove_command.add_command(remove_workspace)
    remove_command.add_command(remove_service)

    if ENABLE_AUTHORIZE_COMMANDS:
        remove_command.add_command(remove_auth)

    if ENABLE_CLUSTER_COMMANDS:
        remove_command.add_command(remove_cluster)

    if ENABLE_SECRETS_COMMANDS:
        remove_command.add_command(remove_secret)
        remove_command.add_command(remove_secret_group)

    return remove_command
