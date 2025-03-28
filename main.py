import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from openai import OpenAI

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load API tokens from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send me a prompt, and I'll generate an image for you!")

# Image generation function
async def generate_image(update: Update, context: CallbackContext) -> None:
    prompt = update.message.text.strip()
    
    if not prompt:
        await update.message.reply_text("Please provide a valid prompt for image generation.")
        return

    await update.message.reply_text("Generating image, please wait...")

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024"
        )
        image_url = response.data[0].url
        await update.message.reply_photo(photo=image_url, caption=f"Prompt: {prompt}")

    except Exception as e:
        logger.error(f"Error generating image: {e}")
        await update.message.reply_text("❌ Failed to generate image. Please try again.")

# Main function to run the bot
async def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))

    logger.info("Bot is running...")
    await app.run_polling()

# Run the bot
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
