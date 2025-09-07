from aiogram import Router
from .secret1 import router as secret1_router
#from .secret2 import router as secret2_router

# Настройка экспорта и роутера
__all__ = ('router',)
router: Router = Router(name=__name__)

# Подключение секретного роутера
router.include_routers(
secret1_router,
#secret2_router,
)
