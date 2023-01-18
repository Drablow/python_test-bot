from loader import bot
from telebot.custom_filters import StateFilter
from tg_API.utils.set_bot_commands import set_default_commands
import datetime
from database.common.models import *
from database.common.models import db, History
from database.core import crud
from site_API.core import headers, params, site_api, url

db_write = crud.create()
db_read = crud.retrieve()

fact_by_number = site_api.get_math_fact()
fact_by_date = site_api.get_date_fact()

response = fact_by_number("GET", url, headers, params, 5, timeout=3)
response = response.json()
data = [{"number": response.get("number"), "message": response.get("text")}]

db_write(db, History, data)

response = fact_by_date("GET", url, headers, params, "6", "21", timeout=3)
response = response.json()
data = [{"number": response.get("year"), "message": response.get("text")}]

db_write(db, History, data)

retrieved = db_read(db, History, History.number, History.message)

for element in retrieved:
    print(element.number, element.message)

# if __name__ == '__main__':
#     bot.add_custom_filter(StateFilter(bot))
#     set_default_commands(bot)
#     bot.infinity_polling()
