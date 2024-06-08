from contextlib import suppress
import logging
from collections.abc import Mapping

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

import database as db
from errors import MinesweeperError
from states import FSMGameState
from cbdata import (
    MenuCallbackFactory,
    FieldCallbackFactory,
    SwitchCallbackFactory,
)
from keyboards import get_game_field_kb, ClickMode
from game.components import GameStatus, GameModes
from game.logic import Game

router = Router()
logger = logging.getLogger(__name__)


async def process_game_end(
    callback: CallbackQuery,
    i18n: Mapping[str, str],
    state: FSMContext,
    game_status: GameStatus,
    gifs: Mapping[str, str],
    player_id: int,
    db_name: str,
):
    match game_status:
        case GameStatus.WIN:
            text = i18n["win_message"]
            if gifs["win"] is not None:
                gif = gifs["win"]
            db.update_player_stat(db_name, player_id, True)
            await callback.answer()
        case GameStatus.LOSE:
            text = i18n["lose_message"]
            notify = i18n["lose_notify"]
            if gifs["lose"] is not None:
                gif = gifs["lose"]
            db.update_player_stat(db_name, player_id, False)
            await callback.answer(notify)

    await callback.message.answer(text=text)
    await callback.message.answer_animation(gif)
    await state.clear()


@router.callback_query(F.data == "cancel", StateFilter(FSMGameState.menu))
async def process_cancel_press(
    callback: CallbackQuery, i18n: Mapping[str, str], state: FSMContext
):
    await callback.message.edit_text(text=i18n["cancel_message"])
    await state.clear()


@router.callback_query(
    StateFilter(FSMGameState.menu),
    MenuCallbackFactory.filter(
        F.mode.in_(set(map(lambda item: item.name, GameModes)))
    ),
)
async def process_mode_press(
    callback: CallbackQuery,
    callback_data: MenuCallbackFactory,
    i18n: Mapping[str, str],
    db_name: str,
    state: FSMContext,
):
    mode = GameModes[callback_data.mode].value

    try:
        game = Game(mode)
    except MinesweeperError:
        logger.exception("Error in game logic")
        await callback.message.edit_text(text=i18n["error"].format())
        await state.clear()
        return

    player_id = callback.from_user.id

    stat = db.get_player_stat(db_name, player_id)
    if stat == db.NOT_INIT:
        db.init_player_stat(db_name, player_id)

    session = {
        "game_id": callback.message.message_id,
        "game_dict": game.to_dict(),
        "is_first_move": True,
    }

    await callback.message.edit_text(
        text=i18n["mines_marked"].format(
            mines_total=mode.number_of_mines, mines_marked=0
        ),
        reply_markup=get_game_field_kb(game, i18n, ClickMode.click),
    )

    await state.set_state(FSMGameState.field)
    await state.set_data(session)


@router.callback_query(
    StateFilter(FSMGameState.field),
    FieldCallbackFactory.filter(
        F.click_mode.in_(set(map(lambda item: item.name, ClickMode)))
    ),
)
async def process_cell_press(
    callback: CallbackQuery,
    callback_data: FieldCallbackFactory,
    state: FSMContext,
    i18n: Mapping[str, str],
    db_name: str,
    gifs: Mapping[str, str],
):
    player_id = callback.from_user.id

    session = await state.get_data()
    game = Game.from_dict(session["game_dict"])
    mode = ClickMode[callback_data.click_mode]

    try:
        if session["is_first_move"]:
            game.generate_mines(callback_data.x, callback_data.y)
            session["is_first_move"] = False

        if mode == ClickMode.click:
            game.open_cell(callback_data.x, callback_data.y)
        else:
            game.toggle_mark(callback_data.x, callback_data.y)
    except MinesweeperError:
        logger.exception("Error in game logic")
        return

    mines_total = game.settings.number_of_mines
    mines_marked = game.marked_cells

    text = i18n["mines_marked"].format(
        mines_total=mines_total, mines_marked=mines_marked
    )

    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text=text, reply_markup=get_game_field_kb(game, i18n, mode)
        )


    match game.status:
        case GameStatus.GOING:
            session["game_dict"] = game.to_dict()
            await state.update_data(**session)
            await callback.answer()
        case _:
            await process_game_end(
                callback, i18n, state, game.status, gifs, player_id, db_name
            )


@router.callback_query(
    StateFilter(FSMGameState.field),
    SwitchCallbackFactory.filter(
        F.click_mode.in_(set(map(lambda item: item.name, ClickMode)))
    ),
)
async def process_switch_press(
    callback: CallbackQuery,
    callback_data: SwitchCallbackFactory,
    i18n: Mapping[str, str],
    state: FSMContext,
):
    session = await state.get_data()
    game = Game.from_dict(session["game_dict"])
    mode = ClickMode[callback_data.click_mode]

    mines_total = game.settings.number_of_mines
    mines_marked = game.marked_cells

    await callback.message.edit_text(
        text=i18n["mines_marked"].format(
            mines_total=mines_total, mines_marked=mines_marked
        ),
        reply_markup=get_game_field_kb(game, i18n, ~mode),
    )
