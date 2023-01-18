import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('hello', 'Привет, ты ввел команду hello'),
    ('survey', 'Опрос'),
    ('history', 'История запросов')
)

# 1. Имя
# 2. Возраст
# 3. Страна
# 4. Город
# 5. Номер телефона
