from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
    bot.send_message(chat_id=message.chat.id, text='Я помогу вам в выборе отеля (выбери команду): '
                 '\n\n /lowprice - Узнать топ самых дешёвых отелей в городе'
                 '\n\n /highprice - Узнать топ самых дорогих отелей в городе'
                 '\n\n /bestdeal - Узнать топ отелей, наиболее подходящих по цене '
                 'и расположению от центра (самые дешёвые и находятся ближе всего к центру)'
                 '\n\n /history - Узнать историю поиска отелей'
                 '\n\n /settings (по желанию) - Установить параметры поиска (язык, валюта)')


