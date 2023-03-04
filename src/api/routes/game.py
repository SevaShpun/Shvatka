from fastapi import APIRouter
from fastapi.params import Depends

from src.api.dependencies import dao_provider, player_provider, active_game_provider
from src.api.models import responses
from src.core.models import dto
from src.core.services.game import get_authors_games
from src.infrastructure.db.dao.holder import HolderDao


async def get_my_games_list(
    player: dto.Player = Depends(player_provider),  # type: ignore[assignment]
    dao: HolderDao = Depends(dao_provider),  # type: ignore[assignment]
) -> list[dto.Game]:
    return await get_authors_games(player, dao.game)


async def get_active_game(
    game: dto.Game = Depends(active_game_provider),  # type: ignore[assignment]
) -> responses.Game:
    return responses.Game.from_core(game)


def setup(router: APIRouter):
    router.add_api_route("/games/my", get_my_games_list, methods=["GET"])
    router.add_api_route("/games/active", get_active_game, methods=["GET"])
