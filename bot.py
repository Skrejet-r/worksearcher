import config
import logging
import langtranslator as lt
import keyboards as kb
import time

from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, \
    KeyboardButton, \
    InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dpstatus import Status
from extradef import lang, stat
from sqldb import dbfuncs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

db = dbfuncs("db_ws.db")

ol = 0


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    if not (db.user_exists(message.from_user.id)):
        await message.answer("Welcome, " + message.from_user.first_name)
        # if user isnt in the db - add him
        db.add_user(message.from_user.id)
        source = "@" + str(message.from_user.username)
        db.upd_source(message.from_user.id, source)
        await Status.A3.set()
        time.sleep(1)
        await bot.send_message(message.from_user.id, "I see you are new here!\nSet language for yourself:",
                               reply_markup=kb.languages)
    else:
        await message.answer(lt.welcome[lang(message.from_user.id)])
        await Status.A1.set()
        source = "@" + str(message.from_user.username)
        db.upd_source(message.from_user.id, source)


@dp.message_handler(commands=["start"], state=Status.A1)
async def welcome(message: types.Message):
    FavB = KeyboardButton(lt.favb[lang(message.from_user.id)], callback_data="fav")
    SearchB = KeyboardButton(lt.searchb[lang(message.from_user.id)], callback_data="sea")
    SettB = KeyboardButton(lt.settb[lang(message.from_user.id)], callback_data="set")
    HelpB = KeyboardButton(lt.helpb[lang(message.from_user.id)], callback_data="hel")
    MyB = KeyboardButton(lt.myb[lang(message.from_user.id)], callback_data="my")
    AddB = KeyboardButton(lt.addb[lang(message.from_user.id)], callback_data="add")

    menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
        .row(SettB, HelpB)
    menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AddB) \
        .row(SettB, HelpB)

    mc = (menu0, menu1)

    await message.answer(lt.welcome[lang(message.from_user.id)],
                         reply_markup=mc[db.set_status(message.from_user.id)[0]])
    await Status.A1.set()
    source = "@" + str(message.from_user.username)
    db.upd_source(message.from_user.id, source)


@dp.message_handler(commands=["help"], state=Status.A1)
async def helper(message: types.Message):
    userstatus = db.set_status(message.from_user.id)[0]
    if userstatus == 0:
        await bot.send_message(message.from_user.id, lt.helping0[lang(message.from_user.id)])
    elif userstatus == 1:
        await bot.send_message(message.from_user.id, lt.helping1[lang(message.from_user.id)])
    else:
        await message.answer("Error")


@dp.message_handler(commands=["lang"], state=Status.A1)
async def lang_choose(message: types.Message):
    await Status.A2.set()
    await bot.send_message(message.from_user.id, "Choose the language:",
                           reply_markup=kb.languages)


@dp.message_handler(commands=["cng_city"], state=Status.A1)
async def regcity(message: types.Message):
    await message.answer(lt.citing1[lang(message.from_user.id)])
    await message.answer(lt.citingB2[lang(message.from_user.id)])
    await Status.city.set()


@dp.message_handler(commands=["cng_age"], state=Status.A1)
async def age_setter(message: types.Message):
    await message.answer(lt.aging1[lang(message.from_user.id)])
    await Status.age2.set()


@dp.message_handler(commands=["cng_name"], state=Status.A1)
async def regname(message: types.Message):
    await bot.send_message(message.from_user.id, lt.naming3[lang(message.from_user.id)] +
                           db.set_name(message.from_user.id)[0])
    await Status.name.set()
    await bot.send_message(message.from_user.id, lt.naming4[lang(message.from_user.id)])


@dp.message_handler(commands=["cng_status"], state=Status.A1)
async def chstatus(message: types.Message):
    await Status.chst.set()
    searcherbut = InlineKeyboardButton(str(lt.status1[lang(message.from_user.id)]), callback_data="0")
    offerbut = InlineKeyboardButton(str(lt.status2[lang(message.from_user.id)]), callback_data="1")

    statusin = InlineKeyboardMarkup().row(searcherbut, offerbut)

    await message.answer(lt.statuswahl2[lang(message.from_user.id)], reply_markup=statusin)


@dp.message_handler(commands=["cng_about"], state=Status.A1)
async def chabout(message: types.Message):
    if db.set_status(message.from_user.id)[0] == 0:
        await Status.about.set()
        await message.answer(lt.about1[lang(message.from_user.id)])
    else:
        await message.answer("?")


@dp.message_handler(commands=["profile"], state=Status.A1)
async def chprofil(message: types.Message):
    ud = message.from_user.id
    if db.set_status(message.from_user.id)[0] == 0:
        await message.answer(
            lt.pp[lang(ud)] + "\n\n" +
            lt.pname0[lang(ud)] + str(db.set_name(ud)[0]) + "\n" +
            lt.page0[lang(ud)] + str(db.set_age(ud)[0]) + "\n" +
            lt.pcity0[lang(ud)] + str(db.set_city(ud)[0]) + "\n" +
            lt.pabout0[lang(ud)] + str(db.set_about(ud)[0])
        )
    elif db.set_status(message.from_user.id)[0] == 1:
        await message.answer(
            lt.pp[lang(ud)] + "\n\n" +
            lt.pname0[lang(ud)] + str(db.set_name(ud)[0]) + "\n" +
            lt.pcity0[lang(ud)] + str(db.set_city(ud)[0]) + "\n"
        )
    else:
        await message.answer("?")


@dp.message_handler(commands=["delete_me"], state=Status.A1)
async def deleting(message: types.Message, state: FSMContext):
    await message.answer(lt.bye[lang(message.from_user.id)])
    await state.finish()
    db.delete(message.from_user.id)


@dp.message_handler(commands=["add_ad"], state=Status.A1)
async def ad_adder(message: types.Message):
    if db.set_status(message.from_user.id)[0] == 1:
        CancelB = InlineKeyboardButton(lt.cancelb[lang(message.from_user.id)], callback_data="-")
        mButton = InlineKeyboardMarkup().row(CancelB)

        if int(db.all_ads(message.from_user.id)[0]) >= 3:
            await message.answer(lt.pososi1[lang(message.from_user.id)])
        elif int(db.all_ads(message.from_user.id)[0]) < 0:
            await message.answer(lt.pososi2[lang(message.from_user.id)])
        else:
            if db.set_status(message.from_user.id)[0] == 1:
                await message.answer(lt.adform[lang(message.from_user.id)], reply_markup=mButton)
                time.sleep(1)
                await Status.ad_naming.set()
                await message.answer(lt.adname[lang(message.from_user.id)])

            else:
                await message.answer("?")
    else:
        await message.answer("?")


@dp.message_handler(commands=["my_ads"], state=Status.A1)
async def all_ads(message: types.Message):
    if db.set_status(message.from_user.id)[0] == 1:
        if True:
            u_id = message.from_user.id
            ad_id = db.nn(u_id)  # all ids of ads
            await message.answer(lt.n_ads[lang(u_id)] + str(len(ad_id)))
            for n in range(len(ad_id)):
                num = ad_id[n]  # only 1 certain id of certain ad

                title = db.set_ad_title2(u_id, num[0])[0]

                min_age = db.set_ad_minage2(u_id, num[0])[0]
                if min_age == 0:
                    min_age = ""

                max_age = db.set_ad_maxage2(u_id, num[0])[0]
                if max_age == 999999:
                    max_age = ""

                about = db.set_ad_about2(u_id, num[0])[0]

                city = db.set_ad_city2(u_id, num[0])[0]

                contact = db.set_ad_contact2(u_id, num[0])[0]

                ader = db.set_name(u_id)[0]

                nkb = n

                time.sleep(0.1)
                await bot.send_message(u_id,
                                       str(n + 1) + ".\n" +
                                       "(" + str(city) + ")" + str(title) + "\n" +
                                       lt.chageb[lang(u_id)] + ": " + str(min_age) + "-" + str(max_age) + "\n" +
                                       "-----------------------------------\n" +
                                       " " + str(about) + "\n" +
                                       "-----------------------------------\n" +
                                       "✉ " + str(contact) + " - " + str(ader),

                                       reply_markup=kb.adupd[nkb]
                                       )
            else:
                await bot.send_message(u_id, lt.aderror1[lang(u_id)])
    else:
        await message.answer("?")


@dp.message_handler(commands=["search"], state=Status.A1)
async def job_searching(message: types.Message):
    global ol
    u_id = message.from_user.id
    age = db.set_age(u_id)[0]
    city = db.set_city(u_id)[0]
    ids = db.getting_all_suitable_ads(city, age)
    num_ids = len(ids)
    if ol < num_ids:
        if db.set_status(u_id)[0] == 0:
            await Status.search.set()

            MenuB = KeyboardButton(lt.menub[lang(u_id)], callback_data="inmenu")
            NextB = KeyboardButton(lt.nextb[lang(u_id)], callback_data="next")

            searchkb = ReplyKeyboardMarkup(resize_keyboard=True).row(MenuB, NextB)

            await message.answer(lt.searching[lang(u_id)], reply_markup=searchkb)

            if num_ids == 0:
                await message.answer(lt.nocitieserror[lang(u_id)])
                await Status.A1.set()
            r_id = (ids[ol])[0]
            inf = db.ad(r_id)
            time.sleep(1)

            await message.answer("(" + str(inf[2]) + ") " + str(inf[0]) + "\n" +
                                 "-----------------------------------\n" +
                                 " " + str(inf[4]) + "\n" +
                                 "-----------------------------------\n" +
                                 "✉ " + str(inf[3]) + " - " + str(inf[1]) + "\n" +
                                 str(inf[7]),

                                 reply_markup=kb.adkb
                                 )
            await Status.search2.set()

        else:
            await message.answer("?")
    else:
        await message.answer("?")


@dp.message_handler(commands=["test"], state=Status.A1)
async def test(message: types.Message):
    await message.answer("@" + message.from_user.username)
    await message.answer(message.from_user.language_code)


@dp.message_handler(commands=["my_favs"], state=Status.A1)
async def my_favs(message: types.Message):
    u_id = message.from_user.id
    if db.set_status(message.from_user.id)[0] == 0:
        n = 0
        lfavs = db.get_favs(u_id)
        num = len(lfavs)
        await message.answer("⭐" + " (" + str(num) + ")")

        while n < num:
            r_id = (lfavs[n])[0]
            inf = db.ad(r_id)
            await message.answer("(" + str(inf[2]) + ") " + str(inf[0]) + "\n" +
                                 "-----------------------------------\n" +
                                 " " + str(inf[4]) + "\n" +
                                 "-----------------------------------\n" +
                                 "✉ " + str(inf[3]) + " - " + str(inf[1]) + "\n" +
                                 str(inf[7])

                                 )
            n += 1

    else:
        await message.answer("?")


@dp.message_handler(commands=["ad"], state=Status.A1)
async def ader(message: types.Message):
    u_id = message.from_user.id
    if u_id == 709987318 or u_id == 663017563:
        await message.answer("+")
        await message.answer("kopf")
        await Status.ad.set()


@dp.message_handler(state=Status.ad)
async def ader2(message: types.Message):
    ad_content = message.text
    db.add_myadkopf(ad_content)
    await Status.ad2.set()
    await message.answer("text")


@dp.message_handler(state=Status.ad2)
async def stfu(message: types.Message):
    content = message.text
    db.add_myadtext(content)
    await message.answer("nice")
    await Status.A1.set()


@dp.message_handler(commands=["startad"], state=Status.A1)
async def stfu(message: types.Message):
    u_id = message.from_user.id
    if u_id == 709987318 or u_id == 663017563:
        db.sav_ad()
        await message.answer("nice")


@dp.message_handler(commands=["stats"], state=Status.A1)
async def stfu(message: types.Message):
    u_id = message.from_user.id
    if u_id == 709987318 or u_id == 663017563:
        await message.answer("users: " + str(len(db.set_uid())))
        await message.answer("saw ad: " + str(len(db.sawadusers())))
        await message.answer("search: " + str(len(db.us0rs())) + "\n" + "offer: " + str(len(db.us1rs())))


@dp.message_handler(lambda message: message.text, state=Status.A1)
async def stfu(message: types.Message):
    if db.useradstatus(message.from_user.id)[0] == 1:
        ad = db.set_myad()
        await bot.send_message(message.from_user.id,
                               str(ad[0]) + "\n" +
                               str(ad[1]))
        db.upd_useradstatus(message.from_user.id, 0)


# +----------------------------------------------------
@dp.message_handler(lambda message: message.text in lt.helpb, state=Status.A1)
async def helper(message: types.Message):
    userstatus = db.set_status(message.from_user.id)[0]
    if userstatus == 0:
        await bot.send_message(message.from_user.id, lt.helping0[lang(message.from_user.id)])
    elif userstatus == 1:
        await bot.send_message(message.from_user.id, lt.helping1[lang(message.from_user.id)])
    else:
        await message.answer("Error")


@dp.message_handler(lambda message: message.text in lt.favb, state=Status.A1)
async def my_favs(message: types.Message):
    u_id = message.from_user.id
    if db.set_status(message.from_user.id)[0] == 0:
        n = 0
        lfavs = db.get_favs(u_id)
        num = len(lfavs)
        await message.answer("⭐" + " (" + str(num) + ")")

        while n < num:
            r_id = (lfavs[n])[0]
            inf = db.ad(r_id)
            await message.answer("(" + str(inf[2]) + ") " + str(inf[0]) + "\n" +
                                 "-----------------------------------\n" +
                                 " " + str(inf[4]) + "\n" +
                                 "-----------------------------------\n" +
                                 "✉ " + str(inf[3]) + " - " + str(inf[1]) + "\n" +
                                 str(inf[7])

                                 )
            n += 1

    else:
        await message.answer("?")


@dp.message_handler(lambda message: message.text in lt.chlangb, state=Status.A1)
async def lang_choose(message: types.Message):
    await Status.A2.set()
    await bot.send_message(message.from_user.id, "Choose the language:",
                           reply_markup=kb.languages)


@dp.message_handler(lambda message: message.text in lt.chnameb, state=Status.A1)
async def regname(message: types.Message):
    await bot.send_message(message.from_user.id, lt.naming3[lang(message.from_user.id)] +
                           db.set_name(message.from_user.id)[0])
    await Status.name.set()
    await bot.send_message(message.from_user.id, lt.naming4[lang(message.from_user.id)])


@dp.message_handler(lambda message: message.text in lt.chageb, state=Status.A1)
async def age_setter(message: types.Message):
    if db.set_status(message.from_user.id)[0] == 0:
        await message.answer(lt.aging1[lang(message.from_user.id)])
        await Status.age2.set()
    else:
        await message.answer("?")


@dp.message_handler(lambda message: message.text in lt.searchb, state=Status.A1)
async def job_searching(message: types.Message):
    if db.set_age(message.from_user.id) == "_":
        await message.answer(lt.noageerror[lang(message.from_user.id)])
    else:
        global ol
        u_id = message.from_user.id
        age = db.set_age(u_id)[0]
        city = db.set_city(u_id)[0]
        ids = db.getting_all_suitable_ads(city, age)
        num_ids = len(ids)
        if ol < num_ids:
            if db.set_status(u_id)[0] == 0:
                await Status.search.set()

                MenuB = KeyboardButton(lt.menub[lang(u_id)], callback_data="inmenu")
                NextB = KeyboardButton(lt.nextb[lang(u_id)], callback_data="next")

                searchkb = ReplyKeyboardMarkup(resize_keyboard=True).row(MenuB, NextB)

                await message.answer(lt.searching[lang(u_id)], reply_markup=searchkb)

                if num_ids == 0:
                    await message.answer(lt.nocitieserror[lang(u_id)])
                    await Status.A1.set()
                r_id = (ids[ol])[0]
                inf = db.ad(r_id)
                time.sleep(1)

                await message.answer("(" + str(inf[2]) + ") " + str(inf[0]) + "\n" +
                                     "-----------------------------------\n" +
                                     " " + str(inf[4]) + "\n" +
                                     "-----------------------------------\n" +
                                     "✉ " + str(inf[3]) + " - " + str(inf[1]) + "\n" +
                                     str(inf[7]),

                                     reply_markup=kb.adkb
                                     )
                await Status.search2.set()

            else:
                await message.answer("?")
        else:
            await message.answer(lt.nomorejobserror[lang(message.from_user.id)])
            if ol >= num_ids:
                ol -= ol


@dp.message_handler(lambda message: message.text in lt.chcityb, state=Status.A1)
async def regcity(message: types.Message):
    await message.answer(lt.citing1[lang(message.from_user.id)])
    await message.answer(lt.citingB2[lang(message.from_user.id)])
    await Status.city.set()


@dp.message_handler(lambda message: message.text in lt.profileb, state=Status.A1)
async def chprofil(message: types.Message):
    ud = message.from_user.id
    if db.set_status(message.from_user.id)[0] == 0:
        await message.answer(
            lt.pp[lang(ud)] + "\n\n" +
            lt.pname0[lang(ud)] + str(db.set_name(ud)[0]) + "\n" +
            lt.page0[lang(ud)] + str(db.set_age(ud)[0]) + "\n" +
            lt.pcity0[lang(ud)] + str(db.set_city(ud)[0]) + "\n" +
            lt.pabout0[lang(ud)] + str(db.set_about(ud)[0])
        )
    elif db.set_status(message.from_user.id)[0] == 1:
        await message.answer(
            lt.pp[lang(ud)] + "\n\n" +
            lt.pname0[lang(ud)] + str(db.set_name(ud)[0]) + "\n" +
            lt.pcity0[lang(ud)] + str(db.set_city(ud)[0]) + "\n"
        )
    else:
        await message.answer("?")


@dp.message_handler(lambda message: message.text in lt.chaboutb, state=Status.A1)
async def chabout(message: types.Message):
    if db.set_status(message.from_user.id)[0] == 0:
        await Status.about.set()
        await message.answer(lt.about1[lang(message.from_user.id)])
    else:
        await message.answer("?")


@dp.message_handler(lambda message: message.text in lt.addb, state=Status.A1)
async def ad_adder(message: types.Message):
    if db.set_status(message.from_user.id)[0] == 1:
        CancelB = InlineKeyboardButton(lt.cancelb[lang(message.from_user.id)], callback_data="-")
        mButton = InlineKeyboardMarkup().row(CancelB)

        if int(db.all_ads(message.from_user.id)[0]) >= 3:
            await message.answer(lt.pososi1[lang(message.from_user.id)])
        elif int(db.all_ads(message.from_user.id)[0]) < 0:
            await message.answer(lt.pososi2[lang(message.from_user.id)])
        else:
            if db.set_status(message.from_user.id)[0] == 1:
                await message.answer(lt.adform[lang(message.from_user.id)], reply_markup=mButton)
                time.sleep(1)
                await Status.ad_naming.set()
                await message.answer(lt.adname[lang(message.from_user.id)])

            else:
                await message.answer("?")
    else:
        await message.answer("?")


@dp.message_handler(lambda message: message.text in lt.chstatusb, state=Status.A1)
async def chstatus(message: types.Message):
    await Status.chst.set()
    searcherbut = InlineKeyboardButton(str(lt.status1[lang(message.from_user.id)]), callback_data="0")
    offerbut = InlineKeyboardButton(str(lt.status2[lang(message.from_user.id)]), callback_data="1")

    statusin = InlineKeyboardMarkup().row(searcherbut, offerbut)

    await message.answer(lt.statuswahl2[lang(message.from_user.id)], reply_markup=statusin)


@dp.message_handler(lambda message: message.text in lt.deleteb, state=Status.A1)
async def deleting(message: types.Message, state: FSMContext):
    await message.answer(lt.bye[lang(message.from_user.id)])
    await state.finish()
    db.delete(message.from_user.id)


@dp.message_handler(lambda message: message.text in lt.settb, state=Status.A1)
async def settings(message: types.Message):
    uid = message.from_user.id
    userstatus = db.set_status(uid)[0]

    LangB = KeyboardButton(lt.chlangb[lang(uid)], callback_data="lang")
    BackB = KeyboardButton(lt.backb[lang(uid)], callback_data="back")
    ProfileB = KeyboardButton(lt.profileb[lang(uid)], callback_data="prof")
    NameB = KeyboardButton(lt.chnameb[lang(uid)], callback_data="name")
    AgeB = KeyboardButton(lt.chageb[lang(uid)], callback_data="age")
    AboutB = KeyboardButton(lt.chaboutb[lang(uid)], callback_data="about")
    CityB = KeyboardButton(lt.chcityb[lang(uid)], callback_data="city")
    DelB = KeyboardButton(lt.deleteb[lang(uid)], callback_data="del")
    StatB = KeyboardButton(lt.chstatusb[lang(uid)], callback_data="stat")

    menu01 = ReplyKeyboardMarkup(resize_keyboard=True).row(BackB, ProfileB, LangB) \
        .row(NameB, AgeB, CityB) \
        .row(AboutB, StatB, DelB)

    menu11 = ReplyKeyboardMarkup(resize_keyboard=True).row(BackB, ProfileB, LangB) \
        .row(NameB, CityB, StatB) \
        .row(DelB)

    mc1 = (menu01, menu11)

    await message.answer("⚙", reply_markup=mc1[userstatus])


@dp.message_handler(lambda message: message.text in lt.backb or message.text in lt.menub, state=Status.A1)
async def backtomenu(message: types.Message):
    uid = message.from_user.id
    userstatus = db.set_status(uid)[0]

    FavB = KeyboardButton(lt.favb[lang(uid)], callback_data="fav")
    SearchB = KeyboardButton(lt.searchb[lang(uid)], callback_data="sea")
    SettB = KeyboardButton(lt.settb[lang(uid)], callback_data="set")
    HelpB = KeyboardButton(lt.helpb[lang(uid)], callback_data="hel")
    MyB = KeyboardButton(lt.myb[lang(uid)], callback_data="my")
    AddB = KeyboardButton(lt.addb[lang(uid)], callback_data="add")

    menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
        .row(SettB, HelpB)
    menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AddB) \
        .row(SettB, HelpB)

    mc = (menu0, menu1)

    await message.answer("⬅", reply_markup=mc[userstatus])


@dp.message_handler(lambda message: message.text in lt.menub, state=Status.search)
async def backtomenu(message: types.Message):
    uid = message.from_user.id
    userstatus = db.set_status(uid)[0]

    FavB = KeyboardButton(lt.favb[lang(uid)], callback_data="fav")
    SearchB = KeyboardButton(lt.searchb[lang(uid)], callback_data="sea")
    SettB = KeyboardButton(lt.settb[lang(uid)], callback_data="set")
    HelpB = KeyboardButton(lt.helpb[lang(uid)], callback_data="hel")
    MyB = KeyboardButton(lt.myb[lang(uid)], callback_data="my")
    AddB = KeyboardButton(lt.addb[lang(uid)], callback_data="add")

    menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
        .row(SettB, HelpB)
    menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AddB) \
        .row(SettB, HelpB)

    mc = (menu0, menu1)

    await message.answer("⬅", reply_markup=mc[userstatus])


@dp.message_handler(lambda message: message.text in lt.myb, state=Status.A1)
async def all_ads(message: types.Message):
    if db.set_status(message.from_user.id)[0] == 1:
        if True:
            u_id = message.from_user.id
            ad_id = db.nn(u_id)  # all ids of ads
            if int(len(ad_id)) == 0:
                await bot.send_message(u_id, lt.aderror1[lang(u_id)])
            else:
                await message.answer(lt.n_ads[lang(u_id)] + str(len(ad_id)))
                for n in range(len(ad_id)):
                    num = ad_id[n]  # only 1 certain id of certain ad

                    title = db.set_ad_title2(u_id, num[0])[0]

                    min_age = db.set_ad_minage2(u_id, num[0])[0]
                    if min_age == 0:
                        min_age = ""

                    max_age = db.set_ad_maxage2(u_id, num[0])[0]
                    if max_age == 999999:
                        max_age = ""

                    about = db.set_ad_about2(u_id, num[0])[0]

                    city = db.set_ad_city2(u_id, num[0])[0]

                    contact = db.set_ad_contact2(u_id, num[0])[0]

                    ader = db.set_name(u_id)[0]

                    nkb = n

                    time.sleep(0.1)
                    await bot.send_message(u_id,
                                           str(n + 1) + ".\n" +
                                           "(" + str(city) + ")" + str(title) + "\n" +
                                           lt.chageb[lang(u_id)] + ": " + str(min_age) + "-" + str(max_age) + "\n" +
                                           "-----------------------------------\n" +
                                           " " + str(about) + "\n" +
                                           "-----------------------------------\n" +
                                           "✉ " + str(contact) + " - " + str(ader),

                                           reply_markup=kb.adupd[nkb]
                                           )

    else:
        await message.answer("?")


# -------------------------------------------------------------------------------------------------


@dp.callback_query_handler(lambda call: True, state=Status.A2)
async def lan_set(call):
    u_id = call.from_user.id
    try:
        if call.message:
            if call.data == "eng":
                db.upd_lang(u_id, 0)

                FavB = KeyboardButton(lt.favb[lang(u_id)], callback_data="fav")
                SearchB = KeyboardButton(lt.searchb[lang(u_id)], callback_data="sea")
                SettB = KeyboardButton(lt.settb[lang(u_id)], callback_data="set")
                HelpB = KeyboardButton(lt.helpb[lang(u_id)], callback_data="hel")
                MyB = KeyboardButton(lt.myb[lang(u_id)], callback_data="my")
                AddB = KeyboardButton(lt.addb[lang(u_id)], callback_data="add")

                menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
                    .row(SettB, HelpB)
                menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AddB) \
                    .row(SettB, HelpB)

                mc = (menu0, menu1)

                await bot.send_message(call.message.chat.id, "English",
                                       reply_markup=mc[db.set_status(u_id)[0]])

            elif call.data == "rus":
                db.upd_lang(u_id, 1)

                FavB = KeyboardButton(lt.favb[lang(u_id)], callback_data="fav")
                SearchB = KeyboardButton(lt.searchb[lang(u_id)], callback_data="sea")
                SettB = KeyboardButton(lt.settb[lang(u_id)], callback_data="set")
                HelpB = KeyboardButton(lt.helpb[lang(u_id)], callback_data="hel")
                MyB = KeyboardButton(lt.myb[lang(u_id)], callback_data="my")
                AddB = KeyboardButton(lt.addb[lang(u_id)], callback_data="add")

                menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
                    .row(SettB, HelpB)
                menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AddB) \
                    .row(SettB, HelpB)

                mc = (menu0, menu1)

                await bot.send_message(call.message.chat.id, "Русский",
                                       reply_markup=mc[db.set_status(u_id)[0]])

            elif call.data == "de":
                db.upd_lang(u_id, 2)

                FavB = KeyboardButton(lt.favb[lang(u_id)], callback_data="fav")
                SearchB = KeyboardButton(lt.searchb[lang(u_id)], callback_data="sea")
                SettB = KeyboardButton(lt.settb[lang(u_id)], callback_data="set")
                HelpB = KeyboardButton(lt.helpb[lang(u_id)], callback_data="hel")
                MyB = KeyboardButton(lt.myb[lang(u_id)], callback_data="my")
                AddB = KeyboardButton(lt.addb[lang(u_id)], callback_data="add")

                menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
                    .row(SettB, HelpB)
                menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AddB) \
                    .row(SettB, HelpB)

                mc = (menu0, menu1)

                await bot.send_message(call.message.chat.id, "Deutsch",
                                       reply_markup=mc[db.set_status(u_id)[0]])

            elif call.data == "arb":
                db.upd_lang(u_id, 3)

                FavB = KeyboardButton(lt.favb[lang(u_id)], callback_data="fav")
                SearchB = KeyboardButton(lt.searchb[lang(u_id)], callback_data="sea")
                SettB = KeyboardButton(lt.settb[lang(u_id)], callback_data="set")
                HelpB = KeyboardButton(lt.helpb[lang(u_id)], callback_data="hel")
                MyB = KeyboardButton(lt.myb[lang(u_id)], callback_data="my")
                AddB = KeyboardButton(lt.addb[lang(u_id)], callback_data="add")

                menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
                    .row(SettB, HelpB)
                menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AddB) \
                    .row(SettB, HelpB)

                mc = (menu0, menu1)

                await bot.send_message(call.message.chat.id, "عربى",
                                       reply_markup=mc[db.set_status(u_id)[0]])

            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text="You chose:", reply_markup=None)
            await Status.A1.set()
    except Exception as e:
        print(repr(e))


@dp.callback_query_handler(lambda call: True, state=Status.A3)
async def lan_set(call):
    u_id = call.from_user.id
    try:
        if call.message:
            if call.data == "eng":
                db.upd_lang(u_id, 0)
                await bot.send_message(call.message.chat.id, "English")

            elif call.data == "rus":
                db.upd_lang(u_id, 1)
                await bot.send_message(call.message.chat.id, "Русский")

            elif call.data == "de":
                db.upd_lang(u_id, 2)
                await bot.send_message(call.message.chat.id, "Deutsch")

            elif call.data == "arb":
                db.upd_lang(u_id, 3)
                await bot.send_message(call.message.chat.id, "عربى")

            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text="You chose:", reply_markup=None)
            await Status.A4.set()
            time.sleep(1)
            await bot.send_message(u_id, lt.naming2[lang(call.from_user.id)])
    except Exception as e:
        print(repr(e))


@dp.message_handler(state=Status.A4)
async def regname(message: types.Message):
    name = message.text
    db.upd_name(message.from_user.id, name)
    time.sleep(0.1)
    await message.answer(str(lt.naming[lang(message.from_user.id)]) + " " +
                         str(db.set_name(message.from_user.id)[0]))

    # keyboard
    searcherbut = InlineKeyboardButton(str(lt.status1[lang(message.from_user.id)]), callback_data="0")
    offerbut = InlineKeyboardButton(str(lt.status2[lang(message.from_user.id)]), callback_data="1")

    statusin = InlineKeyboardMarkup().row(searcherbut, offerbut)

    time.sleep(1)
    await message.answer(lt.statuswahl[lang(message.from_user.id)], reply_markup=statusin)
    await Status.A5.set()


@dp.callback_query_handler(lambda call: True, state=Status.chst)
async def status_set(call):
    u_id = call.from_user.id

    FavB = KeyboardButton(lt.favb[lang(u_id)], callback_data="fav")
    SearchB = KeyboardButton(lt.searchb[lang(u_id)], callback_data="sea")
    SettB = KeyboardButton(lt.settb[lang(u_id)], callback_data="set")
    HelpB = KeyboardButton(lt.helpb[lang(u_id)], callback_data="hel")
    MyB = KeyboardButton(lt.myb[lang(u_id)], callback_data="my")
    AddB = KeyboardButton(lt.addb[lang(u_id)], callback_data="add")

    menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
        .row(SettB, HelpB)
    menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AddB) \
        .row(SettB, HelpB)

    mc = (menu0, menu1)
    try:
        if call.message:
            if call.data == "0":
                db.upd_status(call.from_user.id, 0)
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text=lt.s0[lang(call.from_user.id)], reply_markup=None)
                await bot.send_message(call.from_user.id, lt.avfunc0[lang(call.from_user.id)],
                                       reply_markup=mc[0])
                await bot.send_message(call.from_user.id, lt.noageerror[lang(call.from_user.id)])
            elif call.data == "1":
                db.upd_status(call.from_user.id, 1)
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text=lt.s1[lang(call.from_user.id)], reply_markup=None)
                await bot.send_message(call.from_user.id, lt.avfunc1[lang(call.from_user.id)],
                                       reply_markup=mc[1])
            await Status.A1.set()

    except Exception as e:
        print(repr(e))


@dp.message_handler(state=Status.name)
async def chname(message: types.Message):
    name = message.text
    db.upd_name(message.from_user.id, name)

    if db.set_status(message.from_user.id)[0] == 1:
        db.change_ader_all_ads(message.from_user.id, name)

    await Status.A1.set()
    await bot.send_message(message.from_user.id, lt.naming[lang(message.from_user.id)] +
                           db.set_name(message.from_user.id)[0])


@dp.callback_query_handler(lambda call: True, state=Status.A5)
async def status_set(call):
    try:
        if call.message:
            if call.data == "0":
                db.upd_status(call.from_user.id, 0)
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text=lt.s0[lang(call.from_user.id)], reply_markup=None)
                time.sleep(1)
                await bot.send_message(call.from_user.id, lt.aging1[lang(call.from_user.id)])
                await Status.age.set()

            elif call.data == "1":
                db.upd_status(call.from_user.id, 1)
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text=lt.s1[lang(call.from_user.id)], reply_markup=None)
                time.sleep(1)
                await bot.send_message(call.from_user.id, lt.citingB1[lang(call.from_user.id)])
                time.sleep(1)
                await bot.send_message(call.from_user.id, lt.citingB2[lang(call.from_user.id)])
                await Status.A6B.set()
    except Exception as e:
        print(repr(e))


@dp.message_handler(state=Status.age)
async def age_setter(message: types.Message):
    age = int(message.text)
    if age == int(age):
        db.upd_age(message.from_user.id, age)
    else:
        await message.answer(lt.aging2[lang(message.from_user.id)])
        db.upd_age(message.from_user.id, 0)
    await Status.cityA.set()
    await message.answer(lt.citingA1[lang(message.from_user.id)])
    time.sleep(1)
    await message.answer(lt.citingB2[lang(message.from_user.id)])


@dp.message_handler(state=Status.cityA)
async def city_setter(message: types.Message):
    city = message.text
    db.upd_city(message.from_user.id, city)
    await message.answer(lt.citing[lang(message.from_user.id)] + db.set_city(message.from_user.id)[0])
    time.sleep(1)
    await Status.A7.set()
    await message.answer(lt.about0[lang(message.from_user.id)])


@dp.message_handler(state=Status.A7)
async def regabout(message: types.Message):
    ud = message.from_user.id
    about = message.text
    db.upd_about(ud, about)
    await Status.A1.set()
    await message.answer(
        lt.pp[lang(ud)] + "\n\n" +
        lt.pname0[lang(ud)] + str(db.set_name(ud)[0]) + "\n" +
        lt.page0[lang(ud)] + str(db.set_age(ud)[0]) + "\n" +
        lt.pcity0[lang(ud)] + str(db.set_city(ud)[0]) + "\n" +
        lt.pabout0[lang(ud)] + str(db.set_about(ud)[0])
    )
    time.sleep(2)

    u_id = message.from_user.id

    FavB = KeyboardButton(lt.favb[lang(u_id)], callback_data="fav")
    SearchB = KeyboardButton(lt.searchb[lang(u_id)], callback_data="sea")
    SettB = KeyboardButton(lt.settb[lang(u_id)], callback_data="set")
    HelpB = KeyboardButton(lt.helpb[lang(u_id)], callback_data="hel")
    MyB = KeyboardButton(lt.myb[lang(u_id)], callback_data="my")
    AddB = KeyboardButton(lt.addb[lang(u_id)], callback_data="add")

    menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
        .row(SettB, HelpB)
    menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AddB) \
        .row(SettB, HelpB)

    mc = (menu0, menu1)

    await message.answer(lt.nice1[lang(ud)], reply_markup=mc[0])


@dp.message_handler(state=Status.age2)
async def age_setter(message: types.Message):
    age = int(message.text)
    if age == int(age):
        db.upd_age(message.from_user.id, age)
    else:
        await message.answer(lt.aging2[lang(message.from_user.id)])
        db.upd_age(message.from_user.id, 0)
    await Status.A1.set()
    await message.answer("👍")


@dp.message_handler(state=Status.A6B)
async def regcity(message: types.Message):
    city = message.text
    db.upd_city(message.from_user.id, city)
    await bot.send_message(message.from_user.id, lt.citing[lang(message.from_user.id)] +
                           db.set_city(message.from_user.id)[0])
    await Status.A1.set()
    time.sleep(1)

    u_id = message.from_user.id

    FavB = KeyboardButton(lt.favb[lang(u_id)], callback_data="fav")
    SearchB = KeyboardButton(lt.searchb[lang(u_id)], callback_data="sea")
    SettB = KeyboardButton(lt.settb[lang(u_id)], callback_data="set")
    HelpB = KeyboardButton(lt.helpb[lang(u_id)], callback_data="hel")
    MyB = KeyboardButton(lt.myb[lang(u_id)], callback_data="my")
    AddB = KeyboardButton(lt.addb[lang(u_id)], callback_data="add")

    menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
        .row(SettB, HelpB)
    menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AddB) \
        .row(SettB, HelpB)

    mc = (menu0, menu1)

    await bot.send_message(message.from_user.id, lt.nice2[lang(message.from_user.id)],
                           reply_markup=mc[1])


@dp.message_handler(state=Status.city)
async def city_setter(message: types.Message):
    city = message.text
    db.upd_city(message.from_user.id, city)
    await message.answer(lt.citing[lang(message.from_user.id)] + db.set_city(message.from_user.id)[0])
    await Status.A1.set()


@dp.message_handler(state=Status.about)
async def about_setter(message: types.Message):
    about = message.text
    db.upd_about(message.from_user.id, about)
    await Status.A1.set()
    await message.answer("👍")


# --------------------------------------------------------------------------------------------------------
@dp.message_handler(state=Status.ad_naming)
async def ad_namer(message: types.Message):
    xButton = InlineKeyboardButton(lt.xButton2[lang(message.from_user.id)], callback_data="-")
    mButton = InlineKeyboardMarkup().row(xButton)

    adname = message.text

    db.add_ad(message.from_user.id, adname, db.set_city(message.from_user.id)[0])
    db.ad_admin(message.from_user.id, db.set_name(message.from_user.id)[0])
    await Status.agefrom.set()
    await message.answer(lt.minage[lang(message.from_user.id)], reply_markup=mButton)


@dp.message_handler(state=Status.agefrom)
async def agefrom(message: types.Message):
    xButton = InlineKeyboardButton(lt.xButton2[lang(message.from_user.id)], callback_data="-")
    mButton = InlineKeyboardMarkup().row(xButton)

    minage = int(message.text)

    db.upd_ad_minage(message.from_user.id, minage)
    await Status.ageto.set()
    await message.answer(lt.maxage[lang(message.from_user.id)], reply_markup=mButton)


@dp.message_handler(state=Status.ageto)
async def agefrom(message: types.Message):
    maxage = int(message.text)
    db.upd_ad_maxage(message.from_user.id, maxage)
    await Status.adabout.set()
    await message.answer(lt.adabout[lang(message.from_user.id)])


@dp.message_handler(state=Status.adabout)
async def adabout(message: types.Message):
    about = str(message.text)
    db.upd_ad_about(message.from_user.id, about)
    await Status.adcontact.set()

    xButton = InlineKeyboardButton(lt.xButton1[lang(message.from_user.id)], callback_data="-")
    mButton = InlineKeyboardMarkup().row(xButton)

    await message.answer(lt.adcontact[lang(message.from_user.id)], reply_markup=mButton)


@dp.message_handler(state=Status.adcontact)
async def adcontact(message: types.Message):
    contact = message.text
    db.upd_ad_contact(message.from_user.id, contact)
    await Status.ad_end.set()
    u_id = message.from_user.id
    if (db.set_ad_minage(u_id)[0], db.set_ad_maxage(u_id)[0]) == (0, 999999):
        await bot.send_message(u_id,
                               lt.ad[lang(u_id)] + "\n\n" +
                               str(db.set_ad_title(u_id)[0]) + "\n" +

                               lt.chageb[lang(u_id)] + ": " + " - " + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_about(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_contact(u_id)[0]),

                               reply_markup=kb.adset
                               )

    else:
        await bot.send_message(u_id,
                               lt.ad[lang(u_id)] + "\n\n" +
                               str(db.set_ad_title(u_id)[0]) + "\n" +

                               lt.chageb[lang(u_id)] + ": " + str(db.set_ad_minage(u_id)[0]) + " - "
                               + str(db.set_ad_maxage(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_about(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_contact(u_id)[0]),

                               reply_markup=kb.adset
                               )


@dp.callback_query_handler(lambda call: True, state=Status.ad_end)
async def ad_setting(call):
    u_id = call.from_user.id

    try:
        if call.message:
            if call.data == "del":
                db.ad_delete(u_id)
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text=lt.ad_deleting[lang(u_id)], reply_markup=None)
                await Status.A1.set()

            elif call.data == "upd":

                await Status.ad_upd.set()

                B1 = InlineKeyboardButton(lt.b1[lang(u_id)], callback_data="b1")
                B2 = InlineKeyboardButton(lt.b2[lang(u_id)], callback_data="b2")
                B3 = InlineKeyboardButton(lt.b3[lang(u_id)], callback_data="b3")
                B4 = InlineKeyboardButton(lt.b4[lang(u_id)], callback_data="b4")
                B5 = InlineKeyboardButton(lt.b5[lang(u_id)], callback_data="b5")
                CancelB = InlineKeyboardButton(lt.cancelb[lang(u_id)], callback_data="-")

                Changes_ad = InlineKeyboardMarkup().add(B1).add(B2).add(B3).add(B4).add(B5).add(CancelB)

                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text=lt.ch[lang(u_id)], reply_markup=None)

                time.sleep(0.1)

                if (db.set_ad_minage(u_id)[0], db.set_ad_maxage(u_id)[0]) == (0, 999999):
                    await bot.send_message(u_id,
                                           str(db.set_ad_title(u_id)[0]) + "\n" +

                                           lt.chageb[lang(u_id)] + ": " + " - " + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_about(u_id)[0]) + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_contact(u_id)[0]),

                                           reply_markup=Changes_ad
                                           )

                else:
                    await bot.send_message(u_id,
                                           str(db.set_ad_title(u_id)[0]) + "\n" +

                                           lt.chageb[lang(u_id)] + ": " + str(db.set_ad_minage(u_id)[0]) + " - "
                                           + str(db.set_ad_maxage(u_id)[0]) + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_about(u_id)[0]) + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_contact(u_id)[0]),

                                           reply_markup=Changes_ad
                                           )

            elif call.data == "sav":
                db.plus_ad(u_id)
                db.num_ad(u_id)
                db.ad_saving(u_id)
                await Status.A1.set()
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text=lt.ad_saving[lang(u_id)], reply_markup=None)
                time.sleep(0.5)
                await bot.send_message(u_id, lt.ad_saving2[lang(u_id)], parse_mode="Markdown")

    except Exception as e:
        print(repr(e))


@dp.callback_query_handler(lambda call: True, state=Status.adcontact)
async def ad_setting(call):
    u_id = call.from_user.id

    try:
        if call.message:
            if call.data == "-":
                db.upd_ad_contact(u_id, "-")
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="-", reply_markup=None)

                await Status.ad_end.set()
                if (db.set_ad_minage(u_id)[0], db.set_ad_maxage(u_id)[0]) == (0, 999999):
                    await bot.send_message(u_id,
                                           lt.ad[lang(u_id)] + "\n\n" +
                                           str(db.set_ad_title(u_id)[0]) + "\n" +

                                           lt.chageb[lang(u_id)] + ": " + " - " + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_about(u_id)[0]) + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_contact(u_id)[0]),

                                           reply_markup=kb.adset
                                           )

                else:
                    await bot.send_message(u_id,
                                           lt.ad[lang(u_id)] + "\n\n" +
                                           str(db.set_ad_title(u_id)[0]) + "\n" +

                                           lt.chageb[lang(u_id)] + ": " + str(db.set_ad_minage(u_id)[0]) + " - "
                                           + str(db.set_ad_maxage(u_id)[0]) + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_about(u_id)[0]) + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_contact(u_id)[0]),

                                           reply_markup=kb.adset
                                           )

    except Exception as e:
        print(repr(e))


@dp.callback_query_handler(lambda call: True, state=Status.agefrom)
async def ad_setting(call):
    u_id = call.from_user.id

    xButton = InlineKeyboardButton(lt.xButton2[lang(u_id)], callback_data="-")
    mButton = InlineKeyboardMarkup().row(xButton)

    try:
        if call.message:
            if call.data == "-":
                db.xbutton1(u_id)
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="-", reply_markup=None)
                await Status.ageto.set()
                await bot.send_message(u_id, lt.maxage[lang(u_id)], reply_markup=mButton)

    except Exception as e:
        print(repr(e))


@dp.callback_query_handler(lambda call: True, state=Status.ageto)
async def ad_setting(call):
    u_id = call.from_user.id

    try:
        if call.message:
            if call.data == "-":
                db.xbutton2(u_id)
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="-", reply_markup=None)
                await Status.adabout.set()
                await bot.send_message(u_id, lt.adabout[lang(u_id)])

    except Exception as e:
        print(repr(e))


@dp.callback_query_handler(lambda call: True, state=Status.ad_upd)
async def ad_updating(call):
    u_id = call.from_user.id
    try:
        if call.message:
            if call.data == "b1":
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="🔄", reply_markup=None)
                await Status.xad_naming.set()
                await bot.send_message(u_id, lt.adname[lang(u_id)])

            elif call.data == "b2":
                xButton = InlineKeyboardButton(lt.xButton2[lang(u_id)], callback_data="-")
                mButton = InlineKeyboardMarkup().row(xButton)

                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="🔄", reply_markup=None)

                await Status.xagefrom.set()
                await bot.send_message(u_id, lt.minage[lang(u_id)], reply_markup=mButton)

            elif call.data == "b3":
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="🔄", reply_markup=None)
                await Status.xadabout.set()
                await bot.send_message(u_id, lt.adabout[lang(u_id)])

            elif call.data == "b4":
                xButton = InlineKeyboardButton(lt.xButton1[lang(call.from_user.id)], callback_data="-")
                mButton = InlineKeyboardMarkup().row(xButton)

                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="🔄", reply_markup=None)
                await bot.send_message(u_id, lt.xad_contact[lang(u_id)], reply_markup=mButton)
                await Status.xadcontact.set()

            elif call.data == "b5":
                xButton = InlineKeyboardButton(lt.xButton1[lang(call.from_user.id)], callback_data="-")
                mButton = InlineKeyboardMarkup().row(xButton)

                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="🔄", reply_markup=None)
                await bot.send_message(u_id, lt.citing1[lang(u_id)], reply_markup=mButton)
                await Status.xadcity.set()

            elif call.data == "-":
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="👍", reply_markup=None)

                await Status.ad_end.set()
                if (db.set_ad_minage(u_id)[0], db.set_ad_maxage(u_id)[0]) == (0, 999999):
                    await bot.send_message(u_id,
                                           lt.ad[lang(u_id)] + "\n\n" +
                                           str(db.set_ad_title(u_id)[0]) + "\n" +

                                           lt.chageb[lang(u_id)] + ": " + " - " + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_about(u_id)[0]) + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_contact(u_id)[0]),

                                           reply_markup=kb.adset
                                           )

                else:
                    await bot.send_message(u_id,
                                           lt.ad[lang(u_id)] + "\n\n" +
                                           str(db.set_ad_title(u_id)[0]) + "\n" +

                                           lt.chageb[lang(u_id)] + ": " + str(db.set_ad_minage(u_id)[0]) + " - "
                                           + str(db.set_ad_maxage(u_id)[0]) + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_about(u_id)[0]) + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_contact(u_id)[0]),

                                           reply_markup=kb.adset
                                           )

    except Exception as e:
        print(repr(e))


@dp.callback_query_handler(lambda call: True, state=Status.ad_naming)
async def ad_setting(call):
    u_id = call.from_user.id

    try:
        if call.message:
            if call.data == "-":
                await Status.A1.set()
                await bot.send_message(u_id, lt.canceled[lang(u_id)])
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="👍", reply_markup=None)

    except Exception as e:
        print(repr(e))


@dp.message_handler(state=Status.xad_naming)
async def ad_namer(message: types.Message):
    u_id = message.from_user.id

    adname = message.text
    db.upd_ad_title(u_id, adname)

    await Status.ad_end.set()
    if (db.set_ad_minage(u_id)[0], db.set_ad_maxage(u_id)[0]) == (0, 999999):
        await bot.send_message(u_id,
                               lt.ad[lang(u_id)] + "\n\n" +
                               str(db.set_ad_title(u_id)[0]) + "\n" +

                               lt.chageb[lang(u_id)] + ": " + " - " + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_about(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_contact(u_id)[0]),

                               reply_markup=kb.adset
                               )

    else:
        await bot.send_message(u_id,
                               lt.ad[lang(u_id)] + "\n\n" +
                               str(db.set_ad_title(u_id)[0]) + "\n" +

                               lt.chageb[lang(u_id)] + ": " + str(db.set_ad_minage(u_id)[0]) + " - "
                               + str(db.set_ad_maxage(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_about(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_contact(u_id)[0]),

                               reply_markup=kb.adset
                               )


@dp.message_handler(state=Status.xagefrom)
async def agefrom(message: types.Message):
    xButton = InlineKeyboardButton(lt.xButton2[lang(message.from_user.id)], callback_data="-")
    mButton = InlineKeyboardMarkup().row(xButton)

    minage = int(message.text)

    db.upd_ad_minage(message.from_user.id, minage)
    await Status.xageto.set()
    await message.answer(lt.maxage[lang(message.from_user.id)], reply_markup=mButton)


@dp.callback_query_handler(lambda call: True, state=Status.xagefrom)
async def agefrom(call):
    u_id = call.from_user.id

    xButton = InlineKeyboardButton(lt.xButton2[lang(u_id)], callback_data="-")
    mButton = InlineKeyboardMarkup().row(xButton)

    try:
        if call.message:
            if call.data == "-":
                db.xbutton1(u_id)
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="-", reply_markup=None)
                await Status.xageto.set()
                await bot.send_message(u_id, lt.maxage[lang(u_id)], reply_markup=mButton)

    except Exception as e:
        print(repr(e))


@dp.message_handler(state=Status.xagefrom)
async def agefrom(message: types.Message):
    xButton = InlineKeyboardButton(lt.xButton2[lang(message.from_user.id)], callback_data="-")
    mButton = InlineKeyboardMarkup().row(xButton)

    minage = int(message.text)

    db.upd_ad_minage(message.from_user.id, minage)
    await Status.xageto.set()
    await message.answer(lt.maxage[lang(message.from_user.id)], reply_markup=mButton)


@dp.callback_query_handler(lambda call: True, state=Status.xageto)
async def ageto(call):
    u_id = call.from_user.id

    try:
        if call.message:
            if call.data == "-":
                db.xbutton2(u_id)
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="-", reply_markup=None)

                await Status.ad_end.set()

                if (db.set_ad_minage(u_id)[0], db.set_ad_maxage(u_id)[0]) == (0, 999999):
                    await bot.send_message(u_id,
                                           lt.ad[lang(u_id)] + "\n\n" +
                                           str(db.set_ad_title(u_id)[0]) + "\n" +

                                           lt.chageb[lang(u_id)] + ": " + " - " + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_about(u_id)[0]) + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_contact(u_id)[0]),

                                           reply_markup=kb.adset
                                           )

                else:
                    await bot.send_message(u_id,
                                           lt.ad[lang(u_id)] + "\n\n" +
                                           str(db.set_ad_title(u_id)[0]) + "\n" +

                                           lt.chageb[lang(u_id)] + ": " + str(db.set_ad_minage(u_id)[0]) + " - "
                                           + str(db.set_ad_maxage(u_id)[0]) + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_about(u_id)[0]) + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_contact(u_id)[0]),

                                           reply_markup=kb.adset
                                           )
    except Exception as e:
        print(repr(e))


@dp.message_handler(state=Status.xageto)
async def ageto(message: types.Message):
    u_id = message.from_user.id
    maxage = int(message.text)
    db.upd_ad_maxage(message.from_user.id, maxage)

    await Status.ad_end.set()

    if (db.set_ad_minage(u_id)[0], db.set_ad_maxage(u_id)[0]) == (0, 999999):
        await bot.send_message(u_id,
                               lt.ad[lang(u_id)] + "\n\n" +
                               str(db.set_ad_title(u_id)[0]) + "\n" +

                               lt.chageb[lang(u_id)] + ": " + " - " + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_about(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_contact(u_id)[0]),

                               reply_markup=kb.adset
                               )

    else:
        await bot.send_message(u_id,
                               lt.ad[lang(u_id)] + "\n\n" +
                               str(db.set_ad_title(u_id)[0]) + "\n" +

                               lt.chageb[lang(u_id)] + ": " + str(db.set_ad_minage(u_id)[0]) + " - "
                               + str(db.set_ad_maxage(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_about(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_contact(u_id)[0]),

                               reply_markup=kb.adset
                               )


@dp.message_handler(state=Status.xadabout)
async def ad_about(message: types.Message):
    u_id = message.from_user.id

    about = message.text
    db.upd_ad_about(u_id, about)

    await Status.ad_end.set()

    if (db.set_ad_minage(u_id)[0], db.set_ad_maxage(u_id)[0]) == (0, 999999):
        await bot.send_message(u_id,
                               lt.ad[lang(u_id)] + "\n\n" +
                               str(db.set_ad_title(u_id)[0]) + "\n" +

                               lt.chageb[lang(u_id)] + ": " + " - " + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_about(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_contact(u_id)[0]),

                               reply_markup=kb.adset
                               )

    else:
        await bot.send_message(u_id,
                               lt.ad[lang(u_id)] + "\n\n" +
                               str(db.set_ad_title(u_id)[0]) + "\n" +

                               lt.chageb[lang(u_id)] + ": " + str(db.set_ad_minage(u_id)[0]) + " - "
                               + str(db.set_ad_maxage(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_about(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_contact(u_id)[0]),

                               reply_markup=kb.adset
                               )


@dp.message_handler(state=Status.xadcontact)
async def adcontact(message: types.Message):
    u_id = message.from_user.id

    contact = message.text
    db.upd_ad_contact(message.from_user.id, contact)

    await Status.ad_end.set()

    if (db.set_ad_minage(u_id)[0], db.set_ad_maxage(u_id)[0]) == (0, 999999):
        await bot.send_message(u_id,
                               lt.ad[lang(u_id)] + "\n\n" +
                               str(db.set_ad_title(u_id)[0]) + "\n" +

                               lt.chageb[lang(u_id)] + ": " + " - " + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_about(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_contact(u_id)[0]),

                               reply_markup=kb.adset
                               )

    else:
        await bot.send_message(u_id,
                               lt.ad[lang(u_id)] + "\n\n" +
                               str(db.set_ad_title(u_id)[0]) + "\n" +

                               lt.chageb[lang(u_id)] + ": " + str(db.set_ad_minage(u_id)[0]) + " - "
                               + str(db.set_ad_maxage(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_about(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_contact(u_id)[0]),

                               reply_markup=kb.adset
                               )


@dp.callback_query_handler(lambda call: True, state=Status.xadcontact)
async def ad_contact(call):
    u_id = call.from_user.id

    try:
        if call.message:
            if call.data == "-":
                db.upd_ad_contact(u_id, "-")
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="-", reply_markup=None)

                await Status.ad_end.set()

                if (db.set_ad_minage(u_id)[0], db.set_ad_maxage(u_id)[0]) == (0, 999999):
                    await bot.send_message(u_id,
                                           lt.ad[lang(u_id)] + "\n\n" +
                                           str(db.set_ad_title(u_id)[0]) + "\n" +

                                           lt.chageb[lang(u_id)] + ": " + " - " + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_about(u_id)[0]) + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_contact(u_id)[0]),

                                           reply_markup=kb.adset
                                           )

                else:
                    await bot.send_message(u_id,
                                           lt.ad[lang(u_id)] + "\n\n" +
                                           str(db.set_ad_title(u_id)[0]) + "\n" +

                                           lt.chageb[lang(u_id)] + ": " + str(db.set_ad_minage(u_id)[0]) + " - "
                                           + str(db.set_ad_maxage(u_id)[0]) + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_about(u_id)[0]) + "\n" +
                                           str("------------------------------") + "\n" +
                                           str(db.set_ad_contact(u_id)[0]),

                                           reply_markup=kb.adset
                                           )

    except Exception as e:
        print(repr(e))


@dp.message_handler(state=Status.xadcity)
async def ad_city(message: types.Message):
    u_id = message.from_user.id

    city = message.text
    db.upd_ad_city(message.from_user.id, city)

    await Status.ad_end.set()

    if (db.set_ad_minage(u_id)[0], db.set_ad_maxage(u_id)[0]) == (0, 999999):
        await bot.send_message(u_id,
                               lt.ad[lang(u_id)] + "\n\n" +
                               str(db.set_ad_title(u_id)[0]) + "\n" +

                               lt.chageb[lang(u_id)] + ": " + " - " + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_about(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_contact(u_id)[0]),

                               reply_markup=kb.adset
                               )

    else:
        await bot.send_message(u_id,
                               lt.ad[lang(u_id)] + "\n\n" +
                               str(db.set_ad_title(u_id)[0]) + "\n" +

                               lt.chageb[lang(u_id)] + ": " + str(db.set_ad_minage(u_id)[0]) + " - "
                               + str(db.set_ad_maxage(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_about(u_id)[0]) + "\n" +
                               str("------------------------------") + "\n" +
                               str(db.set_ad_contact(u_id)[0]),

                               reply_markup=kb.adset
                               )


#  -------------------------------------------------------------------------------------------
@dp.callback_query_handler(state=Status.A1)
async def updater(call):
    u_id = call.from_user.id
    ad_id = db.nn(u_id)

    B1 = InlineKeyboardButton(lt.b1[lang(u_id)], callback_data="b1")
    B2 = InlineKeyboardButton(lt.b2[lang(u_id)], callback_data="b2")
    B3 = InlineKeyboardButton(lt.b3[lang(u_id)], callback_data="b3")
    B4 = InlineKeyboardButton(lt.b4[lang(u_id)], callback_data="b4")
    B5 = InlineKeyboardButton(lt.b5[lang(u_id)], callback_data="b5")
    CancelB = InlineKeyboardButton(lt.cancelb1[lang(u_id)], callback_data="-")

    Changes_ad = InlineKeyboardMarkup().add(B1).add(B2).add(B3).add(B4).add(B5).add(CancelB)

    try:
        if call.message:
            if call.data == "d1":
                n1 = ad_id[0]
                n = n1[0]
                if int(db.all_ads(u_id)[0]) < 0:
                    await bot.send_message(u_id, "?")
                else:
                    db.minus_ad(u_id)
                    db.del_ad(n)
                    await bot.send_message(u_id, "———————————————————————————————")
                    await bot.send_message(u_id, lt.ad_deleting[lang(u_id)])

            elif call.data == "d2":
                n1 = ad_id[1]
                n = n1[0]
                if int(db.all_ads(u_id)[0]) < 0:
                    await bot.send_message(u_id, "?")
                else:
                    db.minus_ad(u_id)
                    db.del_ad(n)
                    await bot.send_message(u_id, "———————————————————————————————")
                    await bot.send_message(u_id, lt.ad_deleting[lang(u_id)])

            elif call.data == "d3":
                n1 = ad_id[2]
                n = n1[0]
                if int(db.all_ads(u_id)[0]) < 0:
                    await bot.send_message(u_id, "?")
                else:
                    db.minus_ad(u_id)
                    db.del_ad(n)
                    await bot.send_message(u_id, "———————————————————————————————")
                    await bot.send_message(u_id, lt.ad_deleting[lang(u_id)])

            elif call.data == "d4":
                n1 = ad_id[3]
                n = n1[0]
                if int(db.all_ads(u_id)[0]) < 0:
                    await bot.send_message(u_id, "?")
                else:
                    db.minus_ad(u_id)
                    db.del_ad(n)
                    await bot.send_message(u_id, "———————————————————————————————")
                    await bot.send_message(u_id, lt.ad_deleting[lang(u_id)])

            elif call.data == "d5":
                n1 = ad_id[4]
                n = n1[0]
                if int(db.all_ads(u_id)[0]) < 0:
                    await bot.send_message(u_id, "?")
                else:
                    db.minus_ad(u_id)
                    db.del_ad(n)
                    await bot.send_message(u_id, "———————————————————————————————")
                    await bot.send_message(u_id, lt.ad_deleting[lang(u_id)])

            elif call.data == "d6":
                n1 = ad_id[5]
                n = n1[0]
                if int(db.all_ads(u_id)[0]) < 0:
                    await bot.send_message(u_id, "?")
                else:
                    db.minus_ad(u_id)
                    db.del_ad(n)
                    await bot.send_message(u_id, "———————————————————————————————")
                    await bot.send_message(u_id, lt.ad_deleting[lang(u_id)])

            elif call.data == "d7":
                n1 = ad_id[6]
                n = n1[0]
                if int(db.all_ads(u_id)[0]) < 0:
                    await bot.send_message(u_id, "?")
                else:
                    db.minus_ad(u_id)
                    db.del_ad(n)
                    await bot.send_message(u_id, "———————————————————————————————")
                    await bot.send_message(u_id, lt.ad_deleting[lang(u_id)])

            elif call.data == "d8":
                n1 = ad_id[7]
                n = n1[0]
                if int(db.all_ads(u_id)[0]) < 0:
                    await bot.send_message(u_id, "?")
                else:
                    db.minus_ad(u_id)
                    db.del_ad(n)
                    await bot.send_message(u_id, "———————————————————————————————")
                    await bot.send_message(u_id, lt.ad_deleting[lang(u_id)])

            elif call.data == "d9":
                n1 = ad_id[8]
                n = n1[0]
                if int(db.all_ads(u_id)[0]) < 0:
                    await bot.send_message(u_id, "?")
                else:
                    db.minus_ad(u_id)
                    db.del_ad(n)
                    await bot.send_message(u_id, "———————————————————————————————")
                    await bot.send_message(u_id, lt.ad_deleting[lang(u_id)])
            # -----------------------------------------------
            elif call.data == "u1":
                n1 = ad_id[0]
                n = n1[0]
                await Status.ad_changing.set()
                await bot.send_message(u_id, "———————————————————————————————")
                min_age = db.set_ad_minage2(u_id, n)[0]
                if min_age == 0:
                    min_age = ""

                max_age = db.set_ad_maxage2(u_id, n)[0]
                if max_age == 999999:
                    max_age = ""
                await bot.send_message(u_id,
                                       "(" + str(db.set_ad_city2(u_id, n)[0]) + ")" + str(db.set_ad_title2(u_id, n)[0])
                                       + "\n" +
                                       lt.chageb[lang(u_id)] + ": " + str(min_age) + "-" + str(max_age) + "\n" +
                                       "-----------------------------------\n" +
                                       " " + str(db.set_ad_about2(u_id, n)[0]) + "\n" +
                                       "-----------------------------------\n" +
                                       "✉ " + str(db.set_ad_contact2(u_id, n)[0]) + " - " + str(db.set_name(u_id)),

                                       reply_markup=Changes_ad
                                       )
                db.avaiable(u_id, n)

            elif call.data == "u2":
                n1 = ad_id[1]
                n = n1[0]
                await Status.ad_changing.set()
                await bot.send_message(u_id, "———————————————————————————————")
                min_age = db.set_ad_minage2(u_id, n)[0]
                if min_age == 0:
                    min_age = ""

                max_age = db.set_ad_maxage2(u_id, n)[0]
                if max_age == 999999:
                    max_age = ""
                await bot.send_message(u_id,
                                       "(" + str(db.set_ad_city2(u_id, n)[0]) + ")" + str(db.set_ad_title2(u_id, n)[0])
                                       + "\n" +
                                       lt.chageb[lang(u_id)] + ": " + str(min_age) + "-" + str(max_age) + "\n" +
                                       "-----------------------------------\n" +
                                       " " + str(db.set_ad_about2(u_id, n)[0]) + "\n" +
                                       "-----------------------------------\n" +
                                       "✉ " + str(db.set_ad_contact2(u_id, n)[0]) + " - " + str(db.set_name(u_id)),

                                       reply_markup=Changes_ad
                                       )
                db.avaiable(u_id, n)

            elif call.data == "u3":
                n1 = ad_id[2]
                n = n1[0]
                await Status.ad_changing.set()
                await bot.send_message(u_id, "———————————————————————————————")
                min_age = db.set_ad_minage2(u_id, n)[0]
                if min_age == 0:
                    min_age = ""

                max_age = db.set_ad_maxage2(u_id, n)[0]
                if max_age == 999999:
                    max_age = ""
                await bot.send_message(u_id,
                                       "(" + str(db.set_ad_city2(u_id, n)[0]) + ")" + str(db.set_ad_title2(u_id, n)[0])
                                       + "\n" +
                                       lt.chageb[lang(u_id)] + ": " + str(min_age) + "-" + str(max_age) + "\n" +
                                       "-----------------------------------\n" +
                                       " " + str(db.set_ad_about2(u_id, n)[0]) + "\n" +
                                       "-----------------------------------\n" +
                                       "✉ " + str(db.set_ad_contact2(u_id, n)[0]) + " - " + str(db.set_name(u_id)),

                                       reply_markup=Changes_ad
                                       )
                db.avaiable(u_id, n)

            elif call.data == "u4":
                n1 = ad_id[3]
                n = n1[0]
                await Status.ad_changing.set()
                await bot.send_message(u_id, "———————————————————————————————")
                min_age = db.set_ad_minage2(u_id, n)[0]
                if min_age == 0:
                    min_age = ""

                max_age = db.set_ad_maxage2(u_id, n)[0]
                if max_age == 999999:
                    max_age = ""
                await bot.send_message(u_id,
                                       "(" + str(db.set_ad_city2(u_id, n)[0]) + ")" + str(db.set_ad_title2(u_id, n)[0])
                                       + "\n" +
                                       lt.chageb[lang(u_id)] + ": " + str(min_age) + "-" + str(max_age) + "\n" +
                                       "-----------------------------------\n" +
                                       " " + str(db.set_ad_about2(u_id, n)[0]) + "\n" +
                                       "-----------------------------------\n" +
                                       "✉ " + str(db.set_ad_contact2(u_id, n)[0]) + " - " + str(db.set_name(u_id)),

                                       reply_markup=Changes_ad
                                       )
                db.avaiable(u_id, n)

            elif call.data == "u5":
                n1 = ad_id[4]
                n = n1[0]
                await Status.ad_changing.set()
                await bot.send_message(u_id, "———————————————————————————————")
                min_age = db.set_ad_minage2(u_id, n)[0]
                if min_age == 0:
                    min_age = ""

                max_age = db.set_ad_maxage2(u_id, n)[0]
                if max_age == 999999:
                    max_age = ""
                await bot.send_message(u_id,
                                       "(" + str(db.set_ad_city2(u_id, n)[0]) + ")" + str(db.set_ad_title2(u_id, n)[0])
                                       + "\n" +
                                       lt.chageb[lang(u_id)] + ": " + str(min_age) + "-" + str(max_age) + "\n" +
                                       "-----------------------------------\n" +
                                       " " + str(db.set_ad_about2(u_id, n)[0]) + "\n" +
                                       "-----------------------------------\n" +
                                       "✉ " + str(db.set_ad_contact2(u_id, n)[0]) + " - " + str(db.set_name(u_id)),

                                       reply_markup=Changes_ad
                                       )
                db.avaiable(u_id, n)

            elif call.data == "u6":
                n1 = ad_id[5]
                n = n1[0]
                await Status.ad_changing.set()
                await bot.send_message(u_id, "———————————————————————————————")
                min_age = db.set_ad_minage2(u_id, n)[0]
                if min_age == 0:
                    min_age = ""

                max_age = db.set_ad_maxage2(u_id, n)[0]
                if max_age == 999999:
                    max_age = ""
                await bot.send_message(u_id,
                                       "(" + str(db.set_ad_city2(u_id, n)[0]) + ")" + str(db.set_ad_title2(u_id, n)[0])
                                       + "\n" +
                                       lt.chageb[lang(u_id)] + ": " + str(min_age) + "-" + str(max_age) + "\n" +
                                       "-----------------------------------\n" +
                                       " " + str(db.set_ad_about2(u_id, n)[0]) + "\n" +
                                       "-----------------------------------\n" +
                                       "✉ " + str(db.set_ad_contact2(u_id, n)[0]) + " - " + str(db.set_name(u_id)),

                                       reply_markup=Changes_ad
                                       )
                db.avaiable(u_id, n)

            elif call.data == "u7":
                n = ad_id[6]
                await Status.ad_changing.set()
                await bot.send_message(u_id, "———————————————————————————————")
                min_age = db.set_ad_minage2(u_id, n[0])[0]
                if min_age == 0:
                    min_age = ""

                max_age = db.set_ad_maxage2(u_id, n[0])[0]
                if max_age == 999999:
                    max_age = ""
                await bot.send_message(u_id,
                                       "(" + str(db.set_ad_city2(u_id, n[0])[0]) + ")" +
                                       str(db.set_ad_title2(u_id, n[0])[0])
                                       + "\n" +
                                       lt.chageb[lang(u_id)] + ": " + str(min_age) + "-" + str(max_age) + "\n" +
                                       "-----------------------------------\n" +
                                       " " + str(db.set_ad_about2(u_id, n[0])[0]) + "\n" +
                                       "-----------------------------------\n" +
                                       "✉ " + str(db.set_ad_contact2(u_id, n[0])[0]) + " - " + str(db.set_name(u_id)),

                                       reply_markup=Changes_ad
                                       )
                db.avaiable(u_id, n)

            elif call.data == "u8":
                n1 = ad_id[7]
                n = n1[0]
                await Status.ad_changing.set()
                await bot.send_message(u_id, "———————————————————————————————")
                min_age = db.set_ad_minage2(u_id, n)[0]
                if min_age == 0:
                    min_age = ""

                max_age = db.set_ad_maxage2(u_id, n)[0]
                if max_age == 999999:
                    max_age = ""
                await bot.send_message(u_id,
                                       "(" + str(db.set_ad_city2(u_id, n)[0]) + ")" + str(db.set_ad_title2(u_id, n)[0])
                                       + "\n" +
                                       lt.chageb[lang(u_id)] + ": " + str(min_age) + "-" + str(max_age) + "\n" +
                                       "-----------------------------------\n" +
                                       " " + str(db.set_ad_about2(u_id, n)[0]) + "\n" +
                                       "-----------------------------------\n" +
                                       "✉ " + str(db.set_ad_contact2(u_id, n)[0]) + " - " + str(db.set_name(u_id)),

                                       reply_markup=Changes_ad
                                       )
                db.avaiable(u_id, n)

            elif call.data == "u9":
                n1 = ad_id[8]
                n = n1[0]
                await Status.ad_changing.set()
                await bot.send_message(u_id, "———————————————————————————————")
                min_age = db.set_ad_minage2(u_id, n)[0]
                if min_age == 0:
                    min_age = ""

                max_age = db.set_ad_maxage2(u_id, n)[0]
                if max_age == 999999:
                    max_age = ""
                await bot.send_message(u_id,
                                       "(" + str(db.set_ad_city2(u_id, n)[0]) + ")" + str(db.set_ad_title2(u_id, n)[0])
                                       + "\n" +
                                       lt.chageb[lang(u_id)] + ": " + str(min_age) + "-" + str(max_age) + "\n" +
                                       "-----------------------------------\n" +
                                       " " + str(db.set_ad_about2(u_id, n)[0]) + "\n" +
                                       "-----------------------------------\n" +
                                       "✉ " + str(db.set_ad_contact2(u_id, n)[0]) + " - " + str(db.set_name(u_id)),

                                       reply_markup=Changes_ad
                                       )
                db.avaiable(u_id, n)

    except Exception as e:
        print(repr(e))


@dp.callback_query_handler(state=Status.ad_changing)
async def updating(call):
    u_id = call.from_user.id
    try:
        if call.message:
            if call.data == "-":
                db.ad_saving(call.from_user.id)
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text=lt.cancelb1[lang(u_id)])
                await Status.A1.set()
                ad_id = db.nn(u_id)  # all ids of ads
                await bot.send_message(u_id, lt.n_ads[lang(u_id)] + str(len(ad_id)))
                for n in range(len(ad_id)):
                    num = ad_id[n]  # only 1 certain id of certain ad

                    title = db.set_ad_title2(u_id, num[0])[0]

                    min_age = db.set_ad_minage2(u_id, num[0])[0]
                    if min_age == 0:
                        min_age = ""

                    max_age = db.set_ad_maxage2(u_id, num[0])[0]
                    if max_age == 999999:
                        max_age = ""

                    about = db.set_ad_about2(u_id, num[0])[0]

                    city = db.set_ad_city2(u_id, num[0])[0]

                    contact = db.set_ad_contact2(u_id, num[0])[0]

                    ader = db.set_name(u_id)[0]

                    nkb = n

                    time.sleep(0.1)
                    await bot.send_message(u_id,
                                           str(n + 1) + ".\n" +
                                           "(" + str(city) + ")" + str(title) + "\n" +
                                           lt.chageb[lang(u_id)] + ": " + str(min_age) + "-" + str(max_age) + "\n" +
                                           "-----------------------------------\n" +
                                           " " + str(about) + "\n" +
                                           "-----------------------------------\n" +
                                           "✉ " + str(contact) + " - " + str(ader),

                                           reply_markup=kb.adupd[nkb]
                                           )

            elif call.data == "b1":
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="🔄", reply_markup=None)

                await Status.xad_naming2.set()
                await bot.send_message(u_id, lt.adname[lang(u_id)])

            elif call.data == "b2":
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="🔄", reply_markup=None)

                await Status.xagefrom2.set()
                await bot.send_message(u_id, lt.minage[lang(u_id)])

            elif call.data == "b3":
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="🔄", reply_markup=None)
                await Status.xadabout2.set()
                await bot.send_message(u_id, lt.adabout[lang(u_id)])

            elif call.data == "b4":
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="🔄", reply_markup=None)
                await bot.send_message(u_id, lt.xad_contact[lang(u_id)])
                await Status.xadcontact2.set()

            elif call.data == "b5":
                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text="🔄", reply_markup=None)
                await bot.send_message(u_id, lt.citing1[lang(u_id)])
                await Status.xadcity2.set()

    except Exception as e:
        print(repr(e))


@dp.message_handler(state=Status.xad_naming2)
async def ad_namer2(message: types.Message):
    u_id = message.from_user.id

    adname = message.text
    db.upd_ad_title(u_id, adname)
    db.ad_saving(u_id)

    await bot.send_message(u_id, lt.dtitle[lang(u_id)])
    await Status.A1.set()


@dp.message_handler(state=Status.xagefrom2)
async def minage_changer(message: types.Message):
    u_id = message.from_user.id

    minage = message.text
    db.upd_ad_minage(u_id, minage)

    await message.answer(lt.maxage[lang(u_id)])
    await Status.xageto2.set()


@dp.message_handler(state=Status.xageto2)
async def maxage_changer(message: types.Message):
    u_id = message.from_user.id

    maxage = message.text
    db.upd_ad_maxage(u_id, maxage)
    db.ad_saving(u_id)

    await message.answer(lt.dage[lang(u_id)])
    await Status.A1.set()


@dp.message_handler(state=Status.xadabout2)
async def about_changer(message: types.Message):
    u_id = message.from_user.id

    about = message.text
    db.upd_ad_about(u_id, about)
    db.ad_saving(u_id)

    await message.answer(lt.dabout[lang(u_id)])
    await Status.A1.set()


@dp.message_handler(state=Status.xadcontact2)
async def contact_changer(message: types.Message):
    u_id = message.from_user.id

    contacts = message.text
    db.upd_ad_contact(u_id, contacts)
    db.ad_saving(u_id)

    await message.answer(lt.dcontact[lang(u_id)])
    await Status.A1.set()


@dp.message_handler(state=Status.xadcity2)
async def contact_changer(message: types.Message):
    u_id = message.from_user.id

    city = message.text
    db.upd_ad_contact(u_id, city)
    db.ad_saving(u_id)

    await message.answer(lt.dcity[lang(u_id)])
    await Status.A1.set()


#  -------------------------------------------------------------------------------------------
@dp.message_handler(lambda message: message.text in lt.nextb, state=Status.search2)
async def searching(message: types.Message):
    u_id = message.from_user.id
    age = db.set_age(u_id)[0]
    city = db.set_city(u_id)[0]
    ids = db.getting_all_suitable_ads(city, age)
    num_ids = len(ids)
    global ol
    ol += 1
    print(ol)
    if ol < num_ids:
        r_id = (ids[ol])[0]
        inf = db.ad(r_id)
        await message.answer("(" + str(inf[2]) + ") " + str(inf[0]) + "\n" +
                             "-----------------------------------\n" +
                             " " + str(inf[4]) + "\n" +
                             "-----------------------------------\n" +
                             "✉ " + str(inf[3]) + " - " + str(inf[1]) + "\n" +
                             str(inf[7]),

                             reply_markup=kb.adkb
                             )
    else:
        await message.answer(lt.nomorejobserror[lang(u_id)])
        if ol >= num_ids:
            ol -= ol
        await Status.A1.set()


@dp.message_handler(lambda message: message.text in lt.menub, state=Status.search2)
async def back(message: types.Message):
    uid = message.from_user.id
    userstatus = db.set_status(uid)[0]

    FavB = KeyboardButton(lt.favb[lang(uid)], callback_data="fav")
    SearchB = KeyboardButton(lt.searchb[lang(uid)], callback_data="sea")
    SettB = KeyboardButton(lt.settb[lang(uid)], callback_data="set")
    HelpB = KeyboardButton(lt.helpb[lang(uid)], callback_data="hel")
    MyB = KeyboardButton(lt.myb[lang(uid)], callback_data="my")
    AddB = KeyboardButton(lt.addb[lang(uid)], callback_data="add")

    menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
        .row(SettB, HelpB)
    menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AddB) \
        .row(SettB, HelpB)

    mc = (menu0, menu1)

    await message.answer("⬅", reply_markup=mc[userstatus])

    await Status.A1.set()


@dp.callback_query_handler(state=Status.search2)
async def favorite_adder(call):
    u_id = call.from_user.id
    global ol
    age = db.set_age(u_id)[0]
    city = db.set_city(u_id)[0]
    ids = db.getting_all_suitable_ads(city, age)
    r_id = (ids[ol])[0]
    inf = db.ad(r_id)
    try:
        if call.message:
            if call.data == "fav":
                db.add_favorite(u_id, inf[5], inf[6], r_id)
                await bot.send_message(u_id, lt.favadded[lang(u_id)])

    except Exception as e:
        print(repr(e))


#  -------------------------------------------------------------------------------------------
@dp.message_handler(lambda message: message.text == "Hello" or
                                    message.text == "Hallo" or
                                    message.text == "Привет" or
                                    message.text == "مرحبا",
                    state=Status.A1)
async def suck(message: types.Message):
    await bot.send_message(message.from_user.id, lt.sucker[lang(message.from_user.id)])
    await Status.A1.set()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

# thank you
