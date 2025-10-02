import os
from datetime import datetime

from aiogram import F, Bot
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from openpyxl import Workbook

from bot.filters.base_filter import IsAdmin, first_id_or_none, get_leads
from bot.keyboards.keyboard import operator_list_keyboard, operator_keyboard, statistic_keyboard, OperatorButton
from bot.keyboards.reply import admin_btn, AdminButtons
from database import User, Lead
from database.models import Comment, Meeting

admin_router = Router()
admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())


@admin_router.message(CommandStart())
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


@admin_router.message(F.text == AdminButtons.OPERATORS)
async def operator_list_handler(message: Message) -> None:
    keyboard = await operator_list_keyboard()  # await here!
    if keyboard:
        await message.answer("Operatorlar ro'yxati !", reply_markup=keyboard)
    else:
        await message.answer("Operatorlar topilmadi.")


@admin_router.callback_query(F.data == OperatorButton.BACK)
async def operator_list_handler(callback: CallbackQuery) -> None:
    keyboard = await operator_list_keyboard()  # await here!
    if keyboard:
        await callback.message.edit_text("Operatorlar ro'yxati !", reply_markup=keyboard)
    else:
        await callback.message.answer("Operatorlar topilmadi.")


@admin_router.callback_query(F.data.startswith("operator:"))
async def accept_operator_handler(callback_query: CallbackQuery) -> None:
    operator = int(callback_query.data.split(":")[1])
    user = await User.get(_id=operator)
    await callback_query.message.edit_text(f"{user.first_name or user.last_name}",
                                           reply_markup=operator_keyboard(user.id)
                                           )


@admin_router.callback_query(F.data.startswith("delete:"))
async def delete_operator_handler(callback_query: CallbackQuery) -> None:
    user_id = int(callback_query.data.split(":")[1])
    user = await User.get(_id=user_id)
    leads = await Lead.filter(user_id=user.id)
    lead = await first_id_or_none(leads)

    if lead:
        meetings = await Meeting.filter(lead_id=lead)
        comments = await Comment.filter(lead_id=lead)
        meeting = await first_id_or_none(meetings)
        comment = await first_id_or_none(comments)
        await Meeting.delete(meeting)
        await Comment.delete(comment)
    await Lead.delete(_id=lead)
    user.type = User.Type.USER
    await user.commit()
    keyboard = await operator_list_keyboard()
    await callback_query.message.edit_text(f"{user.first_name or user.last_name} muofaqiyatli o'chirildi",
                                           reply_markup=keyboard)


@admin_router.callback_query(F.data.startswith("statistic:"))
async def statistic_handler(callback_query: CallbackQuery) -> None:
    operator_id = int(callback_query.data.split(":")[1])
    if operator_id:
        operator = await User.get(_id=operator_id)
        txt = f"{operator.first_name or operator.last_name}"
        await callback_query.message.edit_text(txt, reply_markup=statistic_keyboard(operator.id))
    else:
        await callback_query.answer("Error !")


@admin_router.callback_query(F.data.startswith("all:"))
async def all_handler(callback_query: CallbackQuery) -> None:
    operator_id = int(callback_query.data.split(":")[1])
    if operator_id:
        leads = await Lead.filter(operator_id=operator_id,
                                  status=Lead.Status.SOLD
                                  )
        operator = await User.get(_id=operator_id)
        wb = Workbook()
        ws = wb.active
        ws.title = "Sotilgan leadlar"
        ws.append(["ID", "Ism", "Telefon", "Tarmoq"])
        for lead in leads:
            user = await User.get(_id=lead.user_id)
            ws.append([
                lead.id,
                user.first_name or user.last_name,
                user.phone_number,
                lead.visit_by,
            ])
        file_path = f"leads_sold_{operator.first_name or operator.last_name}.xlsx"
        wb.save(file_path)

        await callback_query.message.answer_document(
            FSInputFile(file_path),
        )
        await callback_query.message.answer(
            text=f"<b>{operator.first_name or operator.last_name}</b>",
            parse_mode="html",
            reply_markup=statistic_keyboard(operator_id)
        )
        os.remove(file_path)


    else:
        await callback_query.answer("Error !")


@admin_router.callback_query(F.data.startswith("month:"))
async def month_handler(callback_query: CallbackQuery) -> None:
    operator_id = int(callback_query.data.split(":")[1])
    now = datetime.now()

    start_date = datetime(now.year, now.month, 1)
    if now.month == 12:
        end_date = datetime(now.year + 1, 1, 1)
    else:
        end_date = datetime(now.year, now.month + 1, 1)

    # Leadlarni olish
    leads = await get_leads(operator_id, start_date=start_date, end_date=end_date)

    if not leads:
        await callback_query.message.answer("Bu oyda sotilgan leadlar yo‘q.")
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Sotilgan Leadlar"

    ws.append(["ID", "User", "Phone", "Tarmoq", ])

    for lead in leads:
        user = await User.get(_id=lead.user_id)
        ws.append([
            lead.id,
            user.first_name or user.last_name,
            user.phone_number,
            lead.visit_by,
        ])

    file_path = f"leads_{operator_id}_{now.strftime('%Y_%m')}.xlsx"
    wb.save(file_path)
    os.remove(file_path)

    await callback_query.message.answer_document(FSInputFile(file_path))
