import asyncio

from database.database import Database


async def main():
    db = Database()

    try:
        await db.connect()

        print("=" * 60)
        print("GlavRyba AI")
        print("WAREHOUSE DATABASE SETUP")
        print("=" * 60)

        # =====================================================
        # СКЛАДСКИЕ ТОЧКИ
        # =====================================================

        await db.pool.execute(
            """
            CREATE TABLE IF NOT EXISTS warehouses (
                id SERIAL PRIMARY KEY,

                name TEXT NOT NULL,

                description TEXT,

                restaurant_id INTEGER
                    REFERENCES restaurants(id)
                    ON DELETE SET NULL,

                active BOOLEAN NOT NULL DEFAULT TRUE,

                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
            """
        )

        print("✅ warehouses")

        # =====================================================
        # КАТЕГОРИИ
        # =====================================================

        await db.pool.execute(
            """
            CREATE TABLE IF NOT EXISTS warehouse_categories (
                id SERIAL PRIMARY KEY,

                name TEXT NOT NULL UNIQUE,

                description TEXT,

                active BOOLEAN NOT NULL DEFAULT TRUE,

                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
            """
        )

        print("✅ warehouse_categories")

        # =====================================================
        # ЕДИНИЦЫ ИЗМЕРЕНИЯ
        # =====================================================

        await db.pool.execute(
            """
            CREATE TABLE IF NOT EXISTS units (
                id SERIAL PRIMARY KEY,

                name TEXT NOT NULL UNIQUE,

                short_name TEXT NOT NULL UNIQUE,

                active BOOLEAN NOT NULL DEFAULT TRUE,

                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
            """
        )

        print("✅ units")

        # =====================================================
        # НОМЕНКЛАТУРА
        # =====================================================

        await db.pool.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,

                name TEXT NOT NULL,

                category_id INTEGER
                    REFERENCES warehouse_categories(id)
                    ON DELETE SET NULL,

                unit_id INTEGER NOT NULL
                    REFERENCES units(id)
                    ON DELETE RESTRICT,

                description TEXT,

                barcode TEXT,

                article TEXT,

                min_stock NUMERIC(14, 3)
                    NOT NULL DEFAULT 0,

                active BOOLEAN NOT NULL DEFAULT TRUE,

                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
            """
        )

        print("✅ products")

        # =====================================================
        # ОСТАТКИ
        # =====================================================

        await db.pool.execute(
            """
            CREATE TABLE IF NOT EXISTS stock (
                id SERIAL PRIMARY KEY,

                warehouse_id INTEGER NOT NULL
                    REFERENCES warehouses(id)
                    ON DELETE CASCADE,

                product_id INTEGER NOT NULL
                    REFERENCES products(id)
                    ON DELETE CASCADE,

                quantity NUMERIC(14, 3)
                    NOT NULL DEFAULT 0,

                updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

                CONSTRAINT stock_unique
                    UNIQUE (
                        warehouse_id,
                        product_id
                    ),

                CONSTRAINT stock_quantity_check
                    CHECK (quantity >= 0)
            )
            """
        )

        print("✅ stock")

        # =====================================================
        # ДВИЖЕНИЯ
        # =====================================================

        await db.pool.execute(
            """
            CREATE TABLE IF NOT EXISTS stock_movements (
                id SERIAL PRIMARY KEY,

                warehouse_id INTEGER NOT NULL
                    REFERENCES warehouses(id)
                    ON DELETE RESTRICT,

                product_id INTEGER NOT NULL
                    REFERENCES products(id)
                    ON DELETE RESTRICT,

                movement_type TEXT NOT NULL,

                quantity NUMERIC(14, 3)
                    NOT NULL,

                unit_id INTEGER NOT NULL
                    REFERENCES units(id)
                    ON DELETE RESTRICT,

                related_warehouse_id INTEGER
                    REFERENCES warehouses(id)
                    ON DELETE RESTRICT,

                document_number TEXT,

                comment TEXT,

                created_by INTEGER
                    REFERENCES users(id)
                    ON DELETE SET NULL,

                created_at TIMESTAMP NOT NULL DEFAULT NOW(),

                CONSTRAINT movement_type_check
                    CHECK (
                        movement_type IN (
                            'receipt',
                            'transfer',
                            'writeoff',
                            'inventory'
                        )
                    ),

                CONSTRAINT movement_quantity_check
                    CHECK (quantity > 0)
            )
            """
        )

        print("✅ stock_movements")

        # =====================================================
        # ИНДЕКСЫ
        # =====================================================

        await db.pool.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_warehouses_restaurant
            ON warehouses(restaurant_id)
            """
        )

        await db.pool.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_products_category
            ON products(category_id)
            """
        )

        await db.pool.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_stock_warehouse
            ON stock(warehouse_id)
            """
        )

        await db.pool.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_stock_product
            ON stock(product_id)
            """
        )

        await db.pool.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_movements_warehouse
            ON stock_movements(warehouse_id)
            """
        )

        await db.pool.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_movements_product
            ON stock_movements(product_id)
            """
        )

        await db.pool.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_movements_created_at
            ON stock_movements(created_at)
            """
        )

        print("✅ Индексы")

        # =====================================================
        # БАЗОВЫЕ ЕДИНИЦЫ
        # =====================================================

        default_units = [
            ("Килограмм", "кг"),
            ("Грамм", "г"),
            ("Литр", "л"),
            ("Миллилитр", "мл"),
            ("Штука", "шт"),
            ("Упаковка", "уп"),
        ]

        for name, short_name in default_units:

            await db.pool.execute(
                """
                INSERT INTO units (
                    name,
                    short_name
                )
                VALUES ($1, $2)
                ON CONFLICT DO NOTHING
                """,
                name,
                short_name,
            )

        print("✅ Базовые единицы измерения")

        print("=" * 60)
        print("WAREHOUSE DATABASE SETUP COMPLETE")
        print("=" * 60)

    finally:
        if db.pool:
            await db.pool.close()


if __name__ == "__main__":
    asyncio.run(main())