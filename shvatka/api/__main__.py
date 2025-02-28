import logging

import uvicorn
from fastapi import FastAPI

from shvatka.api.config.parser.main import load_config
from shvatka.api.main_factory import (
    get_paths,
    create_app,
)
from shvatka.common.config.parser.logging_config import setup_logging
from shvatka.infrastructure.db.factory import create_pool, create_redis

logger = logging.getLogger(__name__)


def main() -> FastAPI:
    paths = get_paths()

    setup_logging(paths)
    config = load_config(paths)
    pool = create_pool(config.db)
    app = create_app(pool=pool, redis=create_redis(config.redis), config=config)

    logger.info("app prepared")
    return app


def run():
    uvicorn.run("shvatka.api:main", factory=True, log_config=None)


if __name__ == "__main__":
    run()
