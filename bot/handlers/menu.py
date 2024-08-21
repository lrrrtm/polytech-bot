from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards.menu import get_menu_kb, get_back_btn_kb
from bot.keyboards.schedule import get_schedule_kb
from bot.lexicon import phrases, buttons


router = Router()


@router.message(Command("menu"))
@router.message(F.text.lower() == buttons.lexicon['menu'])
async def cmd_menu(message: Message):
    await message.answer(
        text=phrases.lexicon['cmd_menu'],
        reply_markup=get_menu_kb()
    )


@router.message(F.text == buttons.lexicon['menu_schedule'])
async def menu_schedule(message: Message):
    await message.answer(
        text=message.text,
        reply_markup=get_schedule_kb()
    )


@router.message(F.text == buttons.lexicon['menu_find_teacher'])
async def menu_find_teacher(message: Message):
    await message.answer(
        text="<b>🧑‍🏫 Поиск преподавателя</b>"
             "\n\nЗдесь ты можешь определить, где находится преподаватель согласно его расписанию."
             "\n\nДля этого отправь фамилию или полное ФИО преподавателя.",
        reply_markup=get_back_btn_kb()
    )


@router.message(F.text == buttons.lexicon['back_btn'])
async def back_btn(message: Message):
    await message.answer(
        text=message.text,
        reply_markup=get_menu_kb()
    )
