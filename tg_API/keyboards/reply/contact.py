from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def request_contact() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Отправить контакт', request_contact=True))
    return keyboard
