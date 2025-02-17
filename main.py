import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получение токена из переменной окружения
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN is missing! Set it in Heroku config vars.")

# Создание бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Хэндлер для команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Бот успешно запущен! ✅")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)