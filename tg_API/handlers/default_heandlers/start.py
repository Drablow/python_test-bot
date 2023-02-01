from aiogram import types
from create_bot import bot, dp


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    await message.reply(f"Привет, {message.from_user.full_name}!")
    await bot.send_message(message.from_user.id, text='Я помогу вам в выборе отеля (выбери команду): '
                                                      '\n\n /lowprice - Узнать топ самых дешёвых отелей в городе'
                                                      '\n\n /highprice - Узнать топ самых дорогих отелей в городе'
                                                      '\n\n /bestdeal - Узнать топ отелей, наиболее подходящих по цене '
                                                      'и расположению от центра (самые дешёвые и находятся ближе всего к центру)'
                                                      '\n\n /history - Узнать историю поиска отелей'
                                                      '\n\n /settings (по желанию) - Установить параметры поиска (язык, валюта)')

