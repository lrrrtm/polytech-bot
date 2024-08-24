from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.states.menu import MenuItem
from bot.keyboards.menu import get_menu_kb
from bot.lexicon import phrases

router = Router()
router.message.filter(MenuItem.waiting_for_building)


@router.message(Command("buildings"))
async def cmd_buildings(message: Message):
    await message.answer(
        text=phrases.lexicon['cmd_help'],
        reply_markup=get_menu_kb()
    )
