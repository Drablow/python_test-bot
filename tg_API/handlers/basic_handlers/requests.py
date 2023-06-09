from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InputMedia

from database.core import crud
from site_API.core import site_api, url_dict, lang, headers
from tg_API.keyboards.inline.choice_buttons import menu_search_hotel, get_count_keyboard, get_photos_hotel_keyboard
from tg_API.states.requests_state import FSMRequests
from telegram_bot_calendar import DetailedTelegramCalendar
from aiogram.utils.callback_data import CallbackData

db_write = crud.write()
db_update = crud.update()
db_check_id = crud.check_id()
db_read = crud.read()
db_check_setting = crud.check_setting()
LSTEP_RU = {'y': 'год', 'm': 'месяц', 'd': 'день'}
hotels_callback = CallbackData("response", "page")


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

    calendar, step = DetailedTelegramCalendar(locale='ru').build()
    await callback.message.answer(f"Выберите дату заезда {LSTEP_RU[step]}", reply_markup=calendar)
    await FSMRequests.next()


async def check_in(callback: types.CallbackQuery, state: FSMContext):
    result, key, step = DetailedTelegramCalendar(locale='ru').process(callback.data)

    if not result and key:
        await callback.message.edit_text(f"Выберите {LSTEP_RU[step]}", reply_markup=key)
    elif result:
        await callback.message.edit_text(f"Ваша дата {result}")
        async with state.proxy() as data:
            data['checkInDay'] = int(result.day)
            data['checkInMonth'] = int(result.month)
            data['checkInYear'] = int(result.year)

        calendar, step = DetailedTelegramCalendar(locale='ru').build()
        await callback.message.answer(f"Выберите дату выезда", reply_markup=calendar)
        await FSMRequests.next()


async def check_out(callback: types.CallbackQuery, state: FSMContext):
    result, key, step = DetailedTelegramCalendar(locale='ru').process(callback.data)

    if not result and key:
        await callback.message.edit_text(f"Выберите {LSTEP_RU[step]}", reply_markup=key)
    elif result:
        await callback.message.edit_text(f"Ваша дата {result}")

        async with state.proxy() as data:
            data['checkOutDay'] = int(result.day)
            data['checkOutMonth'] = int(result.month)
            data['checkOutYear'] = int(result.year)

        await FSMRequests.next()
        # await callback.message.answer('Сколько взрослых?')
        await callback.message.edit_text('Сколько отлей смотрим?', reply_markup=get_count_keyboard())


async def count_hotels(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['resultsSize'] = int(callback.data)

    await callback.message.edit_text('Сколько взрослых?')
    await FSMRequests.next()


async def count_parents(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['adults'] = int(message.text)

    await message.answer('Сколько детей?')
    await FSMRequests.next()


async def count_children(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['children'] = int(message.text)

    await message.answer('Введите сумму от:')
    await FSMRequests.next()


async def set_price_min(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['min'] = int(message.text)
    await message.answer('Введите сумму до')
    await FSMRequests.next()


async def set_price_max(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['max'] = int(message.text)
    await message.answer('Загружаю информацию...')

    hotels_list = site_api.get_hotel()
    response = hotels_list(data)

    data_response = list(response.values())

    async with state.proxy() as data:
        data.clear()
        data['hotels'] = data_response

    # async with state.proxy() as data:
    #     data.clear()
    #     data['hotels'] = response

    image = data_response[0]['image']
    name = data_response[0]['name']

    # hotels_callback = CallbackData("response", "page")

    caption = f"Вы выбрали <b>{response.get('name')}</b>"
    keyboard = get_photos_hotel_keyboard(response, hotels_callback)  # Page: 0

    await message.answer_photo(
        photo=image,
        caption=name,
        parse_mode="HTML",
        reply_markup=keyboard
    )
    await FSMRequests.hotel_page_handler.set()


async def hotel_page_handler(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    page = int(callback_data.get("page"))
    async with state.proxy() as data:
        fruit_data = data['hotels'][page]

    caption = f"Отель: {fruit_data.get('name')}\n"
    f"Стоимость за ночь:\n"
    f"Общая стоимость:\n"
    f"Адрес:\n"
    f"До центра города:\n"
    f"Ночей:\n"
    f"Заезд:\n"
    f"Выезд:\n"

    keyboard = get_photos_hotel_keyboard(fruit_data, hotels_callback, page)

    photo = InputMedia(type="photo", media=fruit_data.get("image"), caption=caption)

    await callback.message.edit_media(photo, keyboard)


def register_handlers_requests(dp: Dispatcher):
    dp.register_message_handler(start_menu, Text(equals=['🔎 Поиск отеля', '🔎 Search hotel'], ignore_case=True))
    dp.register_callback_query_handler(requests, state=FSMRequests.requests)
    # dp.register_callback_query_handler(
    #     lang_cur, Text(equals=['setting_choice_no'], ignore_case=True),
    #     state=FSMRequests.search_city)
    dp.register_message_handler(search_city, state=FSMRequests.search_city)
    dp.register_callback_query_handler(city_handler, state=FSMRequests.city_handler)
    dp.register_callback_query_handler(check_in, DetailedTelegramCalendar.func(), state=FSMRequests.check_in)
    dp.register_callback_query_handler(check_out, DetailedTelegramCalendar.func(), state=FSMRequests.check_out)
    dp.register_callback_query_handler(count_hotels, state=FSMRequests.count_hotels)
    dp.register_message_handler(count_parents, state=FSMRequests.count_parents)
    dp.register_message_handler(count_children, state=FSMRequests.count_children)
    dp.register_message_handler(set_price_min, state=FSMRequests.set_price_min)
    dp.register_message_handler(set_price_max, state=FSMRequests.set_price_max)
    dp.register_callback_query_handler(hotel_page_handler, hotels_callback.filter(),
                                       state=FSMRequests.hotel_page_handler)
