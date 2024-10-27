from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


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


class PaginationFAQ(CallbackData, prefix = 'pag'):
    action: str
    page: int
    

def paginatorfaq(length_of_faq: int, page: int = 0) -> InlineKeyboardBuilder:
    '''
    Returns inline keyboard that used for pagination (the ability to select the page of all text)
    '''
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text = '⬅️', callback_data = PaginationFAQ(action = 'prev', page = page).pack()),
        InlineKeyboardButton(text = f'{page+1}/{length_of_faq}', callback_data = PaginationFAQ(action = 'page_number', page = page).pack()),
        InlineKeyboardButton(text = '➡️', callback_data = PaginationFAQ(action = 'next', page = page).pack()),
        width=3
    )
    builder.row(
        InlineKeyboardButton(text = '🏠 Вернуться в меню', callback_data = 'main_menu')
    )
    return builder.as_markup()