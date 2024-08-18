from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text="🗓️ Расписание")
    )
    builder.row(
        KeyboardButton(text="🏢 Корпуса"),
        KeyboardButton(text="🧑‍🏫 Поиск препода")
    )
    builder.row(
        KeyboardButton(text="⚙️ Настройки"),
        KeyboardButton(text="▶️ Дальше"),
    )
    return builder.as_markup(resize_keyboard=True)


def get_back_btn_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text="◀️ Назад")
    )

    return builder.as_markup(resize_keyboard=True)
