import os
import logging
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load environment variables
load_dotenv()

# Telegram & OpenAI API keys
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Configure logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me a prompt, and I'll generate an image for you!")

def generate_image(update: Update, context: CallbackContext) -> None:
    prompt = update.message.text.strip()
    if not prompt:
        update.message.reply_text("Please provide a valid prompt for image generation.")
        return

    update.message.reply_text("Generating image, please wait...")

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024"
        )
        image_url = response.data[0].url
        update.message.reply_photo(photo=image_url, caption=f"Prompt: {prompt}")
    except Exception as e:
        logging.error(f"Error generating image: {e}")
        update.message.reply_text("❌ Failed to generate image. Please try again.")

def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, generate_image))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
