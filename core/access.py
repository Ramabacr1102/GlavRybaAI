from aiogram.types import CallbackQuery

from core.permissions import Permission
from core.permission_service import PermissionService


async def check_permission(
    callback: CallbackQuery,
    db,
    permission: Permission,
) -> bool:

    service = PermissionService(db)

    allowed = await service.check(
        callback.from_user.id,
        permission,
    )

    if not allowed:
        await callback.answer(
            "⛔ У вас нет доступа к этому разделу.",
            show_alert=True,
        )
        return False

    return True