from aiogram import Router
from aiogram.types import Message, CallbackQuery

router = Router()

@router.callback_query()
async def process_inactive_field_press(callback: CallbackQuery):
    await callback.answer()


@router.message()
async def process_other_updates(message: Message, i18n: dict[str, str]):
    await message.answer(i18n["unexpected_command"])
