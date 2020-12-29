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

    ad_naming = State()  # name for ad
    agefrom = State()  # min age for ad
    ageto = State()  # max age for ad
    adcity = State()  # city for ad
    adcontact = State()  # contact for ad
    adabout = State()  # infos about ad
    ad_end = State()  # the /end of ad-creating
    ad_upd = State()  # update of ad

    # extra
    xad_naming = State()
    xagefrom = State()
    xageto = State()
    xadcity = State()
    xadcontact = State()
    xadabout = State()

    # extra 2 (upd/del in all_ads)
    ad_changing = State()
    xad_naming2 = State()
    xagefrom2 = State()
    xageto2 = State()
    xadcity2 = State()
    xadcontact2 = State()
    xadabout2 = State()