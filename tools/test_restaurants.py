import asyncio

from database.database import Database
from database.restaurants import RestaurantRepository


async def main():
    db = Database()

    try:
        await db.connect()

        repository = RestaurantRepository(db)

        restaurants = await repository.get_all()

        print("=" * 60)
        print("РЕСТОРАНЫ")
        print("=" * 60)

        for restaurant in restaurants:
            print(
                f"{restaurant['id']}. "
                f"{restaurant['name']} "
                f"[{'АКТИВЕН' if restaurant['active'] else 'НЕАКТИВЕН'}]"
            )

        print("=" * 60)
        print(f"Всего: {len(restaurants)}")

    finally:
        if db.pool:
            await db.pool.close()


if __name__ == "__main__":
    asyncio.run(main())