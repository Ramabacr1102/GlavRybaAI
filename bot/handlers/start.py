from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.menu import get_main_menu
from bot.keyboards.admin import admin_menu
from bot.services.auth_service import AuthService


router = Router()


@router.message(CommandStart())
async def start_handler(
    message: Message,
    db,
):
    """
    Обработка команды /start.

    Пользователь автоматически регистрируется
    или обновляет свои данные.

    Директор получает административную панель.
    Остальные пользователи получают основное меню.
    """

    auth = AuthService(db)

    user = await auth.register(
        message.from_user
    )

    print(
        "USER =",
        dict(user),
    )

    print(
        "ROLE =",
        user["role"],
    )

    # Директор
    if user["role"] == "director":

        await message.answer(
            "🔥 ПАНЕЛЬ ДИРЕКТОРА 🔥\n\n"
            "Добро пожаловать в GlavRyba AI.\n\n"
            "Выберите необходимый раздел:",
            reply_markup=admin_menu(),
        )

        return

    # Обычный пользователь
    await message.answer(
        "Ассаляму алейкум!\n\n"
        "Добро пожаловать в GlavRyba AI.\n\n"
        "Выберите необходимый раздел:",
        reply_markup=get_main_menu(),
    )