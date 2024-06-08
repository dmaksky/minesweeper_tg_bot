import asyncio
import logging

from aiogram import F, Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import callbacks, commands, others
from keyboards import set_main_menu
from lexicon import LEXICON_EN, LEXICON_RU
from middlewares import TranslatorMiddleware, CheckActiveBoardMiddleware
from settings import config
from database import init_database

TRANSLATIONS = {
    "default": "ru",
    "en": LEXICON_EN,
    "ru": LEXICON_RU,
}

logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("Starting bot")

    bot = Bot(
        config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    if config.session_storage == "memory":
        dp = Dispatcher(storage=MemoryStorage())
    else:
        logger.debug("Redis url: %s", config.redis_dsn)
        logger.debug("Instance: %s", type(config.redis_dsn))
        dp = Dispatcher(storage=RedisStorage.from_url(str(config.redis_dsn)))

    gifs = {"win": config.win_gif, "lose": config.lose_gif}

    init_database(config.database_name)

    await set_main_menu(bot)

    dp.message.filter(F.chat.type == "private")

    dp.include_routers(callbacks.router, commands.router, others.router)

    dp.update.middleware(TranslatorMiddleware())
    dp.callback_query.outer_middleware(CheckActiveBoardMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        translations=TRANSLATIONS,
        gifs=gifs,
        db_name=config.database_name,
    )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )
    asyncio.run(main())
