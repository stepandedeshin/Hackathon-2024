from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

start_message = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = '🤖 GPT Ассистент', callback_data = 'gpt_assistant')],
    [InlineKeyboardButton(text = '📋 FAQ', callback_data = 'faq')],
    [InlineKeyboardButton(text = '🗣️ Онлайн поддержка', callback_data = 'help_by_admin')],
    [InlineKeyboardButton(text = '📱 Авторизация в боте', callback_data = 'auth')]
])


gpt_assistant = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = '🙋‍♂️ Задать вопрос', callback_data = 'ask_gpt_assistant')],
    [InlineKeyboardButton(text = '🏠 Вернуться в меню', callback_data = 'main_menu')],
])


show_faq = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = '🏠 Вернуться в меню', callback_data = f'main_menu_without_deleting')],
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

auth_to_use_online_support = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = '📱 Привязать номер телефона', callback_data = 'auth')],
    [InlineKeyboardButton(text = '🏠 Вернуться в меню', callback_data = 'main_menu')],
])


