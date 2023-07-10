from dataclasses import dataclass, field

from shvatka.core.models import dto
from shvatka.core.views.game import GameView
from tests.utils.time_key import assert_time_key


@dataclass
class GameViewMock(GameView):
    send_puzzle_calls: list[tuple[dto.Team, dto.Level]] = field(default_factory=list)
    send_hint_calls: list[tuple[dto.Team, int, dto.Level]] = field(default_factory=list)
    duplicate_key_calls: list[dto.KeyTime] = field(default_factory=list)
    correct_key_calls: list[dto.KeyTime] = field(default_factory=list)
    wrong_key_calls: list[dto.KeyTime] = field(default_factory=list)
    bonus_key_calls: list[tuple[dto.KeyTime, float]] = field(default_factory=list)
    game_finished_calls: list[dto.Team] = field(default_factory=list)
    game_finished_by_all_calls: set[dto.Team] = field(default_factory=set)

    async def send_puzzle(self, team: dto.Team, level: dto.Level) -> None:
        self.send_puzzle_calls.append((team, level))

    async def send_hint(self, team: dto.Team, hint_number: int, level: dto.Level) -> None:
        self.send_hint_calls.append((team, hint_number, level))

    async def duplicate_key(self, key: dto.KeyTime) -> None:
        self.duplicate_key_calls.append(key)

    async def correct_key(self, key: dto.KeyTime) -> None:
        self.correct_key_calls.append(key)

    async def wrong_key(self, key: dto.KeyTime) -> None:
        self.wrong_key_calls.append(key)

    async def bonus_key(self, key: dto.KeyTime, bonus: float) -> None:
        self.bonus_key_calls.append((key, bonus))

    async def game_finished(self, team: dto.Team) -> None:
        self.game_finished_calls.append(team)

    async def game_finished_by_all(self, team: dto.Team) -> None:
        self.game_finished_by_all_calls.add(team)

    def assert_send_only_puzzle(self, team: dto.Team, level: dto.Level) -> None:
        sent = self.send_puzzle_calls.pop()
        assert len(self.send_puzzle_calls) == 0
        assert sent[0] == team
        assert sent[1] == level

    def assert_send_only_hint(self, team: dto.Team, hint_number: int, level: dto.Level) -> None:
        sent = self.send_hint_calls.pop()
        assert len(self.send_hint_calls) == 0
        assert sent[0] == team
        assert sent[1] == hint_number
        assert sent[2] == level

    def assert_wrong_key_only(self, expected: dto.KeyTime) -> None:
        actual = self.wrong_key_calls.pop()
        assert len(self.wrong_key_calls) == 0
        assert_time_key(expected, actual)

    def assert_correct_key_only(self, expected: dto.KeyTime) -> None:
        actual = self.correct_key_calls.pop()
        assert len(self.correct_key_calls) == 0
        assert_time_key(expected, actual)

    def assert_duplicate_key_only(self, expected: dto.KeyTime) -> None:
        actual = self.duplicate_key_calls.pop()
        assert len(self.duplicate_key_calls) == 0
        assert_time_key(expected, actual)

    def assert_game_finished_only(self, team: dto.Team) -> None:
        actual = self.game_finished_calls.pop()
        assert len(self.game_finished_calls) == 0
        assert team == actual

    def assert_game_finished_all(self, teams: set[dto.Team]) -> None:
        assert len(self.game_finished_by_all_calls) == len(teams)
        assert teams == self.game_finished_by_all_calls
        self.game_finished_by_all_calls.clear()

    def assert_no_unchecked(self) -> None:
        assert len(self.send_puzzle_calls) == 0
        assert len(self.send_hint_calls) == 0
        assert len(self.duplicate_key_calls) == 0
        assert len(self.correct_key_calls) == 0
        assert len(self.wrong_key_calls) == 0
        assert len(self.game_finished_calls) == 0
        assert len(self.game_finished_by_all_calls) == 0
