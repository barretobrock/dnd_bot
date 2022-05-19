from dnd.model import (
    TablePlayer
)
from .users import (
    random_display_name,
    random_user
)


def make_player() -> TablePlayer:
    """Makes a random player"""
    return TablePlayer(
        slack_user_hash=random_user(),
        display_name=random_display_name(),
        avi_url=''
    )

