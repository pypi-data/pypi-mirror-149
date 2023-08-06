from globus_cli.parsing import group

from .create import create_command
from .delete import delete_command
from .list import list_command


@group("role")
def role_command():
    """View and manage index roles"""


role_command.add_command(create_command)
role_command.add_command(delete_command)
role_command.add_command(list_command)
