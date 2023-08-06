from globus_cli.parsing import group

from .list import list_command
from .show import show_command


@group("task")
def task_command():
    """View Task documents"""


task_command.add_command(show_command)
task_command.add_command(list_command)
