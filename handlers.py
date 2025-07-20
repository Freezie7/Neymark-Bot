from aiogram import Router, types, Bot, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import keyboards
router = Router()

@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Здарова! Ты попал в СпикерБот - секретное оружие для школьных выступлений! 🤫\n"
        "Забудь про волнение перед докладом! Я прокачаю твою речь так, что все будут в шоке! 🤩\n\n"
        "Что я умею:\n"
        "• Нахожу все твои 'эээ' и 'ммм'. 🕵️\n"
        "• Подсказываю, как говорить чётче и громче. 🗣️\n"
        "• Делаю твои ответы круче, чем у отличника! 💪\n\n"
        "Отправляй голосовуху и готовься блистать! ✨"
    )

