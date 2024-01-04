import asyncio
import random
import sqlite3 as sq

import database as db
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import Message

import keyboards

BOT_TOKEN = "6889463533:AAH1WQFz5I-4MIRDn2qZR6IvBVvFGFAdKn8"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)

db = sq.connect('tg.db')
cur = db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users ( 
  id INTEGER PRIMARY KEY, 
  name TEXT)""") 
db.commit() 

available_obj = ["Камень", "Ножницы", "Бумага"]

class name(StatesGroup):
    wname = State()

class rename(StatesGroup):
  wname = State()

class obj(StatesGroup):
  object = State()


@dp.message(obj.object, F.text.in_(available_obj))
async def obj_chosen(message: Message, state: FSMContext):
  state_data = await state.get_data()
  state_data.get("keyboard_state", "main")
  rand_obj = random.choice(available_obj)
  await state.update_data(chosen_food=message.text.lower())
  await message.answer(
      text=rand_obj,
      reply_markup=keyboards.make_row_keyboard(available_obj)
  )
  if (rand_obj == "Камень" and message.text == "Ножницы") or (rand_obj == "Бумага" and message.text == "Камень") or (rand_obj == "Ножницы" and message.text == "Бумага"):
    await message.answer(
      text="Вы проиграли!",
      reply_markup=keyboards.game_kb)
    await state.update_data(keyboard_state="game")
    await state.clear()
  elif rand_obj == message.text:
    await state.set_state(obj.object)
  else:
    await message.answer(
      text="Вы выиграли!",
      reply_markup=keyboards.game_kb)
    await state.update_data(keyboard_state="game")
    await state.clear()
  
@dp.message(StateFilter(None), Command("start")) 
async def handle_start(message: Message, state: FSMContext): 
  cur.execute("SELECT name FROM users WHERE id = ?",             
  (message.from_user.id,))  # Используем параметризованный запрос 
  data = cur.fetchone() 
  if data is None:
    if message.chat.type == "private":
      await message.answer(text=f"Привет, {message.from_user.username}! Давай дадим тебе имя. Напиши мне его.") 
      await state.set_state(name.wname) 
    else: await message.answer(text=f"Привет, {message.from_user.username}! У тебя нет имени. Снова напиши мне /start, но в ЛС.") 
  else: 
  # Получаем первый элемент из кортежа, который является именем пользователя. 
    user_name = data[0] 
    if message.chat.type == "private":
      rand = random.randint(1, 10)
      privet = ""
      if rand == 1:
        privet = "Привет, "
      elif rand == 2:
        privet = "Здравствуй, "
      elif rand == 3:
        privet = "Приветствую Вас, "
      elif rand == 4:
        privet = "Здарова, "
      elif rand == 5:
        privet = "Ну здравствуй, "
      elif rand == 6:
        privet = "Здравствуйте, "
      elif rand == 7:
        privet = "Кто сюда пожаловал? А, это "
      elif rand == 8:
        privet = "Ну здарова, "
      elif rand == 9:
        privet = "Приветствую тебя, "
      elif rand == 10:
        privet = "Здравия желаю, "
        
      await message.answer(text=privet + user_name + "!", reply_markup=keyboards.main_kb)
    else:
      rand = random.randint(1, 10)
      privet = ""
      if rand == 1:
        privet = "Привет, "
      elif rand == 2:
        privet = "Здравствуй, "
      elif rand == 3:
        privet = "Приветствую Вас, "
      elif rand == 4:
        privet = "Здарова, "
      elif rand == 5:
        privet = "Ну здравствуй, "
      elif rand == 6:
        privet = "Здравствуйте, "
      elif rand == 7:
        privet = "Кто сюда пожаловал? А, это "
      elif rand == 8:
        privet = "Ну здарова, "
      elif rand == 9:
        privet = "Приветствую тебя, "
      elif rand == 10:
        privet = "Здравия желаю, "
      await message.answer(text=privet + user_name + "!")
      

@dp.message(name.wname) 
async def name_chosen(message: Message, state: FSMContext): 
    uname = message.text 
    cur.execute("INSERT INTO users (id, name) VALUES (?, ?)",               
    (message.from_user.id, uname))  # Используем параметризованный запрос 
    db.commit() 
    await message.answer(text=f'Отлично, {uname}. Ты авторизован! Если хочешь сменить имя, то зайди в меню → "настройки" → "профиль" → "сменить имя".', reply_markup=keyboards.main_kb) 
    await state.clear() 

@dp.message(lambda msg: msg.text.lower() == 'я') 
async def Me(message: Message): 
      cur.execute("SELECT name FROM users WHERE id = ?",             
      (message.from_user.id,))  # Используем параметризованный запрос 
      data = cur.fetchone() 
      if data is None: 
        await message.answer(text=f"Привет, {message.from_user.username}! У тебя нет имени. Напиши мне /start, но в ЛС.") 
      else: 
      # Получаем первый элемент из кортежа, который является именем пользователя. 
        user_name = data[0] 
        if message.chat.type == "private":
          rand = random.randint(1, 10)
          privet = ""
          if rand == 1:
            privet = "Привет, "
          elif rand == 2:
            privet = "Здравствуй, "
          elif rand == 3:
            privet = "Приветствую Вас, "
          elif rand == 4:
            privet = "Здарова, "
          elif rand == 5:
            privet = "Ну здравствуй, "
          elif rand == 6:
            privet = "Здравствуйте, "
          elif rand == 7:
            privet = "Кто сюда пожаловал? А, это "
          elif rand == 8:
            privet = "Ну здарова, "
          elif rand == 9:
            privet = "Приветствую тебя, "
          elif rand == 10:
            privet = "Здравия желаю, "

          await message.answer(text=privet + user_name + "!", reply_markup=keyboards.main_kb)
        else:
          rand = random.randint(1, 10)
          privet = ""
          if rand == 1:
            privet = "Привет, "
          elif rand == 2:
            privet = "Здравствуй, "
          elif rand == 3:
            privet = "Приветствую Вас, "
          elif rand == 4:
            privet = "Здарова, "
          elif rand == 5:
            privet = "Ну здравствуй, "
          elif rand == 6:
            privet = "Здравствуйте, "
          elif rand == 7:
            privet = "Кто сюда пожаловал? А, это "
          elif rand == 8:
            privet = "Ну здарова, "
          elif rand == 9:
            privet = "Приветствую тебя, "
          elif rand == 10:
            privet = "Здравия желаю, "
          await message.answer(text=privet + user_name + "!", reply_markup=keyboards.main_kb)


@dp.message(Command("who"))
async def handle_who(message: Message):
    await message.answer(text="Я бот, который пока ещё неизвестно, для чего нужен. Я ещё в разработке.")

@dp.message(rename.wname) 
async def name_chosen2(message: Message, state: FSMContext): 
    uname = message.text 
    cur.execute("UPDATE users SET name=? WHERE id=?", (uname, message.from_user.id))
    db.commit() 
    await message.answer(text=f'Отлично, {uname}. Ты сменил имя.', reply_markup=keyboards.main_kb) 
    await state.clear() 



@dp.message(StateFilter(None))
async def btn(message: Message, state: FSMContext):
  txt = message.text
  if message.chat.type == 'private':
    if txt == 'Настройки':
      await message.answer(text='Настройки', reply_markup=keyboards.set_kb)
    elif txt == '⏩ обратно':
      if message.reply_markup == keyboards.set_kb:
        await message.answer(text='⏩ обратно', reply_markup=keyboards.main_kb)
      elif message.reply_markup == keyboards.profile_kb:
        await message.answer(text='⏩ обратно', reply_markup=keyboards.set_kb)
      elif message.reply_markup == keyboards.game_kb:
        await message.answer(text='⏩ обратно', reply_markup=keyboards.main_kb)
      else:
        await message.answer(text='⏩ обратно', reply_markup=keyboards.main_kb)
    elif txt == 'Профиль':
      await message.answer(text='Профиль', reply_markup=keyboards.profile_kb)
    elif txt == 'Игры с ботом':
      await message.answer(text='Игры с ботом', reply_markup=keyboards.game_kb)
    elif txt == 'Проверить данные':
      cur.execute("SELECT name FROM users WHERE id = ?",             
      (message.from_user.id,))  # Используем параметризованный запрос 
      data = cur.fetchone() 
      user_name = data[0]
      await message.answer(text=f'Данные. Имя: {user_name}.')
    elif txt == 'Сменить имя':
      await message.answer(text='Итак, ты хочешь сменить имя? Напиши мне его.')
      cur.execute("SELECT name FROM users WHERE id = ?", (message.from_user.id,))
      await state.set_state(rename.wname) 
    elif txt == 'Камень, ножницы, бумага':
      await message.answer(text='Камень, ножницы, бумага')
      await message.answer(
        text="Итак, сейчас будем играть в Камень Ножницы Бумага. Выбери один из трёх предметов (необязательно сначала ножницы).",
        reply_markup=keyboards.make_row_keyboard(available_obj)
      )
      await state.set_state(obj.object)
      # await state.set_state(rename.wname) 


async def main():
    await dp.start_polling(bot)

def register_handlers_name(dp: Dispatcher):
    dp.register_message_handler(handle_start, commands="start", state="*")
    dp.register_message_handler(name_chosen, state=name.wname)
    dp.register_message_handler(name_chosen2, state=name.wname)
    dp.register_message_handler(btn, state="*")


if __name__ == "__main__":
    asyncio.run(main())
