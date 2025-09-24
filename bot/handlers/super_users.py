from aiogram import Router
from aiogram.types import Message

from bot.filters.base_filter import IsSuperUser

super_user = Router()
super_user.message.filter(IsSuperUser())
super_user.callback_query.filter(IsSuperUser())


@super_user.message()
async def admin_handler(message: Message) -> None:
    await message.answer("HI SUPER USER")
