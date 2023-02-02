import logging

from tg_API.keyboards.reply.contact import request_contact
from create_bot import bot

from tg_API.states.contact_information import FSMSurvey
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher


async def survey(message: types.Message):
    await FSMSurvey.name.set()
    await bot.send_message(message.from_user.id, f'Привет, {message.from_user.username} введи свое имя')


# Выход из состояний
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)

    await state.finish()
    await message.reply('Отмена.', reply_markup=types.ReplyKeyboardRemove())


# @dp.message_handler(state=FSMSurvey.name)
async def get_name(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        async with state.proxy() as data:
            data['name'] = message.text

        await FSMSurvey.next()
        await bot.send_message(message.from_user.id, 'Теперь введи свой возраст')

    else:
        await bot.send_message(message.from_user.id, 'Имя может содержать только буквы')


async def get_age(message: types.Message, state: FSMContext) -> None:
    if message.text.isdigit():
        async with state.proxy() as data:
            data['age'] = message.text

        await FSMSurvey.next()
        await bot.send_message(message.from_user.id, 'Теперь введи страну проживания')

    else:
        await bot.send_message(message.from_user.id, 'Возраст может быть только числом')


async def get_country(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['country'] = message.text

    await FSMSurvey.next()
    await bot.send_message(message.from_user.id, 'Теперь введи свой город')


async def get_city(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['city'] = message.text

    await FSMSurvey.next()
    await bot.send_message(message.from_user.id, 'Отправь свой номер нажав на кнопку',
                           reply_markup=request_contact())


async def get_contact(message: types.Message, state: FSMContext) -> None:
    if message.content_type == 'contact':
        async with state.proxy() as data:
            data['phone_number'] = message.contact.phone_number

            text = '{info}\n{name}\n{age}\n{country}\n{city}\n{number}'.format(
                info='Спасибо за предоставленную информацию ваши данные:',
                name=f'Имя - {data.get("name")}',
                age=f'Возраст - {data.get("age")}',
                country=f'Страна - {data.get("country")}',
                city=f'Город -{data.get("city")}',
                number=f'Номер телефона - {data.get("phone_number")}')

            await bot.send_message(message.from_user.id, text, reply_markup=types.ReplyKeyboardRemove())
    else:

        return await bot.send_message(message.from_user.id, 'Чтобы отправить контактную информацию нажми на кнопку')

    await state.finish()


# Регистрируем хендлеры
def register_handlers_survey(dp: Dispatcher):
    dp.register_message_handler(survey, commands=['survey', 'опрос'])
    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(get_name, state=FSMSurvey.name)
    dp.register_message_handler(get_age, state=FSMSurvey.age)
    dp.register_message_handler(get_country, state=FSMSurvey.country)
    dp.register_message_handler(get_city, state=FSMSurvey.city)
    dp.register_message_handler(get_contact, content_types=types.ContentType.ANY, state=FSMSurvey.phone_number)
