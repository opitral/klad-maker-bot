import logging
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.exceptions import TelegramBadRequest

from handlers import router
from settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def notify_admins(bot: Bot, message: str):
    for admin_telegram_id in settings.ADMINS_TELEGRAM_ID:
        try:
            await bot.send_message(admin_telegram_id, message)

        except TelegramBadRequest:
            logging.warning(f"Failed to send message to admin {admin_telegram_id}")

        else:
            logger.info(f"Message successfully sent to admin {admin_telegram_id}")


async def main():
    dispatcher = Dispatcher()
    bot = Bot(token=settings.BOT_API_TOKEN.get_secret_value())

    async def on_startup():
        logger.info("Bot started")
        await notify_admins(bot, "Bot started")

    async def on_shutdown():
        logger.info("Bot stopped")
        await notify_admins(bot, "Bot stopped")

    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    dispatcher.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped by user")
