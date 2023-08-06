from typing import Optional

import rich_click as click

from servicefoundry.build.clients.auth_service_client import AuthServiceClient
from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.console import console
from servicefoundry.build.const import DEFAULT_TENANT_ID, SESSION_FILE
from servicefoundry.build.exceptions import BadRequestException
from servicefoundry.build.lib.messages import (
    PROMPT_ALREADY_LOGGED_OUT,
    PROMPT_LOGOUT_SUCCESSFUL,
    PROMPT_LOGIN_SUCCESSFUL,
)
from servicefoundry.build.model.entity import Cluster
from servicefoundry.build.model.session import ServiceFoundrySession
from servicefoundry.build.session_factory import get_session
from servicefoundry.build.session_factory import logout_session


def _set_cluster_if_only_one():
    client = ServiceFoundryServiceClient.get_client()
    clusters = client.list_cluster()
    if len(clusters) == 1:
        cluster = Cluster.from_dict(clusters[0])
        client.session.set_cluster(cluster.to_dict_for_session())
        client.session.save_session()


def _login_using_device_code() -> ServiceFoundrySession:
    auth_client = AuthServiceClient()
    url, user_code, device_code = auth_client.get_device_code(DEFAULT_TENANT_ID)
    console.print(f"Login Code: {user_code}")
    console.print(
        f"Waiting for authentication. Go to the following url to complete the authentication: {url}"
    )
    click.launch(url)
    session = auth_client.poll_for_auth(DEFAULT_TENANT_ID, device_code)
    session.save_session()
    console.print(PROMPT_LOGIN_SUCCESSFUL)
    console.print(f"Session file stored at {SESSION_FILE}")
    return session


def _login_with_api_key(api_key: str) -> ServiceFoundrySession:
    session = AuthServiceClient().login_with_api_token(
        client_id=DEFAULT_TENANT_ID, api_key=api_key
    )
    console.print(PROMPT_LOGIN_SUCCESSFUL)
    return session


def login(api_key: Optional[str] = None, non_interactive: bool = True):
    try:
        session = get_session()
        user = session.get_user_details()
        console.print(
            f"[yellow]You are logged in as {user['username']!r} with email {user['email']!r}[/]",
        )
    except BadRequestException:
        if non_interactive:
            if not api_key:
                raise ValueError("`api_key` is required in non interactive mode")
            _login_with_api_key(api_key=api_key)
        else:
            _login_using_device_code()
        # TODO (chiragjn): Done to have user make one less choice till we only have one cluster on backend
        _set_cluster_if_only_one()


def logout(non_interactive: bool = True):
    try:
        logout_session()
    except BadRequestException:
        console.print(PROMPT_ALREADY_LOGGED_OUT)
    else:
        console.print(PROMPT_LOGOUT_SUCCESSFUL)
