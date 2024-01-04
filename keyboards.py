from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, reply_keyboard_markup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, types, F

main_kb = ReplyKeyboardMarkup(
  keyboard=[
    [
      KeyboardButton(text="Настройки")
    ],
    [
      KeyboardButton(text="Игры с ботом"),
      KeyboardButton(text="НЕ РАБОТАЕТ")
    ]
  ],
  resize_keyboard=True,
  one_time_keyboard=True,
  selective=True
)

set_kb = ReplyKeyboardMarkup(
  keyboard=[
    [
      KeyboardButton(text="Профиль")
    ],
    [
      KeyboardButton(text="НЕ РАБОТАЕТ"),
      KeyboardButton(text="⏩ обратно")
    ]
  ],
  resize_keyboard=True,
  one_time_keyboard=True,
  selective=True
)
profile_kb = ReplyKeyboardMarkup(
  keyboard=[
    [
      KeyboardButton(text="Проверить данные")
    ],
    [
      KeyboardButton(text="Сменить имя"),
      KeyboardButton(text="⏩ обратно")
    ]
  ],
  resize_keyboard=True,
  one_time_keyboard=True,
  selective=True
)
game_kb = ReplyKeyboardMarkup(
  keyboard=[
    [
      KeyboardButton(text="Камень, ножницы, бумага")
    ],
    [
      KeyboardButton(text="⏩ обратно")
    ]
  ],
  resize_keyboard=True,
  one_time_keyboard=True,
  selective=True
)
def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
  row = [KeyboardButton(text=item) for item in items]
  return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)