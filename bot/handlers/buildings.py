from aiogram import Router, F
from aiogram.types import Message, URLInputFile, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.handlers.menu import cmd_menu
from bot.keyboards.menu import get_back_btn_kb
from bot.lexicon import phrases, buttons
from bot.states.buildings import BuildingsItem
from bot.keyboards.buildings import get_buildings_kb, get_building_action_kb

from models.database import Database

router = Router()
db = Database()


@router.message(BuildingsItem.waiting_for_building, F.text == buttons.lexicon['back_btn'])
async def back_btn_to_main_menu(message: Message, state: FSMContext):
    await message.answer(
        text="Выбор корпуса отменён.",
    )
    await cmd_menu(message, state)


@router.message(BuildingsItem.waiting_for_action, F.text == buttons.lexicon['back_btn'])
async def back_btn_to_buildings(message: Message, state: FSMContext):
    await message.answer(
        text="Выбор действия с корпусом отменён.",
    )
    await menu_buildings(message, state)


@router.message(Command("buildings"))
@router.message(F.text == buttons.lexicon['menu_buildings'])
async def menu_buildings(message: Message, state: FSMContext):
    await state.set_state(BuildingsItem.waiting_for_building)
    await message.answer(
        text="<b>Выберете корпус:</b>",
        reply_markup=get_buildings_kb(),
    )


@router.message(BuildingsItem.waiting_for_building)
async def msg_building(message: Message, state: FSMContext):
    try:
        """image_from_url = URLInputFile(f'{db.get_building_image_url(message.text)}')
        await message.answer_photo(
            image_from_url,
            # caption="Изображение по ссылке"
        )"""
        kb = get_building_action_kb(message.text)
        await message.answer(
            text=f"<b>{message.text}</b>",
            reply_markup=kb
        )
    except Exception as e:
        print(f"Ошибка в получение данных о корпусе: {e}")
        await message.answer(
            text="<b>Ошибка при поиске корпуса!</b>",
        )
        await menu_buildings(message, state)
