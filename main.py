import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from bot.handlers.handler import router
from database import db as database

load_dotenv('.env')

dp = Dispatcher()


async def on_startup():
    logging.info("Starting up...")
    await database.create_all()


async def on_shutdown(bot: Bot):
    # await database.drop_all()
    await bot.delete_my_commands()


async def main() -> None:
    bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
