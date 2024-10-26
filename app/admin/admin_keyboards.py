from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

send_data_again = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Попробовать еще раз', callback_data='send_data_again')],
    [InlineKeyboardButton(text = 'Обратно к командам', callback_data='admin')],
])


send_faq_again = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Попробовать еще раз', callback_data='send_faq_again')],
    [InlineKeyboardButton(text = 'Обратно к командам', callback_data='admin')],
])


cancel_request = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Отмена', callback_data = 'admin')],
])