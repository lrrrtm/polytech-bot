from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.menu import get_menu_kb, get_back_btn_kb
from bot.keyboards.schedule import get_schedule_kb
from bot.lexicon import phrases, buttons
from bot.states.menu import MenuItem
from bot.states.teacher_schedule import TeacherSchedule

router = Router()


@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    await state.set_state(MenuItem.waiting_for_main_menu)
    await message.answer(
        text=phrases.lexicon['cmd_menu'],
        reply_markup=get_menu_kb()
    )


@router.message(MenuItem.waiting_for_main_menu)
async def main_menu_item_selected(message: Message, state: FSMContext):
    await state.clear()

    if message.text == buttons.lexicon['menu_schedule']:
        await state.set_state(MenuItem.waiting_for_schedule_menu)
        await message.answer(
            text=message.text,
            reply_markup=get_schedule_kb()
        )

    elif message.text == buttons.lexicon['menu_find_teacher']:
        await state.set_state(TeacherSchedule.waiting_name_for_find)
        await message.answer(
            text="<b>🧑‍🏫 Поиск преподавателя</b>"
                 "\n\nЗдесь ты можешь определить, где находится преподаватель согласно его расписанию."
                 "\n\nДля этого отправь фамилию или полное ФИО преподавателя.",
            reply_markup=get_back_btn_kb()
        )


@router.message(MenuItem.waiting_for_schedule_menu)
async def main_menu_item_selected(message: Message, state: FSMContext):
    await state.clear()

    if message.text == buttons.lexicon['back_btn']:
        await state.set_state(MenuItem.waiting_for_main_menu)
        await message.answer(
            text=message.text,
            reply_markup=get_menu_kb()
        )
