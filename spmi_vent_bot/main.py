import asyncio
from loguru import logger

from spmi_vent_bot.config import DEBUG


async def main():
    """
    Add logger, delete webhooks and start bot
    """
    logger.remove()
    logger.add("logs/{time:DD_MM_YYYY}.log", 
               level=f"{"DEBUG" if DEBUG else "INFO"}",
               rotation="12:00")
    logger.info("Старт скрипта")

    from spmi_vent_bot.bot import bot, dp
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Бот начал свою работу")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())