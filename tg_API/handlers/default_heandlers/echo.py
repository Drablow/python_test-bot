from aiogram import types, Dispatcher
from create_bot import dp


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
async def echo(message: types.Message):
    await message.reply('Такой команды нет! Воспользуйтесь командой /help.')
    # await message.answer(message.text)


def register_handlers_echo(dp: Dispatcher):
    dp.register_message_handler(echo)
