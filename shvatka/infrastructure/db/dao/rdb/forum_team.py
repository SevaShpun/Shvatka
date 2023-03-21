from typing import Sequence

from sqlalchemy import update, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from shvatka.core.models import dto
from shvatka.infrastructure.crawler.models.team import ParsedTeam
from shvatka.infrastructure.db import models
from .base import BaseDAO


class ForumTeamDAO(BaseDAO[models.ForumTeam]):
    def __init__(self, session: AsyncSession):
        super().__init__(models.ForumTeam, session)

    async def upsert(self, team: ParsedTeam) -> dto.ForumTeam:
        kwargs = dict(
            name=team.name,
            forum_id=team.id,
            url=team.url,
        )
        saved_team = await self.session.scalars(
            insert(models.ForumTeam)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(models.ForumTeam.name,),
                set_=kwargs,
                where=models.ForumTeam.name == team.name,
            )
            .returning(models.ForumTeam)
        )
        return saved_team.one().to_dto()

    async def replace_forum_team(self, primary: dto.Team, secondary: dto.Team):
        await self.session.execute(
            update(models.ForumTeam)
            .where(models.ForumTeam.team_id == secondary.id)
            .values(team_id=primary.id)
        )

    async def get_free_forum_teams(self) -> Sequence[dto.ForumTeam]:
        result = await self.session.scalars(
            select(models.ForumTeam)
            .where(models.ForumTeam.team_id.is_(None))
            .order_by(models.ForumTeam.id)
        )
        return result.all()
