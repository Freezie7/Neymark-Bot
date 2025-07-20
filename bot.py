import asyncio
from aiogram import Bot, Dispatcher
import config
from handlers import router

async def on_startup():
    print("БОТ ЗАПУЩЕН")

async def main():
    bot = Bot(config.TOKEN_BOT)
    dp = Dispatcher()
    dp.include_router(router)  # Подключаем роутер
    dp.startup.register(on_startup)
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())