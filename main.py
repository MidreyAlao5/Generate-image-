import openai
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load your OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_image(update: Update, context: CallbackContext) -> None:
    prompt = ' '.join(context.args)
    if not prompt:
        update.message.reply_text("Please provide a prompt. Usage: /generate <description>")
        return

    try:
        response = openai.images.generate(
            model="dall-e-3",  # Use "dall-e-3" for better quality
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        update.message.reply_photo(photo=image_url, caption="Here is your generated image!")
    except Exception as e:
        update.message.reply_text(f"Image generation failed. Error: {e}")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome! Send /generate <text> to create an image.")

def main():
    bot_token = os.getenv("BOT_TOKEN")
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("generate", generate_image))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
