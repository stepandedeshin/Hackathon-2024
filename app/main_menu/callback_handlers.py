import asyncio

from aiogram.exceptions import TelegramBadRequest
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import Filter
from database.users import return_phone_number_or_none, delete_phone_number

import app.main_menu.keyboard as kb


MainMenuCallbackRouter = Router()


@MainMenuCallbackRouter.callback_query(F.data == 'main_menu')
async def start_message(callback: CallbackQuery) -> None:
    await callback.answer('Меню')
    await callback.message.answer(f'Приветствуем, @{callback.from_user.username}!\nДобро пожаловать в бота поддержки пользователей!', reply_markup = kb.start_message)
    await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)


@MainMenuCallbackRouter.callback_query(F.data == 'gpt_assistant')
async def gpt_assistant_start(callback: CallbackQuery) -> None:
    await callback.answer('GPT Ассистент')
    await callback.message.answer('GPT', reply_markup = kb.gpt_assistant)
    await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)


@MainMenuCallbackRouter.callback_query(F.data == 'faq')
async def show_faq(callback: CallbackQuery) -> None:
    await callback.answer('Часто-задаваемые вопросы')
    await callback.message.answer('Часто-задаваемые вопросы', reply_markup = kb.show_faq)
    await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)


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
