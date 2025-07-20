from aiogram import Router, types, Bot, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import keyboards
router = Router()

@router.message(F.voice)
async def handle_voice(message: Message):
    await message.reply("Голосовое получено")