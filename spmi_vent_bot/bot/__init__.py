from .bot import bot, dp

__all__ = [bot, dp]

from .handlers import routers
for router in routers:
    dp.include_router(router)