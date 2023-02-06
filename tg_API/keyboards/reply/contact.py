from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def request_contact() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Отправить контакт', request_contact=True))

    return keyboard


def main_menu_ru() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_search_hotel = KeyboardButton('🔎 Поиск отеля')
    btn_about_me = KeyboardButton('Что я могу?')
    btn_settings = KeyboardButton('⚙️ Настройки')
    btn_history = KeyboardButton('📖 История')
    keyboard.add(btn_search_hotel).row(btn_about_me, btn_settings, btn_history)

    return keyboard


def main_menu_eng() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_search_hotel = KeyboardButton('🔎 Search hotel')
    btn_about_me = KeyboardButton('About me?')
    btn_settings = KeyboardButton('⚙️ Settings')
    btn_history = KeyboardButton('📖 History')
    keyboard.add(btn_search_hotel).row(btn_about_me, btn_settings, btn_history)

    return keyboard
