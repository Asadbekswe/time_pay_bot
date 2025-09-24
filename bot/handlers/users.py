from aiogram import F
from aiogram import html, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.filters.base_filter import IsUser
from bot.keyboards.reply import request_contact_user
from bot.states.users import UserState
from database import User, Lead

user_router = Router()

user_router.message.filter(IsUser())
user_router.callback_query.filter(IsUser())


@user_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext, command: CommandStart) -> None:
    param = command.args

    if param:
        await Lead.create(
            visit_by=param,
            user_id=message.from_user.id,
        )
    else:
        await Lead.create(
            visit_by="telegram",
            user_id=message.from_user.id,
        )
    await state.set_state(UserState.phone_number)
    await message.answer(f"Assalomu aleykum 👋🏻, {html.bold(message.from_user.full_name)}!",
                         reply_markup=request_contact_user())


@user_router.message(F.contact, UserState.phone_number)
async def user_request_contact_handler(message: Message, state: FSMContext) -> None:
    phone_number = message.contact.phone_number[-9:]
    await state.update_data(phone_number=phone_number)
    await User.update(_id=message.from_user.id, phone_number=phone_number)
    await message.reply("Tez orada Operatorlarimiz siz bilan Bog'lanishadi ✅ !!!", reply_markup=ReplyKeyboardRemove())


@user_router.message(Command("request_operator"))
async def request_operator(message: Message):
    await message.answer("Siz operator bo‘lish uchun ariza yubordingiz!")


@user_router.message(Command("request_admin"))
async def request_admin(message: Message):
    await message.answer("Siz admin bo‘lish uchun ariza yubordingiz!")
