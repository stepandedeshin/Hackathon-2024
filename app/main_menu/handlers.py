from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import app.main_menu.keyboard as kb
from database.users import start_info

MainMenuHandlersRouter = Router()


@MainMenuHandlersRouter.message(CommandStart())
async def start_message(message: Message) -> None:
    '''
    Handle "/start"

    adds an user data to database

    returns None
    '''
    await start_info(message = message)
    await message.answer_photo(photo = 'https://imgur.com/Uqf17Mh', caption = f'Приветствуем, @{message.from_user.username}!\nДобро пожаловать в бота поддержки пользователей!', reply_markup = kb.start_message)
    try:
        await message.bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
    except: pass
    return


@MainMenuHandlersRouter.message(F.text == '🏠 Вернуться в меню')
async def start_message(message: Message) -> None:
    '''
    Handle "🏠 Вернуться в меню" text
    
    get user back to main bot menu

    returns None
    '''
    try:
        await message.bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
    except: pass
    await message.answer_photo(photo = 'https://imgur.com/Uqf17Mh', caption = f'Приветствуем, @{message.from_user.username}!\nДобро пожаловать в бота поддержки пользователей!', reply_markup = kb.start_message)
    await message.bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
    return
