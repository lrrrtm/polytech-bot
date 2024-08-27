from os import getenv
from dotenv import load_dotenv

import telebot

load_dotenv()
bot = telebot.TeleBot(getenv('BOT_TOKEN'), parse_mode='html')


def send_feedback(feedback_data: dict):
    bot.send_message(
        chat_id=getenv('BOT_FEEDBACK_CHAT_ID'),
        text=f"<b>💬 Новое обращение</b>"
             f"\n\n🤠 Пользователь: <b>@{feedback_data['user_nickname']}</b>"
             f"\n🔖 Тема: <b>{feedback_data['topic']}</b>"
             f"\n\n{feedback_data['question_text']}",
    )
