import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram_dialog import DialogRegistry
from dataclass_factory import Factory
from redis.asyncio.client import Redis
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from shvatka.models.config import Config
from shvatka.models.config.db import RedisConfig, DBConfig
from shvatka.models.config.main import Paths
from shvatka.services.scheduler.scheduler import Scheduler
from shvatka.services.username_resolver.user_getter import UserGetter
from tgbot.dialogs import setup_dialogs
from tgbot.handlers import setup_handlers
from tgbot.middlewares import setup_middlewares

logger = logging.getLogger(__name__)


def create_bot(config: Config) -> Bot:
    return Bot(
        token=config.bot.token,
        parse_mode="HTML",
        session=config.bot.create_session(),
    )


def create_dispatcher(
    config: Config, user_getter: UserGetter, dcf: Factory, pool: sessionmaker,
    redis: Redis, scheduler: Scheduler,
) -> Dispatcher:
    dp = Dispatcher(storage=(config.storage.create_storage()))
    setup_middlewares(
        dp=dp,
        pool=pool,
        bot_config=config.bot,
        user_getter=user_getter,
        dcf=dcf,
        redis=redis,
        scheduler=scheduler,
    )
    registry = DialogRegistry(dp)
    setup_dialogs(registry)
    setup_handlers(dp, config.bot)
    return dp


def create_scheduler(
    pool: sessionmaker, redis: Redis, bot: Bot, redis_config: RedisConfig
) -> Scheduler:
    return Scheduler(redis_config=redis_config, pool=pool, redis=redis, bot=bot)


def get_paths() -> Paths:
    if path := os.getenv("BOT_PATH"):
        return Paths(Path(path))
    return Paths(Path(__file__).parent.parent)


def create_pool(db_config: DBConfig) -> sessionmaker:
    engine = create_async_engine(url=make_url(db_config.uri), echo=True)
    pool = sessionmaker(bind=engine, class_=AsyncSession,
                        expire_on_commit=False, autoflush=False)
    return pool


def create_redis(config: RedisConfig) -> Redis:
    logger.info("created redis for %s", config)
    return Redis(host=config.url, port=config.port, db=config.db)
