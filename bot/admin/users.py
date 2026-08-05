from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "admin_users")
async def admin_users(callback: CallbackQuery, db):

    rows = await db.pool.fetch("""
        SELECT
            telegram_id,
            full_name,
            role
        FROM users
        ORDER BY id
    """)

    if not rows:
        await callback.message.edit_text("Пользователей пока нет.")
        await callback.answer()
        return

    text = "👥 Пользователи\n\n"

    for i, row in enumerate(rows, start=1):
        text += (
            f"{i}. {row['full_name']}\n"
            f"🆔 {row['telegram_id']}\n"
            f"🎭 {row['role']}\n\n"
        )

    await callback.message.edit_text(text)

    await callback.answer()