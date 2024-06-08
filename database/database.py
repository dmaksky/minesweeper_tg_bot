import sqlite3
import logging
from contextlib import closing


logger = logging.getLogger()

NOT_INIT = (-1, -1)

CREATE_DB_QUERY: str = """CREATE TABLE IF NOT EXISTS player_stat(
                              player_id INTEGER PRIMARY KEY NOT NULL,
                              losses INTEGER NOT NULL DEFAULT 0,
                              wins INTEGER NOT NULL DEFAULT 0
                          )"""

CREATE_PLAYER_QUERY: str = """INSERT INTO player_stat(player_id)
                              VALUES (?)"""

UPDATE_PLAYER_WINS_QUERY: str = """UPDATE player_stat
                                   SET wins = wins + 1
                                   WHERE player_id == ?"""

UPDATE_PLAYER_LOSSES_QUERY: str = """UPDATE player_stat
                                     SET losses = losses + 1
                                     WHERE player_id == ?"""

GET_PLAYER_STAT_QUERY: str = """SELECT losses, wins FROM player_stat
                                WHERE player_id == ?"""


def init_database(db_name: str) -> None:
    try:
        with closing(sqlite3.connect(db_name)) as conn:
            conn.execute(CREATE_DB_QUERY)
            conn.commit()
    except sqlite3.Error:
        logger.exception("Error in database")


def init_player_stat(db_name: str, player_id: int) -> None:
    try:
        with closing(sqlite3.connect(db_name)) as conn:
            conn.execute(CREATE_PLAYER_QUERY, (player_id,))
            conn.commit()
    except sqlite3.Error:
        logger.exception("Error in database")


def update_player_stat(db_name: str, player_id: int, is_win: bool):
    try:
        with closing(sqlite3.connect(db_name)) as conn:
            if is_win:
                conn.execute(UPDATE_PLAYER_WINS_QUERY, (player_id,))
            else:
                conn.execute(UPDATE_PLAYER_LOSSES_QUERY, (player_id,))
            conn.commit()
    except sqlite3.Error:
        logger.exception("Error in database")


def get_player_stat(db_name: str, player_id: int) -> tuple[int, int]:
    try:
        with closing(sqlite3.connect(db_name)) as conn:
            result = conn.execute(
                GET_PLAYER_STAT_QUERY, (player_id,)
            ).fetchone()
            if not result:
                return NOT_INIT

            return result
    except sqlite3.Error:
        logger.exception("Error in database")
