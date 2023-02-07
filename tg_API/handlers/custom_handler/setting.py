import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from database.common.models import db, Setting
from database.core import crud
from tg_API.keyboards.inline import choice_buttons
from tg_API.keyboards.inline.choice_buttons import get_yes_no
from tg_API.states.set_lang_cur import FSMSetting

db_write = crud.write()
db_update = crud.update()
db_check_id = crud.check_id()


# Точка входа в настройки
async def setting(message: types.Message) -> None:
    # if db_check_setting(db, User, message.from_user.id).exists():
    if db_check_id(db, Setting, message.from_user.id).exists():
        await message.answer('Хотите изменить настройки языка и валюты?', reply_markup=get_yes_no())

    else:
        await FSMSetting.lang.set()
        await message.answer('Выберите язык:', reply_markup=choice_buttons.get_lang_keyboard())


# Блок yes_no
async def setting_choice(callback: types.CallbackQuery, state: FSMContext) -> None:
    if callback.data == 'setting_choice_no':
        await state.finish()
        await callback.answer('Отмена.')
        await callback.message.delete()
    else:
        await FSMSetting.lang.set()
        await callback.message.delete()
        await callback.message.answer('Выберите язык:', reply_markup=choice_buttons.get_lang_keyboard())


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
        data['tg_id'] = callback.from_user.id
        data['lang'] = callback.data

    await FSMSetting.cur.set()
    await callback.answer('Настройки языка применены')
    await callback.message.delete()
    await callback.message.answer('Выберите валюту:', reply_markup=choice_buttons.get_cur_keyboard())


# Выбор валюты
async def cur(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['cur'] = callback.data
    await callback.answer('Настройки валюты применены')
    await callback.message.delete()

    if db_check_id(db, Setting, callback.from_user.id).exists():
        db_update(db, Setting, dict(data))

    else:
        db_write(db, Setting, dict(data))
    await state.finish()


def register_handler_setting(dp: Dispatcher):
    dp.register_message_handler(setting, Text(equals=['⚙️ settings', '⚙️ настройки'], ignore_case=True))
    dp.register_callback_query_handler(
        setting_choice, Text(equals=['setting_choice_yes', 'setting_choice_no'], ignore_case=True))

    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")

    dp.register_callback_query_handler(lang, Text(equals=['RU', 'ENG'], ignore_case=True), state=FSMSetting.lang)
    dp.register_callback_query_handler(cur, Text(equals=['RUB', 'USD', 'EUR'], ignore_case=True), state=FSMSetting.cur)
