import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import settings

async def main() -> None:
    bot = Bot(settings.TOKEN)
    dp = Dispatcher()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot disabled')