from datetime import datetime

from aiogram import Bot
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types import ReplyKeyboardRemove
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

from bot.filters.base_filter import IsOperator, first_id_or_none
from bot.keyboards.keyboard import operator_lead_keyboard, meeting_operator_keyboard, notes_create_delete
from bot.keyboards.reply import operator_btn, OperatorButtons, NotesButtons, operator_notes_btn
from bot.states.users import OperatorCommentState, OperatorMeetingState, OperatorNoteState
from database import Lead, User
from database.models import Meeting, Comment, Note

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
            f"👤 Foydalanuvchi: {user.first_name or user.last_name}\n"
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
            f"👤 <b>Foydalanuvchi:</b> {user.first_name if user.first_name else ""} {user.last_name if user.last_name else ""}\n"
            f"📅 <b>Sana:</b> <code>{meeting.meeting_date.strftime('%d.%m.%Y - %H:%M')}</code>\n"
            f"🏠 <b>Manzil:</b> {meeting.address}\n"
            "-------------------------"
        )
        await message.answer(text, reply_markup=meeting_operator_keyboard(meeting.lead_id))


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
        f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
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

    text = (
        "📅 <b>Ushbu Lead uchun uchrashuv sanasini kiriting!</b>\n\n"
        "⚠️ Faqat hozirgi yil yoki keyingi yil uchun ruxsat beriladi."
    )
    await callback.message.reply(text)
    await callback.message.answer("Uchrashuv sanasi:\n(Misol: 16-01-2025)",
                                  reply_markup=await SimpleCalendar().start_calendar())
    await state.set_state(OperatorMeetingState.meeting_date)


@operator_router.callback_query(SimpleCalendarCallback.filter(), OperatorMeetingState.meeting_date)
async def operator_lead_meeting_date(callback_query: CallbackQuery, callback_data: SimpleCalendarCallback,
                                     state: FSMContext) -> None:
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        if date.strftime("%d.%m.%Y") >= datetime.today().strftime("%d.%m.%Y"):
            await state.update_data(meeting_date=date)
            await callback_query.message.answer(f"✅ Tanlangan sana: {date.strftime('%d-%m-%Y')}")
            await callback_query.message.answer("Endi vaqtni kiriting (masalan: 14:00):")
            await state.set_state(OperatorMeetingState.meeting_time)
        else:
            await callback_query.answer("⚠️ Faqat hozirgi yil yoki keyingi yil uchun ruxsat beriladi.")
            await callback_query.message.answer("Uchrashuv sanasi:\n(Misol: 16-01-2025)",
                                                reply_markup=await SimpleCalendar().start_calendar())
            await state.set_state(OperatorMeetingState.meeting_date)
    else:
        await callback_query.answer("⚠️ Faqat hozirgi yil yoki keyingi yil uchun ruxsat beriladi.")


@operator_router.message(OperatorMeetingState.meeting_time)
async def operator_lead_meeting_time(message: Message, state: FSMContext) -> None:
    meeting_time = message.text
    try:
        if isinstance(meeting_time, str):
            meeting_time = datetime.strptime(meeting_time, "%H:%M").time()
            await state.update_data(meeting_time=meeting_time)
            await state.set_state(OperatorMeetingState.address)
            await message.answer("🏠 Iltimos, uchrashuv manzilini kiriting!")
        else:
            await message.answer("")
    except ValueError:
        await message.answer("⚠️ Vaqt formati noto‘g‘ri! Masalan: 14:00 kiriting.")
        await state.set_state(OperatorMeetingState.meeting_time)


@operator_router.message(OperatorMeetingState.address)
async def operator_lead_meeting_address(message: Message, state: FSMContext) -> None:
    address = message.text.strip()
    data = await state.get_data()

    lead_id = data.get("lead_id")
    operator_id = data.get("operator_id")
    meeting_date = data.get("meeting_date")
    meeting_time = data.get("meeting_time")
    meeting_datetime = datetime.combine(meeting_date, meeting_time)
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
    meeting_id = int(callback.data.split(":")[1])
    print(meeting_id)
    if meeting_id:
        lead = await Lead.get(meeting_id)
        lead.status = Lead.Status.SOLD
        await lead.commit()
        meeting = await Meeting.filter(lead_id=lead.id)
        meeting_id = await first_id_or_none(meeting)
        print(meeting_id)
        if meeting:
            await Meeting.delete(meeting_id)

        await callback.message.edit_text("✅ Tabriklaymiz, Lead ni sotibsiz !!!")
    else:
        await callback.message.answer("Meeting id not found.")


@operator_router.callback_query(F.data.startswith("not_sold:"))
async def operator_lead_not_sold(callback: CallbackQuery) -> None:
    meeting_id = int(callback.data.split(":")[1])
    if meeting_id:
        lead = await Lead.get(meeting_id)
        lead.status = Lead.Status.NOT_SOLD
        await lead.commit()
        meeting = await Meeting.filter(lead_id=lead.id)
        meeting_id = await first_id_or_none(meeting)
        if meeting:
            await Meeting.delete(meeting_id)
        await callback.message.edit_text("😥")
    else:
        await callback.message.answer("Meeting id not found.")


@operator_router.message(F.text == OperatorButtons.NOTES)
async def operator_notes_handler(message: Message, bot: Bot) -> None:
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer(text=OperatorButtons.NOTES, reply_markup=operator_notes_btn())


@operator_router.callback_query(F.data == NotesButtons.NOTES)
async def operator_notes(callback: CallbackQuery) -> None:
    notes = await Note.filter(operator_id=callback.from_user.id)
    if not notes:
        await callback.message.answer("📭 Sizda hali hech qanday eslatma yo‘q.", reply_markup=operator_notes_btn())
        return

    for idx, note in enumerate(notes, start=1):
        text = (
            f"📝 <b>Eslatma #{idx}</b>\n\n"
            f"💡 {note.description}\n"
            f"⏰ <i>{note.note_time.strftime('%Y-%m-%d %H:%M')}</i>")
        await callback.message.answer(text=text, reply_markup=notes_create_delete(note.id))


@operator_router.callback_query(F.data == NotesButtons.CREATE_NOTE)
async def operator_note_create_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.reply("📝 Eslatma matnini kiriting")
    await state.set_state(OperatorNoteState.note_description)


@operator_router.message(OperatorNoteState.note_description)
async def operator_note_description_handler(message: Message, state: FSMContext):
    text = message.text.strip()
    if not text:
        await message.reply("⚠️ Matn bo‘sh bo‘lmasin. Iltimos, eslatma matnini kiriting.")
        return

    await state.update_data(description=text)
    await message.answer("📅 Eslatma sanasini tanlang:", reply_markup=await SimpleCalendar().start_calendar())
    await state.set_state(OperatorNoteState.note_date)


@operator_router.callback_query(SimpleCalendarCallback.filter(), OperatorNoteState.note_date)
async def operator_note_calendar_handler(callback: CallbackQuery, callback_data: SimpleCalendarCallback,
                                         state: FSMContext):
    await callback.answer()
    selected, date_obj = await SimpleCalendar().process_selection(callback, callback_data)

    if not selected:
        await callback.message.answer("Sana tanlanmadi. Iltimos, sanani tanlang.")
        return

    today = datetime.now().date()
    if date_obj.date() < today:
        await callback.message.answer(
            "⚠️ Kechagi yoki avvalgi sanani tanlab bo‘lmaydi. Iltimos, boshqa sana tanlang.",
            reply_markup=await SimpleCalendar().start_calendar()
        )
        return

    await state.update_data(note_date=date_obj)
    await callback.message.answer(f"✅ Tanlangan sana: {date_obj.strftime('%d.%m.%Y')}")
    await callback.message.answer("Endi vaqtni kiriting (masalan: 14:00):")
    await state.set_state(OperatorNoteState.note_time)


@operator_router.message(OperatorNoteState.note_time)
async def operator_note_time_handler(message: Message, state: FSMContext):
    txt = message.text.strip()
    try:
        time_obj = datetime.strptime(txt, "%H:%M").time()
    except ValueError:
        await message.answer("⚠️ Vaqt formati noto‘g‘ri. To‘g‘ri misol: 14:00")
        return

    data = await state.get_data()
    description = data.get("description")
    note_date = data.get("note_date")

    if not description or not note_date:
        await message.answer("⚠️ Kerakli ma'lumot topilmadi. Iltimos, eslatmani qayta yarating.")
        await state.clear()
        return

    note_dt = datetime.combine(note_date, time_obj)

    try:
        await Note.create(
            description=description,
            note_time=note_dt,
            operator_id=message.from_user.id
        )
    except Exception as e:
        await message.answer(f"Xatolik: eslatma saqlanmadi.\n\n{e}")
        await state.clear()
        return

    out = (
        f"✅ Eslatma saqlandi\n\n"
        f"📝 {description}\n"
        f"⏰ {note_dt.strftime('%d.%m.%Y %H:%M')}"
    )
    await message.answer(out)

    await state.clear()


@operator_router.callback_query(F.data.startswith("note_delete"))
async def operator_back(callback: CallbackQuery) -> None:
    note_id = int(callback.data.split(":")[-1])

    note = await Note.delete(note_id)
    if not note:
        await callback.message.reply("❌ Bunday eslatma topilmadi.")
        return

    await callback.message.reply("✅ Muvoffaqiyatli o‘chirildi")


@operator_router.callback_query(F.data == NotesButtons.BACK)
async def operator_back(callback: CallbackQuery, bot: Bot) -> None:
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.message.answer(text="Asosiy Menu 📌", reply_markup=operator_btn())