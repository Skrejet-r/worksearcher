from aiogram.types import ReplyKeyboardMarkup,  \
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