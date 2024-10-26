import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery
from config import settings

from app.main_menu.handlers import MainMenuHandlersRouter
from app.main_menu.callback_handlers import MainMenuCallbackRouter
from app.link_phone.handlers import AuthHandlersRouter
from app.link_phone.callback_handlers import AuthCallbackRouter
from app.online_support.callback_handlers import OnlineSupportCallbackRouter
from database.help_request import DatabaseHelpRequestsRouter
from database.users import DatabaseUsersRouter

async def main() -> None:
    bot = Bot(settings.TOKEN)
    dp = Dispatcher()
    dp.include_routers(MainMenuHandlersRouter, MainMenuCallbackRouter, AuthHandlersRouter, AuthCallbackRouter, DatabaseUsersRouter, DatabaseHelpRequestsRouter, OnlineSupportCallbackRouter)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot disabled')