from aiogram.types import ReplyKeyboardMarkup, \
    KeyboardButton, \
    InlineKeyboardButton, \
    InlineKeyboardMarkup

import langtranslator as lt
from extradef import lang

# --------------------------------------------------------------------------------
# Keyboard for language-choosing
EngLan = InlineKeyboardButton("English", callback_data="eng")
RusLan = InlineKeyboardButton("Русский", callback_data="rus")
DeLan = InlineKeyboardButton("Deutsch", callback_data="de")
ArbLan = InlineKeyboardButton("عربى", callback_data="arb")

languages = InlineKeyboardMarkup().row(EngLan, RusLan, DeLan, ArbLan)
# --------------------------------------------------------------------------------
'''# Keyboard for status-choosing
SearcherBut = InlineKeyboardButton(lt.status1[lang()])
OfferBut = InlineKeyboardButton(lt.status2[lang()])

StatusIn = InlineKeyboardMarkup().row(SearcherBut, OfferBut)
# --------------------------------------------------------------------------------
'''