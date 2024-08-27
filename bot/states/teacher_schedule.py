from aiogram.fsm.state import StatesGroup, State


class TeacherSchedule(StatesGroup):
    waiting_name_for_find = State()
    waiting_name_for_save = State()
