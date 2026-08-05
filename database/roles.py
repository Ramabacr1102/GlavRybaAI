class RoleRepository:

    def __init__(self, db):
        self.db = db

    async def get_role(self, name: str):

        async with self.db.pool.acquire() as conn:

            return await conn.fetchrow(
                """
                SELECT *
                FROM roles
                WHERE name = $1
                """,
                name
            )

    async def get_all_roles(self):

        async with self.db.pool.acquire() as conn:

            return await conn.fetch(
                """
                SELECT *
                FROM roles
                ORDER BY id
                """
            )