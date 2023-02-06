from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from tg_API.keyboards.reply.contact import main_menu_ru, main_menu_eng


async def menu_ru(message: types.Message):
    await message.answer('Основное меню', reply_markup=main_menu_ru())


async def menu_eng(message: types.Message):
    await message.answer('Main menu', reply_markup=main_menu_eng())


def register_handlers_menu(dp: Dispatcher):
    dp.register_message_handler(menu_ru, Text(equals='меню', ignore_case=True))
    dp.register_message_handler(menu_eng, Text(equals='menu', ignore_case=True))
