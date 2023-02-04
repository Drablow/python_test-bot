import re

from aiogram.dispatcher import FSMContext

from loader import bot, dp
from site_API.core import site_api, url_dict, lang, headers
import logging
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from database.core import crud
from database.common.models import db, History, User, Setting
from tg_API.states.requests_state import FSMRequests
from tg_API.states.set_lang_cur import FSMSetting
from tg_API.keyboards.inline.choice_buttons import get_yes_no_setting

# lang_cur = State()
# search_city = State()
# check_in_out = State()
# count_people = State()
# photo = State()


db_write = crud.write()
db_update = crud.update()
db_check_id = crud.check_id()
db_read = crud.read()
db_check_setting = crud.check_setting()


# Вход в запрос к сайту
async def requests(message: types.Message):
    """Уточнение адреса назначения"""
    # if db_check_id(db, User, message.from_user.id).exists():
    #     lang, cur = db_check_setting(db, Setting, message.from_user.id)
    #
    #     await message.answer(
    #         f'<b>Продолжить поиск с текущими настройками?</b>\n'
    #         f'<b>Язык:</b> {lang}\n'
    #         f'<b>Валюта:</b> {cur}',
    #         reply_markup=get_yes_no_setting())
    await message.answer('Какой город Вас интересует?')
    await FSMRequests.search_city.set()


async def search_city(message: types.Message, state: FSMContext) -> None:
    """Обработка запроса пользователя по поиску города, вывод Inline клавиатуры с результатами"""


    temp = await message.answer('Загружаю информацию...')
    city_list = site_api.get_location()

    response = city_list(message, url_dict, headers, lang)
    keyboard = types.InlineKeyboardMarkup()
    text = '⬇️      <b>Уточните локацию</b>      ⬇️'
    if not response:
        await message.answer('По вашему запросу ничего не найдено...\n/help')
    else:
        for city_name, city_id in response.items():
            keyboard.add(types.InlineKeyboardButton(text=city_name, callback_data=city_id))

        await message.answer(text, reply_markup=keyboard)
    await FSMRequests.next()


# @dp.callback_query_handler(func=lambda callback: callback.data)
async def city_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Обработка данных искомого города (id, name), определение следующего шага обработчика"""
    async with state.proxy() as data:
        data['regionId'] = callback.data

    await callback.message.delete()
    await callback.message.answer('Введите дату заезда в формате День-Месяц-Год')
    await FSMRequests.next()
    # bot.send_message(chat_id=callback.message.chat.id, text=callback.data)


async def check_in_out(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['checkInDate'] = message.text

    await message.answer('Введите дату выезда в формате День-Месяц-Год')
    async with state.proxy() as data:
        data['checkOutDate'] = message.text
    await FSMRequests.next()
    await message.answer('Сколько взрослых?')


async def count_people(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['adults'] = message.text

    await message.answer('Сколько детей?')
    async with state.proxy() as data:
        data['children'] = message.text
    await FSMRequests.next()
    await message.answer('Введите сумму от')


async def set_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['min'] = message.text
    await message.answer('Введите сумму до')

    async with state.proxy() as data:
        data['max'] = message.text


def register_handlers_requests(dp: Dispatcher):
    dp.register_message_handler(requests, commands=['lowprice', 'highprice', 'bestdeal'])
    # dp.register_callback_query_handler(
    #     lang_cur, Text(equals=['setting_choice_no'], ignore_case=True),
    #     state=FSMRequests.search_city)
    dp.register_message_handler(search_city, state=FSMRequests.search_city)
    dp.register_callback_query_handler(city_handler, state=FSMRequests.city_handler)
    dp.register_message_handler(check_in_out, state=FSMRequests.check_in_out)
    dp.register_message_handler(count_people, state=FSMRequests.count_people)
    dp.register_message_handler(set_price, state=FSMRequests.set_price)
