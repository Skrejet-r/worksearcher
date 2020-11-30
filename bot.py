import config
import logging
import langtranslator as lt
import keyboards as kb

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dpstatus import Status
from extradef import lang
from sqldb import dbfuncs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

db = dbfuncs("db_ws.db")


async def welcome(message: types.Message):
    if not (db.user_exists(message.from_user.id)):
        await message.answer("Welcome")
        # if user isnt in the db - add him
        db.add_user(message.from_user.id)
        await Status.A2.set()
        await bot.send_message(message.from_user.id, "I see you are new here!\nSet language for yourself:",
                               reply_markup=kb.languages)
    else:
        await message.answer(lt.welcome[lang(message.from_user.id)])


@dp.message_handler(commands=["help"], state=Status.A1)
async def helper(message: types.Message):
    await bot.send_message(message.from_user.id, lt.helping[lang(message.from_user.id)])


@dp.message_handler(commands=["lang"], state=Status.A1)
async def lang_choose(message: types.Message):
    await Status.A2.set()
    await bot.send_message(message.from_user.id, "Choose the language:",
                           reply_markup=kb.languages)


@dp.callback_query_handler(lambda call: True, state=Status.A2)
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
            await Status.A1.set()
    except Exception as e:
        print(repr(e))


@dp.message_handler(lambda message: message.text == "Hello" or
                                    message.text == "Hello" or
                                    message.text == "Привет" or
                                    message.text == "مرحبا"
                    )
async def suck(message: types.Message):
    await bot.send_message(message.from_user.id, lt.sucker[lang(message.from_user.id)])


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
