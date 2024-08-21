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
