from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandObject, Command, CommandStart
from database.users import start_info, addreferal

import app.main_menu.keyboard as kb

HandlersRouter = Router()

