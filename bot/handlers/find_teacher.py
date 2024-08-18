from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.menu import cmd_menu
from bot.keyboards.groups import get_buttons_list
from bot.keyboards.menu import get_menu_kb
from bot.keyboards.schedule import get_schedule_kb, get_inline_location_kb
from bot.lexicon import phrases, buttons
from bot.states.menu import MenuItem
from bot.states.teacher_schedule import TeacherSchedule
from bot.utils.ruz.formatting import get_block_for_location
from bot.utils.ruz.lists import get_teachers_list
from bot.utils.ruz.schedule import get_teacher_location

router = Router()


@router.message(TeacherSchedule.waiting_name_for_find)
async def teacher_name_recieved(message: Message, state: FSMContext):
    response, teachers_list = get_teachers_list(message.text)
    if message.text == buttons.lexicon['back_btn']:
        await state.set_state(MenuItem.waiting_for_main_menu)
        await cmd_menu(message, state)
        return

    if response:  # всё ок
        if len(teachers_list) == 0:  # никого не нашлось
            await message.answer(
                text="По твоему запросу не нашлось ни одного преподавателя, попробуй ещё раз"
            )
        elif len(teachers_list) == 1:  # одно совпадение, сразу дальше
            response, location_data = get_teacher_location(teachers_list[-1]['id'])
            if response:
                text_to_send = get_block_for_location(location_data)
                await message.answer(
                    text=text_to_send,
                    reply_markup=get_inline_location_kb(location_data['url'], location_data['lesson'])
                )
                await cmd_menu(message, state)
            else:
                await message.answer(
                    text="При получении данных возникла ошибка, попробуй ещё раз."
                )
                await cmd_menu(message, state)

        else:  # больше 1 варианта, просим уточнить
            await message.answer(
                text="Нашлось несколько преподавателей, выбери нужного из списка",
                reply_markup=get_buttons_list(teachers_list)
            )
    else:
        await state.set_state(MenuItem.waiting_for_main_menu)
        await message.answer(
            text="При получении данных возникла ошибка, попробуй ещё раз."
        )
        await cmd_menu(message, state)