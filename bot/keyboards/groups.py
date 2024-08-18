from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_buttons_list(data: list) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for element in data:
        builder.button(text=element['name'])

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
