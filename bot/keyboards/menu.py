from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.lexicon import buttons


def get_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text=buttons.lexicon['menu_schedule'])
    )
    builder.row(
        KeyboardButton(text=buttons.lexicon['menu_buildings']),
        KeyboardButton(text=buttons.lexicon['menu_find_teacher'])
    )
    builder.row(
        KeyboardButton(text=buttons.lexicon['menu_settings']),
        KeyboardButton(text=buttons.lexicon['menu_next']),
    )
    return builder.as_markup(resize_keyboard=True)


def get_back_btn_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text=buttons.lexicon['back_btn'])
    )

    return builder.as_markup(resize_keyboard=True)
