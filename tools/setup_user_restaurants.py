import asyncio

from database.database import Database


async def main():
    db = Database()

    try:
        await db.connect()

        print("=" * 60)
        print("GlavRyba AI")
        print("SETUP USER ↔ RESTAURANT")
        print("=" * 60)

        await db.pool.execute(
            """
            CREATE TABLE IF NOT EXISTS user_restaurants (
                id SERIAL PRIMARY KEY,

                user_id INTEGER NOT NULL
                    REFERENCES users(id)
                    ON DELETE CASCADE,

                restaurant_id INTEGER NOT NULL
                    REFERENCES restaurants(id)
                    ON DELETE CASCADE,

                created_at TIMESTAMP DEFAULT NOW(),

                CONSTRAINT user_restaurants_unique
                    UNIQUE (user_id, restaurant_id)
            )
            """
        )

        print("✅ Таблица user_restaurants готова")

        await db.pool.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_user_restaurants_user
            ON user_restaurants(user_id)
            """
        )

        await db.pool.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_user_restaurants_restaurant
            ON user_restaurants(restaurant_id)
            """
        )

        print("✅ Индексы готовы")

        print("=" * 60)
        print("SETUP ЗАВЕРШЁН")
        print("=" * 60)

    finally:
        if db.pool:
            await db.pool.close()


if __name__ == "__main__":
    asyncio.run(main())