from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMRequests(StatesGroup):
    # lang_cur = State()
    search_city = State()
    city_handler = State()
    check_in_out = State()
    count_people = State()
    set_price = State()
    photo = State()
