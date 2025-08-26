import os
from pyrogram import Client, filters
from pymongo import MongoClient

# ==== CONFIG ====
API_ID = 24597778
API_HASH = "0b34ead62566cc7b072c0cf6b86b716e"
BOT_TOKEN = "6050583747:AAEPVadyHjbjQw6lSFlPv66wXNgf_H5idcs"
GROUP_ID = -1002591009357

MONGO_URL = "mongodb+srv://afzal99550:afzal99550@cluster0.aqmbh9q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo = MongoClient(MONGO_URL)
db = mongo["userbot"]
col = db["strings"]

# ==== BOT CLIENT ====
bot = Client("mybot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ==== SAVE COMMAND ====
@bot.on_message(filters.command("save"))
async def save_string(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Usage: /save <string_session>")
    
    string_session = message.text.split(" ", 1)[1]
    col.update_one({"_id": "session"}, {"$set": {"string": string_session}}, upsert=True)
    await message.reply("✅ String session saved successfully!")

# ==== RUN COMMAND ====
@bot.on_message(filters.command("run"))
async def run_command(client, message):
    data = col.find_one({"_id": "session"})
    if not data:
        return await message.reply("❌ No session found. Use /save first.")
    
    string_session = data["string"]

    try:
        async with Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=string_session) as userbot:
            await userbot.send_message(GROUP_ID, "⚡ Ye message USERBOT se bheja gaya hai!")
        await message.reply("✅ Message sent via userbot.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

print("Bot Started...")
bot.run()
