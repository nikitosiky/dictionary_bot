import asyncio
from config import TOKEN
from aiogram import Bot, Dispatcher
from handlers import settings, test, words
from handlers.settings import scheduler


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(settings.router)
    dp.include_router(words.router)
    dp.include_router(test.router)
    bot = Bot(token=TOKEN)
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
