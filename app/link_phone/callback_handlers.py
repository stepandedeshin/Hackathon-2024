import asyncio

from aiogram.exceptions import TelegramBadRequest
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import Filter
from database.users import return_phone_number_or_none, delete_phone_number

import app.link_phone.keyboard as kb


AuthCallbackRouter = Router()


@AuthCallbackRouter.callback_query(F.data == 'edit_phone_number_request')
async def edit_phone_number(callback: CallbackQuery) -> None:
    phone_number = await return_phone_number_or_none(user_id = str(callback.from_user.id))
    await callback.answer('Редактируйте свой номер телефона')
    await callback.message.answer(f'Привязанный вами номер телефона: +{phone_number}\nПоделитесь новым номером телефона!', reply_markup = kb.auth)
    await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)


@AuthCallbackRouter.callback_query(F.data == 'delete_phone_number_request')
async def auth_delete_request(callback: CallbackQuery) -> None:
    phone_number = await return_phone_number_or_none(user_id = str(callback.from_user.id))
    await callback.answer('Редактируйте свой номер телефона')
    await callback.message.answer(f'Привязанный вами номер телефона: +{phone_number}\nВы можете удалить его нажав на кнопку ниже, но больше не сможте использовать GPT Ассистента.\n\nВы в любой момент сможете привязать свой номер заново!', reply_markup = kb.auth_delete)
    await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)


@AuthCallbackRouter.callback_query(F.data == 'delete_phone')
async def auth_delete(callback: CallbackQuery):
    await delete_phone_number(user_id = str(callback.from_user.id))
    await callback.answer('Удаление номера телефона')
    await callback.message.answer('Ваш номер телефона отвязан! Вы в любой момент можете привязать его заново', reply_markup = kb.auth_delete_confirmed)
    await callback.message.bot.delete_message(chat_id = callback.message.chat.id, message_id = callback.message.message_id)