from aiogram.fsm.state import StatesGroup, State


class InputGroupNum(StatesGroup):
    waiting_for_msg = State()
    waiting_for_select = State()