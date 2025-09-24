from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class UserRegister:
    REQUEST_CONTACT = "Telefon Raqam Yuborish 📱"


class UserButtons:
    BECOME_OPERATOR = "Operator Bo'lish 📞"


class OperatorButtons:
    MY_LEADS = "Mening Leadlarim 📌"
    MEETING = "Uchrashuv 🔄"
    NEED_LEADS = "Lead Kerak 📥"


class AdminButtons:
    pass


class SuperUserButtons:
    pass


def request_contact_user():
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text=UserRegister.REQUEST_CONTACT, request_contact=True))
    return rkb.as_markup(resize_keyboard=True)


def operator_btn():
    rkb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=OperatorButtons.MY_LEADS), KeyboardButton(text=OperatorButtons.MEETING),
         KeyboardButton(text=OperatorButtons.NEED_LEADS)]], resize_keyboard=True)
    return rkb
