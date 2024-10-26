from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                            ReplyKeyboardMarkup, KeyboardButton)
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


start_message = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = '🤖 GPT Ассистент', callback_data = 'gpt_assistant')],
    [InlineKeyboardButton(text = '📋 FAQ', callback_data = 'faq')],
    [InlineKeyboardButton(text = '🗣️ Поддержка онлайн', callback_data = 'help_by_admin')],
    [InlineKeyboardButton(text = '📱 Авторизация в боте', callback_data = 'auth')]
])


gpt_assistant = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = '🏠 Вернуться в меню', callback_data = 'main_menu')],
])


show_faq = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = '🏠 Вернуться в меню', callback_data = 'main_menu')],
])


help_by_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = '🔎 Задать вопрос', callback_data = 'start_conversation')],
    [InlineKeyboardButton(text = '🏠 Вернуться в меню', callback_data = 'main_menu')],
])


auth = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = '📲 Поделиться номером телефона', request_contact = True)],
    [KeyboardButton(text = '🏠 Вернуться в меню')],
], one_time_keyboard = True, resize_keyboard = True)


auth_edit_or_delete = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = '📱 Редактировать номер телефона', callback_data = 'edit_phone_number_request')],
    [InlineKeyboardButton(text = '🔗 Отвязать номер телефона', callback_data = 'delete_phone_number_request')],
    [InlineKeyboardButton(text = '🏠 Вернуться в меню', callback_data = 'main_menu')],
])
