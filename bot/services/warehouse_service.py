from database.warehouse import WarehouseRepository


class WarehouseService:

    def __init__(self, db):
        self.warehouses = WarehouseRepository(db)

    async def get_all_warehouses(self):

        return await self.warehouses.get_all()

    async def get_warehouse(
        self,
        warehouse_id: int,
    ):

        return await self.warehouses.get_by_id(
            warehouse_id
        )