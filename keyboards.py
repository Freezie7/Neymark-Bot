from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard():
    keyboard = [
      [KeyboardButton(text="✨Skills Mode"), KeyboardButton(text="🗣️Debate Mode")]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_skillmode_keyboard():
        keyboard = [
            [InlineKeyboardButton(text="Публичные выступления 🎙️", callback_data="one")],
            [InlineKeyboardButton(text="Креативность 🎨", callback_data="two")],
            [InlineKeyboardButton(text="Лаконичность 🎉", callback_data="three")],
            [InlineKeyboardButton(text="Эмпатия 💖", callback_data="four")],
            [InlineKeyboardButton(text="Критическое мышление 🤔", callback_data="five")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_cancel_keyboard():
    keyboard = [
      [KeyboardButton(text="Отмена")]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_mode_keyboard():
        keyboard = [
            [InlineKeyboardButton(text="Мягкий", callback_data="easy_skill")],
            [InlineKeyboardButton(text="Стандартный", callback_data="standart_skill")],
            [InlineKeyboardButton(text="Строгий", callback_data="hard_skill")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_task_difficulty_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="Лёгкое 😄", callback_data="easy_task")],
        [InlineKeyboardButton(text="Среднее ⚖️", callback_data="medium_task")],
        [InlineKeyboardButton(text="Сложное 🔥", callback_data="hard_task")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_debate_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="Предложу тему", callback_data="my_theme")],
        [InlineKeyboardButton(text="Рандомная тема", callback_data="random_theme")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_debate_difficulty_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="Лёгкая😄", callback_data="easy_theme")],
        [InlineKeyboardButton(text="Средняя ⚖️", callback_data="medium_theme")],
        [InlineKeyboardButton(text="Сложная 🔥", callback_data="hard_theme")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_mode_debate_keyboard():
        keyboard = [
            [InlineKeyboardButton(text="Мягкий", callback_data="easy_debate")],
            [InlineKeyboardButton(text="Стандартный", callback_data="standart_debate")],
            [InlineKeyboardButton(text="Строгий", callback_data="hard_debate")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)