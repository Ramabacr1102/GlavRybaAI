import asyncio

from aiogram import Bot, Dispatcher

from config.config import BOT_TOKEN

from database.database import Database

from bot.routers import router

from core.logger import setup_logger
from core.version import VERSION, BUILD, APP_NAME


logger = setup_logger()


async def main():

    logger.info("=" * 60)
    logger.info(APP_NAME)
    logger.info(f"Version : {VERSION}")
    logger.info(f"Build   : {BUILD}")
    logger.info("=" * 60)

    db = Database()
    await db.connect()

    logger.info("PostgreSQL : OK")

    bot = Bot(BOT_TOKEN)

    dp = Dispatcher()

    dp["db"] = db

    dp.include_router(router)

    logger.info("Routers : OK")
    logger.info("Bot : STARTED")

    try:
        await dp.start_polling(bot)

    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())