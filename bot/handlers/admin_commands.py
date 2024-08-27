from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from os import getenv
from json import load
from datetime import datetime

from bot.keyboards.admin import get_admin_kb
from models.redis_s import Redis

router = Router()
rd = Redis()

admins_ids = [409801981, 846455075]


@router.message(Command("check"))
async def cmd_check(message: Message):
    statuses_icons = {
        'running': "🟢",
        'error': "🔴",
        'warning': "🟠"
    }
    if message.from_user.id in admins_ids:
        with open(fr"{getenv('ABSOLUTE_PROJECT_FOLDER')}\parsed_data\groups.json") as file:
            groups_data = load(file)
        with open(fr"{getenv('ABSOLUTE_PROJECT_FOLDER')}\parsed_data\teachers.json") as file:
            teachers_data = load(file)

        await message.answer(
            text=f"\n\n<b>Список групп</b>"
                 f"\nПоследнее обновление: {datetime.strptime(groups_data['last_update'], '%Y-%m-%d %H:%M:%S')}"
                 f"\n\n<b>Список преподавателей</b>"
                 f"\nПоследнее обновление: {datetime.strptime(teachers_data['last_update'], '%Y-%m-%d %H:%M:%S')}"
                 f"\n\n<b>Systemstl</b>"
                 f"\n🟢 bot"
                 f"\n🟢 data_updater"
                 f"\n🟢 flet_settings"
                 f"\n🟢 flask_server"
                 f"\n🟢 redis_server"
                 f"\n🟢 mysql_server",
            reply_markup=get_admin_kb()
        )
