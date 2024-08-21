from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.menu import get_menu_kb, get_back_btn_kb, get_settings_btn_kb
from bot.keyboards.schedule import get_schedule_kb
from bot.lexicon import phrases, buttons
from bot.states.teacher_schedule import TeacherSchedule
from bot.states.menu import MenuItem
from bot.utils.aceess_tokens import get_aceess_token_for_settings

router = Router()


@router.message(Command("menu"))
@router.message(F.text.lower() == buttons.lexicon['menu'])
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=phrases.lexicon['cmd_menu'],
        reply_markup=get_menu_kb()
    )


@router.message(Command("schedule"))
@router.message(F.text == buttons.lexicon['menu_schedule'])
async def menu_schedule(message: Message, state: FSMContext):
    await state.set_state(MenuItem.waiting_for_schedule_menu)
    await message.answer(
        text=message.text,
        reply_markup=get_schedule_kb()
    )


@router.message(Command("buildings"))
@router.message(F.text == buttons.lexicon['menu_buildings'])
async def menu_buildings(message: Message):
    # todo: чёто с картой. Скорее всего схема прохода скрином или просто ссылка на яндекс карты
    #  с маршрутом от текущего местоположения
    await message.answer(
        text=message.text,
        reply_markup=get_menu_kb()
    )


@router.message(Command("find_teacher"))
@router.message(F.text == buttons.lexicon['menu_find_teacher'])
async def menu_find_teacher(message: Message, state: FSMContext):
    await state.set_state(TeacherSchedule.waiting_name_for_find)
    await message.answer(
        text=phrases.lexicon['menu_find_teacher'],
        reply_markup=get_back_btn_kb()
    )


@router.message(Command("settings"))
@router.message(F.text == buttons.lexicon['menu_settings'])
async def menu_settings(message: Message):
    await message.answer(
        text=message.text,
        reply_markup=get_settings_btn_kb(
            user_id=message.from_user.id,
            access_token=get_aceess_token_for_settings(message.from_user.id)
        )
    )


@router.message(F.text == buttons.lexicon['menu_next'])
async def menu_next(message: Message):
    # todo: тут, я так понимаю, должна быть вторая страница меню, но зачем так переносить, если можно всё сделать
    #  на одной с обычным пролистыванием. Считаю, что это лучше чем нагромождение лишними кнопками и действиями.
    #  Поэтому этот хэндлер я бы удалил
    await message.answer(
        text=message.text,
        reply_markup=get_menu_kb()
    )
