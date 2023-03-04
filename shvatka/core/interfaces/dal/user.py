from typing import Protocol

from shvatka.core.interfaces.dal.base import Committer
from shvatka.core.models import dto


class UserUpserter(Committer, Protocol):
    async def upsert_user(self, user: dto.User) -> dto.User:
        raise NotImplementedError


class UserPasswordSetter(Committer, Protocol):
    async def set_password(self, user: dto.User, hashed_password: str):
        raise NotImplementedError


class UserByUsernameResolver(Protocol):
    async def get_by_username(self, username: str) -> dto.User:
        raise NotImplementedError


class UserByIdResolver(Protocol):
    async def get_by_id(self, id_: int) -> dto.User:
        raise NotImplementedError
