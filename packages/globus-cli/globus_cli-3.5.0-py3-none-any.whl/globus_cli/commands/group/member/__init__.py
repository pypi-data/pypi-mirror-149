from globus_cli.parsing import group

from .add import member_add
from .approve import member_approve
from .invite import member_invite
from .list import member_list
from .reject import member_reject
from .remove import member_remove


@group("member")
def group_member() -> None:
    """Manage members in a Globus Group"""


group_member.add_command(member_add)
group_member.add_command(member_remove)
group_member.add_command(member_list)
group_member.add_command(member_approve)
group_member.add_command(member_reject)
group_member.add_command(member_invite)
