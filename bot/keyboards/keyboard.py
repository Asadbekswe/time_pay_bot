from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


class Meeting:
    SOLD = "Sotildi ✅"
    NO_SOLD = "Sotilmadi ❌"


def contact_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📞 Telefon raqamni yuborish",
                    request_contact=True
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def lead_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="YANGI LEAD",
            )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


class OperatorLeadButtons:
    COMMENT = "💬 Comment"
    MEETING = "📅 Uchrashuv"
    SOLD = "✅ Sotildi"
    NOT_SOLD = "❌ Sotilmadi"


def request_operator_keyboard(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Qabul qilish ✅", callback_data=f"acceptance:{user_id}"),
                InlineKeyboardButton(text="Rat Etish ❌", callback_data=f"not_acceptance:{user_id}"),
            ]
        ]
    )


def operator_lead_keyboard(lead_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=OperatorLeadButtons.COMMENT, callback_data=f"comment:{lead_id}"),
                InlineKeyboardButton(text=OperatorLeadButtons.MEETING, callback_data=f"meeting:{lead_id}"),
                InlineKeyboardButton(text=OperatorLeadButtons.SOLD, callback_data=f"sold:{lead_id}"),
                InlineKeyboardButton(text=OperatorLeadButtons.NOT_SOLD, callback_data=f"not_sold:{lead_id}"),
            ]

        ]
    )


def meeting_operator_keyboard(meeting_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=OperatorLeadButtons.SOLD, callback_data=f"sold:{meeting_id}"),
                InlineKeyboardButton(text=OperatorLeadButtons.NOT_SOLD, callback_data=f"not_sold:{meeting_id}"),

            ]
        ]
    )
