from aiogram import html, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database import User

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_data = message.from_user.model_dump(include={'id', 'first_name', 'last_name', 'username'})
    existing_user = await User.get_with_telegram_id(telegram_id=user_data['id'])

    if not existing_user:
        await User.create(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            username=user_data['username'],
            telegram_id=user_data['id'],
        )

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
