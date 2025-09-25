from aiogram import F, Bot
from aiogram import Router
from aiogram.types import Message, CallbackQuery

from bot.filters.base_filter import IsAdmin
from bot.keyboards.reply import admin_btn
from database import User

admin_router = Router()
admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())


@admin_router.message()
async def admin_handler(message: Message) -> None:
    await message.answer(
        f"<blockquote>{message.from_user.full_name}</blockquote> <i><b>Assalomu aleykum, admin 😎 !</b></i>",
        reply_markup=admin_btn())


@admin_router.callback_query(F.data.startswith("acceptance:"))
async def accept_operator_callback(callback: CallbackQuery, bot: Bot) -> None:
    user_id = int(callback.data.split(":")[1])
    user = await User.get(_id=user_id)
    user.type = User.Type.OPERATOR
    await user.commit()

    await callback.message.edit_text(f"{user.first_name or user.last_name} operator sifatida qabul qilindi ✅")
    try:
        await bot.send_message(user_id, "Siz operator sifatida qabul qilindingiz! ✅")
    except Exception as e:
        print(f"Xabar yuborilmadi user_id={user_id}: {e}")


@admin_router.callback_query(F.data.startswith("not_acceptance:"))
async def reject_operator_callback(callback: CallbackQuery, bot: Bot) -> None:
    user_id = int(callback.data.split(":")[1])
    user = await User.get(_id=user_id)

    await callback.message.edit_text(f"{user.first_name or user.last_name} operator sifatida rad etildi ❌")
    try:
        await bot.send_message(user_id, "Siz operator sifatida rad etildingiz ❌")
    except Exception as e:
        print(f"Xabar yuborilmadi user_id={user_id}: {e}")
