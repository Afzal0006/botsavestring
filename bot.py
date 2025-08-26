from pyrogram import Client, filters
from pyrogram.session import StringSession
from pymongo import MongoClient
import os

# ==== CONFIG ====
API_ID = 24597778
API_HASH = "0b34ead62566cc7b072c0cf6b86b716e"
BOT_TOKEN = "6050583747:AAEPVadyHjbjQw6lSFlPv66wXNgf_H5idcs"
MONGO_URL = "mongodb+srv://afzal99550:afzal99550@cluster0.aqmbh9q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Fixed group jahan /run message jayega
TARGET_GROUP = -1002591009357  

# ==== INIT ====
bot = Client("main-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URL)
db = mongo["string_db"]
strings_col = db["strings"]

# ==== COMMANDS ====

@bot.on_message(filters.command("add"))
async def add_string(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Usage: `/add <string_session>`", quote=True)

    string = message.text.split(" ", 1)[1]
    strings_col.insert_one({"string": string})
    await message.reply("✅ String session added successfully!", quote=True)

@bot.on_message(filters.command("list"))
async def list_strings(client, message):
    all_strings = list(strings_col.find())
    if not all_strings:
        return await message.reply("ℹ️ No string sessions saved.", quote=True)

    msg = "📌 **Saved String Sessions:**\n"
    for i, s in enumerate(all_strings, start=1):
        msg += f"{i}. `{s['string'][:15]}...`\n"

    await message.reply(msg, quote=True)

@bot.on_message(filters.command("run"))
async def run_message(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Usage: `/run <text>`", quote=True)

    text = message.text.split(" ", 1)[1]
    all_strings = list(strings_col.find())
    if not all_strings:
        return await message.reply("⚠️ No string sessions saved.", quote=True)

    sent, failed = 0, 0
    for s in all_strings:
        try:
            user = Client(
                name="user",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=s["string"]
            )
            await user.start()
            await user.send_message(TARGET_GROUP, text)
            await user.stop()
            sent += 1
        except Exception as e:
            print(e)
            failed += 1

    await message.reply(f"✅ Done!\n\nSent: {sent}\nFailed: {failed}", quote=True)


print("🤖 Bot started...")
bot.run()
