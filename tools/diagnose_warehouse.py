import asyncio

from database.database import Database


async def main():

    db = Database()

    try:
        await db.connect()

        print("=" * 60)
        print("GlavRyba AI")
        print("WAREHOUSE DIAGNOSTICS")
        print("=" * 60)

        # =====================================================
        # RESTAURANTS
        # =====================================================

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

        print()
        print("RESTAURANTS")
        print("-" * 60)

        print(
            f"Количество ресторанов: {len(restaurants)}"
        )

        for restaurant in restaurants:
            print(dict(restaurant))

        # =====================================================
        # UNITS
        # =====================================================

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

        print()
        print("UNITS")
        print("-" * 60)

        print(
            f"Количество единиц: {len(units)}"
        )

        for unit in units:
            print(dict(unit))

        # =====================================================
        # WAREHOUSES
        # =====================================================

        warehouses = await db.pool.fetch(
            """
            SELECT
                id,
                name,
                description,
                restaurant_id,
                active
            FROM warehouses
            ORDER BY id
            """
        )

        print()
        print("WAREHOUSES")
        print("-" * 60)

        print(
            f"Количество складов: {len(warehouses)}"
        )

        for warehouse in warehouses:
            print(dict(warehouse))

        # =====================================================
        # COUNTS
        # =====================================================

        products_count = await db.pool.fetchval(
            """
            SELECT COUNT(*)
            FROM products
            """
        )

        stock_count = await db.pool.fetchval(
            """
            SELECT COUNT(*)
            FROM stock
            """
        )

        movements_count = await db.pool.fetchval(
            """
            SELECT COUNT(*)
            FROM stock_movements
            """
        )

        print()
        print("COUNTS")
        print("-" * 60)

        print(
            f"products         : {products_count}"
        )

        print(
            f"stock            : {stock_count}"
        )

        print(
            f"stock_movements  : {movements_count}"
        )

        print()
        print("=" * 60)
        print("DIAGNOSTICS COMPLETE")
        print("=" * 60)

    finally:

        if db.pool:
            await db.pool.close()


if __name__ == "__main__":
    asyncio.run(main())