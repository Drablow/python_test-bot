from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from database.core import crud
from site_API.core import site_api, url_dict, lang, headers
from tg_API.keyboards.inline.choice_buttons import menu_search_hotel
from tg_API.states.requests_state import FSMRequests

db_write = crud.write()
db_update = crud.update()
db_check_id = crud.check_id()
db_read = crud.read()
db_check_setting = crud.check_setting()


# Меню поиска отелей
async def start_menu(message: types.Message):
    await FSMRequests.requests.set()
    await message.answer('Выберете категорию поиска отелей', reply_markup=menu_search_hotel())


# Вход в запрос к сайту
async def requests(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['hotel'] = callback.data

    """Уточнение адреса назначения"""
    # if db_check_id(db, User, message.from_user.id).exists():
    #     lang, cur = db_check_setting(db, Setting, message.from_user.id)
    #
    #     await message.answer(
    #         f'<b>Продолжить поиск с текущими настройками?</b>\n'
    #         f'<b>Язык:</b> {lang}\n'
    #         f'<b>Валюта:</b> {cur}',
    #         reply_markup=get_yes_no_setting())
    await callback.message.answer('Какой город Вас интересует?')
    await FSMRequests.next()


async def search_city(message: types.Message, state: FSMContext) -> None:
    """Обработка запроса пользователя по поиску города, вывод Inline клавиатуры с результатами"""

    temp = await message.answer('Загружаю информацию...')
    city_list = site_api.get_location()

    response = city_list(message, url_dict, headers, lang)
    keyboard = types.InlineKeyboardMarkup()
    text = '<b>Уточните локацию</b>      ⬇️'
    await temp.delete()
    if not response:
        await message.answer('По вашему запросу ничего не найдено...\n/help')
    else:
        for city_name, city_id in response.items():
            keyboard.add(types.InlineKeyboardButton(text=city_name, callback_data=city_id))

        await message.answer(text, reply_markup=keyboard)
    await FSMRequests.next()


async def city_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Обработка данных искомого города (id, name), определение следующего шага обработчика"""
    async with state.proxy() as data:
        data['regionId'] = callback.data

    await callback.message.delete()
    await callback.message.answer('Введите дату заезда в формате День-Месяц-Год')
    await FSMRequests.next()


async def check_in(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['checkInDate'] = message.text

    await message.answer('Введите дату выезда в формате День-Месяц-Год')
    await FSMRequests.next()


async def check_out(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['checkOutDate'] = message.text

    await FSMRequests.next()
    await message.answer('Сколько взрослых?')


async def count_parents(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['adults'] = message.text

    await message.answer('Сколько детей?')
    await FSMRequests.next()


async def count_children(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['children'] = message.text

    await message.answer('Введите сумму от:')
    await FSMRequests.next()


async def set_price_min(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['min'] = message.text
    await message.answer('Введите сумму до')
    await FSMRequests.next()


async def set_price_max(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['max'] = message.text
    await state.finish()


def register_handlers_requests(dp: Dispatcher):
    dp.register_message_handler(start_menu, Text(equals=['🔎 Поиск отеля', '🔎 Search hotel'], ignore_case=True))
    dp.register_callback_query_handler(requests, state=FSMRequests.requests)
    # dp.register_callback_query_handler(
    #     lang_cur, Text(equals=['setting_choice_no'], ignore_case=True),
    #     state=FSMRequests.search_city)
    dp.register_message_handler(search_city, state=FSMRequests.search_city)
    dp.register_callback_query_handler(city_handler, state=FSMRequests.city_handler)
    dp.register_message_handler(check_in, state=FSMRequests.check_in)
    dp.register_message_handler(check_out, state=FSMRequests.check_out)
    dp.register_message_handler(count_parents, state=FSMRequests.count_parents)
    dp.register_message_handler(count_children, state=FSMRequests.count_children)
    dp.register_message_handler(set_price_min, state=FSMRequests.set_price_min)
    dp.register_message_handler(set_price_max, state=FSMRequests.set_price_max)
