from aiogram.types import ReplyKeyboardMarkup, \
    KeyboardButton, \
    InlineKeyboardButton, \
    InlineKeyboardMarkup


# --------------------------------------------------------------------------------
# Keyboard for language-choosing
EngLan = InlineKeyboardButton("English", callback_data="eng")
RusLan = InlineKeyboardButton("Русский", callback_data="rus")
DeLan = InlineKeyboardButton("Deutsch", callback_data="de")
ArbLan = InlineKeyboardButton("عربى", callback_data="arb")

languages = InlineKeyboardMarkup().row(EngLan, RusLan, DeLan, ArbLan)
# --------------------------------------------------------------------------------
DeleteB = InlineKeyboardButton("❌", callback_data="del")
UpdateB = InlineKeyboardButton("🔄", callback_data="upd")
SaveB = InlineKeyboardButton("✅", callback_data="sav")

adset = InlineKeyboardMarkup().row(DeleteB, UpdateB, SaveB)
# --------------------------------------------------------------------------------
Delete1B = InlineKeyboardButton("❌", callback_data="d1")
Update1B = InlineKeyboardButton("🔄", callback_data="u1")

Delete2B = InlineKeyboardButton("❌", callback_data="d2")
Update2B = InlineKeyboardButton("🔄", callback_data="u2")

Delete3B = InlineKeyboardButton("❌", callback_data="d3")
Update3B = InlineKeyboardButton("🔄", callback_data="u3")

Delete4B = InlineKeyboardButton("❌", callback_data="d4")
Update4B = InlineKeyboardButton("🔄", callback_data="u4")

Delete5B = InlineKeyboardButton("❌", callback_data="d5")
Update5B = InlineKeyboardButton("🔄", callback_data="u5")

Delete6B = InlineKeyboardButton("❌", callback_data="d6")
Update6B = InlineKeyboardButton("🔄", callback_data="u6")

Delete7B = InlineKeyboardButton("❌", callback_data="d7")
Update7B = InlineKeyboardButton("🔄", callback_data="u7")

Delete8B = InlineKeyboardButton("❌", callback_data="d8")
Update8B = InlineKeyboardButton("🔄", callback_data="u8")

Delete9B = InlineKeyboardButton("❌", callback_data="d9")
Update9B = InlineKeyboardButton("🔄", callback_data="u9")

adupd1 = InlineKeyboardMarkup().row(Delete1B, Update1B)
adupd2 = InlineKeyboardMarkup().row(Delete2B, Update2B)
adupd3 = InlineKeyboardMarkup().row(Delete3B, Update3B)
adupd4 = InlineKeyboardMarkup().row(Delete4B, Update4B)
adupd5 = InlineKeyboardMarkup().row(Delete5B, Update5B)
adupd6 = InlineKeyboardMarkup().row(Delete6B, Update6B)
adupd7 = InlineKeyboardMarkup().row(Delete7B, Update7B)
adupd8 = InlineKeyboardMarkup().row(Delete8B, Update8B)
adupd9 = InlineKeyboardMarkup().row(Delete9B, Update9B)

adupd = (adupd1, adupd2, adupd3, adupd4, adupd5, adupd6, adupd7, adupd8, adupd9)
# --------------------------------------------------------------------------------
'''# Keyboard for status-choosing
SearcherBut = InlineKeyboardButton(lt.status1[lang()])
OfferBut = InlineKeyboardButton(lt.status2[lang()])

StatusIn = InlineKeyboardMarkup().row(SearcherBut, OfferBut)
# --------------------------------------------------------------------------------
'''