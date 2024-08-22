from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards.menu import get_menu_kb
from bot.lexicon import phrases

router = Router()


@router.message()
@router.message(Command("help"))
async def cmd_help(message: Message):
    """Команда /help, но также и мусорка для необработанных событий."""
    await message.answer(
        text=phrases.lexicon['cmd_help'],
        reply_markup=get_menu_kb()
    )
