from aiogram import Router, types, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import keyboards
router = Router()
import os
from utils.speech import speech_to_text, find_pauses
from utils.ai import analyze_with_chatgpt

@router.message(F.voice)
async def handle_voice(message: Message):
    await message.reply(f"⏳ Анализирую...")
    voice = message.voice
    #Скачиваем файл
    file = await message.bot.get_file(voice.file_id)
    voice_path = f"temp_voice_{message.from_user.id}.ogg"
    await message.bot.download_file(file.file_path, destination=voice_path)
    #конвертируем в WAV
    wav_path = f"temp_voice_{message.from_user.id}.wav"
    os.system(f'ffmpeg -i {voice_path} -ar 16000 {wav_path}')
    print("конвертация прошла успешно")
    #Распознавание гс
    text = await speech_to_text(voice_path)
    #получение пауз
    pauses = find_pauses(voice_path)
    if pauses:
        text += f"\n\n⏸ Обнаружено пауз: {len(pauses)}"

    # Глубокий анализ через OpenRouter
    analysis = await analyze_with_chatgpt(text)
    await message.reply(analysis)
    #удаление временных файлов
    os.remove(voice_path)
    os.remove(wav_path)