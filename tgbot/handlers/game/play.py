from aiogram import Bot, Router
from aiogram.types import Message

from db.dao.holder import HolderDao
from shvatka.models import dto
from shvatka.scheduler import Scheduler
from shvatka.services.game_play import check_key
from shvatka.utils.exceptions import InvalidKey
from shvatka.utils.key_checker_lock import KeyCheckerFactory
from tgbot.config.models.main import TgBotConfig
from tgbot.filters.game_status import GameStatusFilter
from tgbot.views.game import GameBotLog, create_bot_game_view, BotOrgNotifier


async def check_key_handler(
    m: Message,
    team: dto.Team,
    player: dto.Player,
    game: dto.FullGame,
    dao: HolderDao,
    scheduler: Scheduler,
    locker: KeyCheckerFactory,
    bot: Bot,
    config: TgBotConfig,
):
    try:
        await check_key(
            key=m.text,
            player=player,
            team=team,
            game=await dao.game.get_full(game.id),
            dao=dao.game_player,
            view=create_bot_game_view(bot=bot, dao=dao),
            game_log=GameBotLog(bot=bot, log_chat_id=config.bot.log_chat),
            org_notifier=BotOrgNotifier(bot=bot),
            locker=locker,
            scheduler=scheduler,
        )
    except InvalidKey:
        pass


def setup() -> Router:
    router = Router(name=__name__)
    router.message.register(check_key, GameStatusFilter(running=True)) # is_team, is_played_player
    return router
