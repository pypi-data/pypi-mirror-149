import click

from globus_cli.login_manager import LoginManager
from globus_cli.parsing import command
from globus_cli.termio import FORMAT_TEXT_RECORD, formatted_print

from .._common import INDEX_FIELDS


@command("create")
@LoginManager.requires_login(LoginManager.SEARCH_RS)
@click.argument("DISPLAY_NAME")
@click.argument("DESCRIPTION")
def create_command(*, login_manager: LoginManager, display_name: str, description: str):
    """(BETA) Create a new Index"""
    index_doc = {"display_name": display_name, "description": description}
    search_client = login_manager.get_search_client()
    formatted_print(
        search_client.post("/beta/index", data=index_doc),
        text_format=FORMAT_TEXT_RECORD,
        fields=INDEX_FIELDS,
    )
