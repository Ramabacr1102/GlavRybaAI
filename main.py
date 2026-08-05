import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import BOT_TOKEN
from database.database import Database

from bot.routers import router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


async def main():

    db = Database()
    await db.connect()

    bot = Bot(BOT_TOKEN)

    dp = Dispatcher()

    # Передаем базу во все обработчики
    dp["db"] = db

    dp.include_router(router)

    print("=" * 50)
    print("GlavRyba AI")
    print("✅ PostgreSQL успешно подключена!")
    print("=" * 50)

    print("=" * 50)
    print("GlavRyba AI")
    print("Бот успешно запущен!")
    print("=" * 50)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())