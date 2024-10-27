from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import app.gpt_assistant.keyboards as kb
from app.gpt_assistant.states import UserRequest
from app.gpt_assistant.user_requests import get_user_request
from database.gpt_requests import add_request

GPTAssistantCallbackRouter = Router()


@GPTAssistantCallbackRouter.callback_query(F.data.startswith('ask_gpt_assistant'))
async def create_request(callback: CallbackQuery, state: FSMContext) -> None:
    '''
    Starts a request state for user to send a request to GPT Assistant

    ask_gpt_assistant may contain an "without_deleting" parameter that makes bot to not delete the last message

    returns None
    '''
    await callback.answer('Задайте вопрос!')
    await callback.message.answer('Задайте вопрос нашему GPT Ассистенту')
    if not 'without_deleting' in callback.data:
        await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)
    await state.set_state(UserRequest.request_text)
    return


@GPTAssistantCallbackRouter.message(UserRequest.request_text)
async def push_request(message: Message, state: FSMContext) -> None:
    '''
    Handles and sends GPT Assistant's answer to user's request or error message

    returns None
    '''
    await state.update_data(request_text = message.text)
    data = await state.get_data()
    request_text = data["request_text"]
    msg_1 = await message.answer('Идет подготовка вашего ответа...')
    try:
        await message.bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
    except: pass
    response = await get_user_request(request_text=request_text)
    try:
        await message.answer(f'Вот ответ на ваш вопрос!\n\n{response}', reply_markup = kb.ask_again_or_menu)
    except: await message.answer('Произошла ошибка на сервере Yandex, попробуйте задать вопрос еще раз!', reply_markup = kb.ask_again_or_menu)
    await add_request(message = message)
    await message.bot.delete_message(chat_id = message.chat.id, message_id = msg_1.message_id)
    return