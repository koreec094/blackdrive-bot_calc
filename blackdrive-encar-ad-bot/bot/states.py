from aiogram.fsm.state import State, StatesGroup


class EncarAdStates(StatesGroup):
    waiting_for_url = State()
