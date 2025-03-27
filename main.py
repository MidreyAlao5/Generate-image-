import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_TOKEN, REPLICATE_TOKEN

logging.basicConfig(level=logging.INFO)

async def generate_image(prompt):
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "version": "f178d751c3...",  # Replace with latest version ID
        "input": {"prompt": prompt}
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 201:
        return None
    prediction = response.json()
    status = prediction["status"]
    while status != "succeeded" and status != "failed":
        result = requests.get(url + "/" + prediction["id"], headers=headers)
        status = result.json()["status"]
    if status == "succeeded":
        return result.json()["output"][0]
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send me a text prompt and I'll turn it into an image!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_text(f"Generating image for: '{prompt}' Please wait...")
    image_url = await generate_image(prompt)
    if image_url:
        await update.message.reply_photo(photo=image_url, caption="Here’s your image!")
    else:
        await update.message.reply_text("Sorry, failed to generate the image.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
