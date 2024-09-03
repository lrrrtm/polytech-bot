from os import getenv

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from bot.utils.aceess_tokens import get_aceess_token_for_settings
from bot.lexicon import buttons


def get_menu_kb(tid: int) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    settings_token = get_aceess_token_for_settings(tid)

    builder.row(
        KeyboardButton(text=buttons.lexicon['menu_schedule'])
    )
    builder.row(
        KeyboardButton(text=buttons.lexicon['menu_buildings']),
        KeyboardButton(text=buttons.lexicon['menu_find_teacher'])
    )
    builder.row(
        KeyboardButton(
            text="Настройки",
            web_app=WebAppInfo(
                url=f"{getenv('WEBAPP_URL')}/settings?uid={tid}&token={settings_token}"
            )
        )
    )
    return builder.as_markup(resize_keyboard=True)


def get_back_btn_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text=buttons.lexicon['back_btn'])
    )

    return builder.as_markup(resize_keyboard=True)
