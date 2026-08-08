from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# =========================================================
# МЕНЮ ПОЛЬЗОВАТЕЛЕЙ
# =========================================================

def users_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 Список пользователей",
                    callback_data="users_list",
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


# =========================================================
# СПИСОК ПОЛЬЗОВАТЕЛЕЙ
# =========================================================

def users_list_keyboard(users):
    buttons = []

    for user in users:
        role = user["role"] or "user"

        buttons.append(
            [
                InlineKeyboardButton(
                    text=(
                        f"👤 {user['full_name']} — {role}"
                    ),
                    callback_data=(
                        f"user_view:{user['id']}"
                    ),
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="admin_users",
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


# =========================================================
# КАРТОЧКА ПОЛЬЗОВАТЕЛЯ
# =========================================================

def user_actions(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎭 Изменить роль",
                    callback_data=(
                        f"user_role:{user_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏢 Рестораны",
                    callback_data=(
                        f"user_restaurants:{user_id}"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ К пользователям",
                    callback_data="users_list",
                )
            ],
        ]
    )


# =========================================================
# ВЫБОР РОЛИ
# =========================================================

def roles_keyboard(user_id: int, roles):
    buttons = []

    for role in roles:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=(
                        f"🎭 {role['name']} — "
                        f"{role['description']}"
                    ),
                    callback_data=(
                        f"user_set_role:"
                        f"{user_id}:"
                        f"{role['name']}"
                    ),
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=(
                    f"user_view:{user_id}"
                ),
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


# =========================================================
# РЕСТОРАНЫ ПОЛЬЗОВАТЕЛЯ
# =========================================================

def user_restaurants_keyboard(
    user_id: int,
    restaurants,
):
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
                        f"{restaurant['name']} ❌"
                    ),
                    callback_data=(
                        f"user_remove_restaurant:"
                        f"{user_id}:"
                        f"{restaurant['id']}"
                    ),
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="➕ Добавить ресторан",
                callback_data=(
                    f"user_add_restaurant:"
                    f"{user_id}"
                ),
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=(
                    f"user_view:{user_id}"
                ),
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


# =========================================================
# ДОСТУПНЫЕ РЕСТОРАНЫ
# =========================================================

def available_restaurants_keyboard(
    user_id: int,
    restaurants,
):
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
                        f"user_assign_restaurant:"
                        f"{user_id}:"
                        f"{restaurant['id']}"
                    ),
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=(
                    f"user_restaurants:{user_id}"
                ),
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )