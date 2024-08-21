from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.lexicon import phrases

router = Router()


@router.message()
async def cmd_help(message: Message):
    """Команда /help, но также и мусорка для необработанных событий."""
    await message.answer(
        text=phrases.lexicon['cmd_help'],
    )
