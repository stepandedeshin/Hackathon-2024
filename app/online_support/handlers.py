from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandObject, Command, CommandStart
from aiogram.fsm.context import FSMContext
from database.users import start_info, add_phone_number

import app.main_menu.keyboard as kb
from app.online_support.states import UserHelp


OnlineSupportHandlersRouter = Router()


@OnlineSupportHandlersRouter.message(Command('start_conversation'))
async def conversation_start(message: Message) -> None:
    await message.answer('Добро пожаловать в онлайн поддержку! Здесь вы можете запросить помощь у онлайн-администраторов', reply_markup = kb.help_by_admin)
    await message.bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)