from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.users import (
    users_menu,
    users_list_keyboard,
    user_actions,
    roles_keyboard,
    user_restaurants_keyboard,
    available_restaurants_keyboard,
)
from bot.keyboards.admin import admin_menu
from bot.services.user_service import UserService


router = Router()


async def is_director(db, telegram_id: int) -> bool:
    role = await db.pool.fetchval(
        """
        SELECT role
        FROM users
        WHERE telegram_id = $1
        """,
        telegram_id,
    )

    return role == "director"


@router.callback_query(F.data == "admin_users")
async def admin_users(
    callback: CallbackQuery,
    db,
):
    if not await is_director(db, callback.from_user.id):
        await callback.answer(
            "⛔ Доступ запрещён",
            show_alert=True,
        )
        return

    await callback.message.edit_text(
        "👥 ПОЛЬЗОВАТЕЛИ\n\n"
        "Управление пользователями и ролями GlavRyba AI.",
        reply_markup=users_menu(),
    )

    await callback.answer()


@router.callback_query(F.data == "users_list")
async def users_list(
    callback: CallbackQuery,
    db,
):
    if not await is_director(db, callback.from_user.id):
        await callback.answer(
            "⛔ Доступ запрещён",
            show_alert=True,
        )
        return

    service = UserService(db)

    users = await service.get_all_users()

    if not users:
        await callback.message.edit_text(
            "👥 ПОЛЬЗОВАТЕЛИ\n\n"
            "Пользователей пока нет.",
            reply_markup=users_menu(),
        )
        await callback.answer()
        return

    await callback.message.edit_text(
        "👥 ПОЛЬЗОВАТЕЛИ\n\n"
        "Выберите пользователя:",
        reply_markup=users_list_keyboard(users),
    )

    await callback.answer()


@router.callback_query(F.data.startswith("user_view:"))
async def user_view(
    callback: CallbackQuery,
    db,
):
    if not await is_director(db, callback.from_user.id):
        await callback.answer(
            "⛔ Доступ запрещён",
            show_alert=True,
        )
        return

    user_id = int(
        callback.data.split(":")[1]
    )

    service = UserService(db)

    user = await service.get_user(user_id)

    if not user:
        await callback.answer(
            "Пользователь не найден",
            show_alert=True,
        )
        return

    role = user["role"] or "user"
    username = user["username"] or "не указан"

    text = (
        "👤 ПОЛЬЗОВАТЕЛЬ\n\n"
        f"ID: {user['id']}\n"
        f"Имя: {user['full_name']}\n"
        f"Username: @{username}\n"
        f"Telegram ID: {user['telegram_id']}\n"
        f"Роль: 🎭 {role}\n"
        f"Дата регистрации: "
        f"{user['created_at']:%d.%m.%Y %H:%M}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=user_actions(user["id"]),
    )

    await callback.answer()


@router.callback_query(F.data.startswith("user_role:"))
async def user_role(
    callback: CallbackQuery,
    db,
):
    if not await is_director(db, callback.from_user.id):
        await callback.answer(
            "⛔ Доступ запрещён",
            show_alert=True,
        )
        return

    user_id = int(
        callback.data.split(":")[1]
    )

    service = UserService(db)

    user = await service.get_user(user_id)

    if not user:
        await callback.answer(
            "Пользователь не найден",
            show_alert=True,
        )
        return

    roles = await service.get_roles()

    await callback.message.edit_text(
        "🎭 ИЗМЕНЕНИЕ РОЛИ\n\n"
        f"Пользователь: {user['full_name']}\n"
        f"Текущая роль: {user['role']}\n\n"
        "Выберите новую роль:",
        reply_markup=roles_keyboard(
            user["id"],
            roles,
        ),
    )

    await callback.answer()


@router.callback_query(F.data.startswith("user_set_role:"))
async def user_set_role(
    callback: CallbackQuery,
    db,
):
    if not await is_director(db, callback.from_user.id):
        await callback.answer(
            "⛔ Доступ запрещён",
            show_alert=True,
        )
        return

    parts = callback.data.split(":")

    user_id = int(parts[1])
    new_role = parts[2]

    service = UserService(db)

    target_user = await service.get_user(user_id)

    if not target_user:
        await callback.answer(
            "Пользователь не найден",
            show_alert=True,
        )
        return

    current_user = await db.pool.fetchrow(
        """
        SELECT
            id,
            role
        FROM users
        WHERE telegram_id = $1
        """,
        callback.from_user.id,
    )

    if (
        current_user["id"] == user_id
        and new_role != "director"
    ):
        await callback.answer(
            "⛔ Нельзя снять роль director с самого себя.",
            show_alert=True,
        )
        return

    try:
        updated_user = await service.set_role(
            user_id,
            new_role,
        )
    except ValueError as error:
        await callback.answer(
            str(error),
            show_alert=True,
        )
        return

    await callback.message.edit_text(
        "✅ РОЛЬ ИЗМЕНЕНА\n\n"
        f"Пользователь: {updated_user['full_name']}\n"
        f"Новая роль: 🎭 {updated_user['role']}",
        reply_markup=user_actions(
            updated_user["id"]
        ),
    )

    await callback.answer(
        "Роль успешно изменена."
    )


@router.callback_query(F.data.startswith("user_restaurants:"))
async def user_restaurants(
    callback: CallbackQuery,
    db,
):
    if not await is_director(db, callback.from_user.id):
        await callback.answer(
            "⛔ Доступ запрещён",
            show_alert=True,
        )
        return

    user_id = int(
        callback.data.split(":")[1]
    )

    service = UserService(db)

    user = await service.get_user(user_id)

    if not user:
        await callback.answer(
            "Пользователь не найден",
            show_alert=True,
        )
        return

    restaurants = await service.get_user_restaurants(
        user_id
    )

    if restaurants:
        lines = [
            "🏢 РЕСТОРАНЫ ПОЛЬЗОВАТЕЛЯ",
            "",
            f"👤 {user['full_name']}",
            "",
            "Назначенные рестораны:",
        ]

        for restaurant in restaurants:
            status = (
                "🟢"
                if restaurant["active"]
                else "🔴"
            )

            lines.append(
                f"{status} {restaurant['name']}"
            )

        text = "\n".join(lines)

    else:
        text = (
            "🏢 РЕСТОРАНЫ ПОЛЬЗОВАТЕЛЯ\n\n"
            f"👤 {user['full_name']}\n\n"
            "Рестораны пока не назначены."
        )

    await callback.message.edit_text(
        text,
        reply_markup=user_restaurants_keyboard(
            user_id,
            restaurants,
        ),
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("user_add_restaurant:")
)
async def user_add_restaurant(
    callback: CallbackQuery,
    db,
):
    if not await is_director(db, callback.from_user.id):
        await callback.answer(
            "⛔ Доступ запрещён",
            show_alert=True,
        )
        return

    user_id = int(
        callback.data.split(":")[1]
    )

    service = UserService(db)

    user = await service.get_user(user_id)

    if not user:
        await callback.answer(
            "Пользователь не найден",
            show_alert=True,
        )
        return

    restaurants = (
        await service.get_available_restaurants(
            user_id
        )
    )

    if not restaurants:
        await callback.answer(
            "Все рестораны уже назначены.",
            show_alert=True,
        )
        return

    await callback.message.edit_text(
        "➕ ДОБАВЛЕНИЕ РЕСТОРАНА\n\n"
        f"Пользователь: {user['full_name']}\n\n"
        "Выберите ресторан:",
        reply_markup=available_restaurants_keyboard(
            user_id,
            restaurants,
        ),
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("user_assign_restaurant:")
)
async def user_assign_restaurant(
    callback: CallbackQuery,
    db,
):
    if not await is_director(db, callback.from_user.id):
        await callback.answer(
            "⛔ Доступ запрещён",
            show_alert=True,
        )
        return

    parts = callback.data.split(":")

    user_id = int(parts[1])
    restaurant_id = int(parts[2])

    service = UserService(db)

    try:
        await service.assign_restaurant(
            user_id,
            restaurant_id,
        )
    except ValueError as error:
        await callback.answer(
            str(error),
            show_alert=True,
        )
        return

    restaurants = await service.get_user_restaurants(
        user_id
    )

    await callback.message.edit_text(
        "🏢 РЕСТОРАНЫ ПОЛЬЗОВАТЕЛЯ\n\n"
        "✅ Ресторан успешно назначен.",
        reply_markup=user_restaurants_keyboard(
            user_id,
            restaurants,
        ),
    )

    await callback.answer(
        "Ресторан назначен."
    )


@router.callback_query(
    F.data.startswith("user_remove_restaurant:")
)
async def user_remove_restaurant(
    callback: CallbackQuery,
    db,
):
    if not await is_director(db, callback.from_user.id):
        await callback.answer(
            "⛔ Доступ запрещён",
            show_alert=True,
        )
        return

    parts = callback.data.split(":")

    user_id = int(parts[1])
    restaurant_id = int(parts[2])

    service = UserService(db)

    await service.remove_restaurant(
        user_id,
        restaurant_id,
    )

    restaurants = await service.get_user_restaurants(
        user_id
    )

    await callback.message.edit_text(
        "🏢 РЕСТОРАНЫ ПОЛЬЗОВАТЕЛЯ\n\n"
        "Ресторан удалён из привязки.",
        reply_markup=user_restaurants_keyboard(
            user_id,
            restaurants,
        ),
    )

    await callback.answer(
        "Ресторан убран."
    )


@router.callback_query(F.data == "admin_menu")
async def admin_menu_callback(
    callback: CallbackQuery,
    db,
):
    if not await is_director(db, callback.from_user.id):
        await callback.answer(
            "⛔ Доступ запрещён",
            show_alert=True,
        )
        return

    await callback.message.edit_text(
        "🔥 ПАНЕЛЬ ДИРЕКТОРА 🔥\n\n"
        "Добро пожаловать в GlavRyba AI.\n\n"
        "Выберите необходимый раздел:",
        reply_markup=admin_menu(),
    )

    await callback.answer()