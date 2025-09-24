from mmap import ACCESS_WRITE

from aiogram import Router
from aiogram.types import Message

from bot.filters.base_filter import IsOperator

operator_router = Router()
operator_router.message.filter(IsOperator())
operator_router.callback_query.filter(IsOperator())


@operator_router.message()
async def lead_handler(message: Message) -> None:
    await message.answer("HI OPERATOR")
