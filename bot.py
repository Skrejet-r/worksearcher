import config
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
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
        await message.answer("I see you are new here!"
                             "\nPress /lang to set language for yourself ")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
