from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.warehouse import (
    warehouse_menu,
    warehouse_points_keyboard,
)

from bot.services.warehouse_service import (
    WarehouseService,
)

from core.access import check_permission
from core.permissions import Permission


router = Router()


@router.callback_query(
    F.data == "warehouse"
)
async def warehouse_menu_callback(
    callback: CallbackQuery,
    db,
):

    if not await check_permission(
        callback,
        db,
        Permission.WAREHOUSE_VIEW,
    ):
        return

    await callback.message.edit_text(
        "📦 СКЛАД\n\n"
        "Управление складской системой "
        "GlavRyba AI.\n\n"
        "Выберите необходимый раздел:",
        reply_markup=warehouse_menu(),
    )

    await callback.answer()


@router.callback_query(
    F.data == "warehouse_points"
)
async def warehouse_points(
    callback: CallbackQuery,
    db,
):

    if not await check_permission(
        callback,
        db,
        Permission.WAREHOUSE_VIEW,
    ):
        return

    service = WarehouseService(db)

    warehouses = (
        await service.get_all_warehouses()
    )

    if not warehouses:

        await callback.message.edit_text(
            "🏢 СКЛАДСКИЕ ТОЧКИ\n\n"
            "Складов пока нет.",
            reply_markup=warehouse_menu(),
        )

        await callback.answer()
        return

    await callback.message.edit_text(
        "🏢 СКЛАДСКИЕ ТОЧКИ\n\n"
        "Выберите склад:",
        reply_markup=warehouse_points_keyboard(
            warehouses
        ),
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("warehouse_view:")
)
async def warehouse_view(
    callback: CallbackQuery,
    db,
):

    if not await check_permission(
        callback,
        db,
        Permission.WAREHOUSE_VIEW,
    ):
        return

    warehouse_id = int(
        callback.data.split(":")[1]
    )

    service = WarehouseService(db)

    warehouse = (
        await service.get_warehouse(
            warehouse_id
        )
    )

    if not warehouse:

        await callback.answer(
            "Склад не найден.",
            show_alert=True,
        )

        return

    status = (
        "🟢 Активен"
        if warehouse["active"]
        else "🔴 Неактивен"
    )

    restaurant = (
        warehouse["restaurant_name"]
        or "Не привязан"
    )

    text = (
        "🏢 СКЛАД\n\n"
        f"Название: {warehouse['name']}\n"
        f"Ресторан: {restaurant}\n"
        f"Статус: {status}\n\n"
        f"{warehouse['description'] or ''}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=warehouse_menu(),
    )

    await callback.answer()


# =========================================================
# ЗАГЛУШКИ БУДУЩИХ РАЗДЕЛОВ
# =========================================================

@router.callback_query(
    F.data == "warehouse_products"
)
async def warehouse_products(
    callback: CallbackQuery,
):

    await callback.answer(
        "📦 Номенклатуру подключим следующим этапом.",
        show_alert=True,
    )


@router.callback_query(
    F.data == "warehouse_stock"
)
async def warehouse_stock(
    callback: CallbackQuery,
):

    await callback.answer(
        "📊 Остатки подключим следующим этапом.",
        show_alert=True,
    )


@router.callback_query(
    F.data == "warehouse_receipt"
)
async def warehouse_receipt(
    callback: CallbackQuery,
):

    await callback.answer(
        "➕ Приход подключим следующим этапом.",
        show_alert=True,
    )


@router.callback_query(
    F.data == "warehouse_transfer"
)
async def warehouse_transfer(
    callback: CallbackQuery,
):

    await callback.answer(
        "🔄 Перемещение подключим следующим этапом.",
        show_alert=True,
    )


@router.callback_query(
    F.data == "warehouse_writeoff"
)
async def warehouse_writeoff(
    callback: CallbackQuery,
):

    await callback.answer(
        "➖ Списание подключим следующим этапом.",
        show_alert=True,
    )


@router.callback_query(
    F.data == "warehouse_inventory"
)
async def warehouse_inventory(
    callback: CallbackQuery,
):

    await callback.answer(
        "📋 Инвентаризацию подключим следующим этапом.",
        show_alert=True,
    )