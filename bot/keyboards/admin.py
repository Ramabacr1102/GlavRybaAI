from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👥 Пользователи",
                    callback_data="admin_users",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏢 Рестораны",
                    callback_data="admin_restaurants",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎭 Роли",
                    callback_data="admin_roles",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📦 Склад",
                    callback_data="warehouse",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Статистика",
                    callback_data="admin_stats",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚙️ Настройки",
                    callback_data="admin_settings",
                )
            ],
        ]
    )