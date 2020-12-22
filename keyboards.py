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
'''# Keyboard for status-choosing
SearcherBut = InlineKeyboardButton(lt.status1[lang()])
OfferBut = InlineKeyboardButton(lt.status2[lang()])

StatusIn = InlineKeyboardMarkup().row(SearcherBut, OfferBut)
# --------------------------------------------------------------------------------
'''