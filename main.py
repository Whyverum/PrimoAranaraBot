import asyncio
import sys

from bot import dp, bot, BotInfo, WebhookApp, setup_middlewares, router
from configs.config import Webhook
from database import db
from middleware import setup_logging


async def on_startup() -> None:
    """Действия при запуске бота."""
    setup_logging()

    # Создание базы данных
    await db.init_db()
    if not await db.check_connection():
        print("Не удалось подключиться к БД!")
        return
    await db.init_default_roles()

    # Настройка информации о боте
    await BotInfo.setup(bots=bot)

    # Настройка middleware
    setup_middlewares(
        dp=dp,
        bot=bot,
        channel_ids=[],
    )

    # Подключение роутеров
    dp.include_router(router)
    BotInfo.start_info_out()


async def run_polling() -> None:
    """Запуск в режиме polling."""
    try:
        await on_startup()
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


async def run_webhook() -> None:
    """Запуск в режиме webhook."""
    app: WebhookApp = WebhookApp(host=Webhook.WEBHOOK_HOST, port=Webhook.WEBHOOK_PORT)
    try:
        await on_startup()
        await app.start()
        # держим процесс живым
        while True:
            await asyncio.sleep(3600)
    finally:
        await app.stop()
        await bot.session.close()


async def main() -> None:
    # Запуск в нужном режиме
    if Webhook.WEBHOOK:
        await run_webhook()
    else:
        await run_polling()


if __name__ == "__main__":
    # Защита для Windows
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("❌ Бот остановлен!")
        sys.exit(0)
