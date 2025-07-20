from aiogram import Router, types, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import keyboards
router = Router()
import os

@router.message(F.voice)
async def handle_voice(message: Message):
    voice = message.voice
    #Скачиваем файл
    file = await message.bot.get_file(voice.file_id)
    voice_path = f"temp_voice_{message.from_user.id}.ogg"
    await message.bot.download_file(file.file_path, destination=voice_path)
    await message.reply("Голосовое сохранено")
    #конвертируем в WAV
    wav_path = f"temp_voice_{message.from_user.id}.wav"
    os.system(f'ffmpeg -i {voice_path} -ar 16000 {wav_path}')
    print("конвертация прошла успешно")