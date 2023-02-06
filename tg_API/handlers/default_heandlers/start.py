from aiogram import types, Dispatcher

from database.common.models import db, Setting
from database.core import crud
from tg_API.keyboards.inline.choice_buttons import get_lang_keyboard
from tg_API.states.set_lang_cur import FSMSetting

db_check_id = crud.check_id()
db_write = crud.write()


async def start_bot(message: types.Message):
    if db_check_id(db, Setting, message.from_user.id).exists():
        await message.answer('Состояние сброшено.')
        await message.answer('Регистрация уже пройдена.')
    else:
        locale = message.from_user.locale.language
        if locale == 'ru':
            await message.answer('Пожалуйста, Выберете ваш язык\n🇺🇸/🇬🇧English\n🇷🇺Русский',
                                 reply_markup=get_lang_keyboard())

        else:
            await message.answer('Please, choose your language\n🇺🇸/🇬🇧English\n🇷🇺Русский',
                                 reply_markup=get_lang_keyboard())
        await FSMSetting.lang.set()


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start'])
