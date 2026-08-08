class WarehouseRepository:

    def __init__(self, db):
        self.db = db

    async def get_all(self):

        async with self.db.pool.acquire() as conn:

            return await conn.fetch(
                """
                SELECT
                    w.id,
                    w.name,
                    w.description,
                    w.restaurant_id,
                    w.active,
                    r.name AS restaurant_name
                FROM warehouses w
                LEFT JOIN restaurants r
                    ON r.id = w.restaurant_id
                ORDER BY w.id
                """
            )

    async def get_by_id(
        self,
        warehouse_id: int,
    ):

        async with self.db.pool.acquire() as conn:

            return await conn.fetchrow(
                """
                SELECT
                    w.id,
                    w.name,
                    w.description,
                    w.restaurant_id,
                    w.active,
                    r.name AS restaurant_name
                FROM warehouses w
                LEFT JOIN restaurants r
                    ON r.id = w.restaurant_id
                WHERE w.id = $1
                """,
                warehouse_id,
            )