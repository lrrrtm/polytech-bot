from aiogram import Router, F
from aiogram.types import Message, URLInputFile, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.handlers.menu import cmd_menu
from bot.keyboards.buildings import get_buildings_kb, get_building_inline_kb
from bot.lexicon import buttons
from bot.states.buildings import BuildingsItem

from models.database import Database

router = Router()
db = Database()


@router.message(BuildingsItem.waiting_for_building, F.text == buttons.lexicon['back_btn'])
async def back_btn_to_main_menu(message: Message, state: FSMContext):
    await message.answer(
        text="Выбор корпуса отменён.",
    )
    await cmd_menu(message, state)


@router.message(Command("buildings"))
@router.message(F.text == buttons.lexicon['menu_buildings'])
async def menu_buildings(message: Message, state: FSMContext):
    await state.set_state(BuildingsItem.waiting_for_building)
    buildings_list = db.get_all_places_names()
    await message.answer(
        text="<b>Выберете корпус:</b>",
        reply_markup=get_buildings_kb(buildings_list),
    )


@router.message(BuildingsItem.waiting_for_building)
async def msg_building(message: Message, state: FSMContext):
    try:
        place_info = db.get_place_info(message.text)
        kb = get_building_inline_kb(place_info)
        await message.answer(
            text=f"<b>{message.text}</b>\n\n"
                 f"{place_info.caption}",
            reply_markup=kb
        )
    except Exception as e:
        print(f"Ошибка в получение данных о корпусе: {e}")
        await message.answer(
            text="<b>Ошибка при поиске корпуса!</b>",
        )
        await menu_buildings(message, state)
