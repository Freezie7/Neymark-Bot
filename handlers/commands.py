from aiogram import Router, types, Bot, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import keyboards
from utils.ai import create_prompt_taskskill, create_analyze_answer, continious_answer
router = Router()

user_dialog_history = {}

class SkillState(StatesGroup):
    skill = State()
    level = State()
    mode = State()
    answer = State()

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

@router.message(F.text == "✨Skills Mode")
async def skill_mode(message: types.Message, state: FSMContext):
    keyboard = keyboards.get_skillmode_keyboard()
    await state.set_state(SkillState.skill)
    await message.answer("Давай прокачаем твои soft skills! Выбери навык который хочешь улучшить", reply_markup=keyboard)

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

@router.message(SkillState.answer)
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
    await state.clear()
    answerbot = await create_analyze_answer(skill, mode, history_str, answer)
    await message.answer(answerbot)
    await add_histotyBOT(message.from_user.id, answerbot)



@router.message()
async def answer_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    history = user_dialog_history.get(user_id, []) 
    if history:
        history_str = "\n".join([f"{sender}: {msg}" for sender, msg in history])
        answerbot = await continious_answer(history_str, message.text)
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

