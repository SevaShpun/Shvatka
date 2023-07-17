from aiogram_dialog import DialogManager
from dataclass_factory import Factory

from shvatka.core.models.dto.scn import TimeHint
from shvatka.tgbot.views.utils import render_time_hints


async def get_level_id(dialog_manager: DialogManager, **_):
    return {
        "level_id": dialog_manager.dialog_data.get("level_id", None)
        or dialog_manager.start_data["level_id"]
    }


async def get_level_data(dialog_manager: DialogManager, **_):
    dialog_data = dialog_manager.dialog_data
    dcf: Factory = dialog_manager.middleware_data["dcf"]
    hints = dcf.load(dialog_data.get("time_hints", []), list[TimeHint])
    return {
        "level_id": dialog_data["level_id"],
        "keys": dialog_data.get("keys", []),
        "time_hints": hints,
        "rendered": render_time_hints(hints) if hints else "пока нет ни одной",
    }


async def get_time_hints(dialog_manager: DialogManager, **_):
    dialog_data = dialog_manager.dialog_data
    dcf: Factory = dialog_manager.middleware_data["dcf"]
    hints = dcf.load(dialog_data.get("time_hints", []), list[TimeHint])
    return {
        "level_id": dialog_manager.start_data["level_id"],
        "time_hints": hints,
        "rendered": render_time_hints(hints) if hints else "пока нет ни одной",
    }
