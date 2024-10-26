from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class UserRequest(StatesGroup):
    request_text = State()