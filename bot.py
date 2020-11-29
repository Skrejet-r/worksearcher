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


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    if not (db.user_exists(message.from_user.id)):
        await message.answer("Welcome")
        # if user isnt in the db - add him
        db.add_user(message.from_user.id)
        await Status.A2.set()
        await bot.send_message(message.from_user.id, "I see you are new here!\nSet language for yourself:",
                               reply_markup=kb.languages)
    else:
        await message.answer(lt.alph1[lang(message.from_user.id)])


@dp.message_handler(state=Status.A2)
async def test(message: types.Message):
    await message.answer("testtest")
    await Status.A1.set()


@dp.callback_query_handler(lambda call: True)
async def lan_set(call):
    u_id = call.message.chat.id
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
    except Exception as e:
        print(repr(e))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
