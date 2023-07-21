from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Jinja

from shvatka.tgbot import states
from .getters import get_time_hints, get_level_id, get_level_data, get_keys
from .handlers import (
    process_time_hint_result,
    start_add_time_hint,
    process_id,
    process_keys,
    save_level,
    save_hints,
    process_level_result,
    start_keys,
    start_hints,
    not_correct_id,
    check_level_id,
    on_start_level_edit,
    on_start_hints_edit,
)
from ..preview_data import RENDERED_HINTS_PREVIEW

level = Dialog(
    Window(
        Const(
            "<b>ID уровня</b>\n\n"
            "Для начала дай уровню короткое описание (ID) (цифры, латинские буквы). "
            "Оно будет использовано в дальнейшем при создании игры, "
            "для указания очередности уровней.\n"
            "\n"
            "Внимание! ID и название файла не должны содержать "
            "конфиденциальной информации, дающих представление о "
            "ключах, локациях и другой существенной информации "
            "поскольку ID и название файла попадают в лог-файлы, предназначенные "
            "для чтения системным администратором"
        ),
        TextInput(
            type_factory=check_level_id,
            on_error=not_correct_id,
            on_success=process_id,
            id="level_id",
        ),
        state=states.LevelSG.level_id,
    ),
    Window(
        Jinja(
            "Написание уровня {{level_id}}:\n"
            "{% if keys %}"
            "🔑Ключей: {{ keys | length }}\n"
            "{% else %}"
            "🔑Ключи не введены\n"
            "{% endif %}"
            "\n💡Подсказки:\n"
            "{{rendered}}"
        ),
        Button(Const("🔑Ключи"), id="keys", on_click=start_keys),
        Button(Const("💡Подсказки"), id="hints", on_click=start_hints),
        Button(
            Const("✅Готово, сохранить"),
            id="save",
            on_click=save_level,
            when=F["dialog_data"]["keys"] & F["dialog_data"]["time_hints"],
        ),
        state=states.LevelSG.menu,
        getter=get_level_data,
        preview_data={
            "level_id": "Pinky Pie",
        },
    ),
    on_process_result=process_level_result,
)

level_edit_dialog = Dialog(
    Window(
        Jinja(
            "Редактирование уровня {{level_id}}:\n"
            "{% if keys %}"
            "🔑Ключей: {{ keys | length }}\n"
            "{% else %}"
            "🔑Ключи не введены\n"
            "{% endif %}"
            "\n💡Подсказки:\n"
            "{{rendered}}"
        ),
        Button(Const("🔑Ключи"), id="keys", on_click=start_keys),
        Button(Const("💡Подсказки"), id="hints", on_click=start_hints),
        Button(
            Const("✅Готово, сохранить"),
            id="save",
            on_click=save_level,
            when=F["dialog_data"]["keys"] & F["dialog_data"]["time_hints"],
        ),
        state=states.LevelEditSg.menu,
        getter=get_level_data,
        preview_data={
            "level_id": "Pinky Pie",
        },
    ),
    on_process_result=process_level_result,
    on_start=on_start_level_edit,
)

keys_dialog = Dialog(
    Window(
        Jinja("Уровень <b>{{level_id}}</b>\n\n"),
        Const("🔑<b>Ключи уровня</b>\n"),
        Jinja(
            "Сейчас сохранены ключи:\n"
            "{% for key in keys %}"
            "🔑<code>{{key}}</code>\n"
            "{% endfor %}"
            "\n Для изменения пришли сообщение с новыми ключами в формате: ",
            when=F["keys"],
        ),
        Const(
            "Отлично, перейдём к ключам. Ключи принимаются в следующих форматах: ", when=~F["keys"]
        ),
        Const(
            "<code>SHENGLISHLETTERSANDDIDGITS СХРУССКИЕБУКВЫИЦИФРЫ</code>.\n"
            "Если требуется указать несколько ключей напишите каждый с новой строки."
        ),
        MessageInput(func=process_keys),
        state=states.LevelKeysSG.keys,
        getter=(get_level_id, get_keys),
    ),
)

hints_dialog = Dialog(
    Window(
        Jinja("💡Подсказки уровня {{level_id}}:\n"),
        Jinja("{{rendered}}"),
        Button(Const("➕Добавить подсказку"), id="add_time_hint", on_click=start_add_time_hint),
        Button(
            Const("👌Достаточно подсказок"),
            id="save",
            on_click=save_hints,
            when=F["dialog_data"]["time_hints"].len() > 1,
        ),
        state=states.LevelHintsSG.time_hints,
        getter=get_time_hints,
        preview_data={
            "time_hints": [],
            "rendered": RENDERED_HINTS_PREVIEW,
            "level_id": "Pinky Pie",
        },
    ),
    on_process_result=process_time_hint_result,
    on_start=on_start_hints_edit,
)
