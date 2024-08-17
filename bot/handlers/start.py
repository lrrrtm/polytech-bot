from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardRemove

from bot.keyboards.groups import get_groups_list_kb
from bot.lexicon import phrases
from bot.utils import group_schedule
from models.database import Database
from bot.states.registration import InputGroupNum

router = Router()

db = Database()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    if not db.get_user_by_tid(message.from_user.id):
        await state.set_state(InputGroupNum.waiting_for_msg)
        await message.answer(
            text=phrases.lexicon['hello']
        )


@router.message(InputGroupNum.waiting_for_msg)
async def search_group(message: Message, state: FSMContext):
    groups_list = group_schedule.get_groups_list(message.text)
    if groups_list[0] is not None:
        if len(groups_list) == 1:
            await state.clear()
            group = groups_list[-1]
            await add_new_user(message, group)
        else:
            await state.set_state(InputGroupNum.waiting_for_select)
            await message.answer(
                text="Нашлось несколько групп, выбери свою из списка",
                reply_markup=get_groups_list_kb(groups_list)
            )

    else:
        await state.clear()
        await message.answer("Ошибочка пу пу пу")


@router.message(InputGroupNum.waiting_for_select)
async def search_group(message: Message, state: FSMContext):
    groups_list = group_schedule.get_groups_list(message.text)
    await state.clear()
    if groups_list[0] is not None:
        group = groups_list[-1]
        await add_new_user(message, group)
    else:
        await message.answer("Ошибочка пу пу пу")


async def add_new_user(message: Message, group: dict):
    db.create_new_user(tid=message.from_user.id, faculty=group['faculty'], group=group['groups'])
    await message.answer(
        text=f"Группа <b>{group['name']}</b> сохранена в твоём профиле. Ты всегда можешь изменить группу, в настройках бота."
             f"\n\nЧтобы перейти в главное меню, отправь или нажми на /menu",
        reply_markup=ReplyKeyboardRemove()
    )
