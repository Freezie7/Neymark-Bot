from aiogram import Router, types, Bot, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import keyboards
from utils.ai import create_prompt_taskskill, create_analyze_answer, continious_answer, create_task_chatgpt_debate, create_prompt_debate, continious_debate
router = Router()

user_dialog_history = {}


class SkillState(StatesGroup):
    skill = State()
    level = State()
    mode = State()
    answer = State()

class DebateState(StatesGroup):
    theme_type = State()
    level = State()
    theme = State()
    mode = State()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    keyboard = keyboards.get_main_keyboard() 
    await message.answer("""
        🌟 Привет, бро! Я SkillDebater — твой наставник по прокачке навыков и мастерству дебатов! 💬  
Хочешь стать увереннее, говорить чётко или побеждать в спорах? 🚀  
    Выбери режим:  
        ✨ Skills Mode — тренируй навыки (публичные выступления, речь и др.)  
        🗣️ Debate Mode — спорь как профи на крутые темы!  
Напиши команду и начнём! 😎
        """, reply_markup=keyboard
    )

#SKILLS MODE
@router.message(F.text == "✨Skills Mode")
async def skill_mode(message: types.Message, state: FSMContext):
    keyboard = keyboards.get_skillmode_keyboard()
    await state.set_state(SkillState.skill)
    await message.answer("Давай прокачаем твои soft skills! Выбери навык который хочешь улучшить", reply_markup=keyboard)

#ОТМЕНА
@router.message(F.text == "Отмена")
async def skill_mode(message: types.Message, state: FSMContext):
    await state.clear()
    keyboard = keyboards.get_main_keyboard() 
    await message.answer("""
        🌟 Привет, бро! Я SkillDebater — твой наставник по прокачке навыков и мастерству дебатов! 💬  
Хочешь стать увереннее, говорить чётко или побеждать в спорах? 🚀  
    Выбери режим:  
        ✨ Skills Mode — тренируй навыки (публичные выступления, речь и др.)  
        🗣️ Debate Mode — спорь как профи на крутые темы!  
Напиши команду и начнём! 😎
        """, reply_markup=keyboard
    )
    user_id = message.from_user.id
    if user_id in user_dialog_history:
        del user_dialog_history[user_id]  # Удаляем история диалога


@router.callback_query(SkillState.skill, F.data.in_({"one", "two", "three","four","five"}))
async def callback_skillmode(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    if callback.data == "one":
        await state.update_data(skill="Публичные выступления 🎙️")
    elif callback.data == "two":
        await state.update_data(skill="Креативность 🎨")
    elif callback.data == "three":
        await state.update_data(skill="Лаконичность 🎉")
    elif callback.data == "four":
        await state.update_data(skill="Эмпатия 💖")
    elif callback.data == "five":
        await state.update_data(skill="Критическое мышление 🤔")
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)

    keyboard = keyboards.get_task_difficulty_keyboard()
    await bot.send_message(chat_id=callback.message.chat.id, text="Хорошо, теперь выбери сложность задания", reply_markup=keyboard)

    await state.set_state(SkillState.level)

@router.callback_query(SkillState.level, F.data.in_({"easy_task", "medium_task", "hard_task"}))
async def callback_level(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    if callback.data == "easy_task":
        await state.update_data(level="Лёгкое")
    elif callback.data == "medium_task":
        await state.update_data(level="Среднее")
    elif callback.data == "hard_task":
        await state.update_data(level="Сложное")
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)

    keyboard = keyboards.get_mode_keyboard()
    await bot.send_message(chat_id=callback.message.chat.id, text="Хорошо, теперь выбери строгость оценивания", reply_markup=keyboard)

    await state.set_state(SkillState.mode)

@router.callback_query(SkillState.mode, F.data.in_({"easy_skill", "standart_skill", "hard_skill"}))
async def callback_mode(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    if callback.data == "easy_skill":
        await state.update_data(mode="Мягкий")
    elif callback.data == "standart_skill":
        await state.update_data(mode="Стандартный")
    elif callback.data == "hard_skill":
        await state.update_data(mode="Строгий")

    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.message.chat.id, text="⌛ Анализирую...")
    data = await state.get_data()
    skill = data["skill"]
    mode = data["mode"]
    level = data["level"]
    answer = await create_prompt_taskskill(skill, mode, level)
    #сохранение в историю
    if callback.from_user.id not in user_dialog_history:
        user_dialog_history[callback.from_user.id] = []
    user_dialog_history[callback.from_user.id].append(("Бот", answer))

    await bot.send_message(chat_id=callback.message.chat.id, text=answer) 
    await state.set_state(SkillState.answer)

@router.message(SkillState.answer, F.text)
async def answer_message(message: types.Message, state: FSMContext):
    await state.update_data(answer=message.text)
    await add_histotyUSER(message.from_user.id, message.text)
    await message.answer("⌛ Анализирую...")
    data = await state.get_data()
    skill = data["skill"]
    mode = data["mode"]
    user_id = message.from_user.id
    history = user_dialog_history.get(user_id, []) 
    if history:
        # Форматируем историю для отправки
        history_str = "\n".join([f"{sender}: {msg}" for sender, msg in history])
    answer = data["answer"]
    answerbot = await create_analyze_answer(skill, mode, history_str, answer)
    keyboard = keyboards.get_cancel_keyboard()
    await message.answer(answerbot, reply_markup=keyboard)
    await add_histotyBOT(message.from_user.id, answerbot)


#DEBATE MODE
@router.message(F.text == "🗣️Debate Mode")
async def debate_mode(message: types.Message, state: FSMContext):
    keyboard = keyboards.get_debate_keyboard()
    await state.set_state(DebateState.theme_type)
    await message.answer("Готов поспорить на актуальные темы? 🗣️ Выбери, хочешь рандомную тему или свою! 😎", reply_markup=keyboard)

@router.callback_query(DebateState.theme_type, F.data.in_({"random_theme", "my_theme"}))
async def callback_theme_choice(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    if callback.data == "random_theme":
        await state.update_data(theme_type="random")
        keyboard = keyboards.get_debate_difficulty_keyboard()
        await bot.send_message(chat_id=callback.message.chat.id, text="Класс, выбери сложность темы! 😎", reply_markup=keyboard)
        await state.set_state(DebateState.level)
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    elif callback.data == "my_theme":
        await state.update_data(theme_type="user")
        await bot.send_message(chat_id=callback.message.chat.id, text="Напиши свою тему для спора! ✍️")
        await state.set_state(DebateState.theme)


@router.callback_query(DebateState.level, F.data.in_({"easy_theme", "medium_theme", "hard_theme"}))
async def callback_level(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    if callback.data == "easy_theme":
        await state.update_data(level="Легкая")
    elif callback.data == "medium_theme":
        await state.update_data(level="Стандартная")
    elif callback.data == "hard_theme":
        await state.update_data(level="Сложная")
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)

    keyboard = keyboards.get_mode_debate_keyboard()
    await bot.send_message(chat_id=callback.message.chat.id, text="Теперь выбери, как строго будем оценивать твои аргументы! 😎", reply_markup=keyboard)
    await state.set_state(DebateState.mode)

@router.message(DebateState.theme)
async def answer_message(message: types.Message, state: FSMContext):
    await state.update_data(theme=message.text)
    keyboard = keyboards.get_mode_debate_keyboard()
    await message.answer("Теперь выбери, как строго будем оценивать твои аргументы! 😎", reply_markup=keyboard)
    await state.set_state(DebateState.mode)

@router.callback_query(DebateState.mode, F.data.in_({"easy_debate", "standart_debate", "hard_debate"}))
async def callback_mode(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    if callback.data == "easy_debate":
        await state.update_data(mode="Мягкий")
    elif callback.data == "standart_debate":
        await state.update_data(mode="Стандартный")
    elif callback.data == "hard_debate":
        await state.update_data(mode="Строгий")

    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.message.chat.id, text="⌛ Анализирую...")
    data = await state.get_data()
    if "level" in data:
       level = data["level"]
    else:
        level = 'Пользовательская тема'
    mode = data["mode"]
    if "theme" in data:
       theme = data["theme"]
    else:
        theme = "Рандомная тема. Придумай тему по уровню сложности"
    answerbot = await create_prompt_debate(mode, level, theme)
    keyboard = keyboards.get_cancel_keyboard()
    await bot.send_message(chat_id=callback.message.chat.id, text=answerbot, reply_markup=keyboard)
    #сохранение в историю
    if callback.from_user.id not in user_dialog_history:
        user_dialog_history[callback.from_user.id] = []
    user_dialog_history[callback.from_user.id].append(("Бот", answerbot))


@router.message(DebateState.mode, F.text)
async def answer_message_debate(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await add_histotyUSER(message.from_user.id, message.text)
    history = user_dialog_history.get(user_id, []) 
    if history:
        await message.answer("⌛ Анализирую...")
        data = await state.get_data()
        mode = data["mode"]
        history_str = "\n".join([f"{sender}: {msg}" for sender, msg in history])
        answerbot = await continious_debate(history_str, message.text, mode)
        await add_histotyBOT(message.from_user.id, answerbot)
        await message.answer(answerbot)




@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Помощь: ...")


async def add_histotyBOT(userid: int, mes: str):
    if userid not in user_dialog_history:
        user_dialog_history[userid] = []
    user_dialog_history[userid].append(("Бот: ", mes))

async def add_histotyUSER(userid: int, mes: str):
    if userid not in user_dialog_history:
        user_dialog_history[userid] = []
    user_dialog_history[userid].append(("Пользователь: ", mes))

