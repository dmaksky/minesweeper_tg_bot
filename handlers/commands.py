from collections.abc import Mapping

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message

from states import FSMGameState
from keyboards import get_game_menu_kb
from database import get_player_stat, NOT_INIT

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, i18n: Mapping[str, str]):
    await message.answer(text=i18n["/start"])


@router.message(Command(commands="help"), StateFilter(default_state))
async def process_help_command(message: Message, i18n: Mapping[str, str]):
    await message.answer(text=i18n["/help"])


@router.message(Command(commands="play"), StateFilter(default_state))
async def process_play_command(
    message: Message, i18n: Mapping[str, str], state: FSMContext
):
    await message.answer(
        text=i18n["/play"], reply_markup=get_game_menu_kb(i18n)
    )
    await state.set_state(FSMGameState.menu)


@router.message(Command(commands="stat"), StateFilter(default_state))
async def process_stat_command(
    message: Message, i18n: Mapping[str, str], db_name: str
):
    player_id = message.from_user.id
    stat = get_player_stat(db_name, player_id)

    if stat == NOT_INIT:
        text = i18n["no_stat"]
    else:
        losses, wins = stat
        text = i18n["stat"].format(losses=losses, wins=wins)

    await message.answer(text=text)
