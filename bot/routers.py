from aiogram import Router

from bot.handlers.start import router as start_router
from bot.callbacks.menu import router as menu_callback_router

from bot.admin.users import router as admin_users_router
from bot.admin.restaurants import router as admin_restaurants_router


router = Router()

router.include_router(start_router)
router.include_router(menu_callback_router)

router.include_router(admin_users_router)
router.include_router(admin_restaurants_router)