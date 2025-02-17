import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Получаем токен из переменных окружения
TOKEN = os.getenv("TOKEN")

# Проверяем, установлен ли токен
if not TOKEN:
    raise ValueError("❌ ОШИБКА: Переменная окружения 'TOKEN' не установлена!")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("✅ Бот запущен и работает!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)