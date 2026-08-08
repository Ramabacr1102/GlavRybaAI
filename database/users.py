class UserRepository:

    def __init__(self, db):
        self.db = db

    # =========================================================
    # USERS
    # =========================================================

    async def add_user(
        self,
        telegram_id: int,
        full_name: str,
        username: str,
    ):
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(
                """
                INSERT INTO users (
                    telegram_id,
                    full_name,
                    username
                )
                VALUES ($1, $2, $3)
                ON CONFLICT (telegram_id)
                DO UPDATE SET
                    full_name = EXCLUDED.full_name,
                    username = EXCLUDED.username
                RETURNING
                    id,
                    telegram_id,
                    full_name,
                    username,
                    role,
                    created_at
                """,
                telegram_id,
                full_name,
                username,
            )

    async def get_user(
        self,
        telegram_id: int,
    ):
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(
                """
                SELECT
                    id,
                    telegram_id,
                    full_name,
                    username,
                    role,
                    created_at
                FROM users
                WHERE telegram_id = $1
                """,
                telegram_id,
            )

    async def get_by_id(
        self,
        user_id: int,
    ):
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(
                """
                SELECT
                    id,
                    telegram_id,
                    full_name,
                    username,
                    role,
                    created_at
                FROM users
                WHERE id = $1
                """,
                user_id,
            )

    async def get_all(self):
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(
                """
                SELECT
                    id,
                    telegram_id,
                    full_name,
                    username,
                    role,
                    created_at
                FROM users
                ORDER BY id
                """
            )

    async def set_role_by_id(
        self,
        user_id: int,
        role: str,
    ):
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(
                """
                UPDATE users
                SET role = $1
                WHERE id = $2
                RETURNING
                    id,
                    telegram_id,
                    full_name,
                    username,
                    role,
                    created_at
                """,
                role,
                user_id,
            )

    # =========================================================
    # USER ↔ RESTAURANTS
    # =========================================================

    async def get_user_restaurants(
        self,
        user_id: int,
    ):
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(
                """
                SELECT
                    r.id,
                    r.name,
                    r.active
                FROM restaurants r
                INNER JOIN user_restaurants ur
                    ON ur.restaurant_id = r.id
                WHERE ur.user_id = $1
                ORDER BY r.id
                """,
                user_id,
            )

    async def get_available_restaurants(
        self,
        user_id: int,
    ):
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(
                """
                SELECT
                    r.id,
                    r.name,
                    r.active
                FROM restaurants r
                WHERE r.id NOT IN (
                    SELECT restaurant_id
                    FROM user_restaurants
                    WHERE user_id = $1
                )
                ORDER BY r.id
                """,
                user_id,
            )

    async def assign_restaurant(
        self,
        user_id: int,
        restaurant_id: int,
    ):
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(
                """
                INSERT INTO user_restaurants (
                    user_id,
                    restaurant_id
                )
                VALUES ($1, $2)
                ON CONFLICT (
                    user_id,
                    restaurant_id
                )
                DO NOTHING
                RETURNING
                    id,
                    user_id,
                    restaurant_id
                """,
                user_id,
                restaurant_id,
            )

    async def remove_restaurant(
        self,
        user_id: int,
        restaurant_id: int,
    ):
        async with self.db.pool.acquire() as conn:
            return await conn.execute(
                """
                DELETE FROM user_restaurants
                WHERE user_id = $1
                  AND restaurant_id = $2
                """,
                user_id,
                restaurant_id,
            )