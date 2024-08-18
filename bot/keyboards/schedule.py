from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from models.database import Database

db = Database()

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


def get_inline_location_kb(url: str, location: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="🗓️ Полное расписание", url=url)

    if location is not None:
        print(location)
        place_name = location['places'].split(',')[0]
        place_info = db.get_place_info(place_name)

        builder.button(text="🗺️ Маршрут до корпуса", url=f"https://yandex.ru/maps/-/{place_info.yandex_maps_id}")

    builder.adjust(1)

    return builder.as_markup()
