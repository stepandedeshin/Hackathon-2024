from aiogram import F, Router
from aiogram.types import Message

import app.link_phone.keyboard as kb
from database.users import add_phone_number

AuthHandlersRouter = Router()


@AuthHandlersRouter.message(F.contact)
async def auth_by_phone(message: Message) -> None:
    '''
    Handles a message that requires specific type of message (Contact)
    Adds a phone number from shared contact to database

    returns None
    '''
    await add_phone_number(message = message)
    try:
        await message.bot.delete_messages(chat_id = message.chat.id, message_ids = [message.message_id - 1,  message.message_id - 2])
    except: pass
    await message.answer(f'Спасибо за привязку номера телефона!\nВаш телефон: {message.contact.phone_number}', reply_markup = kb.auth_edit_or_delete)
    await message.bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
    return