from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def warehouse_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏢 Складские точки",
                    callback_data="warehouse_points",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📦 Номенклатура",
                    callback_data="warehouse_products",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Остатки",
                    callback_data="warehouse_stock",
                )
            ],
            [
                InlineKeyboardButton(
                    text="➕ Приход",
                    callback_data="warehouse_receipt",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Перемещение",
                    callback_data="warehouse_transfer",
                )
            ],
            [
                InlineKeyboardButton(
                    text="➖ Списание",
                    callback_data="warehouse_writeoff",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Инвентаризация",
                    callback_data="warehouse_inventory",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="main_menu",
                )
            ],
        ]
    )


def warehouse_points_keyboard(warehouses):

    buttons = []

    for warehouse in warehouses:

        status = (
            "🟢"
            if warehouse["active"]
            else "🔴"
        )

        buttons.append(
            [
                InlineKeyboardButton(
                    text=(
                        f"{status} "
                        f"{warehouse['name']}"
                    ),
                    callback_data=(
                        f"warehouse_view:"
                        f"{warehouse['id']}"
                    ),
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="warehouse",
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )