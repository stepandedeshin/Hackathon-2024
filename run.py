import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.admin.admin_callback import AdminPanelRouter
from app.gpt_assistant.callback_handlers import GPTAssistantCallbackRouter
from app.link_phone.callback_handlers import AuthCallbackRouter
from app.link_phone.handlers import AuthHandlersRouter
from app.main_menu.callback_handlers import MainMenuCallbackRouter
from app.main_menu.handlers import MainMenuHandlersRouter
from app.online_support.callback_handlers import OnlineSupportCallbackRouter
from app.online_support.handlers import OnlineSupportHandlersRouter
from config import settings
from database.gpt_requests import DatabaseGPTRequestsRouter
from database.help_request import DatabaseHelpRequestsRouter
from database.users import DatabaseUsersRouter


async def main() -> None:
    '''
    Starts dispatcher polling and includes API Routers
    '''
    bot = Bot(settings.TOKEN)
    dp = Dispatcher()
    dp.include_routers(AuthHandlersRouter, AuthCallbackRouter, MainMenuHandlersRouter, MainMenuCallbackRouter, OnlineSupportHandlersRouter, GPTAssistantCallbackRouter, DatabaseGPTRequestsRouter, DatabaseUsersRouter, DatabaseHelpRequestsRouter, AdminPanelRouter, OnlineSupportCallbackRouter)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot disabled')