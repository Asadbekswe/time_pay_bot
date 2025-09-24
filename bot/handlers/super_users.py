from aiogram import Router
from aiogram.types import Message

from bot.filters.base_filter import IsSuperUser

super_user_router = Router()
super_user_router.message.filter(IsSuperUser())
super_user_router.callback_query.filter(IsSuperUser())


@super_user_router.message()
async def admin_handler(message: Message) -> None:
    await message.answer("HI SUPER USER")
