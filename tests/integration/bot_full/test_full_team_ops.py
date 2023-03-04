from datetime import datetime

import pytest
from aiogram import Dispatcher
from aiogram.methods import SendMessage, GetChatAdministrators, GetChat, GetChatMember
from aiogram.types import Update, Message, ChatMemberOwner, ChatMemberMember
from aiogram_tests.mocked_bot import MockedBot

from src.infrastructure.db.dao.holder import HolderDao
from src.core.models.enums.chat_type import ChatType
from src.core.services.player import upsert_player, get_my_role
from src.core.services.user import upsert_user
from src.core.utils.datetime_utils import tz_utc
from src.tgbot.views.commands import CREATE_TEAM_COMMAND, ADD_IN_TEAM_COMMAND
from tests.fixtures.chat_constants import create_tg_chat
from tests.fixtures.user_constants import (
    create_tg_user,
    create_dto_hermione,
    create_tg_from_dto,
)


@pytest.mark.asyncio
async def test_create_team(dp: Dispatcher, bot: MockedBot, dao: HolderDao):
    chat = create_tg_chat(type_=ChatType.supergroup)
    harry = create_tg_user()
    bot.add_result_for(
        GetChatAdministrators, ok=True, result=[ChatMemberOwner(user=harry, is_anonymous=False)]
    )
    bot.add_result_for(GetChat, ok=True, result=chat)
    bot.add_result_for(SendMessage, ok=True)
    update = Update(
        update_id=1,
        message=Message(
            message_id=2,
            from_user=harry,
            chat=chat,
            text="/" + CREATE_TEAM_COMMAND.command,
            date=datetime.now(tz=tz_utc),
        ),
    )
    await dp.feed_update(bot, update)
    assert await dao.team.count() == 1
    assert await dao.team_player.count() == 1
    team = (await dao.team._get_all())[0]

    assert chat.title == team.name

    hermi = create_dto_hermione()
    hermi_message = Message(
        message_id=3,
        from_user=create_tg_from_dto(hermi),
        chat=chat,
        text="hi everyone",
        date=datetime.now(tz=tz_utc),
    )
    update = Update(
        update_id=2,
        message=hermi_message,
    )
    await dp.feed_update(bot, update)

    bot.add_result_for(
        method=GetChatMember, ok=True, result=ChatMemberMember(user=create_tg_from_dto(hermi))
    )
    bot.add_result_for(SendMessage, ok=True)
    update = Update(
        update_id=3,
        message=Message(
            message_id=4,
            from_user=harry,
            chat=chat,
            text=f"/{ADD_IN_TEAM_COMMAND.command} brain",
            reply_to_message=hermi_message,
            date=datetime.now(tz=tz_utc),
        ),
    )
    await dp.feed_update(bot, update)
    assert await dao.team_player.count() == 2
    player = await upsert_player(await upsert_user(hermi, dao.user), dao.player)
    assert await get_my_role(player, dao.team_player) == "brain"
