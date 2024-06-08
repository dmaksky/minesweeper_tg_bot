import logging
from collections.abc import Awaitable, Callable
from typing import Any
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, TelegramObject

logger = logging.getLogger(__name__)


class CheckActiveBoardMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        state: FSMContext = data.get("state")
        current_state = await state.get_state()
        if current_state is None or current_state.endswith("menu"):
            return await handler(event, data)
        logger.debug("Current state: %s", current_state)
        logger.debug("Current callback data: %s", event.data)
        session = await state.get_data()
        if session["game_id"] != event.message.message_id:
            logger.debug("Press button from inactive board")
            return

        await handler(event, data)
