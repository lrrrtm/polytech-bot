from aiogram.fsm.state import StatesGroup, State


class BuildingsItem(StatesGroup):
    waiting_for_building = State()
