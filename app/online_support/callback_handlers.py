import asyncio

from aiogram.exceptions import TelegramBadRequest
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, Message
from aiogram.filters import Filter
from database.users import return_phone_number_or_none, delete_phone_number
from database.help_request import add_thread, return_user_by_thread_id, return_user_by_user_id
from aiogram.fsm.context import FSMContext

import app.online_support.keyboard as kb
from app.online_support.states import UserHelp


OnlineSupportCallbackRouter = Router()


@OnlineSupportCallbackRouter.callback_query(F.data == 'start_conversation')
async def start_conv(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)
    await state.set_state(UserHelp.user_message)
    await callback.message.answer('Отправьте ваш вопрос и администратор в скором времени на него ответит!')
    
    
@OnlineSupportCallbackRouter.message(UserHelp.user_message)
async def send_help(message: Message, state: FSMContext):
    await state.update_data(user_id = str(message.from_user.id))
    await state.update_data(first_message = str(message.from_user.id))
    await state.update_data(date = message.date)
    data = await state.get_data()
    try:
        thread_id = data["thread_id"]
        await message.bot.send_message(text = message.text, chat_id = '-1002437414181', message_thread_id = thread_id)
    except:
        topic = await message.bot.create_forum_topic(chat_id = '-1002437414181', name = f'{message.from_user.id} - {message.from_user.username}')
        await state.update_data(thread_id = topic.message_thread_id)
        data = await state.get_data()
        await add_thread(data = data)
        await message.bot.send_message(text = f'Новое обращение от пользователя @{message.from_user.username}\n\n{message.text}', chat_id = '-1002437414181', message_thread_id = topic.message_thread_id)
    await state.set_state(UserHelp.user_message)


@OnlineSupportCallbackRouter.message()
async def help_message(message: Message):
    pass