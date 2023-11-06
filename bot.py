import asyncio
import logging
import sys
import settings

from tortoise import Tortoise
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.start.router import start_router

# Bot token can be obtained via https://t.me/BotFather

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(start_router)


async def main() -> None:
    bot = Bot(settings.BOT_TOKEN, parse_mode=ParseMode.HTML)

    try:
        await Tortoise.init(
            db_url=f'sqlite://{settings.DB_URL}',
            modules={
                'models': ['db.models.user']
            }
        )
        await Tortoise.generate_schemas()

        await bot.set_my_commands(
            commands=[
                types.BotCommand(command='start', description='Запустить бота'),
            ],
            scope=types.BotCommandScopeDefault()
        )

        await dp.start_polling(bot)

    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())