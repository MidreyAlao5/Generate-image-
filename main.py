import os
import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Model version (Update this to the latest version from Replicate)
MODEL_VERSION = "f178d751c3..."  # Replace with actual version

async def start(update: Update, context: CallbackContext):
    """Handle /start command."""
    await update.message.reply_text("Welcome! Send me a text prompt and I'll turn it into an image!")

async def generate(update: Update, context: CallbackContext):
    """Handle /generate command."""
    if not context.args:
        await update.message.reply_text("Please provide a prompt! Example: `/generate A futuristic city at night`")
        return

    prompt = " ".join(context.args)
    await update.message.reply_text(f"Generating image for: {prompt}... Please wait!")

    image_url = await generate_image(prompt)

    if image_url:
        await update.message.reply_photo(photo=image_url, caption=f"Here is your generated image for: {prompt}")
    else:
        await update.message.reply_text("❌ Image generation failed. Try again later!")

async def generate_image(prompt):
    """Send request to Replicate API and fetch generated image."""
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "version": MODEL_VERSION,
        "input": {"prompt": prompt}
    }

    # Send request to Replicate API
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 201:
        return None

    prediction = response.json()
    poll_url = prediction["urls"]["get"]

    # Polling for result
    while True:
        result = requests.get(poll_url, headers=headers).json()
        status = result["status"]

        if status == "succeeded":
            return result["output"][0]
        elif status == "failed":
            return None

        await asyncio.sleep(2)  # Wait before polling again

def main():
    """Start the bot."""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
