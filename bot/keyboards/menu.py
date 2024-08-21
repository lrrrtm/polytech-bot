from os import getenv

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

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
        KeyboardButton(text=buttons.lexicon['menu_settings'])
    )
    return builder.as_markup(resize_keyboard=True)


def get_settings_btn_kb(user_id: int, access_token: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Открыть найстройки",
        web_app=WebAppInfo(
            url=f"{getenv('CONTROL_PANEL_URL')}/settings?uid={user_id}&token={access_token}"
        )
    )

    return builder.as_markup()


def get_back_btn_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text=buttons.lexicon['back_btn'])
    )

    return builder.as_markup(resize_keyboard=True)
