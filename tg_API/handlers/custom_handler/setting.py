import logging
from tg_API.states.set_lang_cur import FSMSetting
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from tg_API.keyboards.inline import choice_buttons


# Точка входа в настройки
async def setting(message: types.Message) -> None:
    await FSMSetting.lang.set()
    await message.answer('Выберите язык:', reply_markup=choice_buttons.get_lang_keyboard())


# Выход из состояний
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)

    await state.finish()
    await message.reply('Отмена.', reply_markup=types.ReplyKeyboardRemove())


# Выбор языка
async def lang(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['lang'] = callback.data

    await FSMSetting.cur.set()
    await callback.answer('Настройки языка применены')
    await callback.message.answer('Выберите валюту:', reply_markup=choice_buttons.get_cur_keyboard())


# Выбор валюты
async def cur(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['cur'] = callback.data
    await callback.answer('Настройки валюты применены')

    await state.finish()


def register_handler_setting(dp: Dispatcher):
    dp.register_message_handler(setting, commands=['setting'])
    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_callback_query_handler(lang, Text(equals=['lang'], ignore_case=True), state=FSMSetting.lang)
    dp.register_callback_query_handler(cur, Text(equals=['cur'], ignore_case=True), state=FSMSetting.cur)
