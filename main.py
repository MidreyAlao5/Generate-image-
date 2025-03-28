import openai
import telebot
import os

# Set up environment variables (Make sure to set these in your deployment)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Send me a text prompt, and I'll generate an image for you using AI!")

@bot.message_handler(commands=['generate'])
def generate_image(message):
    prompt = message.text.replace("/generate", "").strip()
    
    if not prompt:
        bot.reply_to(message, "Please provide a prompt for the image generation. Example: `/generate a futuristic city`")
        return
    
    bot.reply_to(message, "Generating image, please wait...")

    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,  # Generate one image
            size="1024x1024"  # You can also use "512x512" or "256x256"
        )

        image_url = response['data'][0]['url']
        bot.send_photo(message.chat.id, image_url, caption="Here is your AI-generated image!")

    except Exception as e:
        bot.reply_to(message, f"Image generation failed. Error: {str(e)}")

# Start polling
bot.polling()
