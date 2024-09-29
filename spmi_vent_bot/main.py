from .config import DEBUG
import asyncio

from loguru import logger


async def main():
    """
    Add logger, delete webhooks and start bot
    """
    from spmi_vent_bot.bot import bot, dp

    logger.remove()
    logger.add("logs/{time:DD_MM_YYYY}.log", 
               level=f"{"DEBUG" if DEBUG else "INFO"}",
               rotation="12:00")
    
    await bot.delete_webhook(drop_pending_updates=True)
        
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())