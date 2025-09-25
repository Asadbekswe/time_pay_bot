from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery

from bot.filters.base_filter import IsSuperUser
from database import User

super_user_router = Router()
super_user_router.message.filter(IsSuperUser())
super_user_router.callback_query.filter(IsSuperUser())


@super_user_router.message()
async def admin_handler(message: Message) -> None:
    await message.answer("HI SUPER USER")


@super_user_router.callback_query(F.data.startswith("acceptance:"))
async def accept_operator_callback(callback: CallbackQuery, bot: Bot) -> None:
    user_id = int(callback.data.split(":")[1])
    user = await User.get(_id=user_id)
    user.type = User.Type.ADMIN
    await user.commit()

    await callback.message.edit_text(f"{user.first_name or user.last_name} admin sifatida qabul qilindi ✅")
    try:
        await bot.send_message(user_id, "Siz admin sifatida qabul qilindingiz! ✅")
    except Exception as e:
        print(f"Xabar yuborilmadi user_id={user_id}: {e}")


@super_user_router.callback_query(F.data.startswith("not_acceptance:"))
async def reject_operator_callback(callback: CallbackQuery, bot: Bot) -> None:
    user_id = int(callback.data.split(":")[1])
    user = await User.get(_id=user_id)

    await callback.message.edit_text(f"{user.first_name or user.last_name} admin sifatida rad etildi ❌")
    try:
        await bot.send_message(user_id, "Siz admin sifatida rad etildingiz ❌")
    except Exception as e:
        print(f"Xabar yuborilmadi user_id={user_id}: {e}")
