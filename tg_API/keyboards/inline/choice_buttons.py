from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def menu_search_hotel() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Бюджетные', callback_data='lowprice'),
        InlineKeyboardButton(text='Бизнес класс', callback_data='highprice'),
        InlineKeyboardButton(text='Оптимальный выбор', callback_data='bestdeal'),
        InlineKeyboardButton(text='Отмена', callback_data='cancel')
    ]

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard



# Инлайн кнопки для выбора языка
def get_lang_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='RU', callback_data='RU'),
        InlineKeyboardButton(text='ENG', callback_data='ENG')
    ]

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


# Инлайн кнопки для выбора валюты
def get_cur_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='RUB', callback_data='RUB'),
        InlineKeyboardButton(text='USD', callback_data='USD'),
        InlineKeyboardButton(text='EUR', callback_data='EUR')
    ]

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


def get_yes_no() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Да', callback_data='survey_choice_yes'),
        InlineKeyboardButton(text='Нет', callback_data='survey_choice_no')
    ]

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


