from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_groups_list_kb(groups_list: list) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for group in groups_list:
        builder.button(text=group['name'])

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
