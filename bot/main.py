from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.message import ContentType
from aiogram.utils import executor
import os

API_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="🎮 Открыть кейсы", web_app=WebAppInfo(url=WEBAPP_URL))
    )
    await message.answer("Добро пожаловать! Нажми кнопку ниже, чтобы открыть Mini App:", reply_markup=keyboard)

@dp.message_handler(commands=['balance'])
async def balance(message: types.Message):
    await message.answer("Ваш баланс: 1000 монет 💰")

@dp.message_handler(commands=['pay'])
async def pay(message: types.Message):
    prices = [types.LabeledPrice(label="Пополнение баланса", amount=50000)]
    await bot.send_invoice(
        message.chat.id,
        title="Пополнение",
        description="Вы получите 500 монет",
        provider_token=PAYMENT_TOKEN,
        currency="RUB",
        prices=prices,
        start_parameter="topup",
        payload="balance_topup"
    )

@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    await message.answer("✅ Платёж получен! Баланс пополнен.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
