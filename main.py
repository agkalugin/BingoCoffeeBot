import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Получаем токен из переменной окружения
TOKEN = os.getenv("TOKEN")
ADMIN_ID = 68189  # ID твоего аккаунта

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class Registration(StatesGroup):
    full_name = State()
    phone_number = State()

# Клавиатура для запроса номера телефона
phone_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
phone_keyboard.add(KeyboardButton("Отправить номер телефона", request_contact=True))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    welcome_text = (
        "Привет! Этот бот создан для подключения к программе лояльности Bingo Coffee.\n"
        "С каждой покупки вам будет возвращаться от 2 до 5% на бонусный счёт.\n"
        "За регистрацию вам начисляется 100 рублей!\n\n"
        "Пожалуйста, введите ваше ФИО:"
    )
    await message.answer(welcome_text)
    await Registration.full_name.set()

@dp.message_handler(state=Registration.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Теперь отправьте ваш номер телефона", reply_markup=phone_keyboard)
    await Registration.phone_number.set()

@dp.message_handler(content_types=types.ContentType.CONTACT, state=Registration.phone_number)
async def get_phone_number_contact(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await process_phone_number(message, state, phone_number)

@dp.message_handler(state=Registration.phone_number)
async def get_phone_number_text(message: types.Message, state: FSMContext):
    phone_number = message.text
    await process_phone_number(message, state, phone_number)

async def process_phone_number(message: types.Message, state: FSMContext, phone_number: str):
    data = await state.get_data()
    full_name = data.get("full_name")
    last_four_digits = phone_number[-4:] if len(phone_number) >= 4 else phone_number
    
    # Отправка данных админу
    admin_message = (
        f"🔔 **Новая регистрация в программе лояльности:**\n"
        f"👤 **ФИО:** {full_name}\n"
        f"📞 **Телефон:** {phone_number}\n"
        f"🔢 **Последние 4 цифры:** {last_four_digits}"
    )
    try:
        await bot.send_message(ADMIN_ID, admin_message)  # Отправка админу по chat_id
        await bot.send_message("@kalugin", admin_message)  # Отправка в @kalugin
    except Exception as e:
        logging.error(f"Ошибка отправки данных админу: {e}")
    
    # Ответ пользователю
    await message.answer(f"✅ **Регистрация завершена!**\n📢 **При покупке называйте последние 4 цифры:** `{last_four_digits}`")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)