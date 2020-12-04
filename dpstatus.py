from aiogram.dispatcher.filters.state import State, StatesGroup


class Status(StatesGroup):
    name = State()  # cng_name
    chst = State()  # cng_status
    A1 = State()  # neutral
    A2 = State()  # lang
    A3 = State()  # reg
    A4 = State()  # reg
    A5 = State()  # reg