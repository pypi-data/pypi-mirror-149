import uuid

from globus_cli.login_manager import LoginManager
from globus_cli.parsing import command
from globus_cli.termio import FORMAT_TEXT_RECORD, formatted_print

from .._common import INDEX_FIELDS, index_id_arg


@command("show")
@index_id_arg
@LoginManager.requires_login(LoginManager.SEARCH_RS)
def show_command(*, login_manager: LoginManager, index_id: uuid.UUID):
    """Display information about an index"""
    search_client = login_manager.get_search_client()
    formatted_print(
        search_client.get_index(index_id),
        text_format=FORMAT_TEXT_RECORD,
        fields=INDEX_FIELDS,
    )
