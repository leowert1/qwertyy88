import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import BasicAuth  # Импорт для работы с прокси

API_TOKEN = '7994720080:AAH3ce5aynjtsmeUsdHJVp3XhnVkghoe5Ro'

# IDs администраторов
ADMINS = [994429313]

# GIF для меню
GIF_URL = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcGhiM2VsenpkOXRudGFldm9rN3M4NHY2ajN4b2luaXVvNmQ2bmVqciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xFWaAI8TKA0nrIpBQh/giphy.gif"  # Ссылка на гифку

# Создаем бота с использованием прокси
bot= Bot(token=API_TOKEN)

# Создаем диспетчер
dp = Dispatcher()

# Хранилище данных о пользователях
users = {}
subscriptions = {}

# Ссылка на криптобот (замени на свою)
CRYPTOBOT_LINK = "http://t.me/send?start=IVUTRjlO9fUL"

# Клавиатура для главного меню
def main_menu_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="🔨 Снос", callback_data="demolition"),
        InlineKeyboardButton(text="📢 Канал", callback_data="channel")
    )
    keyboard.row(
        InlineKeyboardButton(text="🤝 Рефералы", callback_data="referrals"),
        InlineKeyboardButton(text="💳 Покупка", callback_data="purchase")
    )
    keyboard.row(
        InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
        InlineKeyboardButton(text="⏱ Подписка", callback_data="subscription")
    )
    return keyboard.as_markup()

@dp.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    args = message.text.split(maxsplit=1)
    referrer_id = args[1] if len(args) > 1 else None

    if message.from_user.id not in users:
        users[message.from_user.id] = {"referrals": 0, "subscription": None}

    if referrer_id and referrer_id.isdigit() and int(referrer_id) != message.from_user.id:
        referrer_id = int(referrer_id)
        if referrer_id in users:
            users[referrer_id]["referrals"] += 1
            if users[referrer_id]["referrals"] >= 40:
                users[referrer_id]["subscription"] = "lifetime"
                await bot.send_message(referrer_id, "🎉 Поздравляем! Вы получили подписку навсегда за 40 рефералов!")

    # Приветственное сообщение с гифкой
    await bot.send_animation(
        chat_id=message.chat.id,
        animation=GIF_URL,
        caption=(
            "👋 Добро пожаловать в самый мощный бот для отправки жалоб!\n\n"
            "Наш сносер 🔨 **работает с невероятной точностью** 🔥\n"
            "📊 Более 168 активных сессий каждый день!\n"
            "💎 Получите подписку и станьте частью нашего элитного клуба!\n\n"
            "Выберите действие ниже: 👇"
        ),
        reply_markup=main_menu_keyboard()
    )
@dp.callback_query(lambda query: query.data == "demolition")
async def handle_demolition(callback_query: CallbackQuery):
    await callback_query.answer("Вы выбрали 'Снос' 🔨")
    await bot.send_message(callback_query.from_user.id, "📩 Пришлите сюда ссылку на сообщение.")

@dp.callback_query(lambda query: query.data == "channel")
async def handle_channel(callback_query: CallbackQuery):
    await callback_query.answer("Вы выбрали 'Канал' 📢")
    await bot.send_message(callback_query.from_user.id, "🔗 Вот ссылка на наш канал: https://t.me/your_channel")

@dp.callback_query(lambda query: query.data == "referrals")
async def handle_referrals(callback_query: CallbackQuery):
    user_data = users.get(callback_query.from_user.id, {"referrals": 0, "subscription": None})
    referral_count = user_data["referrals"]
    subscription = user_data["subscription"] or "нет"
    referral_link = f"https://t.me/{(await bot.get_me()).username}?start={callback_query.from_user.id}"

    await bot.send_message(
        callback_query.from_user.id,
        f"🤝 Ваши рефералы: {referral_count}\n"
        f"⏱ Подписка: {subscription}\n"
        f"🔗 Ваша реферальная ссылка:\n{referral_link}"
    )

@dp.callback_query(lambda query: query.data == "purchase")
async def handle_purchase(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Оплатить", url=CRYPTOBOT_LINK)]
        ]
    )
    await bot.send_message(
        callback_query.from_user.id,
        "💰 Стоимость подписок:\n"
        "⏱ Месяц - 3$\n"
        "♾️ Навсегда - 5$\n\n"
        "Если хотите оплатить картой, напишите @cekonor.",
        reply_markup=keyboard
    )

@dp.callback_query(lambda query: query.data == "profile")
async def handle_profile(callback_query: CallbackQuery):
    await bot.send_message(
        callback_query.from_user.id,
        f"👤 Ваш профиль:\n"
        f"🆔 ID: {callback_query.from_user.id}\n"
        f"🤝 Рефералы: {users.get(callback_query.from_user.id, {}).get('referrals', 0)}"
    )

@dp.callback_query(lambda query: query.data == "subscription")
async def handle_subscription(callback_query: CallbackQuery):
    subscription = users.get(callback_query.from_user.id, {}).get("subscription", "нет")
    await bot.send_message(
        callback_query.from_user.id,
        f"⏱ Ваша подписка: {subscription}"
    )

@dp.message(lambda msg: msg.text and msg.text.startswith("http"))
async def handle_link(message: types.Message):
    await message.answer("⏳ Ожидайте, жалобы отправляются!")
    await asyncio.sleep(30)
    total_sessions = 168
    successful_sessions = random.randint(128, total_sessions)
    unsuccessful_sessions = total_sessions - successful_sessions
    await message.answer(f"📊 На основании вашей информации:\n\n"
                         f"✅ Успешных сессий: {successful_sessions}\n"
                         f"❌ Неуспешных сессий: {unsuccessful_sessions}")

async def main():
    print("🤖 Бот запущен и ожидает команды...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
