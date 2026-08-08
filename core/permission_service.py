from core.permissions import (
    Permission,
    has_permission,
)


class PermissionService:

    def __init__(self, db):
        self.db = db

    async def get_user_role(
        self,
        telegram_id: int,
    ) -> str:

        role = await self.db.pool.fetchval(
            """
            SELECT role
            FROM users
            WHERE telegram_id = $1
            """,
            telegram_id,
        )

        return role or "user"

    async def check(
        self,
        telegram_id: int,
        permission: Permission,
    ) -> bool:

        role = await self.get_user_role(
            telegram_id
        )

        return has_permission(
            role,
            permission,
        )

    async def require(
        self,
        telegram_id: int,
        permission: Permission,
    ):
        allowed = await self.check(
            telegram_id,
            permission,
        )

        if not allowed:
            raise PermissionError(
                "Доступ запрещён."
            )

        return True