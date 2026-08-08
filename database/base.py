class BaseRepository:

    def __init__(self, db):
        self.db = db

    async def execute(self, query, *args):
        async with self.db.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query, *args):
        async with self.db.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query, *args):
        async with self.db.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query, *args):
        async with self.db.pool.acquire() as conn:
            return await conn.fetchval(query, *args)