from aiogram.dispatcher.filters.state import State, StatesGroup


class Status(StatesGroup):
    name = State()  # cng_name
    chst = State()  # cng_status
    age = State()  # age reg
    age2 = State()  # cng_age
    city = State()  # cng_city
    cityA = State()  # city reg
    A1 = State()  # neutral
    A2 = State()  # lang
    A3 = State()  # reg
    A4 = State()  # reg
    A5 = State()  # reg
    A6A = State()  # reg
    A6B = State()  # reg