import asyncio

from database.database import Database


async def main():
    db = Database()

    try:
        await db.connect()

        print("=" * 60)
        print("ТАБЛИЦЫ POSTGRESQL")
        print("=" * 60)

        tables = await db.pool.fetch(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
            """
        )

        for table in tables:
            print(f"• {table['table_name']}")

        print("=" * 60)
        print("СТРУКТУРА restaurants")
        print("=" * 60)

        columns = await db.pool.fetch(
            """
            SELECT
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = 'restaurants'
            ORDER BY ordinal_position
            """
        )

        if not columns:
            print("❌ Таблица restaurants не найдена")
        else:
            for column in columns:
                print(
                    f"• {column['column_name']} | "
                    f"{column['data_type']} | "
                    f"NULL={column['is_nullable']} | "
                    f"default={column['column_default']}"
                )

        print("=" * 60)
        print("ДАННЫЕ restaurants")
        print("=" * 60)

        restaurants = await db.pool.fetch(
            """
            SELECT *
            FROM restaurants
            ORDER BY id
            """
        )

        if not restaurants:
            print("ℹ️ Таблица restaurants пока пустая")
        else:
            for restaurant in restaurants:
                print(dict(restaurant))

        print("=" * 60)

    finally:
        if db.pool:
            await db.pool.close()


if __name__ == "__main__":
    asyncio.run(main())