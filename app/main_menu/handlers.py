from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandObject, Command, CommandStart
from database.users import start_info, add_phone_number

import app.main_menu.keyboard as kb


MainMenuHandlersRouter = Router()


@MainMenuHandlersRouter.message(CommandStart())
async def start_message(message: Message) -> None:
    await start_info(message = message)
    await message.answer(f'Приветствуем, @{message.from_user.username}!\nДобро пожаловать в бота поддержки пользователей!', reply_markup = kb.start_message)
    await message.bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)


@MainMenuHandlersRouter.message(F.text == '🏠 Вернуться в меню')
async def start_message(message: Message) -> None:
    try:
        await message.bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
    except: pass
    await message.answer(f'Приветствуем, @{message.from_user.username}!\nДобро пожаловать в бота поддержки пользователей!', reply_markup = kb.start_message)
    await message.bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
