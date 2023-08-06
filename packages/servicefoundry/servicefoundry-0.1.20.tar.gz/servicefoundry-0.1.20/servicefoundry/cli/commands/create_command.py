import logging

import rich_click as click
from rich import print_json

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.console import console
from servicefoundry.cli.config import CliConfig
from servicefoundry.cli.const import ENABLE_CLUSTER_COMMANDS, ENABLE_SECRETS_COMMANDS
from servicefoundry.cli.display_util import print_obj
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


@click.group(name="create")
def create_command():
    # TODO (chiragjn): Figure out a way to update supported resources based on ENABLE_* flags
    """
    Create servicefoundry resources

    \b
    Supported resources:
    - workspace
    """
    pass


@click.command(name="cluster", help="create new cluster")
@click.argument("name")
@click.argument("region")
@click.argument("aws_account_id")
@click.argument("server_name")
@click.argument("ca_data")
@click.argument("server_url")
@handle_exception_wrapper
def create_cluster(name, region, aws_account_id, server_name, ca_data, server_url):
    tfs_client = ServiceFoundryServiceClient.get_client()
    cluster = tfs_client.create_cluster(
        name, region, aws_account_id, server_name, ca_data, server_url
    )
    print_obj("Cluster", cluster)


@click.command(name="workspace", help="create new workspace in cluster")
@click.argument("space_name")
@click.option(
    "--cluster_id",
    type=click.STRING,
    help="cluster id to create this workspace in.",
)
@handle_exception_wrapper
def create_workspace(space_name, cluster_id):
    tfs_client = ServiceFoundryServiceClient.get_client()
    if not cluster_id:
        cluster = tfs_client.session.get_cluster()
        if not cluster:
            raise Exception(
                "cluster_id is neither passed in as option, nor set in context. "
                "Use `sfy use cluster` to pick a cluster context and then rerun this command"
            )
        cluster_id = cluster["id"]
    response = tfs_client.create_workspace(cluster_id, space_name)
    space = response["workspace"]
    if not CliConfig.get("json"):
        tfs_client.tail_logs(response["runId"], wait=True)
    else:
        print_json(data=response)

    print_obj("Workspace", space)
    console.print(
        f"Setting {space['name']!r} as the default workspace. "
        f"You can pick a different one using `sfy use workspace`"
    )


@click.command(name="secret-group", help="create secret-group")
@click.argument("secret_group_name")
@handle_exception_wrapper
def create_secret_group(secret_group_name):
    tfs_client = ServiceFoundryServiceClient.get_client()
    response = tfs_client.create_secret_group(secret_group_name)
    print_obj(f"Secret Group", response)


@click.command(name="secret", help="create secret")
@click.argument("secret_group_id")
@click.argument("secret_key")
@click.argument("secret_value")
@handle_exception_wrapper
def create_secret(secret_group_id, secret_key, secret_value):
    tfs_client = ServiceFoundryServiceClient.get_client()
    response = tfs_client.create_secret(secret_group_id, secret_key, secret_value)
    print_obj(response["id"], response)


def get_create_command():
    create_command.add_command(create_workspace)

    if ENABLE_CLUSTER_COMMANDS:
        create_command.add_command(create_cluster)

    if ENABLE_SECRETS_COMMANDS:
        create_command.add_command(create_secret)
        create_command.add_command(create_secret_group)

    return create_command
