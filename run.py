import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery
from config import settings

from database.help_request import DatabaseHelpRequestsRouter
from database.users import DatabaseUsersRouter

async def main() -> None:
    bot = Bot(settings.TOKEN)
    dp = Dispatcher()
    dp.include_routers(DatabaseUsersRouter, DatabaseHelpRequestsRouter)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot disabled')