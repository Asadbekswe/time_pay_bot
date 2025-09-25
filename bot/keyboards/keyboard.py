from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


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


def request_operator_keyboard(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Qabul qilish ✅", callback_data=f"acceptance:{user_id}"),
                InlineKeyboardButton(text="Rat Etish ❌", callback_data=f"not_acceptance:{user_id}"),
            ]
        ]
    )


def lead_operator_keyboard(lead_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Comment", callback_data=f"comment:{lead_id}"),
                InlineKeyboardButton(text="Uchrashuv", callback_data=f"meeting:{lead_id}"),
                InlineKeyboardButton(text="Sotildi", callback_data=f"sold:{lead_id}"),
                InlineKeyboardButton(text="Sotilmadi", callback_data=f"no_sold:{lead_id}"),
            ]

        ]
    )

# def meeting_operator_keyboard(meeting_id: int):
#     return InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text)
#             ]
#         ]
#     )
