from sqlalchemy import (
    Column,
    VARCHAR,
    Integer,
)
# local imports
from dnd.model.base import Base


class TablePlayer(Base):
    """player table"""

    player_id = Column(Integer, primary_key=True, autoincrement=True)
    slack_user_hash = Column(VARCHAR(50), nullable=False, unique=True)
    display_name = Column(VARCHAR(120), nullable=False)
    avi_url = Column(VARCHAR(255), nullable=False)

    def __init__(self, slack_user_hash: str, display_name: str, avi_url: str, is_active: bool = True):
        self.slack_user_hash = slack_user_hash,
        self.display_name = display_name
        self.avi_url = avi_url
        self.is_active = is_active

    def __repr__(self) -> str:
        return f'<TablePlayer(id={self.player_id}, slack_hash={self.slack_user_hash}, ' \
               f'display_name={self.display_name})>'
