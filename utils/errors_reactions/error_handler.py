from os import getenv
from dotenv import load_dotenv

import telebot

load_dotenv()
bot = telebot.TeleBot(getenv('BOT_TOKEN'), parse_mode='html')


def answer_to_error(error_msg: str, tid: int):
    bot.send_message(
        chat_id=tid,
        text=f"<b>Упс, что-то поломалось</b>"
             f"На нашей стороне произошла ошибка, попробуй выполнить действие ещё раз. "
             f"Если не поможет, сделай скриншот или запиши видео с моментом, где возникает ошибка и отправь нам, "
             f"нажав на кнопку под этим сообщением."
             f"\n\nОшибка: {error_msg}",
        reply_markup=telebot.types.InlineKeyboardMarkup(
            keyboard=[telebot.types.InlineKeyboardButton(
                text="Написать в поддержку",
                url="https://forms.yandex.ru/u/66c0f6d42530c215f5889e54/"
            )
            ]
        )
    )
