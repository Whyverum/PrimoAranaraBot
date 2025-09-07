from typing import Any

from aiohttp import web
from aiogram.types import Update

from .bots import dp, bot
from middleware import loggers

class WebhookApp:
    """Приложение aiohttp для обработки webhook-запросов."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8080) -> None:
        self.host = host
        self.port = port
        self.app: web.Application = web.Application()
        self.app.router.add_post("/webhook", self.handle_update)
        self.runner: web.AppRunner | None = None
        self.site: web.TCPSite | None = None

    @staticmethod
    async def handle_update(request: web.Request) -> web.Response:
        """Обработчик входящих запросов от Telegram."""
        try:
            update_json: dict[str, Any] = await request.json()
            update: Update = Update.model_validate(update_json)
            await dp.feed_update(bot=bot, update=update)
        except Exception as e:
            print(f"Ошибка обработки webhook-запроса: {e}")
            return web.Response(status=500)

        return web.Response(status=200)

    async def start(self) -> None:
        """Асинхронный запуск aiohttp-приложения."""
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, self.host, self.port)
        await self.site.start()
        loggers.info(f"🌍 Webhook сервер запущен на http://{self.host}:{self.port}")

    async def stop(self) -> None:
        """Остановка aiohttp-приложения."""
        if self.runner:
            await self.runner.cleanup()
