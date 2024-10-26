from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

use_bot_while_waiting = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = '🏠 Вернуться в меню', callback_data = 'main_menu_without_deleting')]
])