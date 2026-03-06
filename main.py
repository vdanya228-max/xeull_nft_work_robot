import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Временное хранилище активированных пользователей (для демо)
activated_users = set()

# Кнопки главного меню
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Выдать звезды на передачу")],
        [KeyboardButton(text="Создать сыллку"), KeyboardButton(text="Подключится к сессии")],
        [KeyboardButton(text="Ваши логи")]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обработка команды /start
    """
    await message.answer("Привет введи код которые тебе выдали при покупке")

@dp.message(F.text == "xeull_test")
async def process_test_code(message: Message) -> None:
    """
    Обработка тестового кода
    """
    activated_users.add(message.from_user.id)
    await message.answer("вы получили тестовую подписку, для покупки полной подписки обратитесь к @xeull_robot")
    
    # Отправляем статус пользователя
    status_text = (
        f"Привет {message.from_user.first_name}\n"
        "Подписка: Не активирована\n"
        "Баланс: 0 Ton\n"
        "профит: 0 Ton"
    )
    await message.answer(status_text, reply_markup=main_menu_keyboard)

@dp.message(F.text.in_({"Создать сыллку", "Выдать звезды на передачу", "Подключится к сессии", "Ваши логи"}))
async def process_menu_buttons(message: Message) -> None:
    """
    Обработка кнопок меню
    """
    error_text = (
        "у вас не активирована подписка и вы не добавлены в вайт лист"
    )
    await message.answer(error_text)
    
    status_text = (
        f"Привет {message.from_user.first_name}\n"
        "Подписка: Не активирована\n"
        "Баланс: 0 Ton\n"
        "профит: 0 Ton"
    )
    await message.answer(status_text, reply_markup=main_menu_keyboard)

@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Обработка всех остальных сообщений
    """
    if not message.text or message.from_user.id in activated_users:
        return
    
    await message.answer("Неверный код. Пожалуйста, введите корректный код активации.")

async def main() -> None:
    # Удаляем вебхук, чтобы бот мог работать в режиме Long Polling
    await bot.delete_webhook(drop_pending_updates=True)
    print("Бот запущен в режиме Long Polling (GitHub Actions)...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
