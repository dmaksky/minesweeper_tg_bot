from collections.abc import Mapping

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from game.components import GameModes
from cbdata import MenuCallbackFactory

MENU_WIDTH = 1


def get_game_menu_kb(lexicon: Mapping[str, str]) -> InlineKeyboardMarkup:
    buttons = []
    kb_builder = InlineKeyboardBuilder()

    for mode in GameModes:
        buttons.append(
            InlineKeyboardButton(
                text=lexicon["game_mode"].format(**mode.value._asdict()),
                callback_data=MenuCallbackFactory(mode=mode.name).pack(),
            )
        )

    buttons.append(
        InlineKeyboardButton(
            text=lexicon["cancel_menu_entry"], callback_data="cancel"
        )
    )

    kb_builder.row(*buttons, width=MENU_WIDTH)
    return kb_builder.as_markup()
