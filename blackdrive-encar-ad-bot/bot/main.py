import asyncio

from aiogram import Bot, Dispatcher

from bot.config import settings
from bot.handlers.encar_ad import router as encar_router
from bot.handlers.start import router as start_router
from bot.utils.logger import setup_logging


async def main() -> None:
    setup_logging()
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(encar_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
