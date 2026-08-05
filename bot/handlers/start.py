from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.menu import get_main_menu
from bot.keyboards.admin import admin_menu
from bot.services.auth_service import AuthService

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, db):

    auth = AuthService(db)

    user = await auth.register(message.from_user)

    print("USER =", dict(user))
    print("ROLE =", user["role"])

    if user["role"] == "director":

        await message.answer(
            "🔥 ДИРЕКТОР TEST 123 🔥",
            reply_markup=admin_menu()
        )
        return

    await message.answer(
        "Ассаляму алейкум!\n\n"
        "Добро пожаловать в GlavRyba AI.",
        reply_markup=get_main_menu()
    )