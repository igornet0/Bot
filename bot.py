import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from parser import get_resp_prepod
from config import *
import keyboards as kb
from sqlighter import SQLighter

class Stats(StatesGroup):
    GetTimetable = State()
    GetName = State()


# инициализируем бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
database = SQLighter('bd.db')

@dp.message_handler(commands=["start"], content_types=types.ContentTypes.TEXT)
async def start_command(message: types.Message, state: FSMContext):
    await message.answer('Привет!', reply_markup=kb.kb_start())

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def get_timetable(message: types.Message, state: FSMContext):
    response = message.text.lower()
    if response == 'расписание':
        await message.answer('Пришли мне фамилию и инициалы преподавателя, например Иванов И.И.',
                             reply_markup=kb.back())
        await Stats.GetName.set()


@dp.message_handler(state=Stats.GetName, content_types=types.ContentTypes.TEXT)
async def send_timetable(message: types.Message, state: FSMContext):
    response = message.text
    lst_response = response.split()
    if lst_response[0].count('.') > 0:
        en = lst_response[0]
        las = lst_response[1]
    else:
        en = lst_response[1]
        las = lst_response[0]
    id, value = database.get_id(las, en)
    database.create_timetable(id)
    timetable = database.get_timetable(id)
    if not timetable:
        timetable = get_resp_prepod(value)
        for key, item in timetable.items():
            for key1, item in item.items():
                for i in item:
                    database.add_timetable(id, key, i[2], i[-1], i[0], i[3], i[1], i[4], key1)
    timetable = database.get_timetable(id)
    s = ''

                             reply_markup=kb.back())
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
    database.create_table()
    logging.basicConfig(filename='log.txt', level=logging.INFO)
    executor.start_polling(dp, on_shutdown=shutdown)
