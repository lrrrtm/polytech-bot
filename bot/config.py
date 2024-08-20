from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from handlers import start, about, menu, find_teacher, help

load_dotenv()

bot = Bot(token=getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode='html'))
dp = Dispatcher()

dp.include_routers(
    start.router,
    about.router,
    menu.router,
    find_teacher.router,
    help.router,
)