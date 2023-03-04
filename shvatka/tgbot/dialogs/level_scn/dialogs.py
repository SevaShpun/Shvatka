from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Jinja

from shvatka.tgbot import states
from .getters import get_time_hints, get_level_id
from .handlers import process_result, start_add_time_hint, process_id, process_keys, save_level
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
        MessageInput(func=process_id),
        state=states.LevelSG.level_id,
    ),
    Window(
        Jinja("Уровень <b>{{level_id}}</b>\n\n"),
        Const(
            "<b>Ключи уровня</b>\n\n"
            "Отлично, перейдём к ключам. Ключи принимаются в следующих форматах: "
            "<code>SHENGLISHLETTERSANDDIDGITS СХРУССКИЕБУКВЫИЦИФРЫ</code>.\n"
            "Если требуется указать несколько ключей напишите каждый с новой строки."
        ),
        MessageInput(func=process_keys),
        state=states.LevelSG.keys,
        getter=get_level_id,
    ),
    Window(
        Jinja("Подсказки уровня {{level_id}}:\n"),
        Jinja("{{rendered}}"),
        Button(Const("Добавить подсказку"), id="add_time_hint", on_click=start_add_time_hint),
        Button(
            Const("Готово, сохранить"),
            id="save",
            on_click=save_level,
            when=lambda d, *_, **__: len(d["time_hints"]) > 1,
        ),
        state=states.LevelSG.time_hints,
        getter=get_time_hints,
        preview_data={
            "time_hints": [],
            "rendered": RENDERED_HINTS_PREVIEW,
            "level_id": "Pinky Pie",
        },
    ),
    on_process_result=process_result,
)
