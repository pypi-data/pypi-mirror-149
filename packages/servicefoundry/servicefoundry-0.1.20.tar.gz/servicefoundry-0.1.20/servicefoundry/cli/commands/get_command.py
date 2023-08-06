import logging

import rich_click as click

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.console import console
from servicefoundry.cli.const import ENABLE_CLUSTER_COMMANDS, ENABLE_SECRETS_COMMANDS
from servicefoundry.cli.display_util import print_obj
from servicefoundry.cli.util import handle_exception_wrapper

logger = logging.getLogger(__name__)

WORKSPACE_DISPLAY_FIELDS = [
    "name",
    # "id",
    "status",
    # "clusterId"
    # "namespace",
    "createdBy",
    "createdAt",
    # "updatedAt",
]

SERVICE_DISPLAY_FIELDS = ["id", "name", "metadata", "status"]

DEPLOYMENT_DISPLAY_FIELDS = [
    "id",
    "name",
    "serviceId",
    "createdBy",
    # "domain",
    # "createdAt",
    # "updatedAt",
]


@click.group(name="get")
def get_command():
    # TODO (chiragjn): Figure out a way to update supported resources based on ENABLE_* flags
    """
    Get servicefoundry resources

    \b
    Supported resources:
    - workspace
    - service
    - deployment
    """
    pass


@click.command(name="cluster", help="show cluster metadata")
@click.argument("cluster_id")
@handle_exception_wrapper
def get_cluster(cluster_id):
    tfs_client = ServiceFoundryServiceClient.get_client()
    cluster = tfs_client.get_cluster(cluster_id)
    print_obj("Cluster", cluster)


@click.command(name="workspace", help="show workspace metadata")
@click.argument("workspace_name")
@handle_exception_wrapper
def get_workspace(workspace_name):
    tfs_client = ServiceFoundryServiceClient.get_client()
    cluster = tfs_client.session.get_cluster()
    if cluster is None:
        raise Exception(
            "Cluster info not set. "
            "Use `sfy use cluster` to set current cluster and rerun this command."
        )
    spaces = tfs_client.get_workspace_by_name(workspace_name, cluster["id"])
    if len(spaces) == 0:
        raise Exception("Error: No workspace found with the given name.")
    if len(spaces) > 1:
        raise Exception(
            "Error: More than one workspace found with the same name. Please contact truefoundry admin."
        )
    print_obj("Workspace", spaces[0], columns=WORKSPACE_DISPLAY_FIELDS)


@click.command(name="service", help="show service metadata")
@click.argument("service_id")
@handle_exception_wrapper
def get_service(service_id):
    tfs_client = ServiceFoundryServiceClient.get_client()
    service = tfs_client.get_service(service_id)
    print_obj("Service", service, columns=SERVICE_DISPLAY_FIELDS)


@click.command(name="deployment", help="show deployment metadata")
@click.argument("deployment_id")
@handle_exception_wrapper
def get_deployment(deployment_id):
    tfs_client = ServiceFoundryServiceClient.get_client()
    deployment = tfs_client.get_deployment(deployment_id)
    print_obj("Deployment", deployment, columns=DEPLOYMENT_DISPLAY_FIELDS)


@click.command(name="secret-group", help="show secret-group")
@click.argument("secret_group_id")
@handle_exception_wrapper
def get_secret_group(secret_group_id):
    tfs_client = ServiceFoundryServiceClient.get_client()
    response = tfs_client.get_secret_group(secret_group_id)
    print_obj(f"Secret Group", response)


@click.command(name="secret", help="show secret")
@click.argument("secret_id")
@handle_exception_wrapper
def get_secret(secret_id):
    tfs_client = ServiceFoundryServiceClient.get_client()
    response = tfs_client.get_secret(secret_id)
    print_obj(response["id"], response)


@click.command(name="context", help="show current context")
@handle_exception_wrapper
def get_current_context():
    tfs_client = ServiceFoundryServiceClient.get_client()
    cluster = tfs_client.session.get_cluster()
    workspace = tfs_client.session.get_workspace()
    if workspace:
        console.print(f"Workspace: {workspace['name']} ({cluster['id']})")
    elif cluster:
        console.print(f"No workspaces found ({cluster['id']})")
    else:
        console.print(
            f"Context not set. Please use `sfy use workspace` to pick a default workspace"
        )


def get_get_command():
    get_command.add_command(get_workspace)
    get_command.add_command(get_service)
    get_command.add_command(get_deployment)

    if ENABLE_CLUSTER_COMMANDS:
        get_command.add_command(get_cluster)

    if ENABLE_SECRETS_COMMANDS:
        get_command.add_command(get_secret)
        get_command.add_command(get_secret_group)

    return get_command
