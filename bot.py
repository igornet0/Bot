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
database = SQLighter('db.db')

@dp.message_handler(commands=["start"], content_types=types.ContentTypes.TEXT)
async def start_command(message: types.Message, state: FSMContext):
    #await bot.send_message(477406355,"Я готов любить и быть с тобой максимально долго, на сколько это возможно❤️‍🩹")
    await message.answer('Привет!', reply_markup=kb.kb_start())

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def get_timetable(message: types.Message, state: FSMContext):
    response = message.text.lower()
    #await bot.send_message(477406355, "Я готов любить и быть с тобой максимально долго, на сколько это возможно❤️‍🩹")
    if response == 'расписание':
        await message.answer('Пришли мне фамилию и инициалы преподавателя, например Иванов И.И.',
                             reply_markup=kb.back())
        await Stats.GetName.set()
    else:
        await message.answer('Такой команды нет',
                             reply_markup=kb.kb_start())


@dp.message_handler(state=Stats.GetName, content_types=types.ContentTypes.TEXT)
async def send_timetable(message: types.Message, state: FSMContext):
    response = message.text
    if response.lower() == 'назад️':
        await message.answer('иди нахуй Аня Беляева ты меня заебала я тебя любил но ты этого не оценил соси хуй тупая шмара', reply_markup=kb.kb_start())
        await state.finish()
        return
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
        await message.answer("Нет такого преподавателя, повторите ввод")
        return
    id, value = l[0]
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
        if f"📆{item[1]}: \n" != s_t:
            if s_t:
                s = s + s_t + s_tt + "\n"
            s_t = f"📆{item[1]}: \n"
            p = "" if str(item[3]).isdigit() else item[3]
            s_ttt = f"🕘{item[2]}"
            s_tt = f"🕘{item[2]} \n *{p}{item[4]} {item[5]}* \n{item[6]},{item[7]} ({item[8]})\n\n"
        else:
            p = "" if str(item[3]).isdigit() else item[3]
            s_tt_1 = f"*{p}{item[4]} {item[5]}* \n{item[6]},{item[7]} ({item[8]})\n\n"
            if s_ttt != f"🕘{item[2]}":
                s_tt_1 = f"🕘{item[2]} \n " + s_tt_1
                s_ttt = f"🕘{item[2]}"
            s_tt += s_tt_1

    s = s + s_t + s_tt
    await message.answer(s, reply_markup=kb.kb_start(), parse_mode="Markdown")
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
