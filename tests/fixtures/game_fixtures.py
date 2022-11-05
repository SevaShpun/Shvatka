import asyncio

import pytest_asyncio
from dataclass_factory import Factory

from db.dao.holder import HolderDao
from shvatka.clients.file_storage import FileStorage
from shvatka.models import dto
from shvatka.models.dto.scn.game import RawGameScenario
from shvatka.models.enums.played import Played
from shvatka.services.game import upsert_game
from shvatka.services.player import join_team
from shvatka.services.waiver import add_vote, approve_waivers


@pytest_asyncio.fixture
async def game(
    complex_scn: RawGameScenario, author: dto.Player, dao: HolderDao, dcf: Factory, file_storage: FileStorage,
) -> dto.FullGame:
    return await upsert_game(
        complex_scn,
        author,
        dao.game_upserter,
        dcf,
        file_storage,
    )


@pytest_asyncio.fixture
async def completed_game(
    game: dto.FullGame, gryffindor: dto.Team, slytherin: dto.Team,
    harry: dto.Player, ron: dto.Player, hermione: dto.Player, draco: dto.Player,
    dao: HolderDao,
):
    await join_team(ron, gryffindor, harry, dao.player_in_team)
    await join_team(hermione, gryffindor, harry, dao.player_in_team)
    await dao.game.start_waivers(game)

    await add_vote(game, gryffindor, harry, Played.yes, dao.waiver_vote_adder)
    await add_vote(game, gryffindor, hermione, Played.yes, dao.waiver_vote_adder)
    await add_vote(game, gryffindor, ron, Played.no, dao.waiver_vote_adder)
    await add_vote(game, slytherin, draco, Played.yes, dao.waiver_vote_adder)
    await approve_waivers(game, gryffindor, harry, dao.waiver_approver)
    await dao.game.set_started(game)

    await dao.key_time.save_key(
        key="SHWRONG", team=gryffindor, level=game.levels[0], game=game,
        player=ron, is_correct=False, is_duplicate=False,
    )
    await dao.key_time.save_key(
        key="SH123", team=gryffindor, level=game.levels[0], game=game,
        player=harry, is_correct=True, is_duplicate=False,
    )
    await dao.key_time.save_key(
        key="SH123", team=slytherin, level=game.levels[0], game=game,
        player=draco, is_correct=True, is_duplicate=False,
    )
    await dao.key_time.save_key(
        key="SH123", team=gryffindor, level=game.levels[0], game=game,
        player=hermione, is_correct=True, is_duplicate=True,
    )
    await dao.key_time.save_key(
        key="SH321", team=slytherin, level=game.levels[0], game=game,
        player=draco, is_correct=True, is_duplicate=False,
    )
    await dao.game_player.level_up(slytherin, game.levels[0], game)
    await asyncio.sleep(1)
    await dao.key_time.save_key(
        key="SH123", team=gryffindor, level=game.levels[0], game=game,
        player=ron, is_correct=True, is_duplicate=False,
    )
    await dao.game_player.level_up(gryffindor, game.levels[0], game)
    await asyncio.sleep(2)
    await dao.key_time.save_key(
        key="SHOOT", team=gryffindor, level=game.levels[1], game=game,
        player=hermione, is_correct=True, is_duplicate=False,
    )
    await dao.game_player.level_up(gryffindor, game.levels[1], game)
    await asyncio.sleep(1)
    await dao.key_time.save_key(
        key="SHOOT", team=slytherin, level=game.levels[1], game=game,
        player=draco, is_correct=True, is_duplicate=False,
    )
    await dao.game_player.level_up(slytherin, game.levels[1], game)
    await dao.commit()

    return game
