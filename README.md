# Telegram AI Image Generator Bot

This bot generates AI images using Replicate's Stable Diffusion API.

## Setup
1. Add environment variables:
- TELEGRAM_BOT_TOKEN
- REPLICATE_API_TOKEN

2. Run Locally:
```
pip install -r requirements.txt
python main.py
```

3. Deploy to Railway:
```
railway init
railway up
```

## Usage
Send the bot a text prompt and it will generate an AI image.
