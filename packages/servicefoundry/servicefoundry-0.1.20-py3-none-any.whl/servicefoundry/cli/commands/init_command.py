import logging
import os
import os.path
import shutil
from types import SimpleNamespace

import questionary
import rich_click as click
from questionary import Choice

from servicefoundry.build import lib
from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.console import console
from servicefoundry.build.parser.sf_template import SfTemplate
from servicefoundry.build.parser.template_parameters import (
    NUMBER,
    OPTIONS,
    STRING,
    WORKSPACE,
)
from servicefoundry.build.session_factory import get_session
from servicefoundry.build.util import BadRequestException
from servicefoundry.cli.const import TEMP_FOLDER
from servicefoundry.cli.util import get_space_choices, handle_exception_wrapper

logger = logging.getLogger(__name__)

MSG_CREATE_NEW_SPACE = "Create a new workspace"


@click.command(help="Initialize new service for servicefoundry")
@handle_exception_wrapper
def init():
    # Get SFSClient
    tfs_client = ServiceFoundryServiceClient.get_client()

    # Get Session else do login
    try:
        get_session()
    except BadRequestException:
        do_login = questionary.select(
            "You need to login to create a service", ["Login", "Exit"]
        ).ask()
        if do_login == "Login":
            lib.login(non_interactive=False)
        else:
            return

    # Setup temp folder to download templates
    if os.path.exists(TEMP_FOLDER):
        shutil.rmtree(TEMP_FOLDER)
    os.mkdir(TEMP_FOLDER)

    # Static call to get list of templates
    templates = tfs_client.get_templates_list()

    # Choose a template of service to be created.
    template_choices = [
        Choice(f'{t["id"]} - {t["description"]}', value=t["id"]) for t in templates
    ]
    template_id = questionary.select("Choose a template", template_choices).ask()
    sf_template = SfTemplate.get_template(f"truefoundry.com/v1/{template_id}")

    parameters = {}
    for param in sf_template.parameters:
        if param.kind == STRING:
            parameters[param.id] = questionary.text(
                param.prompt, default=param.default
            ).ask()
        elif param.kind == NUMBER:
            while True:
                value = questionary.text(param.prompt, default=str(param.default)).ask()
                if value.isdigit():
                    parameters[param.id] = int(value)
                    break
                else:
                    print("Not an integer Value. Try again")
        elif param.kind == OPTIONS:
            parameters[param.id] = questionary.select(
                param.prompt, choices=param.options
            ).ask()
        elif param.kind == WORKSPACE:
            space_choices = get_space_choices(tfs_client)
            space_choices.append(
                Choice(title=MSG_CREATE_NEW_SPACE, value=MSG_CREATE_NEW_SPACE)
            )
            space = questionary.select(param.prompt, choices=space_choices).ask()

            if space == MSG_CREATE_NEW_SPACE:
                cluster = tfs_client.session.get_cluster()
                if not cluster:
                    raise Exception(
                        "No default cluster set to create workspace. "
                        "Use `sfy use cluster` to pick and set a default cluster"
                    )
                new_space_name = questionary.text(
                    "Please provide a name for your workspace"
                ).ask()
                response = tfs_client.create_workspace(
                    cluster_id=cluster["id"], name=new_space_name
                )
                console.print("Please wait while your workspace is being created. ")
                tfs_client.tail_logs(runId=response["runId"], wait=True)
                console.print(
                    f"Done, created new workspace with name {new_space_name!r}"
                )
                space = response["workspace"]

            space_fqn = space["fqn"]
            parameters[param.id] = space_fqn

    sf_template.generate_project(parameters)

    if sf_template.post_init_instruction:
        console.print(
            sf_template.post_init_instruction.format(
                parameters=SimpleNamespace(**parameters)
            )
        )


def get_init_command():
    return init
