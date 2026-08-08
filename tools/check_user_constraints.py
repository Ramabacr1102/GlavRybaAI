import asyncio

from database.database import Database


async def main():
    db = Database()

    try:
        await db.connect()

        print("=" * 60)
        print("USERS CONSTRAINTS")
        print("=" * 60)

        rows = await db.pool.fetch(
            """
            SELECT
                tc.constraint_name,
                tc.constraint_type,
                kcu.column_name
            FROM information_schema.table_constraints tc
            LEFT JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            WHERE tc.table_schema = 'public'
              AND tc.table_name = 'users'
            ORDER BY tc.constraint_name
            """
        )

        if not rows:
            print("Ограничений не найдено.")
        else:
            for row in rows:
                print(
                    f"{row['constraint_name']} | "
                    f"{row['constraint_type']} | "
                    f"{row['column_name']}"
                )

        print("=" * 60)

    finally:
        if db.pool:
            await db.pool.close()


if __name__ == "__main__":
    asyncio.run(main())