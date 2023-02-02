from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_lang_keyboard():
    buttons = [
        InlineKeyboardButton(text='RU', callback_data='lang'),
        InlineKeyboardButton(text='ENG', callback_data='lang')
    ]

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_cur_keyboard():
    buttons = [
        InlineKeyboardButton(text='RUB', callback_data='cur'),
        InlineKeyboardButton(text='USD', callback_data='cur'),
        InlineKeyboardButton(text='EUR', callback_data='cur')
    ]

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard
