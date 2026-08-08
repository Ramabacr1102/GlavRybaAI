import asyncio

from database.database import Database


async def main():
    db = Database()

    try:
        await db.connect()

        print("=" * 60)
        print("GlavRyba AI — USERS & ROLES CHECK")
        print("=" * 60)

        for table_name in ("users", "roles"):
            print()
            print("=" * 60)
            print(f"ТАБЛИЦА: {table_name}")
            print("=" * 60)

            exists = await db.pool.fetchval(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                      AND table_name = $1
                )
                """,
                table_name,
            )

            if not exists:
                print(f"❌ Таблица {table_name} не существует")
                continue

            print(f"✅ Таблица {table_name} существует")
            print()
            print("КОЛОНКИ:")

            columns = await db.pool.fetch(
                """
                SELECT
                    ordinal_position,
                    column_name,
                    data_type,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = $1
                ORDER BY ordinal_position
                """,
                table_name,
            )

            for column in columns:
                print(
                    f"{column['ordinal_position']}. "
                    f"{column['column_name']} | "
                    f"{column['data_type']} | "
                    f"NULL={column['is_nullable']} | "
                    f"default={column['column_default']}"
                )

            count = await db.pool.fetchval(
                f"SELECT COUNT(*) FROM {table_name}"
            )

            print()
            print(f"Количество записей: {count}")

            rows = await db.pool.fetch(
                f"""
                SELECT *
                FROM {table_name}
                ORDER BY 1
                LIMIT 20
                """
            )

            if rows:
                print()
                print("ДАННЫЕ:")

                for row in rows:
                    print(dict(row))
            else:
                print("ℹ️ Записей пока нет")

        print()
        print("=" * 60)
        print("ПРОВЕРКА ЗАВЕРШЕНА")
        print("=" * 60)

    finally:
        if db.pool:
            await db.pool.close()


if __name__ == "__main__":
    asyncio.run(main())