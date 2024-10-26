from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandObject, Command, CommandStart
from database.users import start_info, add_phone_number

import app.link_phone.keyboard as kb


AuthHandlersRouter = Router()


@AuthHandlersRouter.message(F.contact)
async def auth_by_phone(message: Message) -> None:
    await add_phone_number(message = message)
    try:
        await message.bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
    except: pass
    await message.answer(f'Спасибо за привязку номера телефона!\nВаш телефон: +{message.contact.phone_number}', reply_markup = kb.auth_edit_or_delete)
    await message.bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)