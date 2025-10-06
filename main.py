import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from bot.handlers.admins import admin_router
from bot.handlers.operators import operator_router
from bot.handlers.super_users import super_user_router
from bot.handlers.users import user_router
from bot.tasks.task import reminder_worker
from utils import on_startup, on_shutdown

load_dotenv()

dp = Dispatcher()


async def main() -> None:
    bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(user_router, operator_router, admin_router, super_user_router)
    asyncio.create_task(reminder_worker(bot))
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())