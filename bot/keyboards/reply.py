from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class UserRegister:
    REQUEST_CONTACT = "Telefon Raqam Yuborish 📱"


class UserButtons:
    BECOME_OPERATOR = "Operator Bo'lish 📞"


class OperatorButtons:
    MY_LEADS = "Mening Leadlarim 📌"
    MEETINGS = "Uchrashuvlar ⏰"
    NEED_LEADS = "Lead Kerak 📥"


class AdminButtons:
    USERS = "Foydalanuvchilar 🧍🏻🧍🏻‍♀️"
    OPERATORS = "Operatorlar 👥"
    ADMINS = "Adminlar 😎"
    SUPER_USER = "BOSS 👑"


class SuperUserButtons:
    pass


def request_contact_user():
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text=UserRegister.REQUEST_CONTACT, request_contact=True))
    return rkb.as_markup(resize_keyboard=True)


def operator_btn():
    rkb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=OperatorButtons.MY_LEADS), KeyboardButton(text=OperatorButtons.MEETINGS),
         KeyboardButton(text=OperatorButtons.NEED_LEADS)]],
        resize_keyboard=True)
    return rkb


def admin_btn():
    rkb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=AdminButtons.OPERATORS)]],
        resize_keyboard=True)
    return rkb
