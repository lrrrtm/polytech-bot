from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from bot.lexicon import buttons
from bot.lexicon.phrases import lexicon

from models.database import Database

db = Database()


def get_buildings_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buildings_list = db.get_all_places_names()

    for item in buildings_list:
        builder.add(KeyboardButton(text=item))
    builder.adjust(2)
    builder.add(KeyboardButton(text=buttons.lexicon['back_btn']))

    return builder.as_markup(one_time_keyboard=True, resize_keyboard=True)


def get_building_action_kb(building_name: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    yandex_building_id = db.get_building_map_id(building_name)

    builder.row(InlineKeyboardButton(text="Маршрут", url=f'https://yandex.ru/maps/-/{yandex_building_id[-1]}'))
    # todo: сейчас блок обработки ошибок, но в будущем когда в базе будут необходимые поля данных,
    #  то и заменить блок на if not None:
    try:
        inside_map_url = db.get_building_inside_map_url(building_name)
        builder.row(InlineKeyboardButton(text="Карта корпуса", url=inside_map_url))
    except Exception as e:
        print(f"Ошибка при попытке вернуть поле inside_map в базе данных: {e}")
    # builder.row(InlineKeyboardButton(text=buttons.lexicon['back_btn'], callback_data='back_btn'))
    # после тестов понял, что инлайн кнопка назад не нужна. Нужна только на реплай кб

    return builder.as_markup()
