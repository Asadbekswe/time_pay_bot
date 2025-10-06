from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import User


class OperatorButton:
    DELETE = "O'chiqish 🗑"
    STATISTIC = "Statistic 📊"
    BACK = "Ortga"


class OperatorLeadButtons:
    COMMENT = "💬 Comment"
    MEETING = "📅 Uchrashuv"
    SOLD = "✅ Sotildi"
    NOT_SOLD = "❌ Sotilmadi"


def request_operator_keyboard(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Qabul qilish ✅", callback_data=f"acceptance:{user_id}"),
                          InlineKeyboardButton(text="Rat Etish ❌", callback_data=f"not_acceptance:{user_id}")]])


def operator_lead_keyboard(lead_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=OperatorLeadButtons.COMMENT, callback_data=f"comment:{lead_id}"),
                          InlineKeyboardButton(text=OperatorLeadButtons.MEETING, callback_data=f"meeting:{lead_id}"),
                          InlineKeyboardButton(text=OperatorLeadButtons.SOLD, callback_data=f"sold:{lead_id}"),
                          InlineKeyboardButton(text=OperatorLeadButtons.NOT_SOLD,
                                               callback_data=f"not_sold:{lead_id}")]])


def meeting_operator_keyboard(meeting_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=OperatorLeadButtons.SOLD, callback_data=f"sold:{meeting_id}"),
                          InlineKeyboardButton(text=OperatorLeadButtons.NOT_SOLD,
                                               callback_data=f"not_sold:{meeting_id}")]])


async def operator_list_keyboard():
    operators = await User.filter(type=User.Type.OPERATOR)
    if not operators:
        return None

    buttons = [
        [InlineKeyboardButton(
            text=f"{operator.first_name or operator.last_name}",
            callback_data=f"operator:{operator.id}"
        )]
        for operator in operators
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def operator_keyboard(operator_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=OperatorButton.DELETE, callback_data=f"delete:{operator_id}"),
            InlineKeyboardButton(text=OperatorButton.STATISTIC, callback_data=f"statistic:{operator_id}")],
            [InlineKeyboardButton(text=OperatorButton.BACK, callback_data=OperatorButton.BACK)]])


class StatisticMenu:
    MONTH = "Oy"
    ALL = "Tuliq Statistika"


def statistic_keyboard(operator_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=StatisticMenu.MONTH, callback_data=f"month:{operator_id}"),
                InlineKeyboardButton(text=StatisticMenu.ALL, callback_data=f"all:{operator_id}"),

            ],
            [
                InlineKeyboardButton(text=OperatorButton.BACK, callback_data=OperatorButton.BACK),

            ]
        ]
    )
