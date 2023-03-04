from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from shvatka.core.models import dto
from shvatka.core.services.player import get_full_team_player, get_my_team
from shvatka.core.utils.exceptions import PlayerNotInTeam
from shvatka.infrastructure.db.dao.holder import HolderDao


class TeamPlayerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        dao: HolderDao = data["dao"]
        player: dto.Player = data["player"]
        team = await get_my_team(player=player, dao=dao.team_player)
        try:
            team_player = await get_full_team_player(player, team, dao.team_player)
        except PlayerNotInTeam:
            team_player = None
        data["team_player"] = team_player
        result = await handler(event, data)
        return result
