from pyrogram import Client, filters, idle
from flask import Flask
import threading
import os

# ====== TELEGRAM BOT CONFIG ======
API_ID =  38713734       
API_HASH = "e897266b97b591e003868c56f59ff815"
BOT_TOKEN = "8227009859:AAHKngOwHWmPdu0OWyPmP0npwHZubJscKGQ"

# ====== PYROGRAM BOT ======
bot = Client(
    "godfather_movie_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

DATABASE_CHANNELS = [
    "GodfatherWorldMovies",
    "Godfather_Hollywood",
    "GodfatherTamilMovies"
]

@bot.on_message(filters.private & filters.text)
async def search_movie(client, message):
    query = message.text.strip()
    results = []

    for channel in DATABASE_CHANNELS:
        try:
            async for msg in client.search_messages(channel, query, limit=5):
                if msg.text or msg.caption:
                    text = msg.text or msg.caption
                    link = f"https://t.me/{channel}/{msg.id}"
                    results.append(f"🎬 **{channel}**\n{text}\n🔗 {link}")
        except:
            continue

    if results:
        await message.reply_text(
            "\n\n".join(results),
            disable_web_page_preview=True
        )
    else:
        await message.reply_text("❌ Movie not found in my database.")

# ====== FLASK KEEP-ALIVE (FOR RENDER) ======
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

# ====== START BOT ======
bot.start()
idle()
