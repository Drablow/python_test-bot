from aiogram import types, Dispatcher
from create_bot import dp, bot


async def start_bot(message: types.Message):
    await message.reply(f"Привет, {message.from_user.full_name}!")
    await bot.send_message(message.from_user.id, text='Я помогу вам в выборе отеля (выбери команду): '
                                                      '\n\n /lowprice - Узнать топ самых дешёвых отелей в городе'
                                                      '\n\n /highprice - Узнать топ самых дорогих отелей в городе'
                                                      '\n\n /bestdeal - Узнать топ отелей, наиболее подходящих по цене '
                                                      'и расположению от центра (самые дешёвые и находятся ближе всего к центру)'
                                                      '\n\n /history - Узнать историю поиска отелей'
                                                      '\n\n /settings (по желанию) - Установить параметры поиска (язык, валюта)')


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start'])
