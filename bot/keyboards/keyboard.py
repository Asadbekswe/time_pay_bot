from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
