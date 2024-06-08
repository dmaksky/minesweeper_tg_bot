import logging
from random import sample
from itertools import chain
from dataclasses import asdict
from typing import Self

import errors
from game.components import (
    GameStatus,
    GameModeSettings,
    CellState,
    Cell,
    GameDict,
)

MAX_WIDTH = 8
MAX_HEIGHT = 12

logger = logging.getLogger(__name__)


class Game:
    def __init__(self, mode: GameModeSettings) -> None:
        self.settings: GameModeSettings = mode
        self._founded_mines: int = 0
        self.marked_cells: int = 0
        self.status: GameStatus = GameStatus.GOING
        self.field: list[list[Cell]] = self._gen_field()

    def _gen_field(self) -> list[list[Cell]]:
        width = self.settings.field_width
        height = self.settings.field_height

        if not (0 < width <= MAX_WIDTH) or not (0 < height <= MAX_HEIGHT):
            raise errors.FieldGenerationError(
                errors.error_messages["FieldGenerationError"]
            )

        field = [
            [Cell(False, 0, CellState.CLOSED) for _ in range(width)]
            for _ in range(height)
        ]

        return field

    def generate_mines(self, x: int, y: int) -> None:
        field_copy = self.field.copy()
        field_copy[x] = field_copy[x].copy()
        try:
            field_copy[x].pop(y)
            mine_cells = sample(
                list(chain.from_iterable(field_copy)),
                self.settings.number_of_mines,
            )
        except IndexError as err:
            raise errors.CellOpeningError(
                errors.error_messages["CellOpeningIndexError"]
            ) from err
        except ValueError as err:
            raise errors.MinesGenerationError(
                errors.error_messages["MinesGenerationError"]
            ) from err

        for cell in mine_cells:
            cell.is_mine = True

        self._count_mines_around_cells()

    def _get_neigh_cells(self, x: int, y: int) -> list[tuple[Cell, int, int]]:
        cells_indexes = (
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x, y - 1),
            (x, y + 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
        )

        neigh_cells = [
            (self.field[x][y], x, y)
            for (x, y) in cells_indexes
            if 0 <= x < self.settings.field_height
            and 0 <= y < self.settings.field_width
        ]

        return neigh_cells

    def _count_mines_around_cells(self) -> None:
        for x, row in enumerate(self.field):
            for y, cell in enumerate(row):
                neigh_cells = [
                    neigh_cell.is_mine
                    for neigh_cell, _, _ in self._get_neigh_cells(x, y)
                ]
                cell.neigh_mines_num = neigh_cells.count(True)

    def _show_all_mines(self) -> None:
        mines = [cell for row in self.field for cell in row if cell.is_mine]

        for mine in mines:
            mine.state = CellState.OPENED

    def _open_neigh_cells(self, cell: Cell, x: int, y: int) -> None:
        cell.state = CellState.OPENED

        if cell.neigh_mines_num != 0:
            return

        neigh_cells = [
            (neigh_cell, x, y)
            for neigh_cell, x, y in self._get_neigh_cells(x, y)
            if not neigh_cell.is_mine and neigh_cell.state == CellState.CLOSED
        ]

        for cell, x, y in neigh_cells:
            try:
                self._open_neigh_cells(cell, x, y)
            except RecursionError as err:
                raise errors.CellOpeningError(
                    errors.error_messages["CellOpeningRecursionError"]
                ) from err

    def open_cell(self, x: int, y: int) -> None:
        try:
            cell: Cell = self.field[x][y]
        except IndexError as err:
            raise errors.CellOpeningError(
                errors.error_messages["CellOpeningIndexError"]
            ) from err

        if cell.state == CellState.OPENED:
            return

        if cell.is_mine:
            self._show_all_mines()
            self.status = GameStatus.LOSE
            return

        self._open_neigh_cells(cell, x, y)

    def toggle_mark(self, x: int, y: int) -> None:
        try:
            cell: Cell = self.field[x][y]
        except IndexError as err:
            raise errors.MarkToggleError(
                errors.error_messages["MarkToggleError"]
            ) from err

        match cell.state:
            case CellState.MARKED:
                cell.state = CellState.CLOSED
            case CellState.CLOSED:
                cell.state = CellState.MARKED
            case _:
                return

        self.marked_cells += cell.state

        if cell.is_mine:
            self._founded_mines += cell.state

        if self._founded_mines == self.settings.number_of_mines:
            self.status = GameStatus.WIN

    def to_dict(self) -> GameDict:
        return {
            "settings": self.settings._asdict(),
            "founded_mines": self._founded_mines,
            "marked_cells": self.marked_cells,
            "field": [[asdict(cell) for cell in row] for row in self.field],
        }

    @classmethod
    def from_dict(cls, data: GameDict) -> Self:
        mode_settings = GameModeSettings(**data["settings"])
        game = cls(mode_settings)
        game._founded_mines = data["founded_mines"]
        game.marked_cells = data["marked_cells"]
        game.field = [
            [
                Cell(
                    cell["is_mine"],
                    cell["neigh_mines_num"],
                    CellState(cell["state"]),
                )
                for cell in row
            ]
            for row in data["field"]
        ]
        return game
