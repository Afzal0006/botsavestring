from pyrogram import Client, filters
from pyrogram.session import StringSession
from pymongo import MongoClient

# === CONFIG ===
API_ID = 24597778
API_HASH = "0b34ead62566cc7b072c0cf6b86b716e"
BOT_TOKEN = "6050583747:AAEPVadyHjbjQw6lSFlPv66wXNgf_H5idcs"
MONGO_URL = "mongodb+srv://afzal99550:afzal99550@cluster0.aqmbh9q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
TARGET_GROUP = -1002591009357  # Group ID

# === Mongo ===
mongo = MongoClient(MONGO_URL)
db = mongo["string_sessions"]
col = db["sessions"]

# === Bot Client ===
bot = Client("string_manager", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Save String
@bot.on_message(filters.command("add") & filters.private)
async def add_string(_, msg: Message):
    if len(msg.command) < 2:
        return await msg.reply("❌ Please provide a string session")
    string = msg.command[1]

    col.insert_one({"string": string})
    await msg.reply("✅ String session saved!")

# Run Message
@bot.on_message(filters.command("run") & filters.private)
async def run_message(_, msg: Message):
    if len(msg.command) < 2:
        return await msg.reply("❌ Usage: /run your_message")

    text = msg.text.split(" ", 1)[1]
    sessions = col.find()

    sent, failed = 0, 0
    for s in sessions:
        try:
            user = Client(StringSession(s["string"]), api_id=API_ID, api_hash=API_HASH)
            await user.start()
            await user.send_message(TARGET_GROUP, text)
            await user.stop()
            sent += 1
        except Exception as e:
            failed += 1

    await msg.reply(f"✅ Done!\nSent: {sent}\nFailed: {failed}")

bot.run()
