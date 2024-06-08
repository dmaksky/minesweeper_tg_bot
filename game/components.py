from enum import Enum, IntEnum, auto
from typing import NamedTuple, TypedDict, Any
from dataclasses import dataclass


class GameModeSettings(NamedTuple):
    field_width: int
    field_height: int
    number_of_mines: int


class CellState(IntEnum):
    CLOSED = -1
    OPENED = 0
    MARKED = 1


@dataclass(slots=True)
class Cell:
    is_mine: bool
    neigh_mines_num: int
    state: CellState


class GameStatus(Enum):
    GOING = auto()
    LOSE = auto()
    WIN = auto()


class GameModes(Enum):
    SMALL = GameModeSettings(8, 8, 10)
    BIG = GameModeSettings(8, 12, 20)


class GameDict(TypedDict):
    settings: dict[str, int]
    founded_mines: int
    marked_cells: int
    field: list[list[dict[str, Any]]]
