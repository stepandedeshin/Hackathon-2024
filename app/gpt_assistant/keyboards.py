from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ask_again_or_menu = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = '🙋‍♂️ Спросить еще раз', callback_data = 'ask_gpt_assistant_without_deleting')],
    [InlineKeyboardButton(text = '🏠 Вернуться в меню', callback_data = 'main_menu_without_deleting')],
])