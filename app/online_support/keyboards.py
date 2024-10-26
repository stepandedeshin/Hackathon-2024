from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                            ReplyKeyboardMarkup, KeyboardButton)
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


use_bot_while_waiting = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = '🏠 Вернуться в меню', callback_data = 'main_menu_without_deleting')]
])