from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

auth = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = '📲 Поделиться номером телефона', request_contact = True)],
    [KeyboardButton(text = '🏠 Вернуться в меню')],
], one_time_keyboard = True, resize_keyboard = True)

auth_edit_or_delete = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = '📱 Редактировать номер телефона', callback_data = 'edit_phone_number_request')],
    [InlineKeyboardButton(text = '🔗 Отвязать номер телефона', callback_data = 'delete_phone_number_request')],
    [InlineKeyboardButton(text = '🏠 Вернуться в меню', callback_data = 'main_menu')],
])

auth_delete = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = '🔧 Отвязать номер телефона', callback_data = 'delete_phone')],
    [InlineKeyboardButton(text = '🏠 Вернуться в меню', callback_data = 'main_menu')],
])

auth_delete_confirmed = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = '📱 Привязать номер телефона', callback_data = 'auth')],
    [InlineKeyboardButton(text = '🏠 Вернуться в меню', callback_data = 'main_menu')],
])