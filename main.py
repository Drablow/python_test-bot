# from loader import bot
# import tg_API.handlers
# from telebot.custom_filters import StateFilter
# from tg_API.utils.set_bot_commands import set_default_commands
#
#
#
# if __name__ == '__main__':
#     bot.add_custom_filter(StateFilter(bot))
#     set_default_commands(bot)
#     bot.infinity_polling()


import logging
from aiogram.utils import executor
from loader import dp
from tg_API.handlers.basic_handlers import requests
from tg_API.handlers.custom_handler import survey, setting
from tg_API.handlers.default_heandlers import start, help, echo


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


async def on_startup(dispatcher):
    print('Bot online')


if __name__ == '__main__':
    requests.register_handlers_requests(dp)
    survey.register_handlers_survey(dp)
    setting.register_handler_setting(dp)
    start.register_handlers_start(dp)
    help.register_message_help(dp)
    echo.register_handlers_echo(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
