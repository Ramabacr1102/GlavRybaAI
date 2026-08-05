from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram import F

router = Router()


@router.callback_query(F.data == "admin")
async def admin_panel(callback: CallbackQuery):

    await callback.message.edit_text(

        "⚙️ Панель администратора\n\n"
        "Выберите действие.",

        reply_markup=None

    )

    await callback.answer()