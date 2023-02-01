from loader import bot
import tg_API.handlers
from telebot.custom_filters import StateFilter
from tg_API.utils.set_bot_commands import set_default_commands



if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()


# import logging
# from aiogram.utils import executor
# from create_bot import dp, bot
#
# from tg_API.handlers.custom_handler import survey
# from tg_API.handlers.default_heandlers import echo
# # Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(level=logging.INFO)
#
#
# async def on_startup(dispatcher):
#     print('Bot online')
#
#
# if __name__ == '__main__':
#     survey.register_handlers_survey(dp)
#     echo.register_handlers_echo(dp)
#
#     executor.start_polling(dp, skip_updates=True, on_startup=on_startup)