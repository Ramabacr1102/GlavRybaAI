import asyncpg


class Database:

    def __init__(self):
        self.pool = None

    async def connect(self):

        self.pool = await asyncpg.create_pool(
            user="postgres",
            password="GlavRyba2026!",
            database="glavryba_ai",
            host="localhost",
            port=5433
        )

        print("=" * 40)
        print("GlavRyba AI")
        print("✅ PostgreSQL успешно подключена!")
        print("=" * 40)