from aiogram.dispatcher.filters.state import State, StatesGroup


class Status(StatesGroup):
    A1 = State()  # neutral
    A2 = State()  # lang
    A3 = State()  # reg
    A4 = State()  # reg