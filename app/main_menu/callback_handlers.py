import asyncio

from aiogram.exceptions import TelegramBadRequest
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from database.users import return_phone_number_or_none, delete_phone_number

import app.main_menu.keyboard as kb


MainMenuCallbackRouter = Router()


@MainMenuCallbackRouter.callback_query(F.data.startswith('main_menu'))
async def start_message(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer('Меню')
    await callback.message.answer(f'Приветствуем, @{callback.from_user.username}!\nДобро пожаловать в бота поддержки пользователей!', reply_markup = kb.start_message)
    if not 'without_deleting' in callback.data:
        await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)
    if 'without_deleting' in callback.data:
        await state.clear()
        

@MainMenuCallbackRouter.callback_query(F.data == 'gpt_assistant')
async def gpt_assistant_start(callback: CallbackQuery) -> None:
    await callback.answer('GPT Ассистент')
    phone_number = await return_phone_number_or_none(user_id=str(callback.from_user.id))
    if phone_number:
        await callback.message.answer('GPT Ассистент поможет вам найти ответ на ваш вопрос, опираясь на документацию', reply_markup = kb.gpt_assistant)
    else:
        await callback.message.answer('Вы не авторизованы! Чтобы использовать GPT Ассистента необходимо привязать свой номер телефона!', reply_markup = kb.auth_to_use_gpt)
    await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)


@MainMenuCallbackRouter.callback_query(F.data == 'faq')
async def show_faq(callback: CallbackQuery) -> None:
    await callback.answer('')
    faq_questions = open('faq.txt', 'r', encoding='utf-8').read()
    message_limit = 4096 
    parts = [faq_questions[i:i+message_limit] for i in range(0, len(faq_questions), message_limit)]
    for part in parts[0:-1:]:
        await callback.message.answer(part)
    await callback.message.answer(parts[-1], reply_markup=kb.show_faq)


@MainMenuCallbackRouter.callback_query(F.data == 'help_by_admin')
async def conversation_start(callback: CallbackQuery) -> None:
    await callback.answer('Онлайн поддержка')
    await callback.message.answer('Добро пожаловать в онлайн поддержку! Здесь вы можете запросить помощь у онлайн-администраторов', reply_markup = kb.help_by_admin)
    await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)


@MainMenuCallbackRouter.callback_query(F.data == 'auth')
async def auth_start(callback: CallbackQuery) -> None:
    await callback.answer('Авторизация')
    phone_number = await return_phone_number_or_none(user_id = str(callback.from_user.id))
    if not phone_number:
        await callback.message.answer('Привяжите номер телефона, чтобы пользоваться GPT Ассистентом!', reply_markup = kb.auth)
    else:
        await callback.message.answer(f'Привязанный вами номер телефона: +{phone_number}\nЗдесь вы можете его изменить или удалить', reply_markup = kb.auth_edit_or_delete)
    await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)
