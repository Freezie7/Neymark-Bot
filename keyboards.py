from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    keyboard = [
      [KeyboardButton(text="✨Skills Mode"), KeyboardButton(text="🗣️Debate Mode")]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)