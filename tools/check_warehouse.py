import asyncio

from database.database import Database


TABLES = [
    "warehouses",
    "warehouse_categories",
    "units",
    "products",
    "stock",
    "stock_movements",
]


async def main():

    db = Database()

    try:
        await db.connect()

        print("=" * 60)
        print("GlavRyba AI")
        print("WAREHOUSE DATABASE CHECK")
        print("=" * 60)

        for table in TABLES:

            exists = await db.pool.fetchval(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = $1
                )
                """,
                table,
            )

            if exists:
                print(f"✅ {table}")
            else:
                print(f"❌ {table}")

        print("=" * 60)

        print("UNITS")
        print("=" * 60)

        units = await db.pool.fetch(
            """
            SELECT
                id,
                name,
                short_name,
                active
            FROM units
            ORDER BY id
            """
        )

        for unit in units:
            print(dict(unit))

        print("=" * 60)

        print("WAREHOUSES")
        print("=" * 60)

        warehouses = await db.pool.fetch(
            """
            SELECT
                id,
                name,
                restaurant_id,
                active
            FROM warehouses
            ORDER BY id
            """
        )

        if warehouses:
            for warehouse in warehouses:
                print(dict(warehouse))
        else:
            print("Складских точек пока нет.")

        print("=" * 60)
        print("WAREHOUSE DATABASE CHECK COMPLETE")
        print("=" * 60)

    finally:
        if db.pool:
            await db.pool.close()


if __name__ == "__main__":
    asyncio.run(main())