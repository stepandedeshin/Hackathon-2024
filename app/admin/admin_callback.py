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


from config import settings


class AdminProtect(Filter):
    def __init__(self):
        self.admins = settings.ADMINS

    async def __call__(self, message: Message):
        return message.chat.id in self.admins


