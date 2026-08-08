import asyncio

from database.database import Database


async def main():

    db = Database()

    try:
        await db.connect()

        await db.pool.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_warehouses_restaurant_unique
            ON warehouses(restaurant_id)
            """
        )

        print(
            "✅ Уникальность складов по ресторанам создана."
        )

    finally:

        if db.pool:
            await db.pool.close()


if __name__ == "__main__":
    asyncio.run(main())