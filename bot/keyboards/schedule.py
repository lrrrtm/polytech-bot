from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_schedule_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text="📆 Сегодня"),
        KeyboardButton(text="➡️ Завтра"),
    )
    builder.row(
        KeyboardButton(text="◀️ Назад"),
        KeyboardButton(text="⭐ Избранное")
    )

    return builder.as_markup(resize_keyboard=True)
