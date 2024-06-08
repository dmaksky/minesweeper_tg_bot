from typing import Any
from collections.abc import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")

        if user is None:
            return await handler(event, data)

        user_lang = user.language_code
        translations = data.get("translations")

        if translations is None:
            return await handler(event, data)

        data["i18n"] = translations.get(
            user_lang, translations[translations["default"]]
        )

        return await handler(event, data)
