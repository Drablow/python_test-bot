import logging
from aiogram.types import Message
from tg_API.keyboards.reply.contact import request_contact
from tg_API.keyboards.inline.choice_buttons import get_yes_no_survey
from tg_API.states.contact_information import FSMSurvey
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from database.core import crud
from database.common.models import db, History, User

db_write = crud.write()
db_update = crud.update()
db_check_id = crud.check_id()


# Вход в опросник, проверяем есть ли запись в базе
async def survey(message: types.Message):

    if db_check_id(db, User, message.from_user.id).exists():
        await message.answer('Ваша анкета заполнена, хотите обновить?', reply_markup=get_yes_no_survey())

    else:
        await FSMSurvey.name.set()
        await message.answer(f'Привет введи свое имя')


# Блок yes_no
async def survey_choice(callback: types.CallbackQuery, state: FSMContext) -> None:
    if callback.data == 'survey_choice_no':
        await state.finish()
        await callback.answer('Отмена.')
        await callback.message.delete()
    else:
        await FSMSurvey.name.set()
        await callback.message.answer('Введите свое имя')


# Выход из состояний
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)

    await state.finish()
    await message.answer('Запись была отменена.', reply_markup=types.ReplyKeyboardRemove())


# Получаем имя и регистрируем следующее состояние
async def get_name(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        async with state.proxy() as data:
            data['tg_id'] = message.from_user.id
            data['name'] = message.text

        await FSMSurvey.next()
        await message.answer('Теперь введи свой возраст')

    else:
        await message.answer('Имя может содержать только буквы')


# Получаем возраст и регистрируем следующее состояние
async def get_age(message: types.Message, state: FSMContext) -> None:
    if message.text.isdigit():
        async with state.proxy() as data:
            data['age'] = message.text

        await FSMSurvey.next()
        await message.answer('Теперь введи страну проживания')

    else:
        await message.answer('Возраст может быть только числом')


# Получаем Страну проживания и регистрируем следующее состояние
async def get_country(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['country'] = message.text

    await FSMSurvey.next()
    await message.answer('Теперь введи свой город')


# Получаем город проживания и регистрируем следующее состояние
async def get_city(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['city'] = message.text

    await FSMSurvey.next()
    await message.answer('Отправь свой номер нажав на кнопку', reply_markup=request_contact())


# Получаем телефон и завершаем опрос
async def get_contact(message: types.Message, state: FSMContext) -> Message:
    if message.content_type == 'contact':
        async with state.proxy() as data:
            data['phone_number'] = message.contact.phone_number

        text = '{info}\n{name}\n{age}\n{country}\n{city}\n{number}'.format(
            info='<b>Спасибо за предоставленную информацию ваши данные:</b>',
            name=f'<b>Имя:</b> <u>{data.get("name")}</u>',
            age=f'<b>Возраст:</b> <u> {data.get("age")}</u>',
            country=f'<b>Страна:</b> <u>{data.get("country")}</u>',
            city=f'<b>Город:</b> <u>{data.get("city")}</u>',
            number=f'<b>Номер телефона:</b> <u> {data.get("phone_number")}</u>')

        if db_check_id(db, User, message.from_user.id).exists():
            db_update(db, User, dict(data))
        else:
            db_write(db, User, dict(data))

        await message.answer(text, reply_markup=types.ReplyKeyboardRemove())
    else:

        return await message.answer('Чтобы отправить контактную информацию нажми на кнопку')

    await state.finish()


# Регистрируем хендлеры
def register_handlers_survey(dp: Dispatcher):
    dp.register_message_handler(survey, commands=['survey', 'опрос'])
    dp.register_callback_query_handler(
        survey_choice, Text(equals=['survey_choice_yes', 'survey_choice_no'], ignore_case=True))

    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")

    dp.register_message_handler(get_name, state=FSMSurvey.name)
    dp.register_message_handler(get_age, state=FSMSurvey.age)
    dp.register_message_handler(get_country, state=FSMSurvey.country)
    dp.register_message_handler(get_city, state=FSMSurvey.city)
    dp.register_message_handler(get_contact, content_types=types.ContentType.ANY, state=FSMSurvey.phone_number)
