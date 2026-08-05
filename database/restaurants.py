class RestaurantRepository:

    def __init__(self, db):
        self.db = db

    async def get_all(self):

        async with self.db.pool.acquire() as conn:

            return await conn.fetch("""
                SELECT *
                FROM restaurants
                ORDER BY id
            """)

    async def add(self, name):

        async with self.db.pool.acquire() as conn:

            await conn.execute("""
                INSERT INTO restaurants(name)
                VALUES($1)
            """, name)

    async def delete(self, restaurant_id):

        async with self.db.pool.acquire() as conn:

            await conn.execute("""
                DELETE FROM restaurants
                WHERE id=$1
            """, restaurant_id)