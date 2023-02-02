# from telebot.types import Message
# import re
# from loader import bot
# from telebot import types
# from site_API.core import site_api, url_dict, lang, headers
#
#
# @bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
# def set_func(message: Message) -> None:
#     """Уточнение адреса назначения"""
#
#     bot.send_message(chat_id=message.chat.id, text='Какой город Вас интересует?')
#     bot.register_next_step_handler(message=message, callback=search_city)
#
#
# def search_city(message: Message) -> None:
#     """Обработка запроса пользователя по поиску города, вывод Inline клавиатуры с результатами"""
#
#     temp = bot.send_message(chat_id=message.chat.id, text='Загружаю информацию...')
#     city_list = site_api.get_location()
#
#     response = city_list(message, url_dict, headers, lang)
#     keyboard = types.InlineKeyboardMarkup()
#     text = '⬇️      <b>Уточните локацию</b>      ⬇️'
#     if not response:
#         bot.edit_message_text(chat_id=message.chat.id, text='По вашему запросу ничего не найдено...\n/help')
#     else:
#         for city_name, city_id in response.items():
#             keyboard.add(types.InlineKeyboardButton(text=city_name, callback_data=city_id))
#
#         bot.edit_message_text(chat_id=message.chat.id, message_id=temp.id,
#                               text=text, reply_markup=keyboard, parse_mode='HTML')
#
#
#
#
# @bot.callback_query_handler(func=lambda callback: callback.data)
# def city_handler(callback) -> None:
#     """Обработка данных искомого города (id, name), определение следующего шага обработчика"""
#     bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
#     bot.send_message(chat_id=callback.message.chat.id, text=callback.data)
#
#
#
#
