import asyncio

from aiogram.exceptions import TelegramBadRequest
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, Message, Voice
from aiogram.filters import Filter
from database.users import return_phone_number_or_none, delete_phone_number
from database.help_request import add_thread, return_user_by_thread_id, return_user_by_user_id
from database.gpt_requests import add_request
from aiogram.fsm.context import FSMContext

import app.gpt_assistant.keyboards as kb
from app.gpt_assistant.user_requests import get_user_request
from app.gpt_assistant.states import UserRequest


GPTAssistantCallbackRouter = Router()


@GPTAssistantCallbackRouter.callback_query(F.data.startswith('ask_gpt_assistant'))
async def create_request(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer('Задайте вопрос!')
    await callback.message.answer('Задайте вопрос нашему GPT Ассистенту')
    if not 'without_deleting' in callback.data:
        await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)
    await state.set_state(UserRequest.request_text)
    return

@GPTAssistantCallbackRouter.message(UserRequest.request_text)
async def push_request(message: Message, state: FSMContext) -> None:
    await state.update_data(request_text = message.text)
    data = await state.get_data()
    request_text = data["request_text"]
    msg_1 = await message.answer('Идет подготовка вашего ответа...')
    try:
        await message.bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
    except: pass
    response = await get_user_request(request_text=request_text)
    await message.answer(f'Вот ответ на ваш вопрос!\n\n{response}', reply_markup = kb.ask_again_or_menu)
    await add_request(message = message)
    await message.bot.delete_message(chat_id = message.chat.id, message_id = msg_1.message_id)
    return