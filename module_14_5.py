from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = InlineKeyboardMarkup()
button = InlineKeyboardMarkup(text = "Рассчитать норму калорий", callback_data = 'calories')
button2 = InlineKeyboardMarkup(text = "Формулы расчёта", callback_data = 'formulas')

kb.add(button, button2)

buy_menu = InlineKeyboardMarkup(resize_keyboard=True)
button_ = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')
button_2 = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')
button_3 = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')
button_4 = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
kb.insert(button_)
kb.insert(button_2)
kb.insert(button_3)
kb.insert(button_4)

online_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Информация'),
            KeyboardButton(text='Рассчитать'),
        ],
        [ KeyboardButton(text='Купить') ,
         KeyboardButton(text='Регистрация') ]
    ],
    resize_keyboard=True
)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open("Product1.jpg", "rb") as APPLE:
        await message.answer_photo(APPLE, f"Название: Product1 | Описание: APPLE | Цена: {1*100}")
    with open("Product2.jpg", "rb") as lemon:
        await message.answer_photo(lemon, f"Название: Product2 | Описание: lemon | Цена: {2*100}")
    with open("Product3.jpg", "rb") as orange:
        await message.answer_photo(orange, f"Название: Product3 | Описание: orange | Цена: {3*100}")
    with open("Product4.jpg", "rb") as pear:
        await message.answer_photo(pear, f"Название: Product4 | Описание: pear | Цена: {4*100}")
    await message.answer("Выберите продукт для покупки:", reply_markup=buy_menu)

@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()
@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    data = await state.get_data()
    await message.answer(f"Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer(f"Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    Calories = ((10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']))-161)*1.375
    await message.answer(f'Норма калорий: {Calories}')
    await state.finish()

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = online_menu)


@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('((10 х вес(кг) + 6.25 х рост(см) - 5 х возраст(лет))-161) х 1.375 (уровень активности)')
    await call.answer()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text) is True:
        await message.answer(f"Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email: ')
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    users_data = await state.get_data()
    add_user(users_data["username"], users_data["email"], users_data["age"])
    await message.answer("Регистрация прошла успешно")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)