from aiogram import types
from create_bot import dp

from tg_API.config_data.config import DEFAULT_COMMANDS


@dp.message_handler(commands=['help'])
async def bot_help(message: types.Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    await message.reply('\n'.join(text))
