import enum
from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    VARCHAR,
    Integer,
    TEXT
)
# local imports
from dnd.model.base import Base


class DndErrorType(enum.Enum):
    INPUT_ERROR = enum.auto()           # Err from input processing
    GAME_ERROR = enum.auto()            # Err from game mechanics
    GAME_ROUND_ERROR = enum.auto()      # Err from game round mechanics
    PLAYER_ERROR = enum.auto()          # Err from player procedures
    PLAYER_ROUND_ERROR = enum.auto()    # Err from player round mechanics


class TableCahError(Base):
    """error table"""

    error_id = Column(Integer, primary_key=True, autoincrement=True)
    error_type = Column(Enum(DndErrorType), nullable=False)
    error_class = Column(VARCHAR(150), nullable=False)
    error_text = Column(VARCHAR(255), nullable=False)
    error_traceback = Column(TEXT)

    player_key = Column(ForeignKey('dnd.player.player_id'))

    def __init__(self, error_type: DndErrorType, error_class: str, error_text: str, error_traceback: str = None,
                 player_key: int = None):
        self.error_type = error_type
        self.error_class = error_class
        self.error_text = error_text
        self.error_traceback = error_traceback
        self.player_key = player_key

    def __repr__(self) -> str:
        return f'<TableCahError(type={self.error_type.name} class={self.error_class}, text={self.error_text[:20]})>'
