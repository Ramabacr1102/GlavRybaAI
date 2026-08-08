from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bot.keyboards.restaurants import (
    restaurants_menu,
    restaurant_actions,
    restaurant_list_keyboard,
)
from bot.services.restaurant_service import RestaurantService


router = Router()


class RestaurantStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_edit_name = State()


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


@router.callback_query(F.data == "admin_restaurants")
async def admin_restaurants(
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
        "🏢 РЕСТОРАНЫ\n\n"
        "Управление ресторанами GlavRyba AI.",
        reply_markup=restaurants_menu(),
    )

    await callback.answer()


@router.callback_query(F.data == "restaurant_list")
async def restaurant_list(
    callback: CallbackQuery,
    db,
):
    if not await is_director(db, callback.from_user.id):
        await callback.answer(
            "⛔ Доступ запрещён",
            show_alert=True,
        )
        return

    service = RestaurantService(db)
    restaurants = await service.get_all()

    await callback.message.edit_text(
        "🏢 РЕСТОРАНЫ\n\n"
        "Выберите ресторан:",
        reply_markup=restaurant_list_keyboard(restaurants),
    )

    await callback.answer()


@router.callback_query(F.data.startswith("restaurant_view:"))
async def restaurant_view(
    callback: CallbackQuery,
    db,
):
    if not await is_director(db, callback.from_user.id):
        await callback.answer(
            "⛔ Доступ запрещён",
            show_alert=True,
        )
        return

    restaurant_id = int(callback.data.split(":")[1])

    service = RestaurantService(db)
    restaurant = await service.get_by_id(restaurant_id)

    if not restaurant:
        await callback.answer(
            "Ресторан не найден",
            show_alert=True,
        )
        return

    status = "🟢 Активен" if restaurant["active"] else "🔴 Неактивен"

    text = (
        "🏢 РЕСТОРАН\n\n"
        f"ID: {restaurant['id']}\n"
        f"Название: {restaurant['name']}\n"
        f"Статус: {status}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=restaurant_actions(
            restaurant["id"],
            restaurant["active"],
        ),
    )

    await callback.answer()


@router.callback_query(F.data == "restaurant_add")
async def restaurant_add(
    callback: CallbackQuery,
    state: FSMContext,
    db,
):
    if not await is_director(db, callback.from_user.id):
        await callback.answer(
            "⛔ Доступ запрещён",
            show_alert=True,
        )
        return

    await state.set_state(
        RestaurantStates.waiting_for_name
    )

    await callback.message.edit_text(
        "➕ ДОБАВЛЕНИЕ РЕСТОРАНА\n\n"
        "Введите название нового ресторана.\n\n"
        "Для отмены отправьте /cancel",
    )

    await callback.answer()


@router.message(RestaurantStates.waiting_for_name)
async def restaurant_add_name(
    message: Message,
    state: FSMContext,
    db,
):
    if message.text == "/cancel":
        await state.clear()

        await message.answer(
            "❌ Добавление отменено.",
            reply_markup=restaurants_menu(),
        )
        return

    service = RestaurantService(db)

    try:
        restaurant = await service.add(message.text)
    except ValueError as error:
        await message.answer(f"⚠️ {error}")
        return

    await state.clear()

    await message.answer(
        "✅ Ресторан добавлен.\n\n"
        f"ID: {restaurant['id']}\n"
        f"Название: {restaurant['name']}\n"
        "Статус: 🟢 Активен",
        reply_markup=restaurants_menu(),
    )


@router.callback_query(F.data.startswith("restaurant_edit:"))
async def restaurant_edit(
    callback: CallbackQuery,
    state: FSMContext,
    db,
):
    if not await is_director(db, callback.from_user.id):
        await callback.answer(
            "⛔ Доступ запрещён",
            show_alert=True,
        )
        return

    restaurant_id = int(callback.data.split(":")[1])

    service = RestaurantService(db)
    restaurant = await service.get_by_id(restaurant_id)

    if not restaurant:
        await callback.answer(
            "Ресторан не найден",
            show_alert=True,
        )
        return

    await state.update_data(
        restaurant_id=restaurant_id
    )

    await state.set_state(
        RestaurantStates.waiting_for_edit_name
    )

    await callback.message.edit_text(
        "✏️ ИЗМЕНЕНИЕ РЕСТОРАНА\n\n"
        f"Текущее название: {restaurant['name']}\n\n"
        "Введите новое название.\n\n"
        "Для отмены отправьте /cancel",
    )

    await callback.answer()


@router.message(RestaurantStates.waiting_for_edit_name)
async def restaurant_edit_name(
    message: Message,
    state: FSMContext,
    db,
):
    if message.text == "/cancel":
        await state.clear()

        await message.answer(
            "❌ Изменение отменено.",
            reply_markup=restaurants_menu(),
        )
        return

    data = await state.get_data()
    restaurant_id = data.get("restaurant_id")

    service = RestaurantService(db)

    try:
        restaurant = await service.update_name(
            restaurant_id,
            message.text,
        )
    except ValueError as error:
        await message.answer(f"⚠️ {error}")
        return

    await state.clear()

    await message.answer(
        "✅ Название изменено.\n\n"
        f"ID: {restaurant['id']}\n"
        f"Название: {restaurant['name']}",
        reply_markup=restaurants_menu(),
    )


@router.callback_query(
    F.data.startswith("restaurant_activate:")
)
async def restaurant_activate(
    callback: CallbackQuery,
    db,
):
    if not await is_director(db, callback.from_user.id):
        await callback.answer(
            "⛔ Доступ запрещён",
            show_alert=True,
        )
        return

    restaurant_id = int(callback.data.split(":")[1])

    service = RestaurantService(db)

    restaurant = await service.activate(restaurant_id)

    if not restaurant:
        await callback.answer(
            "Ресторан не найден",
            show_alert=True,
        )
        return

    await callback.message.edit_text(
        "🟢 РЕСТОРАН АКТИВИРОВАН\n\n"
        f"{restaurant['name']}",
        reply_markup=restaurant_actions(
            restaurant["id"],
            True,
        ),
    )

    await callback.answer("Ресторан активирован")


@router.callback_query(
    F.data.startswith("restaurant_deactivate:")
)
async def restaurant_deactivate(
    callback: CallbackQuery,
    db,
):
    if not await is_director(db, callback.from_user.id):
        await callback.answer(
            "⛔ Доступ запрещён",
            show_alert=True,
        )
        return

    restaurant_id = int(callback.data.split(":")[1])

    service = RestaurantService(db)

    restaurant = await service.deactivate(restaurant_id)

    if not restaurant:
        await callback.answer(
            "Ресторан не найден",
            show_alert=True,
        )
        return

    await callback.message.edit_text(
        "🔴 РЕСТОРАН ДЕАКТИВИРОВАН\n\n"
        f"{restaurant['name']}",
        reply_markup=restaurant_actions(
            restaurant["id"],
            False,
        ),
    )

    await callback.answer("Ресторан деактивирован")