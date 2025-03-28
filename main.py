import os
import openai
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables from .env
load_dotenv()

# Get API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the bot starts"""
    await update.message.reply_text("🎨 Send me a prompt, and I'll generate an image using DALL·E!")

async def generate_image(update: Update, context: CallbackContext) -> None:
    """Generate an image using OpenAI DALL·E"""
    user_prompt = update.message.text
    await update.message.reply_text("🖌 Generating image, please wait...")

    try:
        response = openai.Image.create(
            prompt=user_prompt,
            n=1,  # Generate one image
            size="1024x1024"
        )
        image_url = response['data'][0]['url']

        # Send the image to the user
        await update.message.reply_photo(photo=image_url, caption=f"🖼 Here’s your image!\n\nPrompt: {user_prompt}")

    except Exception as e:
        logger.error(f"Error generating image: {e}")
        await update.message.reply_text("❌ Failed to generate image. Please try again later.")

def main():
    """Start the bot"""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))

    # Run the bot
    app.run_polling()

if __name__ == "__main__":
    main()
