from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.menu import get_main_menu, get_back_menu


router = Router()


@router.callback_query(F.data == "analytics")
async def analytics_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "📊 АНАЛИТИКА\n\n"
        "Здесь будет аналитика GlavRyba AI.\n\n"
        "Продажи, выручка, себестоимость, прибыль, "
        "списания и другие показатели.",
        reply_markup=get_back_menu()
    )

    await callback.answer()


@router.callback_query(F.data == "restaurants")
async def restaurants_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "🍽 РЕСТОРАНЫ\n\n"
        "Управление ресторанами и точками.",
        reply_markup=get_back_menu()
    )

    await callback.answer()


@router.callback_query(F.data == "warehouse")
async def warehouse_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "📦 СКЛАД\n\n"
        "Остатки, движение товаров, "
        "списания и инвентаризация.",
        reply_markup=get_back_menu()
    )

    await callback.answer()


@router.callback_query(F.data == "staff")
async def staff_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "👥 ПЕРСОНАЛ\n\n"
        "Сотрудники, должности, "
        "графики и показатели работы.",
        reply_markup=get_back_menu()
    )

    await callback.answer()


@router.callback_query(F.data == "finance")
async def finance_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "💰 ФИНАНСЫ\n\n"
        "Доходы, расходы, прибыль "
        "и финансовые показатели.",
        reply_markup=get_back_menu()
    )

    await callback.answer()


@router.callback_query(F.data == "settings")
async def settings_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "⚙️ НАСТРОЙКИ\n\n"
        "Настройки системы GlavRyba AI.",
        reply_markup=get_back_menu()
    )

    await callback.answer()


@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery):
    text = (
        "Ассаляму алейкум!\n\n"
        "Добро пожаловать в систему GlavRyba AI.\n\n"
        "Выберите необходимый раздел:"
    )

    await callback.message.edit_text(
        text,
        reply_markup=get_main_menu()
    )

    await callback.answer()