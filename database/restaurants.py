class RestaurantRepository:
    """
    Repository для работы с ресторанами.

    Таблица PostgreSQL:

        restaurants
        ├── id
        ├── name
        └── active
    """

    def __init__(self, db):
        self.db = db

    async def get_all(self):
        """
        Получить все рестораны.
        """

        async with self.db.pool.acquire() as conn:
            return await conn.fetch(
                """
                SELECT
                    id,
                    name,
                    active
                FROM restaurants
                ORDER BY id
                """
            )

    async def get_active(self):
        """
        Получить только активные рестораны.
        """

        async with self.db.pool.acquire() as conn:
            return await conn.fetch(
                """
                SELECT
                    id,
                    name,
                    active
                FROM restaurants
                WHERE active = TRUE
                ORDER BY id
                """
            )

    async def get_by_id(
        self,
        restaurant_id: int,
    ):
        """
        Получить ресторан по ID.
        """

        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(
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

    async def add(self, name: str):
        """
        Добавить ресторан.
        """

        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(
                """
                INSERT INTO restaurants (
                    name
                )
                VALUES ($1)
                RETURNING
                    id,
                    name,
                    active
                """,
                name,
            )

    async def update_name(
        self,
        restaurant_id: int,
        name: str,
    ):
        """
        Изменить название ресторана.
        """

        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(
                """
                UPDATE restaurants
                SET name = $1
                WHERE id = $2
                RETURNING
                    id,
                    name,
                    active
                """,
                name,
                restaurant_id,
            )

    async def set_active(
        self,
        restaurant_id: int,
        active: bool,
    ):
        """
        Изменить статус ресторана.
        """

        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(
                """
                UPDATE restaurants
                SET active = $1
                WHERE id = $2
                RETURNING
                    id,
                    name,
                    active
                """,
                active,
                restaurant_id,
            )

    async def delete(
        self,
        restaurant_id: int,
    ):
        """
        Физическое удаление.
        Пока не используется в Telegram.
        """

        async with self.db.pool.acquire() as conn:
            return await conn.execute(
                """
                DELETE FROM restaurants
                WHERE id = $1
                """,
                restaurant_id,
            )