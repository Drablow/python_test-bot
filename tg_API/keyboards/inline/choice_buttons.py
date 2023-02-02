from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Инлайн кнопки для выбора языка
def get_lang_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='RU', callback_data='lang'),
        InlineKeyboardButton(text='ENG', callback_data='lang')
    ]

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


# Инлайн кнопки для выбора валюты
def get_cur_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='RUB', callback_data='cur'),
        InlineKeyboardButton(text='USD', callback_data='cur'),
        InlineKeyboardButton(text='EUR', callback_data='cur')
    ]

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


def get_yes_no_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Да', callback_data='accept'),
        InlineKeyboardButton(text='Нет', callback_data='cancel')
    ]

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard
