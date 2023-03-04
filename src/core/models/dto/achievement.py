from dataclasses import dataclass
from datetime import datetime

from .player import Player
from .. import enums


@dataclass
class Achievement:
    player: Player
    name: enums.Achievement
    first: bool
    at: datetime | None = None
