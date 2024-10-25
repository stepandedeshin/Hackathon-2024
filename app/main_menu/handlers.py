from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandObject, Command, CommandStart
from database.users import start_info

import app.main_menu.keyboard as kb

MainMenuHandlersRouter = Router()

@MainMenuHandlersRouter.message(CommandStart())
async def start_message(message: Message) -> None:
    await start_info(message = message)
    await message.answer(f'Приветствуем @{message.from_user.username}\nДобро пожаловать в бота поддержки пользователей!')