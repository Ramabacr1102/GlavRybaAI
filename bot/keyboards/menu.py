from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📊 Аналитика",
                    callback_data="analytics"
                ),
                InlineKeyboardButton(
                    text="🍽 Рестораны",
                    callback_data="restaurants"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📦 Склад",
                    callback_data="warehouse"
                ),
                InlineKeyboardButton(
                    text="👥 Персонал",
                    callback_data="staff"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="💰 Финансы",
                    callback_data="finance"
                ),
                InlineKeyboardButton(
                    text="⚙️ Настройки",
                    callback_data="settings"
                ),
            ],
        ]
    )

    return keyboard


def get_back_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="main_menu"
                )
            ]
        ]
    )

    return keyboard