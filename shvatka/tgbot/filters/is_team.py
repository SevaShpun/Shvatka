from dataclasses import dataclass

from aiogram.filters import BaseFilter

from shvatka.core.models import dto


@dataclass
class IsTeamFilter(BaseFilter):
    is_team: bool = True

    async def __call__(self, obj, team: dto.Team) -> bool:
        return (team is not None) == self.is_team
