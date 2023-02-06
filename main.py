# import logging
#
# from aiogram.utils import executor
#
# from loader import dp
# from tg_API.handlers.basic_handlers import requests, main_menu
# from tg_API.handlers.custom_handler import survey, setting
# from tg_API.handlers.default_heandlers import start, help, echo

import asyncio
# # Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(level=logging.INFO)
#
#
# async def on_startup(dispatcher):
#     print('Bot online')
#
#
# if __name__ == '__main__':
#     main_menu.register_handlers_menu(dp)
#
#     requests.register_handlers_requests(dp)
#     survey.register_handlers_survey(dp)
#     setting.register_handler_setting(dp)
#     start.register_handlers_start(dp)
#     help.register_message_help(dp)
#     echo.register_handlers_echo(dp)
#
#     executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from language_middleware import setup_middleware
from tg_API.config_data.config import load_config
from tg_API.handlers.basic_handlers import requests, main_menu
from tg_API.handlers.custom_handler import survey, setting
from tg_API.handlers.default_heandlers import start, help, echo

logger = logging.getLogger(__name__)


# def register_all_middlewares(dp):
#     dp.setup_middleware(...)
#
#
# def register_all_filters(dp):
#     dp.filters_factory.bind(...)


def register_all_handlers(dp):
    main_menu.register_handlers_menu(dp)
    requests.register_handlers_requests(dp)
    survey.register_handlers_survey(dp)
    setting.register_handler_setting(dp)
    start.register_handlers_start(dp)
    help.register_message_help(dp)
    echo.register_handlers_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )
    config = load_config('.env')

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config

    # register_all_middlewares(dp)
    # register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
