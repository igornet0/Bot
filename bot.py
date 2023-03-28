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
    if response == 'Назад':
        await message.answer('иди нахуй Аня Беляева ты меня заебала я тебя любил но ты этого не оценил соси хуй тупая шмара', reply_markup=kb.kb_start())
        await state.finish()
    lst_response = response.split()
    try:
        if lst_response[0].count('.') > 0:
            en = lst_response[0]
            las = lst_response[1]
        else:
            en = lst_response[1]
            las = lst_response[0]
    except Exception as e:
        await message.answer("Не верно введён формат, повторите ввод")
        return
    l = database.get_id(las, en)
    if not l:
        await message.answer("Нет такого преподавателя")
        return
    id, value = l
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
    s_t = ''
    s_tt = ''
    s_ttt = ''
    for item in timetable:
        if f"{item[1]}: \n" != s_t:
            if s_t:
                s = s + s_t + s_tt + '\n'
            s_t = f"{item[1]}: \n"
            p = '' if item[3] == '1' else item[3]
            s_ttt = f"{item[2]}"
            s_tt = f"{item[2]} \n {p}{item[4]} {item[5]} {item[6]} {item[7]} {item[8]}\n"
        else:
            p = '' if item[3] == '1' else item[3]
            s_tt += f"{p}{item[4]} {item[5]} {item[6]} {item[7]} {item[8]}\n"
            if s_ttt != f"{item[2]}":
                s_tt = f"{item[2]} \n " + s_tt
                s_ttt = f"{item[2]}"
    s = s + s_t + s_tt
    await message.answer(s, reply_markup=kb.kb_start())
    await state.finish()

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
