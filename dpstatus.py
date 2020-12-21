from aiogram.dispatcher.filters.state import State, StatesGroup


class Status(StatesGroup):
    name = State()  # cng_name
    chst = State()  # cng_status
    age = State()  # age reg
    age2 = State()  # cng_age
    city = State()  # cng_city
    about = State()  # cng_about
    cityA = State()  # city reg
    Profile = State()  # profile / reg

    A1 = State()  # neutral
    A2 = State()  # lang

    A3 = State()  # reg lang
    A4 = State()  # reg name
    A5 = State()  # reg status
    A6A = State()  # reg
    A6B = State()  # reg end 1
    A7 = State()  # reg end 0

    ad_naming = State()