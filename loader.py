from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from language_middleware import setup_middleware
from tg_API.config_data import config
from tg_API.config_data.config import load_config

config = load_config('.env')

bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
bot['config'] = config

# Настроим i18n middleware для работы с многоязычностью
i18n = setup_middleware(dp)

_ = i18n.gettext

