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

from tg_API.handlers.custom_handler import survey, setting
from tg_API.handlers.default_heandlers import start, help, echo

import datetime
from database.common.models import *
from database.core import crud
from database.common.models import db, History, User

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# db_write = crud.create()
# db_read = crud.retrieve()
#
# data = {}
# data['tg_id'] = '1'
# # data['name'] = 'Валера'
# # data['age'] = 28
# # data['country'] = 'Россия'
# # data['city'] = 'Самара'
# # data['phone_number'] = '+79279039662'
# # data['lang'] = 'RU'
# # data['cur'] = 'RUB'
#
# db_write(db, User, data)

async def on_startup(dispatcher):
    print('Bot online')


if __name__ == '__main__':

    survey.register_handlers_survey(dp)
    setting.register_handler_setting(dp)
    start.register_handlers_start(dp)
    help.register_message_help(dp)
    echo.register_handlers_echo(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)