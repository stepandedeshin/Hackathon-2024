from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandObject, Command, CommandStart
from database.users import start_info, add_phone_number

import app.main_menu.keyboard as kb

