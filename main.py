import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

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
        [KeyboardButton(text="Ваши логи"), KeyboardButton(text="Приобрести подписку")]
    ],
    resize_keyboard=True
)

# Кнопки для выбора подписки
subscription_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подписка на неделю", callback_data="subscribe_week")],
        [InlineKeyboardButton(text="Подписка на месяц", callback_data="subscribe_month")]
    ]
)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обработка команды /start
    """
    await message.answer("Привет введи код которые тебе выдали при покупке", reply_markup=main_menu_keyboard)

@dp.message(F.text == "Приобрести подписку")
async def subscribe_handler(message: Message):
    await message.answer("Выберите период подписки:", reply_markup=subscription_keyboard)

@dp.callback_query(F.data == "subscribe_week")
async def process_subscribe_week(callback: CallbackQuery):
    payment_info = (
        "После оплаты вы получите персональный ключ подписки, который активирует доступ ко всем функциям сервиса на выбранный срок. "
        "Ключ выдается сразу после успешной оплаты и позволяет начать пользоваться сервисом без ожидания. "
        "Спасибо за вашу покупку и доверие!"
    )
    payment_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Оплатить", url="t.me/send?start=IVaKicb1xSdb")]]
    )
    await callback.message.answer(payment_info, reply_markup=payment_keyboard)
    await callback.answer()

@dp.callback_query(F.data == "subscribe_month")
async def process_subscribe_month(callback: CallbackQuery):
    payment_info = (
        "После оплаты вы получите персональный ключ подписки, который активирует доступ ко всем функциям сервиса на выбранный срок. "
        "Ключ выдается сразу после успешной оплаты и позволяет начать пользоваться сервисом без ожидания. "
        "Спасибо за вашу покупку и доверие!"
    )
    payment_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Оплатить", url="t.me/send?start=IV5cWEdhWa1Z")]]
    )
    await callback.message.answer(payment_info, reply_markup=payment_keyboard)
    await callback.answer()

@dp.message(lambda message: message.text and message.text.strip().lower() in {"xeull_work#122026", "xeull_work#202612"})
async def process_activation_keys(message: Message):
    activated_users.add(message.from_user.id)
    
    activation_message = (
        "✅ Ключ успешно активирован!\n\n"
        "У вас активирована подписка, и вы добавлены в вайт лист.\n"
        "Из-за текущей нагрузки на сервер полный функционал может стать доступен через несколько минут или часов.\n\n"
        "Как только активация завершится, мы отправим вам уведомление. Спасибо за ожидание! 🚀"
    )
    await message.answer(activation_message, reply_markup=main_menu_keyboard)

@dp.message(lambda message: message.text and message.text.strip().lower() == "xeull_test")
async def process_test_code(message: Message) -> None:
    """
    Обработка тестового кода
    """
    activated_users.add(message.from_user.id)
    await message.answer("вы получили тестовую подписку, для покупки полной подписки обратитесь к @xeull_robot")
    
    # Отправляем статус пользователя
    status_text = (
        f"Привет {message.from_user.first_name}\n"
        "Подписка: Активирована (Тестовая)\n"
        "Баланс: 0 Ton\n"
        "профит: 0 Ton"
    )
    await message.answer(status_text, reply_markup=main_menu_keyboard)

@dp.message(F.text.in_({"Создать сыллку", "Выдать звезды на передачу", "Подключится к сессии", "Ваши логи"}))
async def process_menu_buttons(message: Message) -> None:
    """
    Обработка кнопок меню
    """
    if message.from_user.id in activated_users:
        await message.answer("✅ Ваша подписка активна.\nДоступ к функциям настраивается, пожалуйста, подождите завершения активации.")
        
        status_text = (
            f"Привет {message.from_user.first_name}\n"
            "Подписка: Активирована\n"
            "Баланс: 0 Ton\n"
            "профит: 0 Ton"
        )
        await message.answer(status_text, reply_markup=main_menu_keyboard)
        return
        
    error_text = (
        "у вас не активирована подписка и вы не добавлены в вайт лист\n\n"
        "для покупки полной версии обратитесь к @xeull_robot\n\n"
        "стоимость 10$ за неделю и 30$ за месяц"
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
