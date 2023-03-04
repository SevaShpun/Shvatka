from dataclasses import dataclass

from src.core.interfaces.dal.key_log import TypedKeyGetter
from src.core.models import dto
from src.infrastructure.db.dao import KeyTimeDao, OrganizerDao


@dataclass
class TypedKeyGetterImpl(TypedKeyGetter):
    key_time: KeyTimeDao
    organizer: OrganizerDao

    async def get_typed_keys(self, game: dto.Game) -> list[dto.KeyTime]:
        return await self.key_time.get_typed_keys(game=game)

    async def get_by_player(self, game: dto.Game, player: dto.Player) -> dto.SecondaryOrganizer:
        return await self.organizer.get_by_player(game=game, player=player)

    async def get_by_player_or_none(
        self, game: dto.Game, player: dto.Player
    ) -> dto.SecondaryOrganizer | None:
        return await self.organizer.get_by_player_or_none(game=game, player=player)
