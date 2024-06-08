from enum import Flag, auto
from collections.abc import Mapping

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from game.components import CellState, Cell
from game.logic import Game
from cbdata import FieldCallbackFactory, SwitchCallbackFactory


class ClickMode(Flag):
    click = auto()
    mark = auto()


def get_game_field_kb(
    game: Game, lexicon: Mapping[str, str], click_mode: ClickMode
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = []

    for x, row in enumerate(game.field):
        for y, cell in enumerate(row):
            match cell:
                case Cell(state=CellState.OPENED, is_mine=True):
                    text = lexicon["mine"]
                case Cell(
                    state=CellState.OPENED, neigh_mines_num=mines_num
                ) if mines_num > 0:
                    text = lexicon["mines_num"].format(mines_num=mines_num)
                case Cell(state=CellState.OPENED):
                    text = lexicon["opened"]
                case Cell(state=CellState.MARKED):
                    text = lexicon["marked"]
                case _:
                    text = lexicon["closed"]

            buttons.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=FieldCallbackFactory(
                        x=x, y=y, click_mode=str(click_mode.name)
                    ).pack(),
                )
            )

    text = lexicon[click_mode.name]

    kb_builder.add(*buttons)
    kb_builder.adjust(game.settings.field_width)
    kb_builder.row(
        InlineKeyboardButton(
            text=text,
            callback_data=SwitchCallbackFactory(
                click_mode=str(click_mode.name)
            ).pack(),
        )
    )
    kb_builder.button
    return kb_builder.as_markup()
