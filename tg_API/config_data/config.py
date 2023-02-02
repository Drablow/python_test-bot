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
    ('help', "Вывести список команд"),
    ('survey', 'Записать ваши контактные данные'),
    ('lowprice', 'Бюджетные отели'),
    ('highprice', 'Бизнес отеля'),
    ('bestdeal', 'Индивидуальный запрос '),
    ('history', 'История запросов')


)


