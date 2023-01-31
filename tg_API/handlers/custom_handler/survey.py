from tg_API.keyboards.reply.contact import request_contact
# from loader import bot

from tg_API.states.contact_information import FSMAdmin
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text, state
from create_bot import dp, bot
from aiogram import types, Dispatcher


# from telebot.types import Message


# @dp.message_handler(commands=['survey', 'опрос'], state=None)
async def survey(message: types.Message):
    await FSMAdmin.name.set()
    await bot.send_message(message.from_user.id, f'Привет, {message.from_user.username} введи свое имя')


# @dp.message_handler(content_types=['name'], state=FSMAdmin.name)
async def get_name(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        async with state.proxy() as data:
            data['name'] = message.text

        await FSMAdmin.next()
        await bot.send_message(message.from_user.id, 'Теперь введи свой возраст')

    else:
        await bot.send_message(message.from_user.id, 'Имя может содержать только буквы')


# @dp.message_handler(content_types=['age'], state=FSMAdmin.age)
async def get_age(message: types.Message, state: FSMContext) -> None:
    if message.text.isdigit():
        async with state.proxy() as data:
            data['age'] = message.text

        await FSMAdmin.next()
        await bot.send_message(message.from_user.id, 'Теперь введи страну проживания')

    else:
        await bot.send_message(message.from_user.id, 'Возраст может быть только числом')


# @dp.message_handler(content_types=['country'], state=FSMAdmin.country)
async def get_country(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['country'] = message.text

    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, 'Теперь введи свой город')


# @dp.message_handler(content_types=['city'], state=FSMAdmin.city)
async def get_city(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['city'] = message.text

    await FSMAdmin.next()
    await bot.send_message(message.from_user.id,
                           'Спасибо, записал. Отправь свой номер нажав на кнопку',
                           reply_markup=request_contact())


# @dp.message_handler(content_types=['text', 'contact'], state=FSMAdmin.phone_number)
async def get_contact(message: types.Message, state: FSMContext) -> None:
    if message.content_type == 'contact':
        async with state.proxy() as data:
            data['phone_number'] = message.contact.phone_number

            text = f'Спасибо за предоставленную информацию ваши данные: \n' \
                   f'Имя - {data["name"]}\nВозраст - {data["age"]}\nСтрана - {data["country"]} ' \
                   f'Город -{data["city"]}\nНомер телефона - {data["phone_number"]}'

            await bot.send_message(message.from_user.id, text)
    else:
        await bot.send_message(message.from_user.id, 'Чтобы отправить контактную информацию нажми на кнопку')

    await state.finish()


# Выход из состояний
# @dp.register_message_handler(state="*", commands='отмена')
# @dp.register_message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')


# Регистрируем хендлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(survey, commands=['survey', 'опрос'], state=None)
    dp.register_message_handler(get_name, content_types=['name'], state=FSMAdmin.name)
    dp.register_message_handler(get_age, content_types=['age'], state=FSMAdmin.age)
    dp.register_message_handler(get_country, content_types=['country'], state=FSMAdmin.country)
    dp.register_message_handler(get_city, content_types=['city'], state=FSMAdmin.city)
    dp.register_message_handler(get_contact, content_types=['text', 'contact'], state=FSMAdmin.phone_number)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
