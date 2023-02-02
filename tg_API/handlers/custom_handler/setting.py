import logging
from create_bot import bot, dp
from tg_API.states.set_lang_cur import FSMSetting
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Начало настроек
async def setting(message: types.Message):
    inkb = InlineKeyboardMarkup(row_width=2)
    btn_RU = InlineKeyboardButton(text='RU', callback_data='ru_RU')
    btn_ENG = InlineKeyboardButton(text='ENG', callback_data='en_US')
    inkb.add(btn_RU, btn_ENG)

    await FSMSetting.lang.set()
    await  message.answer('Выберите язык:', reply_markup=inkb)


# Выход из состояний
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)

    await state.finish()
    await message.reply('Отмена.', reply_markup=types.ReplyKeyboardRemove())


# Выбор языка
async def lang(callback: types.CallbackQuery, state: FSMContext):
    inkb2 = InlineKeyboardMarkup(row_width=3)
    btn_RUB = InlineKeyboardButton(text='RUB', callback_data='RUB')
    btn_USD = InlineKeyboardButton(text='USD', callback_data='USD')
    btn_EUR = InlineKeyboardButton(text='EUR', callback_data='EUR')
    inkb2.add(btn_RUB, btn_USD, btn_EUR)

    async with state.proxy() as data:
        data['lang'] = callback.data

    await FSMSetting.cur.set()
    await callback.answer('Настройки языка применены')
    await callback.message.answer('Выберите валюту:', reply_markup=inkb2)


# Выбор валюты
async def cur(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['cur'] = callback.data
    await callback.answer('Настройки валюты применены')

    await state.finish()


def register_handler_setting(dp: Dispatcher):
    dp.register_message_handler(setting, commands=['setting'])
    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_callback_query_handler(lang, Text(equals=["ru", 'eng'], ignore_case=True), state=FSMSetting.lang)
    dp.register_callback_query_handler(cur, Text(equals=["rub", 'usd', 'eur'], ignore_case=True), state=FSMSetting.cur)
