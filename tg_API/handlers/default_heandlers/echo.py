from aiogram import types, Dispatcher


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
async def echo(message: types.Message):
    await message.reply('Такой команды нет! Воспользуйтесь командой /help.')
    # await message.answer(message.text)


def register_handlers_echo(dp: Dispatcher):
    dp.register_message_handler(echo)
