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


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    if not (db.user_exists(message.from_user.id)):
        await message.answer("Welcome")
        # if user isnt in the db - add him
        db.add_user(message.from_user.id)
        await Status.A3.set()
        time.sleep(1)
        await bot.send_message(message.from_user.id, "I see you are new here!\nSet language for yourself:",
                               reply_markup=kb.languages)
    else:
        await message.answer(lt.welcome[lang(message.from_user.id)])
        await Status.A1.set()


@dp.message_handler(commands=["start"], state=Status.A1)
async def welcome(message: types.Message):
    FavB = KeyboardButton(lt.favb[lang(message.from_user.id)], callback_data="fav")
    SearchB = KeyboardButton(lt.searchb[lang(message.from_user.id)], callback_data="sea")
    SettB = KeyboardButton(lt.settb[lang(message.from_user.id)], callback_data="set")
    HelpB = KeyboardButton(lt.helpb[lang(message.from_user.id)], callback_data="hel")
    MyB = KeyboardButton(lt.myb[lang(message.from_user.id)], callback_data="my")
    AddB = KeyboardButton(lt.addb[lang(message.from_user.id)], callback_data="add")
    AplB = KeyboardButton(lt.aplb[lang(message.from_user.id)], callback_data="apl")

    menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
        .row(SettB, HelpB)
    menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AplB, AddB) \
        .row(SettB, HelpB)

    mc = (menu0, menu1)

    await message.answer(lt.welcome[lang(message.from_user.id)],
                         reply_markup=mc[db.set_status(message.from_user.id)[0]])
    await Status.A1.set()


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
        await message.answer(lt.adform[lang(message.from_user.id)])
        time.sleep(1)
        await Status.ad_naming.set()
        await message.answer(lt.adname[lang(message.from_user.id)])

    else:
        await message.answer("?")


# -------------------------------------------------------------------------------------------------
@dp.message_handler(lambda message: message.text in lt.helpb, state=Status.A1)
async def helper(message: types.Message):
    userstatus = db.set_status(message.from_user.id)[0]
    if userstatus == 0:
        await bot.send_message(message.from_user.id, lt.helping0[lang(message.from_user.id)])
    elif userstatus == 1:
        await bot.send_message(message.from_user.id, lt.helping1[lang(message.from_user.id)])
    else:
        await message.answer("Error")


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
    SsB = KeyboardButton(lt.settsearchb[lang(uid)], callback_data="sets")
    DelB = KeyboardButton(lt.deleteb[lang(uid)], callback_data="del")
    StatB = KeyboardButton(lt.chstatusb[lang(uid)], callback_data="stat")

    menu01 = ReplyKeyboardMarkup(resize_keyboard=True).row(BackB, ProfileB, LangB) \
        .row(NameB, AgeB, CityB) \
        .row(AboutB, StatB, DelB) \
        .row(SsB)

    menu11 = ReplyKeyboardMarkup(resize_keyboard=True).row(BackB, ProfileB, LangB) \
        .row(NameB, CityB, StatB) \
        .row(DelB)

    mc1 = (menu01, menu11)

    await message.answer("⚙", reply_markup=mc1[userstatus])


@dp.message_handler(lambda message: message.text in lt.backb, state=Status.A1)
async def backtomenu(message: types.Message):
    uid = message.from_user.id
    userstatus = db.set_status(uid)[0]

    FavB = KeyboardButton(lt.favb[lang(uid)], callback_data="fav")
    SearchB = KeyboardButton(lt.searchb[lang(uid)], callback_data="sea")
    SettB = KeyboardButton(lt.settb[lang(uid)], callback_data="set")
    HelpB = KeyboardButton(lt.helpb[lang(uid)], callback_data="hel")
    MyB = KeyboardButton(lt.myb[lang(uid)], callback_data="my")
    AddB = KeyboardButton(lt.addb[lang(uid)], callback_data="add")
    AplB = KeyboardButton(lt.aplb[lang(uid)], callback_data="apl")

    menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
        .row(SettB, HelpB)
    menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AplB, AddB) \
        .row(SettB, HelpB)

    mc = (menu0, menu1)

    await message.answer("⬅", reply_markup=mc[userstatus])


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
                AplB = KeyboardButton(lt.aplb[lang(u_id)], callback_data="apl")

                menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
                    .row(SettB, HelpB)
                menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AplB, AddB) \
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
                AplB = KeyboardButton(lt.aplb[lang(u_id)], callback_data="apl")

                menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
                    .row(SettB, HelpB)
                menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AplB, AddB) \
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
                AplB = KeyboardButton(lt.aplb[lang(u_id)], callback_data="apl")

                menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
                    .row(SettB, HelpB)
                menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AplB, AddB) \
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
                AplB = KeyboardButton(lt.aplb[lang(u_id)], callback_data="apl")

                menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
                    .row(SettB, HelpB)
                menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AplB, AddB) \
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
    AplB = KeyboardButton(lt.aplb[lang(u_id)], callback_data="apl")

    menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
        .row(SettB, HelpB)
    menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AplB, AddB) \
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
    AplB = KeyboardButton(lt.aplb[lang(u_id)], callback_data="apl")

    menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
        .row(SettB, HelpB)
    menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AplB, AddB) \
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
    AplB = KeyboardButton(lt.aplb[lang(u_id)], callback_data="apl")

    menu0 = ReplyKeyboardMarkup(resize_keyboard=True).row(FavB, SearchB) \
        .row(SettB, HelpB)
    menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(MyB, AplB, AddB) \
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


@dp.message_handler(state=Status.ad_naming)
async def ad_namer(message: types.Message):
    adname = message.text
    db.add_ad(message.from_user.id, adname)
    await Status.A1.set()


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

# let's goooo
