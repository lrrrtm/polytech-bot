from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.menu import cmd_menu
from bot.lexicon import buttons, phrases  # todo: вынести все цитаты
from bot.keyboards.menu import get_back_btn_kb
from bot.keyboards.groups import get_buttons_list
from bot.utils.ruz.lists import get_teachers_list
from bot.utils.ruz.schedule import get_teacher_location
from bot.states.teacher_schedule import TeacherSchedule
from bot.keyboards.schedule import get_inline_location_kb
from bot.utils.ruz.formatting import get_block_for_location

router = Router()


@router.message(TeacherSchedule.waiting_name_for_find, F.text == buttons.lexicon['back_btn'])
async def back_btn(message: Message, state: FSMContext):
    await cmd_menu(message, state)


@router.message(TeacherSchedule.waiting_name_for_find)
async def teacher_name_recieved(message: Message, state: FSMContext):
    teachers_list = get_teachers_list(message.text)

    if len(teachers_list) == 0:
        await message.answer(
            text="По твоему запросу не нашлось ни одного преподавателя, попробуй ещё раз.",
            reply_markup=get_back_btn_kb()
        )
    elif len(teachers_list) == 1:
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

    else:
        if len(teachers_list) > 50:
            await message.answer(
                text="Нашлось слишком много совпадений по твоему запросу, напиши более полное ФИО преподавателя"
            )
        else:
            await message.answer(
                text="Нашлось несколько преподавателей, выбери нужного из списка:",
                reply_markup=get_buttons_list(teachers_list)
            )
