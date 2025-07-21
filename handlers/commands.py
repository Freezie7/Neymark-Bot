from aiogram import Router, types, Bot, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import keyboards
from utils.ai import analyze_with_chatgpt
router = Router()

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

@router.message()
async def handle_mes(message: types.Message):
    analysis = await analyze_with_chatgpt(message.text)
    await message.reply(analysis)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Помощь: ...")

