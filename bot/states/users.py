from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    phone_number = State()

