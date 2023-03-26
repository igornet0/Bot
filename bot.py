import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


from config import *
from sqlighter import SQLighter

class Stats(StatesGroup):
    GetTimetable = State()


# инициализируем бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
database = SQLighter('bd.db')

@dp.message_handler(commands=["start"], content_types=types.ContentTypes.TEXT)
async def start_command(message: types.Message, state: FSMContext):
    await message.answer('Привет! Отправь мне фамилию и инициалы преподавателя, чье расписание ты хочешь узнать')


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def send_timetable(message: types.Message, state: FSMContext):
    response = message.text.lower()
    lst_response = response.split()
    if lst_response[0].count('.') > 0:
        en = lst_response[0]
        las = lst_response[1]
    else:
        en = lst_response[1]
        las = lst_response[0]
    database.get_teacher
        pass

@dp.message_handler(state=Stats.GetTimetable, content_types=types.ContentTypes.TEXT)
async def get_timetable(message: types.Message, state: FSMContext):
    pass

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    print("#######################")
    print('#                     #')
    print('#     Бот запущен     #')
    print('#                     #')
    print("#######################")
    logging.basicConfig(filename='log.txt', level=logging.INFO)
    executor.start_polling(dp, on_shutdown=shutdown)
