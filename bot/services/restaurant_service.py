from database.restaurants import RestaurantRepository


class RestaurantService:
    """
    Сервис управления ресторанами.
    """

    def __init__(self, db):
        self.repository = RestaurantRepository(db)

    async def get_all(self):
        """
        Получить все рестораны.
        """
        return await self.repository.get_all()

    async def get_active(self):
        """
        Получить только активные рестораны.
        """
        return await self.repository.get_active()

    async def get_by_id(self, restaurant_id: int):
        """
        Получить ресторан по ID.
        """
        return await self.repository.get_by_id(
            restaurant_id
        )

    async def add(self, name: str):
        """
        Добавить ресторан.
        """

        name = name.strip()

        if not name:
            raise ValueError(
                "Название ресторана не может быть пустым."
            )

        return await self.repository.add(name)

    async def update_name(
        self,
        restaurant_id: int,
        name: str,
    ):
        """
        Изменить название ресторана.
        """

        name = name.strip()

        if not name:
            raise ValueError(
                "Название ресторана не может быть пустым."
            )

        return await self.repository.update_name(
            restaurant_id,
            name,
        )

    async def activate(
        self,
        restaurant_id: int,
    ):
        """
        Активировать ресторан.
        """

        return await self.repository.set_active(
            restaurant_id,
            True,
        )

    async def deactivate(
        self,
        restaurant_id: int,
    ):
        """
        Деактивировать ресторан.
        """

        return await self.repository.set_active(
            restaurant_id,
            False,
        )