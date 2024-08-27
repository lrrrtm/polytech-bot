from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_admin_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="🔁 Перезапуск systemctl", callback_data="insert_data")
    builder.button(text="📚 Обновление данных", callback_data="insert_data")

    builder.adjust(1)

    return builder.as_markup()
