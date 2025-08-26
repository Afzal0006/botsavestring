from pyrogram import Client, filters
from pymongo import MongoClient

# ====== CONFIG (filled) ======
API_ID = 24597778
API_HASH = "0b34ead62566cc7b072c0cf6b86b716e"
BOT_TOKEN = "6050583747:AAEPVadyHjbjQw6lSFlPv66wXNgf_H5idcs"
MONGO_URL = "mongodb+srv://afzal99550:afzal99550@cluster0.aqmbh9q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
GROUP_ID = -1002591009357  # Fixed group

# MongoDB connection
mongo_client = MongoClient(MONGO_URL)
db = mongo_client["telegram_bot"]
collection = db["users"]

# Bot Client
bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ====== HANDLERS ======

@bot.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_text(
        "✅ Bot is running!\n\n"
        "📌 Commands:\n"
        "/start - Check bot status\n"
        "/run - Send test message in group\n"
        "/save <text> - Save something to DB\n"
        "/get - Fetch your saved data\n"
    )


@bot.on_message(filters.command("run"))
async def run_handler(client, message):
    try:
        await bot.send_message(GROUP_ID, "⚡ Bot test message via /run command!")
        await message.reply_text("✅ Done! Message sent to group.")
    except Exception as e:
        await message.reply_text(f"❌ Failed: {e}")


@bot.on_message(filters.command("save"))
async def save_handler(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: /save <text>")
    
    data = " ".join(message.command[1:])
    collection.update_one(
        {"user_id": message.from_user.id},
        {"$set": {"data": data}},
        upsert=True
    )
    await message.reply_text("✅ Your data has been saved!")


@bot.on_message(filters.command("get"))
async def get_handler(client, message):
    user_data = collection.find_one({"user_id": message.from_user.id})
    if user_data and "data" in user_data:
        await message.reply_text(f"📂 Saved Data:\n\n{user_data['data']}")
    else:
        await message.reply_text("❌ No data found. Use /save to add some.")


# ====== RUN ======
if __name__ == "__main__":
    print("🚀 Bot Started...")
    bot.run()
