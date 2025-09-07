from aiogram import Router
#from .commands import router as cmd_routers
from .messages import router as messages_routers
from .secret import router as secret_routers

# Настройка экспорта и роутера
__all__ = ("router",)
router: Router = Router(name=__name__)

# Подключение роутеров
router.include_routers(
    #cmd_routers,
secret_routers,
    messages_routers,
)
