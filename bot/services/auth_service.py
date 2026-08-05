from database.users import UserRepository


class AuthService:

    def __init__(self, db):
        self.users = UserRepository(db)

    async def register(self, telegram_user):

        await self.users.add_user(
            telegram_id=telegram_user.id,
            full_name=telegram_user.full_name,
            username=telegram_user.username or ""
        )

        return await self.users.get_user(
            telegram_user.id
        )