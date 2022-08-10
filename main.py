import telebot
from telebot.types import Message
import json

bot_client = telebot.TeleBot(token="5499043180:AAEmbgJJ5shiKCQ9KnvN5S-2yAfw3PhBVuU")
ADMIN_CHAT_ID = 362857450


@bot_client.message_handler(commands=["start"])
def start(message: Message):
    with open("users.json", "r") as f_o:
        data_from_json = json.load(f_o)

    user_id = message.from_user.id
    username = message.from_user.username

    if str(user_id) not in data_from_json:
        data_from_json[user_id] = {"username": username}

    with open("users.json", "w") as f_o:
        json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    bot_client.reply_to(message=message, text=str(f"Вы зарегистрированы: {username}. "
                                                  f"Ваш user_id: {user_id}"))


def handle_standup_speech(message: Message):
    bot_client.reply_to(message, "Спасибо большое! Желаю успехов и хорошего дня!")


@bot_client.message_handler(commands=["say_standup_speech"])
def say_standup_speech(message: Message):
    bot_client.reply_to(message, text="Привет! Чем ты занимался вчера?"
                                      "Что будешь делать сегодня?"
                                      "Какие есть трудности?")
    bot_client.register_next_step_handler(message, handle_standup_speech)


bot_client.polling()
