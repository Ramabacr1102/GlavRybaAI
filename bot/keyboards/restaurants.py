from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def restaurants_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 Список ресторанов",
                    callback_data="restaurant_list",
                )
            ],
            [
                InlineKeyboardButton(
                    text="➕ Добавить ресторан",
                    callback_data="restaurant_add",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="admin_menu",
                )
            ],
        ]
    )


def restaurant_list_keyboard(restaurants):
    buttons = []

    for restaurant in restaurants:

        status = (
            "🟢"
            if restaurant["active"]
            else "🔴"
        )

        buttons.append(
            [
                InlineKeyboardButton(
                    text=(
                        f"{status} "
                        f"{restaurant['name']}"
                    ),
                    callback_data=(
                        f"restaurant_view:"
                        f"{restaurant['id']}"
                    ),
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="➕ Добавить ресторан",
                callback_data="restaurant_add",
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="admin_restaurants",
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def restaurant_actions(
    restaurant_id: int,
    active: bool,
):
    buttons = []

    buttons.append(
        [
            InlineKeyboardButton(
                text="✏️ Изменить название",
                callback_data=(
                    f"restaurant_edit:"
                    f"{restaurant_id}"
                ),
            )
        ]
    )

    if active:

        buttons.append(
            [
                InlineKeyboardButton(
                    text="🔴 Деактивировать",
                    callback_data=(
                        f"restaurant_deactivate:"
                        f"{restaurant_id}"
                    ),
                )
            ]
        )

    else:

        buttons.append(
            [
                InlineKeyboardButton(
                    text="🟢 Активировать",
                    callback_data=(
                        f"restaurant_activate:"
                        f"{restaurant_id}"
                    ),
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ К списку",
                callback_data="restaurant_list",
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )