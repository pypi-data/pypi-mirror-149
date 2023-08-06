from globus_cli.parsing import group

from .accept import invite_accept
from .decline import invite_decline


@group("invite")
def group_invite() -> None:
    """Manage invitations to a Globus Group"""


group_invite.add_command(invite_accept)
group_invite.add_command(invite_decline)
