from aiogram.fsm.state import State, StatesGroup


class AdminDoc(StatesGroup):
    admin_data = State()
    admin_faq = State()