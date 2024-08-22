from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.menu import cmd_menu
from bot.lexicon import buttons
from bot.states.menu import MenuItem


router = Router()


@router.message(MenuItem.waiting_for_schedule_menu, F.text == buttons.lexicon['back_btn'])
async def back_btn(message: Message, state: FSMContext):
    await message.answer(
        text="Поиск расписания отменён.",
    )
    await cmd_menu(message, state)


# todo: Логика такая: по умолчанию будет открывать сегодняшнее расписание,
#  и при этом выводится с инлайн кнопками каждого дня следующих 2 недель.
#  При
@router.message(Command("schedule"))
@router.message(F.text == buttons.lexicon['menu_schedule'])
async def menu_schedule(message: Message, state: FSMContext):
    await state.set_state(MenuItem.waiting_for_schedule_menu)
    await message.answer(
        text=message.text,
        reply_markup=get_schedule_kb()
    )
