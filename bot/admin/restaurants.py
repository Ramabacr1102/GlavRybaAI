from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "admin_restaurants")
async def restaurants(callback: CallbackQuery):

    print("RESTAURANTS CLICKED")

    await callback.message.edit_text(
        "ТЕСТ ПРОШЕЛ"
    )

    await callback.answer()