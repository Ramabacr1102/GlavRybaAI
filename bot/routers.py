from aiogram import Router


# =========================================================
# START
# =========================================================

from bot.handlers.start import (
    router as start_router,
)


# =========================================================
# ADMIN — WAREHOUSE
# =========================================================

from bot.admin.warehouse import (
    router as warehouse_router,
)


# =========================================================
# MAIN MENU
# =========================================================

from bot.callbacks.menu import (
    router as menu_callback_router,
)


# =========================================================
# ADMIN — USERS
# =========================================================

from bot.admin.users import (
    router as admin_users_router,
)


# =========================================================
# MAIN ROUTER
# =========================================================

router = Router()


# START
router.include_router(
    start_router
)


# IMPORTANT:
# Warehouse must be registered BEFORE
# the old generic menu callbacks.
#
# Otherwise bot.callbacks.menu.py
# catches callback_data="warehouse"
# first.

router.include_router(
    warehouse_router
)


# MAIN MENU CALLBACKS
router.include_router(
    menu_callback_router
)


# ADMIN — USERS
router.include_router(
    admin_users_router
)