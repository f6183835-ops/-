import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_BOT_TOKEN = "8992996368:AAHau2vpV24IiWODlbOaBz3xlZppq5gBbpc"
CARTESIA_API_KEY = "sk_car_LYuLMSyVfnfaP9VM4Czgzu"
VOICE_ID = "70999f90-ec46-4b54-8e32-366960230821"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো! আমাকে যেকোনো মেসেজ পাঠান, আমি ভয়েস জেনারেট করে দেব।")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text("ভয়েস তৈরি হচ্ছে, দয়া করে অপেক্ষা করুন...")

    url = "https://api.cartesia.ai/tts/bytes"
    headers = {
        "Cartesia-Version": "2026-08-14",
        "X-API-Key": CARTESIA_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "model_id": "sonic-3.6",
        "transcript": text,
        "voice": {
            "mode": "id",
            "id": VOICE_ID
        },
        "output_format": {
            "container": "wav",
            "encoding": "pcm_s16le",
            "sample_rate": 44100
        },
        "generation_config": {
            "speed": 1,
            "volume": 1
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        audio_path = "output.wav"
        with open(audio_path, "wb") as f:
            f.write(response.content)

        with open(audio_path, "rb") as audio:
            await update.message.reply_voice(voice=audio)
        
        if os.path.exists(audio_path):
            os.remove(audio_path)
    else:
        await update.message.reply_text("ভয়েস তৈরি করতে সমস্যা হয়েছে।")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
  
