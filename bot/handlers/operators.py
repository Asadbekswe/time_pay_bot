from aiogram import Router, F
from aiogram.types import Message

from bot.filters.base_filter import IsOperator
from bot.keyboards.reply import operator_btn, OperatorButtons
from database import Lead, User

operator_router = Router()
operator_router.message.filter(IsOperator())
operator_router.callback_query.filter(IsOperator())


@operator_router.message()
async def lead_handler(message: Message) -> None:
    await message.answer(
        f"<blockquote>{message.from_user.full_name}</blockquote> <i><b>Assalomu aleykum, bugungi aloqalarda </b></i><tg-spoiler> OMAD !!! </tg-spoiler>",
        reply_markup=operator_btn())


@operator_router.message(F.text == OperatorButtons.MY_LEADS)
async def my_leads_handler(message: Message) -> None:
    leads = await Lead.filter(operator_id=message.from_user.id, status=Lead.Status.NEW_LEAD)
    for lead in leads:
        user = await User.get(lead.user_id)
        text = f"""
        Lead ID: {lead.id} \n
        Lead Status 📌: {lead.status.value.capitalize()} \n
        Foydalanuvchi 👤: {user.first_name} {user.last_name} \n
        Telefon raqami 📞: +998{user.phone_number} \n
        Username: @{user.username if user.username else "🤷🏻"}
        """
        await message.answer(text)


@operator_router.message(F.text == OperatorButtons.MEETING)
async def meeting_handler(message: Message) -> None:
    pass


@operator_router.message(F.text == OperatorButtons.NEED_LEADS)
async def need_leads_handler(message: Message) -> None:
    pass
