from database.users import UserRepository


class UserService:

    def __init__(self, db):
        self.users = UserRepository(db)

    # =========================================================
    # USERS
    # =========================================================

    async def get_all_users(self):
        return await self.users.get_all()

    async def get_user(self, user_id: int):
        return await self.users.get_by_id(user_id)

    # =========================================================
    # ROLES
    # =========================================================

    async def get_roles(self):
        async with self.users.db.pool.acquire() as conn:
            return await conn.fetch(
                """
                SELECT
                    id,
                    name,
                    description
                FROM roles
                ORDER BY id
                """
            )

    async def get_role(self, role_name: str):
        async with self.users.db.pool.acquire() as conn:
            return await conn.fetchrow(
                """
                SELECT
                    id,
                    name,
                    description
                FROM roles
                WHERE name = $1
                """,
                role_name,
            )

    async def set_role(
        self,
        user_id: int,
        role: str,
    ):
        role_data = await self.get_role(role)

        if not role_data:
            raise ValueError(
                "Такой роли не существует."
            )

        return await self.users.set_role_by_id(
            user_id,
            role,
        )

    # =========================================================
    # RESTAURANTS
    # =========================================================

    async def get_user_restaurants(
        self,
        user_id: int,
    ):
        return await self.users.get_user_restaurants(
            user_id
        )

    async def get_available_restaurants(
        self,
        user_id: int,
    ):
        return await self.users.get_available_restaurants(
            user_id
        )

    async def assign_restaurant(
        self,
        user_id: int,
        restaurant_id: int,
    ):
        restaurant = await self.users.db.pool.fetchrow(
            """
            SELECT
                id,
                name,
                active
            FROM restaurants
            WHERE id = $1
            """,
            restaurant_id,
        )

        if not restaurant:
            raise ValueError(
                "Ресторан не найден."
            )

        return await self.users.assign_restaurant(
            user_id,
            restaurant_id,
        )

    async def remove_restaurant(
        self,
        user_id: int,
        restaurant_id: int,
    ):
        return await self.users.remove_restaurant(
            user_id,
            restaurant_id,
        )