# import os
# from dotenv import load_dotenv, find_dotenv
# from sys import exit
#
# if not find_dotenv():
#     exit('Переменные окружения не загружены т.к отсутствует файл .env')
# else:
#     load_dotenv()
#
# BOT_TOKEN = os.getenv("BOT_TOKEN")
# if not BOT_TOKEN:
#     exit("Error: no token provided")
#
#
# RAPID_API_KEY = os.getenv('RAPID_API_KEY')


from dataclasses import dataclass
from typing import List
from environs import Env

DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести список команд"),
    ('survey', 'Записать ваши контактные данные'),
    ('lowprice', 'Бюджетные отели'),
    ('highprice', 'Бизнес отели'),
    ('bestdeal', 'Индивидуальный запрос '),
    ('history', 'История запросов')
)


@dataclass
class TgBot:
    token: str
    admin_ids: List[int]


@dataclass
class SiteAPI:
    key: str
    host: str


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config():
    tg_bot: TgBot
    # db: DbConfig
    site_api: SiteAPI
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMINS')))
        ),
        site_api=SiteAPI(
            key=env.str('RAPID_API_KEY'),
            host=env.str('RAPID_API_Host')
        ),
        misc=Miscellaneous()
    )
