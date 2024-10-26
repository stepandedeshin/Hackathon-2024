from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class UserHelp(StatesGroup):
    user_id = State()
    thread_id = State()
    user_message = State()
    date = State()
