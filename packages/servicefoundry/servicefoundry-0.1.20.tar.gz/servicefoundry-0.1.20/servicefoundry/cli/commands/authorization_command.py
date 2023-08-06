import logging

import rich_click as click

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.cli.display_util import print_obj
from servicefoundry.cli.util import handle_exception_wrapper

logger = logging.getLogger(__name__)


@click.group(name="auth", help="servicefoundry auth list|create|update|remove")
def authorize():
    pass


@click.command(name="create", help="create auth")
@click.argument("resource_type")
@click.argument("resource_id")
@click.argument("user_id")
@click.argument("role")
@handle_exception_wrapper
def create(resource_id, resource_type, user_id, role):
    tfs_client = ServiceFoundryServiceClient.get_client()
    response = tfs_client.create_authorization(
        resource_id, resource_type, user_id, role
    )
    print_obj(f"Auth for {resource_type}: {resource_id}", response)


@click.command(name="update", help="update auth")
@click.argument("authorization_id")
@click.argument("role")
@handle_exception_wrapper
def update(authorization_id, role):
    tfs_client = ServiceFoundryServiceClient.get_client()
    _ = tfs_client.update_authorization(authorization_id, role)


def get_authorization_command():
    authorize.add_command(create)
    authorize.add_command(update)
    return authorize
