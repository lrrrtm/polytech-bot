from aiogram.fsm.state import StatesGroup, State


class MenuItem(StatesGroup):
    waiting_for_main_menu = State()
    waiting_for_schedule_menu = State()
    waiting_for_building = State()
