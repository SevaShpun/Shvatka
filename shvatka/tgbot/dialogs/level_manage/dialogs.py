from aiogram import F
from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, SwitchTo, Select, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Jinja

from shvatka.tgbot import states
from shvatka.tgbot.filters import is_key
from .getters import get_level_id, get_orgs
from .handlers import (
    edit_level,
    show_level,
    level_testing,
    cancel_level_test,
    process_key_message,
    send_to_testing,
)

level_manage = Dialog(
    Window(
        Jinja("Уровень <b>{{level.name_id}}</b>\n{{rendered}}"),
        Cancel(Const("🔙Назад")),
        Button(
            Const("✏Редактирование"),
            id="level_edit",
            on_click=edit_level,
            when="False",
        ),
        Button(
            Const("📂Показать"),
            id="level_show",
            on_click=show_level,
        ),
        Button(
            Const("🧩Тестировать"),
            id="level_test",
            on_click=level_testing,
        ),
        SwitchTo(
            Const("🧩Отправить на тестирование"),
            id="send_to_test",
            state=states.LevelManageSG.send_to_test,
            when=F["level"].game_id,
        ),
        state=states.LevelManageSG.menu,
        getter=get_level_id,
    ),
    Window(
        Jinja(
            "Уровень {{level.name_id}} (№{{level.number_in_game}} в игре {{game.name}})\n"
            "Кому отправить его на тестирование?\n\n"
            "ℹЧтобы добавить кого-то в этот список, нужно добавить организатора из меню игры"
        ),
        SwitchTo(Const("🔙Назад"), id="back", state=states.LevelManageSG.menu),
        ScrollingGroup(
            Select(
                Jinja("{{item.player.name_mention}}"),
                id="game_orgs",
                item_id_getter=lambda x: x.id,
                items="orgs",
                on_click=send_to_testing,
            ),
            id="game_orgs_sg",
            width=1,
            height=10,
        ),
        state=states.LevelManageSG.send_to_test,
        getter=get_orgs,
    ),
)


level_test_dialog = Dialog(
    Window(
        Jinja("Идёт тестирование уровня <b>{{level.name_id}}</b>"),
        Button(
            Const("⤴Прервать"),
            id="level_test_cancel",
            on_click=cancel_level_test,
        ),
        MessageInput(func=process_key_message, content_types=ContentType.TEXT, filter=is_key),
        getter=get_level_id,
        state=states.LevelTestSG.wait_key,
    ),
)
