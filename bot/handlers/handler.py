from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select

from bot.keyboards.keyboard import contact_keyboard, lead_keyboard
from database import User

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext, command: CommandStart) -> None:
    param = command.args
    user_data = message.from_user.model_dump(include={'id', 'first_name', 'last_name', 'username'})
    if param:
        user = await User.get(_id=user_data['id'])
        if user.type == user.Type.OPERATOR:
            await message.answer("", reply_markup=lead_keyboard())

        # elif user.type == user.Type.ADMIN:
        #     await message.answer("", reply_markup=contact_keyboard())
        # elif user.type == user.Type.SUPER_USER:
        #     await message.answer("", reply_markup=contact_keyboard())
        #
        else:
            await state.update_data(start_param=param)
            await message.answer("Assalomu alaykum !", reply_markup=contact_keyboard())
    else:
        param = "boshqa"
        await message.answer("Assalomu alaykum !", reply_markup=contact_keyboard())
        await state.update_data(start_param=param)


@router.message(F.contact)
async def contact_handler(message: Message, state: FSMContext) -> None:
    user_data = message.from_user.model_dump(include={'id', 'first_name', 'last_name', 'username'})
    contact = message.contact
    road = await state.get_data()
    print(f"{contact}\n{user_data['first_name']} {user_data['last_name']}")
    await User.create(
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        username=user_data['username'],
        telegram_id=message.from_user.id,
        type=User.Type.USER,
        road=road.get('param'),
        phone_number=contact.phone_number
    )

    await message.answer("✅ Foydalanuvchi ma'lumotlari saqlandi.")
