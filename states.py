from aiogram.fsm.state import State, StatesGroup


class FSMGameState(StatesGroup):
    menu = State()
    field = State()
