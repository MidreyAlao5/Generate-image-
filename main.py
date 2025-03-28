import openai
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_image(update: Update, context) -> None:
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("Please provide a prompt. Usage: /generate <description>")
        return

    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        await update.message.reply_photo(photo=image_url, caption="Here is your generated image!")
    except Exception as e:
        await update.message.reply_text(f"Image generation failed. Error: {e}")

async def start(update: Update, context) -> None:
    await update.message.reply_text("Welcome! Send /generate <text> to create an image.")

def main():
    bot_token = os.getenv("BOT_TOKEN")
    app = Application.builder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate_image))

    app.run_polling()

if __name__ == "__main__":
    main()
