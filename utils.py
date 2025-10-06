import logging

from aiogram import Bot
from aiogram.types import BotCommand


async def on_startup(bot: Bot):
    my_commands = [
        BotCommand(command='start', description="🏁 Bo'tni ishga tushirish"),
        BotCommand(command='myinfo', description="📝 Mening malumotlarim"),
        # BotCommand(command="request operator 📞", description="Operator Bo'lish 📞"),
        # BotCommand(command="request admin  😎", description="Admin Bo'lish 😎"),
        BotCommand(command='help', description="🆘 yordam"),
    ]
    await bot.set_my_commands(commands=my_commands)
    logging.info("Starting up...")
    # await database.create_all()


async def on_shutdown(bot: Bot):
    # await database.drop_all()
    await bot.delete_my_commands()
