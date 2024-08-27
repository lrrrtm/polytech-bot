from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from bot.lexicon import buttons

from models.database import Location


def get_buildings_kb(buildings_list: list[str]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for item in buildings_list:
        builder.add(KeyboardButton(text=item))
    builder.adjust(2)
    builder.add(KeyboardButton(text=buttons.lexicon['back_btn']))

    return builder.as_markup(resize_keyboard=True)


def get_building_inline_kb(place_info: Location) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Открыть в Яндекс.Картах", url=f'https://yandex.ru/maps/-/{place_info.yandex_maps_id}'))
    # todo: сейчас блок обработки ошибок, но в будущем когда в базе будут необходимые поля данных,
    #  то и заменить блок на if not None (добавить проверку в методы Database):
    try:
        builder.row(InlineKeyboardButton(text="Карта корпуса", url=place_info.inside_map))
    except Exception as e:
        print(f"Ошибка при попытке вернуть поле inside_map в базе данных: {e}")

    return builder.as_markup()
