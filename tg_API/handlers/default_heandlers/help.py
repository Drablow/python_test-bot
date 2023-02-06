from aiogram import types, Dispatcher

from tg_API.config_data.config import DEFAULT_COMMANDS


async def help_bot(message: types.Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    await message.reply('\n'.join(text))


def register_message_help(dp: Dispatcher):
    dp.register_message_handler(help_bot, commands=['help'])
