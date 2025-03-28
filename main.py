import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import openai

# Load environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Configure OpenAI API
openai.api_key = OPENAI_API_KEY

# Logging setup
logging.basicConfig(level=logging.INFO)

async def generate_image(prompt: str):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response["data"][0]["url"]
    except Exception as e:
        logging.error(f"OpenAI Error: {e}")
        return None

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    await message.reply("Hello! Send me a text prompt, and I'll generate an image using AI.")

@dp.message_handler()
async def handle_prompt(message: Message):
    await message.reply("Generating image... Please wait.")
    image_url = await generate_image(message.text)
    
    if image_url:
        await message.reply_photo(image_url, caption="Here is your AI-generated image!")
    else:
        await message.reply("Failed to generate an image. Please try again later.")

if __name__ == '__main__':
    logging.info("Bot is starting...")
    executor.start_polling(dp, skip_updates=True)
