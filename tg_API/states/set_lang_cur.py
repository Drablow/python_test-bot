from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMSetting(StatesGroup):
    lang = State()
    cur = State()

