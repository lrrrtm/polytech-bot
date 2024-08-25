from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from handlers import (start, menu, schedule, find_teacher, help, about, admin_commands)

load_dotenv()

bot = Bot(token=getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode='html'))
dp = Dispatcher()

dp.include_routers(
    start.router,
    menu.router,
    schedule.router,
    find_teacher.router,
    about.router,
    help.router,
    admin_commands.router
)
