from os import getenv

import telebot
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(getenv('BOT_TOKEN'), parse_mode='html')

app = Flask(__name__)


def send_feedback(feedback_data: dict):
    bot.send_message(
        chat_id=getenv('BOT_FEEDBACK_CHAT_ID'),
        text=f"<b>💬 Новое обращение</b>"
             f"\n\n🤠 Пользователь: <b>@{feedback_data['user_nickname']}</b>"
             f"\n🔖 Тема: <b>{feedback_data['topic']}</b>"
             f"\n\n{feedback_data['question_text']}",
    )


@app.route('/send_feedback', methods=['POST'])
def feedback():
    data = request.json
    send_feedback(data['params'])

    response = {
        'status': 'success',
        'message': 'Feedback received!'
    }
    return jsonify(response), 201


if __name__ == '__main__':
    app.run(port=5000)
