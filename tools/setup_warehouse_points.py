import asyncio

from database.database import Database


async def main():

    db = Database()

    try:
        await db.connect()

        print("=" * 60)
        print("GlavRyba AI")
        print("WAREHOUSE POINTS SETUP")
        print("=" * 60)

        restaurants = await db.pool.fetch(
            """
            SELECT
                id,
                name,
                active
            FROM restaurants
            ORDER BY id
            """
        )

        if not restaurants:
            print("❌ Рестораны не найдены.")
            return

        for restaurant in restaurants:

            warehouse_name = (
                f"Склад — {restaurant['name']}"
            )

            warehouse = await db.pool.fetchrow(
                """
                INSERT INTO warehouses (
                    name,
                    description,
                    restaurant_id,
                    active
                )
                VALUES (
                    $1,
                    $2,
                    $3,
                    $4
                )
                ON CONFLICT DO NOTHING
                RETURNING
                    id,
                    name,
                    restaurant_id,
                    active
                """,
                warehouse_name,
                (
                    f"Основной склад ресторана "
                    f"{restaurant['name']}"
                ),
                restaurant["id"],
                restaurant["active"],
            )

            if warehouse:

                print(
                    f"✅ Создан: "
                    f"{warehouse['name']}"
                )

            else:

                existing = await db.pool.fetchrow(
                    """
                    SELECT
                        id,
                        name
                    FROM warehouses
                    WHERE restaurant_id = $1
                    """,
                    restaurant["id"],
                )

                if existing:
                    print(
                        f"ℹ️ Уже существует: "
                        f"{existing['name']}"
                    )

        print("=" * 60)
        print("WAREHOUSE POINTS SETUP COMPLETE")
        print("=" * 60)

    finally:

        if db.pool:
            await db.pool.close()


if __name__ == "__main__":
    asyncio.run(main())