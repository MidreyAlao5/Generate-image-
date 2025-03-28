import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Replace with your Hugging Face API key
HF_API_KEY = "YOUR_HF_API_KEY"
HF_MODEL = "stabilityai/stable-diffusion-2"  # Model name

# Function to generate images using Hugging Face
def generate_image(prompt):
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.content  # Returns image data
    else:
        return None  # Handle errors

# Telegram command to generate images
async def image_command(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Please provide a prompt! Example: /image A futuristic city at sunset")
        return

    prompt = " ".join(context.args)
    await update.message.reply_text("Generating image, please wait...")

    image_data = generate_image(prompt)

    if image_data:
        await update.message.reply_photo(photo=image_data, caption=f"Prompt: {prompt}")
    else:
        await update.message.reply_text("Failed to generate image. Try again later.")

# Start bot
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Send /image <prompt> to generate an image.")

def main():
    BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("image", image_command))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
