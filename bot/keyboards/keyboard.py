from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


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
