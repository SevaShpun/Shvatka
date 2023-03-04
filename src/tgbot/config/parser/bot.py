from src.tgbot.config.models.bot import BotConfig, BotApiConfig, BotApiType


def load_bot_config(dct: dict) -> BotConfig:
    return BotConfig(
        token=dct["token"],
        log_chat=dct["log_chat"],
        game_log_chat=dct["game_log_chat"],
        superusers=dct["superusers"],
        bot_api=load_botapi(dct["botapi"]),
        telegraph_token=dct["telegraph_token"],
    )


def load_botapi(dct: dict) -> BotApiConfig:
    return BotApiConfig(
        type=BotApiType[dct["type"]],
        botapi_url=dct.get("botapi_url", None),
        botapi_file_url=dct.get("file_url", None),
    )
