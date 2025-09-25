from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    phone_number = State()


class OperatorCommentState(StatesGroup):
    lead_id = State()
    description = State()
    comment = State()


class OperatorMeetingState(StatesGroup):
    lead_id = State()
    operator_id = State()
    meeting_date = State()
    address = State()
