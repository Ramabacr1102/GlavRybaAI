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

        await self.create_tables()

    async def create_tables(self):

        async with self.pool.acquire() as conn:

            # Таблица ролей
            await conn.execute("""
            CREATE TABLE IF NOT EXISTS roles(
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            );
            """)

            # Таблица пользователей
            await conn.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE,
                full_name TEXT,
                username TEXT,
                role_id INTEGER REFERENCES roles(id),
                created_at TIMESTAMP DEFAULT NOW()
            );
            """)

            # Таблица ресторанов
            await conn.execute("""
            CREATE TABLE IF NOT EXISTS restaurants(
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE,
                active BOOLEAN DEFAULT TRUE
            );
            """)

            # Первичное заполнение ролей
            await conn.execute("""
            INSERT INTO roles(name, description)
            VALUES
            ('director','Полный доступ'),
            ('manager','Управляющий'),
            ('accountant','Бухгалтер'),
            ('warehouse','Склад'),
            ('cashier','Кассир'),
            ('hr','HR'),
            ('it','IT')
            ON CONFLICT (name) DO NOTHING;
            """)