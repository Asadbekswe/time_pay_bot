from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class UserRegister:
    REQUEST_CONTACT = "Telefon Raqam Yuborish 📱"


class UserButtons:
    BECOME_OPERATOR = "Operator Bo'lish 📞"


class OperatorButtons:
    SOLD = "Sotildi 🎉"
    MEETING = "Uchrashuv 🔄"
    REQUEST_CONTACT = "Telefon Raqam Yuborish 📱"


class AdminButtons:
    pass


class SuperUserButtons:
    pass


def request_contact_user():
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text=UserRegister.REQUEST_CONTACT, request_contact=True))
    return rkb.as_markup(resize_keyboard=True)