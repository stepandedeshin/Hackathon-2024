from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

use_bot_while_waiting = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = '🏠 Вернуться в меню', callback_data = 'main_menu_without_deleting')]
])

auth_to_use_online_support = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = '📱 Привязать номер телефона', callback_data = 'auth')],
    [InlineKeyboardButton(text = '🏠 Вернуться в меню', callback_data = 'main_menu')],
])