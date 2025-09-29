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
    meeting_time = State()
    address = State()


class OperatorNoteState(StatesGroup):
    note_description = State()
    note_date = State()
    note_time = State()
