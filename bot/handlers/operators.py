import datetime

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.filters.base_filter import IsOperator
from bot.keyboards.keyboard import lead_operator_keyboard
from bot.keyboards.reply import operator_btn, OperatorButtons
from database import Lead, User
from database.models import Meeting

operator_router = Router()
operator_router.message.filter(IsOperator())
operator_router.callback_query.filter(IsOperator())


def limit(limit):
    def decorator(func):
        pass


@operator_router.message(CommandStart())
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
async def meeting_handler(message: Message, bot: Bot) -> None:
    meetings = await Meeting.filter(meeting_id=message.from_user.id)


@operator_router.message(F.text == OperatorButtons.NEED_LEADS)
async def need_leads_handler(message: Message) -> None:
    operator = await User.get(message.from_user.id)
    leads = await Lead.filter(
        status=Lead.Status.NEW_LEAD,
        operator_id=operator.id
    )
    operator_lead_count = len(leads)
    my_lead_count = 5 - operator_lead_count

    if my_lead_count <= 0:
        await message.answer("Sizda yangi lead olish limitiga yetdingiz ✅")
        return
    unassigned_leads = await Lead.filter(status=Lead.Status.NEW_LEAD,
                                         operator_id=None)
    print(unassigned_leads)
    print("salom")
    if not unassigned_leads:
        await message.answer("Hozir Lead yuq !")
        return
    unassigned_leads = sorted(unassigned_leads, key=lambda l: l.id)  # emulate order_by(Lead.id.asc())

    leads_to_send = unassigned_leads[:my_lead_count]

    await message.answer(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Lead berilgan sana!")
    for lead in leads_to_send:
        user = await User.get(lead.user_id)
        lead.operator_id = operator.id
        await lead.commit()
    await message.answer(f"Leadlar mening leadlarimga tushdi !✅ {my_lead_count}")
