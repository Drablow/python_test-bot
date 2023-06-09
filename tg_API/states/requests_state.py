from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMRequests(StatesGroup):
    requests = State()
    search_city = State()
    city_handler = State()
    check_in = State()
    check_out = State()
    count_hotels = State()
    count_parents = State()
    count_children = State()
    set_price_min = State()
    set_price_max = State()
    hotel_page_handler = State()

