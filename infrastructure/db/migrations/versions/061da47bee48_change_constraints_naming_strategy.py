"""change constraints naming strategy

Revision ID: 061da47bee48
Revises: 51e122b5e734
Create Date: 2023-01-28 12:28:35.762087

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "061da47bee48"
down_revision = "852f6bcc741f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("chats_tg_id_key", "chats", type_="unique")
    op.create_unique_constraint(op.f("uq__chats__tg_id"), "chats", ["tg_id"])
    op.drop_constraint("files_info_guid_key", "files_info", type_="unique")
    op.create_unique_constraint(op.f("uq__files_info__guid"), "files_info", ["guid"])
    op.drop_constraint("games_author_id_name_key", "games", type_="unique")
    op.drop_constraint("games_name_key", "games", type_="unique")
    op.create_unique_constraint(op.f("uq__games__author_id"), "games", ["author_id", "name"])
    op.create_unique_constraint(op.f("uq__games__name"), "games", ["name"])
    op.drop_constraint("levels_author_id_name_id_key", "levels", type_="unique")
    op.create_unique_constraint(op.f("uq__levels__author_id"), "levels", ["author_id", "name_id"])
    op.drop_constraint(
        "levels_times_game_id_team_id_level_number_key", "levels_times", type_="unique"
    )
    op.create_unique_constraint(
        op.f("uq__levels_times__game_id"), "levels_times", ["game_id", "team_id", "level_number"]
    )
    op.drop_constraint("organizers_player_id_game_id_key", "organizers", type_="unique")
    op.create_unique_constraint(
        op.f("uq__organizers__player_id"), "organizers", ["player_id", "game_id"]
    )
    op.drop_constraint("players_user_id_key", "players", type_="unique")
    op.create_unique_constraint(op.f("uq__players__user_id"), "players", ["user_id"])
    op.drop_constraint("teams_chat_id_key", "teams", type_="unique")
    op.create_unique_constraint(op.f("uq__teams__chat_id"), "teams", ["chat_id"])
    op.drop_constraint("users_tg_id_key", "users", type_="unique")
    op.create_unique_constraint(op.f("uq__users__tg_id"), "users", ["tg_id"])
    op.drop_constraint("waivers_game_id_team_id_player_id_key", "waivers", type_="unique")
    op.create_unique_constraint(
        op.f("uq__waivers__game_id"), "waivers", ["game_id", "team_id", "player_id"]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("uq__waivers__game_id"), "waivers", type_="unique")
    op.create_unique_constraint(
        "waivers_game_id_team_id_player_id_key", "waivers", ["game_id", "team_id", "player_id"]
    )
    op.drop_constraint(op.f("uq__users__tg_id"), "users", type_="unique")
    op.create_unique_constraint("users_tg_id_key", "users", ["tg_id"])
    op.drop_constraint(op.f("uq__teams__chat_id"), "teams", type_="unique")
    op.create_unique_constraint("teams_chat_id_key", "teams", ["chat_id"])
    op.drop_constraint(op.f("uq__players__user_id"), "players", type_="unique")
    op.create_unique_constraint("players_user_id_key", "players", ["user_id"])
    op.drop_constraint(op.f("uq__organizers__player_id"), "organizers", type_="unique")
    op.create_unique_constraint(
        "organizers_player_id_game_id_key", "organizers", ["player_id", "game_id"]
    )
    op.drop_constraint(op.f("uq__levels_times__game_id"), "levels_times", type_="unique")
    op.create_unique_constraint(
        "levels_times_game_id_team_id_level_number_key",
        "levels_times",
        ["game_id", "team_id", "level_number"],
    )
    op.drop_constraint(op.f("uq__levels__author_id"), "levels", type_="unique")
    op.create_unique_constraint("levels_author_id_name_id_key", "levels", ["author_id", "name_id"])
    op.drop_constraint(op.f("uq__games__name"), "games", type_="unique")
    op.drop_constraint(op.f("uq__games__author_id"), "games", type_="unique")
    op.create_unique_constraint("games_name_key", "games", ["name"])
    op.create_unique_constraint("games_author_id_name_key", "games", ["author_id", "name"])
    op.drop_constraint(op.f("uq__files_info__guid"), "files_info", type_="unique")
    op.create_unique_constraint("files_info_guid_key", "files_info", ["guid"])
    op.drop_constraint(op.f("uq__chats__tg_id"), "chats", type_="unique")
    op.create_unique_constraint("chats_tg_id_key", "chats", ["tg_id"])
    # ### end Alembic commands ###
