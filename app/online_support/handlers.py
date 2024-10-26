from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

import app.main_menu.keyboard as kb

OnlineSupportHandlersRouter = Router()


@OnlineSupportHandlersRouter.message(Command('start_conversation'))
async def conversation_start(message: Message) -> None:
    '''
    Starts a conversation state by using "/start-conversation"

    returns None
    '''
    await message.answer('Добро пожаловать в онлайн поддержку! Здесь вы можете запросить помощь у онлайн-администраторов', reply_markup = kb.help_by_admin)
    await message.bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
    return