import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Channel ID
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # Admin ID (Aapka Telegram ID)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Keyboard Buttons
join_channel_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{os.getenv('CHANNEL_USERNAME')}"),
    InlineKeyboardButton("✅ Done", callback_data="check_join")
)

get_hack_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton("🚀 Get Hack")
)

# Start Command
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer_photo(
        photo=open("welcome.jpg", "rb"),
        caption="🔔 Pehle channel join karein, phir continue karein.",
        reply_markup=join_channel_keyboard
    )

# Channel Join Check
@dp.callback_query_handler(lambda c: c.data == "check_join")
async def check_join(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        user_channel_status = await bot.get_chat_member(CHANNEL_ID, user_id)
        if user_channel_status.status in ["member", "administrator", "creator"]:
            await bot.send_message(user_id, "✅ Aapne channel join kar liya hai! Get Hack ka button enable ho gaya hai.", reply_markup=get_hack_keyboard)
        else:
            await bot.send_message(user_id, "⚠️ Pehle channel join karein!", reply_markup=join_channel_keyboard)
    except:
        await bot.send_message(user_id, "⚠️ Pehle channel join karein!", reply_markup=join_channel_keyboard)

# Get Hack Button
@dp.message_handler(lambda message: message.text == "🚀 Get Hack")
async def get_hack(message: types.Message):
    user_id = message.from_user.id
    user_channel_status = await bot.get_chat_member(CHANNEL_ID, user_id)
    
    if user_channel_status.status in ["member", "administrator", "creator"]:
        await bot.send_document(user_id, open("hack_tool.apk", "rb"), caption="✅ Hack Tool Download Karein")
    else:
        await message.answer("⚠️ Pehle channel join karein!", reply_markup=join_channel_keyboard)

# Broadcast Feature (Admin Only)
@dp.message_handler(commands=['broadcast'])
async def broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    text = message.text.replace("/broadcast ", "")
    users = [12345678, 23456789]  # Yaha database se user IDs load karein
    for user in users:
        try:
            await bot.send_message(user, text)
        except:
            pass
    await message.answer("✅ Broadcast sent!")

# Stats Command
@dp.message_handler(commands=['stats'])
async def stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    total_users = 100  # Yaha database se total users count karein
    await message.answer(f"📊 Total Users: {total_users}")

async def main():
    await dp.start_polling()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
