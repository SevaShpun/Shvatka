from datetime import datetime, timedelta
from typing import Sequence

from sqlalchemy import select, or_, ScalarResult, Result, ColumnElement
from sqlalchemy import update, not_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from shvatka.core.models import dto
from shvatka.core.models import enums
from shvatka.core.utils.datetime_utils import tz_utc
from shvatka.core.utils.exceptions import (
    PlayerAlreadyInTeam,
    PlayerRestoredInTeam,
    PlayerNotInTeam,
)
from shvatka.infrastructure.db import models
from .base import BaseDAO


class TeamPlayerDao(BaseDAO[models.TeamPlayer]):
    def __init__(self, session: AsyncSession):
        super().__init__(models.TeamPlayer, session)

    async def get_team(
        self, player: dto.Player, for_date: datetime | None = None
    ) -> dto.Team | None:
        result: Result[tuple[models.TeamPlayer]] = await self.session.execute(
            select(models.TeamPlayer)
            .options(
                joinedload(models.TeamPlayer.team)
                .joinedload(models.Team.captain)
                .joinedload(models.Player.user),
                joinedload(models.TeamPlayer.team)
                .joinedload(models.Team.captain)
                .joinedload(models.Player.forum_user),
                joinedload(models.TeamPlayer.team).joinedload(models.Team.chat),
                joinedload(models.TeamPlayer.team).joinedload(models.Team.forum_team),
            )
            .where(
                models.TeamPlayer.player_id == player.id,
                *get_leaved_condition(for_date),
            )
        )
        try:
            team_player = result.scalar_one()
        except NoResultFound:
            return None
        team: models.Team = team_player.team
        return team.to_dto_chat_prefetched()

    async def have_team(self, player: dto.Player) -> bool:
        return await self.get_team(player) is not None

    async def join_team(
        self,
        player: dto.Player,
        team: dto.Team,
        role: str,
        as_captain: bool = False,
        joined_at: datetime | None = None,
    ):
        if team_player := await self.need_restore(player, team):
            team_player.date_left = None
            await self.session.merge(team_player)
            raise PlayerRestoredInTeam(player=player, team=team)
        team_player = models.TeamPlayer(
            player_id=player.id,
            team_id=team.id,
            role=role,
        )
        if joined_at:
            team_player.date_joined = joined_at
        if as_captain:
            team_player.can_remove_players = True
            team_player.can_manage_waivers = True
            team_player.can_add_players = True
            team_player.can_change_team_name = True
            team_player.can_manage_players = True
        self.session.add(team_player)
        await self._flush(team_player)

    async def leave_team(self, player: dto.Player, at: datetime | None = None):
        if at is None:
            at = datetime.now(tz=tz_utc)
        pit = await self._get_my_team_player(player, at)
        pit.date_left = at
        await self._flush(pit)

    async def check_player_free(self, player: dto.Player):
        if players_team := await self.get_team(player):
            raise PlayerAlreadyInTeam(
                player=player,
                team=players_team,
                text=f"user {player.id} already in team {players_team.id}",
            )

    async def need_restore(self, player: dto.Player, team: dto.Team) -> models.TeamPlayer | None:
        today = datetime.now(tz=tz_utc).date()
        result: ScalarResult[models.TeamPlayer] = await self.session.scalars(
            select(models.TeamPlayer).where(
                models.TeamPlayer.player_id == player.id,
                models.TeamPlayer.date_left >= today,
                models.TeamPlayer.date_left < today + timedelta(days=1),
                models.TeamPlayer.team_id == team.id,
            )
        )
        return result.one_or_none()

    async def get_players(self, team: dto.Team) -> Sequence[dto.FullTeamPlayer]:
        result = await self.session.scalars(
            select(models.TeamPlayer)
            .where(
                models.TeamPlayer.team_id == team.id,
                *not_leaved(),
            )
            .options(
                joinedload(models.TeamPlayer.player).joinedload(models.Player.user),
                joinedload(models.TeamPlayer.player).joinedload(models.Player.forum_user),
            )
        )
        players: Sequence[models.TeamPlayer] = result.all()
        return [
            dto.FullTeamPlayer.from_simple(
                team_player=team_player.to_dto(),
                player=team_player.player.to_dto_user_prefetched(),
                team=team,
            )
            for team_player in players
        ]

    async def get_team_player(self, player: dto.Player) -> dto.TeamPlayer:
        return (await self._get_my_team_player(player)).to_dto()

    async def flip_permission(
        self, player: dto.TeamPlayer, permission: enums.TeamPlayerPermission
    ):
        await self.session.execute(
            update(models.TeamPlayer)
            .where(models.TeamPlayer.id == player.id)
            .values(**{permission.name: not_(getattr(models.TeamPlayer, permission.name))})
        )

    async def change_role(self, team_player: dto.TeamPlayer, role: str) -> None:
        await self.session.execute(
            update(models.TeamPlayer)
            .where(models.TeamPlayer.id == team_player.id)
            .values(role=role)
        )

    async def change_emoji(self, team_player: dto.TeamPlayer, emoji: str) -> None:
        await self.session.execute(
            update(models.TeamPlayer)
            .where(models.TeamPlayer.id == team_player.id)
            .values(emoji=emoji)
        )

    async def replace_team_players(self, primary: dto.Team, secondary: dto.Team):
        await self.session.execute(
            update(models.TeamPlayer)
            .where(models.TeamPlayer.team_id == secondary.id)
            .values(team_id=primary.id)
        )

    async def _get_my_team_player(
        self, player: dto.Player, at: datetime | None = None
    ) -> models.TeamPlayer:
        result: Result[tuple[models.TeamPlayer]] = await self.session.execute(
            select(models.TeamPlayer).where(
                models.TeamPlayer.player_id == player.id,
                *get_leaved_condition(at),
            )
        )
        try:
            return result.scalar_one()
        except NoResultFound:
            raise PlayerNotInTeam(player=player)


def get_leaved_condition(for_date: datetime | None = None) -> Sequence[ColumnElement["bool"]]:
    if for_date is None:
        leaved_condition = not_leaved()
    else:
        leaved_condition = not_leaved_for_date(for_date)
    return leaved_condition


def not_leaved_for_date(for_date: datetime) -> Sequence[ColumnElement["bool"]]:
    return (
        or_(
            models.TeamPlayer.date_left > for_date,
            *not_leaved(),
        ),
        models.TeamPlayer.date_joined < for_date,
    )


def not_leaved() -> Sequence[ColumnElement["bool"]]:
    return (models.TeamPlayer.date_left.is_(None),)
