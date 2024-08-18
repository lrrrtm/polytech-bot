from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text="🗓️ Расписание")
    )
    builder.row(
        KeyboardButton(text="📍 Где корпус?"),
        KeyboardButton(text="🧑‍🏫 Поиск препода")
    )
    builder.row(
        KeyboardButton(text="⚙️ Настройки"),
        KeyboardButton(text="Что-то ещё"),
    )
    return builder.as_markup(resize_keyboard=True)
