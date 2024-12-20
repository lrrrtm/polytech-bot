from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.menu import (get_menu_kb, get_back_btn_kb)
from bot.keyboards.schedule import get_schedule_kb
from bot.lexicon import phrases, buttons
from bot.states.teacher_schedule import TeacherSchedule
from bot.states.menu import MenuItem
from models.redis_s import Redis

router = Router()
rd = Redis()


@router.message(Command("menu"))
@router.message(F.text.lower() == buttons.lexicon['menu'])
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=phrases.lexicon['cmd_menu'],
        reply_markup=get_menu_kb(message.from_user.id)
    )


@router.message(Command("schedule"))
@router.message(F.text == buttons.lexicon['menu_schedule'])
async def menu_schedule(message: Message, state: FSMContext):
    await state.set_state(MenuItem.waiting_for_schedule_menu)
    await message.answer(
        text=message.text,
        reply_markup=get_schedule_kb()
    )


@router.message(Command("find_teacher"))
@router.message(F.text == buttons.lexicon['menu_find_teacher'])
async def menu_find_teacher(message: Message, state: FSMContext):
    await state.set_state(TeacherSchedule.waiting_name_for_find)
    await message.answer(
        text=phrases.lexicon['menu_find_teacher'],
        reply_markup=get_back_btn_kb()
    )
