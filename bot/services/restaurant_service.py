from database.restaurants import RestaurantRepository


class RestaurantService:

    def __init__(self, db):
        self.repo = RestaurantRepository(db)

    async def get_restaurants(self):
        return await self.repo.get_all()

    async def create_restaurant(self, name):
        await self.repo.add(name)

    async def delete_restaurant(self, restaurant_id):
        await self.repo.delete(restaurant_id)