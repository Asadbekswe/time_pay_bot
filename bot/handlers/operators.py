import datetime
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from bot.filters.base_filter import IsOperator
from bot.keyboards.keyboard import operator_lead_keyboard
from bot.keyboards.reply import operator_btn, OperatorButtons
from bot.states.users import OperatorCommentState, OperatorMeetingState
from database import Lead, User
from database.models import Meeting, Comment

operator_router = Router()
operator_router.message.filter(IsOperator())
operator_router.callback_query.filter(IsOperator())


@operator_router.message(CommandStart())
async def lead_handler(message: Message) -> None:
    await message.answer(
        f"<blockquote>{message.from_user.full_name}</blockquote> <i><b>Assalomu aleykum, bugungi aloqalarda </b><tg-spoiler> OMAD !!! </tg-spoiler></i>",
        reply_markup=operator_btn())


@operator_router.message(F.text == OperatorButtons.MY_LEADS)
async def my_leads_handler(message: Message) -> None:
    leads = await Lead.filter(operator_id=message.from_user.id, status=Lead.Status.NEW_LEAD, order_by="created_at",
                              desc=True)

    if not leads:
        await message.answer("📭 Hozircha yangi lead mavjud emas.")
        return

    for lead in leads:
        user = await User.get(lead.user_id)
        text = (
            f"🆔 Lead ID: {lead.id}\n"
            f"📌 Holati: {lead.status.value}\n"
            f"👤 Foydalanuvchi: {user.first_name} {user.last_name}\n"
            f"📞 Telefon: +998{user.phone_number}\n"
            f"💬 Username: {"@" + user.username if user.username else '🤷🏻'}"
        )
        await message.answer(text, reply_markup=operator_lead_keyboard(lead.id))


@operator_router.message(F.text == OperatorButtons.MEETINGS)
async def meeting_handler(message: Message) -> None:
    meetings = await Meeting.filter(operator_id=message.from_user.id)

    if not meetings:
        await message.answer("📭 Sizda hali uchrashuvlar mavjud emas!")
        return

    for meeting in meetings:
        lead = await Lead.get(meeting.lead_id)
        user = await User.get(lead.user_id)

        text = (
            f"📌 <b>LEAD ID:</b> {meeting.lead_id}\n"
            f"👤 <b>Foydalanuvchi:</b> {user.first_name} {user.last_name}\n"
            f"📅 <b>Sana:</b> <code>{meeting.meeting_date.strftime('%d.%m.%Y - %H:%M')}</code>\n"
            f"🏠 <b>Manzil:</b> {meeting.address}\n"
            "-------------------------"
        )
        await message.answer(text)


@operator_router.message(F.text == OperatorButtons.NEED_LEADS)
async def need_leads_handler(message: Message) -> None:
    operator = await User.get(message.from_user.id)

    operator_leads = await Lead.filter(
        status=Lead.Status.NEW_LEAD,
        operator_id=operator.id,
    )
    taken_count = len(operator_leads)
    remaining_quota = 5 - taken_count

    if remaining_quota <= 0:
        await message.answer("⚠️ Siz yangi lead olish limitiga yetdingiz ✅")
        return

    unassigned_leads = await Lead.filter(
        status=Lead.Status.NEW_LEAD,
        operator_id=None,
        order_by="id"
    )

    if not unassigned_leads:
        await message.answer("📭 Hozircha yangi lead mavjud emas.")
        return

    leads_to_assign = unassigned_leads[:remaining_quota]

    for lead in leads_to_assign:
        lead.operator_id = operator.id
        await lead.commit()

    await message.answer(
        f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"🎉 {len(leads_to_assign)} ta lead sizga biriktirildi! Endi u Mening Leadlarimda ⬅️\n"
        f"👤 Operator: {operator.first_name if operator.first_name else ""} {operator.last_name if operator.last_name else ""}"
    )


@operator_router.callback_query(F.data.startswith("comment:"))
async def operator_lead_add_comment(callback: CallbackQuery, state: FSMContext) -> None:
    lead_id = int(callback.data.split(':')[-1])
    await state.set_state(OperatorCommentState.description)
    await state.update_data(lead_id=lead_id)
    await callback.message.reply("📝 Ushbu lead uchun comment yozing !!!", reply_markup=ReplyKeyboardRemove())


@operator_router.message(OperatorCommentState.description)
async def operator_lead_comment_description(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    await Comment.create(
        lead_id=data['lead_id'],
        description=message.text
    )

    await message.answer("✅ Leadga comment muvaffaqiyatli qo'shildi !!!", reply_markup=operator_btn())
    await state.clear()


@operator_router.callback_query(F.data.startswith("meeting:"))
async def operator_lead_create_meeting(callback: CallbackQuery, state: FSMContext) -> None:
    lead_id = int(callback.data.split(':')[-1])
    await state.update_data(
        lead_id=lead_id,
        operator_id=callback.from_user.id
    )
    await state.set_state(OperatorMeetingState.meeting_date)

    text = (
        "📅 <b>Ushbu Lead uchun uchrashuv sanasini kiriting!</b>\n\n"
        "Format: <code>kun.oy.yil - soat:minut</code>\n"
        "Masalan: <code>12.06.2025 - 14:00</code>\n"
        "⚠️ Faqat hozirgi yil yoki keyingi yil uchun ruxsat beriladi."
    )
    await callback.message.reply(text)


@operator_router.message(OperatorMeetingState.meeting_date)
async def operator_lead_meeting_date(message: Message, state: FSMContext) -> None:
    user_input = message.text.strip()
    now = datetime.now()
    current_year = now.year
    next_year = current_year + 1

    try:
        meeting_datetime = datetime.strptime(user_input, "%d.%m.%Y - %H:%M")
    except ValueError:
        await message.answer(
            "⚠️ <b>Format noto‘g‘ri!</b> Iltimos, quyidagi formatda kiriting: "
            "<code>12.06.2025 - 14:00</code>")
        return

    if meeting_datetime.year not in (current_year, next_year):
        await message.answer(
            f"⚠️ Faqat hozirgi yil (<b>{current_year}</b>) yoki keyingi yil (<b>{next_year}</b>) "
            "uchun ruxsat beriladi. Qayta kiriting!")
        return

    await state.update_data(meeting_datetime=meeting_datetime)

    await state.set_state(OperatorMeetingState.address)
    await message.answer("🏠 Iltimos, uchrashuv manzilini kiriting!")


@operator_router.message(OperatorMeetingState.address)
async def operator_lead_meeting_address(message: Message, state: FSMContext) -> None:
    address = message.text.strip()
    data = await state.get_data()

    lead_id = data.get("lead_id")
    operator_id = data.get("operator_id")
    meeting_datetime = data.get("meeting_datetime")

    await Meeting.create(
        lead_id=lead_id,
        operator_id=operator_id,
        meeting_date=meeting_datetime,
        address=address
    )

    await message.answer(
        f"✅ <b>Uchrashuv muvaffaqiyatli qo'shildi!</b>\n"
        f"📅 Sana: <code>{meeting_datetime.strftime('%d.%m.%Y - %H:%M')}</code>\n"
        f"🏠 Manzil: <b>{address}</b>")
    await state.clear()


@operator_router.callback_query(F.data.startswith("sold:"))
async def operator_lead_sold(callback: CallbackQuery) -> None:
    pass


@operator_router.callback_query(F.data.startswith("not_sold:"))
async def operator_lead_not_sold(callback: CallbackQuery) -> None:
    pass
