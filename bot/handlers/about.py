from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.lexicon import phrases

router = Router()


@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(
        text=phrases.lexicon['cmd_about']
    )
