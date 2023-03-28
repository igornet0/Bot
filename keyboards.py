from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


def kb_start():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item1 = KeyboardButton(text="Расписание")
    markup.add(item1)
    return markup

def back():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item1 = KeyboardButton(text="Назад️")
    markup.add(item1)
    return markup
