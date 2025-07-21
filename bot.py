import asyncio
from aiogram import Bot, Dispatcher
import config
from handlers import routers

async def on_startup():
    print("БОТ ЗАПУЩЕН")

async def main():
    bot = Bot(config.TOKEN_BOT)
    dp = Dispatcher()

    for router in routers:  # Подключаем все обработчики
            dp.include_router(router)

    dp.startup.register(on_startup)
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())