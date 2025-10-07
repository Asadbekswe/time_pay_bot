from aiogram import F, Bot
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.filters.base_filter import IsUser
from bot.keyboards.keyboard import request_operator_keyboard
from bot.keyboards.reply import request_contact_user
from bot.states.users import UserState
from database import User, Lead

user_router = Router()

user_router.message.filter(IsUser())
user_router.callback_query.filter(IsUser())


@user_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext, command: CommandStart) -> None:
    param = command.args or "telegram"

    lead = await Lead.filter(user_id=message.from_user.id, status=Lead.Status.NEW_LEAD)

    if not lead:
        await Lead.create(
            visit_by=param,
            user_id=message.from_user.id,
        )
        await state.set_state(UserState.phone_number)

        await message.answer(
            f"👋🏻 Assalomu aleykum, <b>{message.from_user.full_name}</b>!\n" f"📱 Telefon raqamingizni yuboring.",
            reply_markup=request_contact_user()
        )
    else:
        text = (
            f"⏳ Tez orada siz bilan aloqaga chiqamiz!\n\n"
            f"🙏 Keltirilgan noqulayliklar uchun uzr so‘raymiz, <b>{message.from_user.full_name}</b>.\n\n"
            f"🤝 Hurmat bilan — <b>TimePay jamoasi</b>!"
        )
        await message.answer(text)


@user_router.message(F.contact, UserState.phone_number)
async def user_request_contact_handler(message: Message, state: FSMContext) -> None:
    phone_number = message.contact.phone_number[-9:]
    await state.update_data(phone_number=phone_number)
    await User.update(_id=message.from_user.id, phone_number=phone_number)
    await message.reply_video("Tez orada Operatorlarimiz siz bilan Bog'lanishadi ✅ !!!",
                        reply_markup=ReplyKeyboardRemove())


@user_router.message(Command("request_operator"))
async def request_operator(message: Message, bot: Bot) -> None:
    await message.answer("📨 Siz operator bo‘lish uchun ariza yubordingiz!")

    admins = await User.filter(type=User.Type.ADMIN)
    user = await User.get(_id=message.from_user.id)

    text = (
        f"👤 FISH: {user.first_name or ''} {user.last_name or ''}\n"
        f"📛 Username: @{user.username if user.username else '🤷🏻'}\n"
        f"📱 Tel: +998{user.phone_number}\n"
    )

    for admin in admins:
        try:
            await bot.send_message(
                admin.id,
                text=text,
                reply_markup=request_operator_keyboard(user_id=user.id),
            )
        except Exception as e:
            print(f"❌ Xatolik: {e}")


@user_router.message(Command("request_admin"))
async def request_admin(message: Message, bot: Bot) -> None:
    await message.answer("✅ Siz admin bo‘lish uchun ariza yubordingiz!")

    super_users = await User.filter(type=User.Type.SUPER_USER)
    user = await User.get(_id=message.from_user.id)

    text = (
        f"👤 FISH: {user.first_name or ''} {user.last_name or ''}\n"
        f"📛 Username: @{user.username if user.username else '🤷🏻'}\n"
        f"📱 Tel: +998{user.phone_number}\n"
    )

    for super_user in super_users:
        try:
            await bot.send_message(
                super_user.id,
                text=text,
                reply_markup=request_operator_keyboard(user_id=user.id),
            )
        except Exception as e:
           print(f"❌ Xatolik: {e}")
