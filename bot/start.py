import asyncio
import logging

from config import bot, dp
from threading import Thread

logging.basicConfig(level=logging.INFO)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
