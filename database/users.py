class UserRepository:

    def __init__(self, db):
        self.db = db

    async def add_user(
        self,
        telegram_id: int,
        full_name: str,
        username: str
    ):

        async with self.db.pool.acquire() as conn:

            await conn.execute(
                """
                INSERT INTO users
                (
                    telegram_id,
                    full_name,
                    username
                )

                VALUES
                (
                    $1,
                    $2,
                    $3
                )

                ON CONFLICT (telegram_id)

                DO NOTHING
                """,
                telegram_id,
                full_name,
                username
            )

    async def get_user(self, telegram_id: int):

        async with self.db.pool.acquire() as conn:

            return await conn.fetchrow(
                """
                SELECT *
                FROM users
                WHERE telegram_id = $1
                """,
                telegram_id
            )

    async def set_role(self, telegram_id: int, role: str):

        async with self.db.pool.acquire() as conn:

            await conn.execute(
                """
                UPDATE users
                SET role = $1
                WHERE telegram_id = $2
                """,
                role,
                telegram_id
            )