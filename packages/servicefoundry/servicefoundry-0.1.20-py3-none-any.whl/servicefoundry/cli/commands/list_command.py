import logging

import rich_click as click

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.model.entity import Cluster
from servicefoundry.cli.const import (
    ENABLE_AUTHORIZE_COMMANDS,
    ENABLE_CLUSTER_COMMANDS,
    ENABLE_SECRETS_COMMANDS,
)
from servicefoundry.cli.display_util import print_list
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


@click.group(name="list")
def list_command():
    # TODO (chiragjn): Figure out a way to update supported resources based on ENABLE_* flags
    """
    Servicefoundry list resources

    \b
    Supported resources:
    - workspace
    - service
    - deployment
    """
    pass


@click.command(name="cluster", help="list cluster")
@handle_exception_wrapper
def list_cluster():
    tfs_client = ServiceFoundryServiceClient.get_client()
    clusters = tfs_client.list_cluster()
    print_list("Clusters", clusters, Cluster().display_columns_ps)


@click.command(name="workspace", help="list workspaces")
@handle_exception_wrapper
def list_workspace():
    tfs_client = ServiceFoundryServiceClient.get_client()
    spaces = tfs_client.list_workspace()
    print_list("Workspaces", spaces, columns=WORKSPACE_DISPLAY_FIELDS)


@click.command(name="service", help="list service in a workspace")
@click.option(
    "--workspace_name",
    type=click.STRING,
    help="workspace name to list services from.",
)
@handle_exception_wrapper
def list_service(workspace_name):
    tfs_client = ServiceFoundryServiceClient.get_client()
    current_workspace = tfs_client.session.get_workspace()
    if not workspace_name:
        # Name is not passed, if not in context raise and Exception
        if current_workspace is None:
            raise Exception(
                "workspace is not passed in as option nor is available in context. "
                "Use `sfy use workspace` to pick a default workspace or provide a workspace name"
                "using --workspace_name option"
            )

        workspace_id = current_workspace["id"]
        workspace_name = current_workspace["name"]
    else:
        # Name is passed, if not same as context fetch and forward
        if workspace_name == current_workspace["name"]:
            workspace_id = current_workspace["id"]
        else:
            cluster_id = tfs_client.session.get_cluster()["id"]
            spaces = tfs_client.get_workspace_by_name(workspace_name, cluster_id)
            if len(spaces) > 1:
                raise Exception(
                    "Error: More than one workspace found with the same name. Please contact truefoundry admin."
                )

            workspace_id = spaces[0]["id"]

    services = tfs_client.list_service_by_workspace(workspace_id)
    print_list(
        f"Services in Workspace {workspace_name!r}",
        services,
        columns=SERVICE_DISPLAY_FIELDS,
    )


@click.command(name="deployment", help="list deployment")
@click.argument("service_id")
@handle_exception_wrapper
def list_deployment(service_id):
    tfs_client: ServiceFoundryServiceClient = ServiceFoundryServiceClient.get_client()
    deployments = tfs_client.list_deployment(service_id)
    print_list(
        f"Deployments of Service: {service_id}",
        deployments,
        columns=DEPLOYMENT_DISPLAY_FIELDS,
    )


@click.command(name="secret-group", help="list secret groups")
@handle_exception_wrapper
def list_secret_group():
    tfs_client = ServiceFoundryServiceClient.get_client()
    response = tfs_client.get_secret_groups()
    print_list("Secret Groups", response)


@click.command(name="secret", help="list secrets in a group")
@click.argument("secret_group_id")
@handle_exception_wrapper
def list_secret(secret_group_id):
    tfs_client = ServiceFoundryServiceClient.get_client()
    response = tfs_client.get_secrets_in_group(secret_group_id)
    print_list("Secrets", response)


@click.command(name="authorize", help="list authorization for a resource id.")
@click.argument("resource_type", type=click.Choice(["workspace"], case_sensitive=False))
@click.argument("resource_id")
@handle_exception_wrapper
def list_authorize(resource_type, resource_id):
    tfs_client = ServiceFoundryServiceClient.get_client()
    response = tfs_client.get_authorization_for_resource(resource_type, resource_id)
    print_list(f"Auth for {resource_type}: {resource_id}", response)


def get_list_command():
    list_command.add_command(list_workspace)
    list_command.add_command(list_service)
    list_command.add_command(list_deployment)

    if ENABLE_AUTHORIZE_COMMANDS:
        list_command.add_command(list_authorize)
    if ENABLE_CLUSTER_COMMANDS:
        list_command.add_command(list_cluster)
    if ENABLE_SECRETS_COMMANDS:
        list_command.add_command(list_secret)
        list_command.add_command(list_secret_group)

    return list_command
