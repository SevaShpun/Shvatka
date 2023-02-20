from typing import Iterable

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from infrastructure.db import models
from shvatka.models import dto
from .base import BaseDAO


class PlayerDao(BaseDAO[models.Player]):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Player, session)

    async def upsert_player(self, user: dto.User) -> dto.Player:
        try:
            return await self.get_by_user(user)
        except NoResultFound:
            return await self.create_for_user(user)

    async def get_by_id(self, id_: int) -> dto.Player:
        player = await self._get_by_id(id_, (joinedload(models.Player.user, innerjoin=True),))
        return player.to_dto_user_prefetched()

    async def get_by_user(self, user: dto.User) -> dto.Player:
        result = await self.session.execute(
            select(models.Player).join(models.Player.user).where(models.User.id == user.db_id)
        )
        player = result.scalar_one()
        return player.to_dto(user)

    async def create_for_user(self, user: dto.User) -> dto.Player:
        user_db = await self.session.get(models.User, user.db_id)
        player = models.Player()
        user_db.player = player
        self._save(player)
        await self._flush(player)
        return player.to_dto(user)

    async def create_for_forum_user(self, user: dto.ForumUser) -> dto.Player:
        forum_user_db = await self.session.get(models.ForumUser, user.db_id)
        player = models.Player()
        forum_user_db.player = player
        self._save(player)
        await self._flush(player)
        return player.to_dto(None)  # TODO

    async def promote(self, actor: dto.Player, target: dto.Player):
        target_player = await self._get_by_id(target.id)
        target_player.can_be_author = True
        target_player.promoted_by_id = actor.id

    async def get_by_ids_with_user_and_pit(self, ids: Iterable[int]) -> list[dto.VotedPlayer]:
        result = await self.session.execute(
            select(models.Player, models.TeamPlayer)
            .options(
                joinedload(models.Player.user, innerjoin=True),
            )
            .join(models.Player.teams)
            .where(
                models.Player.id.in_(ids),  # noqa
                models.TeamPlayer.date_left.is_(None),  # noqa
            )
        )
        players = result.all()
        return [
            dto.VotedPlayer(
                player.to_dto_user_prefetched(),
                pit.to_dto(),
            )
            for player, pit in players
        ]
