import asyncio

from aiogram.exceptions import TelegramBadRequest
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, Message, Voice
from aiogram.filters import Filter, Command
from database.users import return_phone_number_or_none, delete_phone_number
from database.help_request import add_thread, return_user_by_thread_id, return_user_by_user_id
from database.gpt_requests import add_request
from aiogram.fsm.context import FSMContext

import app.gpt_assistant.keyboards as kb
from app.gpt_assistant.user_requests import get_user_request
from app.gpt_assistant.data_requests import get_data_request
from app.admin.states import AdminDoc


from config import settings


AdminPanelRouter = Router()


class AdminProtect(Filter):
    def __init__(self):
        self.admins = settings.ADMINS

    async def __call__(self, message: Message):
        return message.chat.id in self.admins


@AdminPanelRouter.message(AdminProtect(), Command('admin'))
async def admin_start(message: Message):
    await message.answer('Добро пожаловать в панель админа!\nСписок команд:\n/change_gpt_data - Принимает файл формата .txt и на основе этого текста формируется список возможных вопросов, которые будут функционировать в GPT Ассистенте\n/change_faq_data - Принимает файл формата .txt с вопросасм и ответами на ЧаВо, при нажатии на кнопку FAQ в меню бота текстом высланного сообщения будет текст файла')


@AdminPanelRouter.message(AdminProtect(), Command('change_gpt_data'))
async def change_gpt_data(message: Message, state: FSMContext):
    await state.set_state(AdminDoc.admin_doc)
    await message.answer('Отправьте файл формата .txt с названием "data.txt" для изменения')


@AdminPanelRouter.message(AdminDoc.admin_doc)
async def change_doc(message: Message, state: FSMContext):
    if message.document.mime_type == 'text/plain' and message.document.file_name == 'data.txt':
        file_id = message.document.file_id
        file = await message.bot.get_file(file_id = file_id)
        await message.bot.download_file(file.file_path, destination='data.txt')
        await message.answer('Файл принят, теперь GPT Ассистент формирует возможные вопросы на основе данного текста!...')
        datastring = await get_data_request(filename='data.txt')
        data_file = open('data.txt', 'w', encoding='utf-8')
        data_file.write('')
        data_file.write(datastring)
        await message.answer('Файл обработан! Теперь GPT Ассистент имеет новый список возможных вопросов')
        await state.clear()
    else:
        await message.answer('Сообщение не является документом формата txt или не называется data.txt! Отправьте файл еще раз или вернитесь в админ-меню')


@AdminPanelRouter.message(AdminProtect(), Command('change_faq_data'))
async def change_gpt_data(message: Message, state: FSMContext):
    await state.set_state(AdminDoc.admin_doc)
    await message.answer('Отправьте файл формата .txt с названием "faq.txt" для изменения')


@AdminPanelRouter.message(AdminDoc.admin_doc)
async def change_doc(message: Message, state: FSMContext):
    if message.document.mime_type == 'text/plain' and message.document.file_name == 'faq.txt':
        file_id = message.document.file_id
        file = await message.bot.get_file(file_id = file_id)
        await message.bot.download_file(file.file_path, destination='faq.txt')
        await message.answer('Файл принят, теперь данные FAQ будут показываться пользователю при запросе')
        await state.clear()
    else:
        await message.answer('Сообщение не является документом формата txt или не называется faq.txt! Отправьте файл еще раз или вернитесь в админ-меню')
    
    
