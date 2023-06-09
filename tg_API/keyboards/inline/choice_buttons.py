from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.callback_data import CallbackData


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


def get_count_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='1', callback_data='1'),
        InlineKeyboardButton(text='2', callback_data='2'),
        InlineKeyboardButton(text='3', callback_data='3'),
        InlineKeyboardButton(text='4', callback_data='4'),
        InlineKeyboardButton(text='5', callback_data='5'),
        InlineKeyboardButton(text='6', callback_data='6'),
        InlineKeyboardButton(text='7', callback_data='7'),
        InlineKeyboardButton(text='8', callback_data='8'),
        InlineKeyboardButton(text='9', callback_data='9'),
    ]

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(text='10', callback_data='10'))
    return keyboard


def get_photos_hotel_keyboard(data: dict, hotels_callback: CallbackData, page: int = 0) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    has_next_page = len(data) >= page + 1

    if page != 0:
        keyboard.add(
            InlineKeyboardButton(
                text="< Назад",
                callback_data=hotels_callback.new(page=page - 1)
            )
        )

    keyboard.add(
        InlineKeyboardButton(
            text=f"• {page + 1}",
            callback_data="dont_click_me",
        )
    )

    if has_next_page:
        keyboard.add(
            InlineKeyboardButton(
                text="Вперёд >",
                callback_data=hotels_callback.new(page=page + 1)
            )
        )

    return keyboard
