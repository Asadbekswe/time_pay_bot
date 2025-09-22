from aiogram import html, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.reply import request_contact_user
from bot.states.users import UserState
from database import User

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    user_data = message.from_user.model_dump(include={'id', 'first_name', 'last_name', 'username'})
    existing_user = await User.get(_id=user_data['id'])

    if not existing_user:
        await User.create(
            id=user_data['id'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            username=user_data['username'],
        )
    await state.set_state(UserState.phone_number)
    await message.answer(f"Assalomu aleykum 👋🏻, {html.bold(message.from_user.full_name)}!",
                         reply_markup=request_contact_user())


@router.message(F.contact, UserState.phone_number)
async def user_request_contact_handler(message: Message, state: FSMContext) -> None:
    phone_number = message.contact.phone_number[-9:]
    await state.update_data(phone_number=phone_number)
    await User.update(_id=message.from_user.id, phone_number=phone_number)
    await message.reply("Tez orada Operatorlarimiz siz bilan Bog'lanishadi ✅ !!!")
