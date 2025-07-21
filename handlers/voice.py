from aiogram import Router, types, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import keyboards
import os
from utils.speech import speech_to_text
from utils.ai import create_analyze_answer, continious_answer, continious_debate
from handlers.commands import user_dialog_history  # Импортируем user_dialog_history из commands.py

router = Router()

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

#Skills Mode
@router.message(SkillState.answer, F.voice)
async def handle_skill_voice(message: types.Message, state: FSMContext, bot: Bot):
    await message.reply("⏳ Анализирую твой голосовой ответ...")
    voice = message.voice
    user_id = message.from_user.id
    data = await state.get_data()
    skill = data["skill"]
    mode = data["mode"]

    # Скачиваем и конвертируем голосовое сообщение
    file = await message.bot.get_file(voice.file_id)
    voice_path = f"temp_voice_{user_id}.ogg"
    await message.bot.download_file(file.file_path, destination=voice_path)

    wav_path = f"temp_voice_{user_id}.wav"
    if os.system(f'ffmpeg -i {voice_path} -ar 16000 {wav_path}') != 0:
        await message.reply("⚠️ Ошибка при конвертации аудио. Попробуй ещё раз!")
        if os.path.exists(voice_path):
            os.remove(voice_path)
        await state.clear()
        return

    # Транскрибируем текст
    text = await speech_to_text(voice_path)

    # Сохраняем ответ в историю
    await add_histotyUSER(user_id, text)
    history = user_dialog_history.get(user_id, [])
    history_str = "\n".join([f"{sender}: {msg}" for sender, msg in history])

    # Анализируем ответ
    analysis = await create_analyze_answer(skill, mode, history_str, text)
    if analysis.startswith("⚠️"):
        await message.reply(analysis)
        if os.path.exists(voice_path):
            os.remove(voice_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)
        await state.clear()
        return

    # Сохраняем ответ бота в историю
    await add_histotyBOT(user_id, analysis)
    keyboard = keyboards.get_cancel_keyboard()
    await message.reply(analysis, reply_markup=keyboard)

    # Очищаем временные файлы
    if os.path.exists(voice_path):
        os.remove(voice_path)
    if os.path.exists(wav_path):
        os.remove(wav_path)

#Debate Mode
@router.message(DebateState.mode, F.voice)
async def handle_debate_voice(message: types.Message, state: FSMContext, bot: Bot):
    await message.reply("⏳ Анализирую твои голосовые аргументы...")
    voice = message.voice
    user_id = message.from_user.id
    data = await state.get_data()
    mode = data["mode"]

    # Скачиваем и конвертируем голосовое сообщение
    file = await message.bot.get_file(voice.file_id)
    voice_path = f"temp_voice_{user_id}.ogg"
    await message.bot.download_file(file.file_path, destination=voice_path)

    wav_path = f"temp_voice_{user_id}.wav"
    if os.system(f'ffmpeg -i {voice_path} -ar 16000 {wav_path}') != 0:
        await message.reply("⚠️ Ошибка при конвертации аудио. Попробуй ещё раз!")
        if os.path.exists(voice_path):
            os.remove(voice_path)
        await state.clear()
        return

    # Транскрибируем текст
    text = await speech_to_text(voice_path)

    # Сохраняем ответ в историю
    await add_histotyUSER(user_id, text)
    history = user_dialog_history.get(user_id, [])
    history_str = "\n".join([f"{sender}: {msg}" for sender, msg in history])

    # Анализируем ответ
    analysis = await continious_debate(history_str, text, mode)
    if analysis.startswith("⚠️"):
        await message.reply(analysis)
        if os.path.exists(voice_path):
            os.remove(voice_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)
        await state.clear()
        return

    # Сохраняем ответ бота в историю
    await add_histotyBOT(user_id, analysis)
    keyboard = keyboards.get_cancel_keyboard()
    await message.reply(analysis, reply_markup=keyboard)

    # Очищаем временные файлы
    if os.path.exists(voice_path):
        os.remove(voice_path)
    if os.path.exists(wav_path):
        os.remove(wav_path)

async def add_histotyUSER(userid: int, mes: str):
    if userid not in user_dialog_history:
        user_dialog_history[userid] = []
    user_dialog_history[userid].append(("Пользователь: ", mes))

async def add_histotyBOT(userid: int, mes: str):
    if userid not in user_dialog_history:
        user_dialog_history[userid] = []
    user_dialog_history[userid].append(("Бот: ", mes))