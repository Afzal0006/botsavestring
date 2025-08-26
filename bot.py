from pyrogram import Client, filters
from pymongo import MongoClient
import asyncio

# ========== CONFIG ==========
API_ID = 24597778
API_HASH = "0b34ead62566cc7b072c0cf6b86b716e"
BOT_TOKEN = "6050583747:AAEPVadyHjbjQw6lSFlPv66wXNgf_H5idcs"

MONGO_URL = "mongodb+srv://afzal99550:afzal99550@cluster0.aqmbh9q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "multi_session_bot"
COLLECTION = "sessions"
# ============================

# Telegram Bot client
bot = Client("main_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# MongoDB client
mongo = MongoClient(MONGO_URL)
db = mongo[DB_NAME]
sessions = db[COLLECTION]

# /start
@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(_, msg):
    await msg.reply_text(
        "👋 Bot ready hai!\n\nCommands:\n"
        "/add <string_session>\n"
        "/list\n"
        "/remove <index>\n"
        "/run <your message>"
    )

# /add {string_session}
@bot.on_message(filters.command("add") & filters.private)
async def add_session(_, msg):
    if len(msg.command) < 2:
        return await msg.reply_text("⚠ Usage: `/add <string_session>`")

    string_session = msg.text.split(" ", 1)[1]

    if sessions.find_one({"string": string_session}):
        return await msg.reply_text("❌ Ye session pehle se saved hai.")

    sessions.insert_one({"string": string_session})
    await msg.reply_text("✅ String session saved successfully!")

# /list
@bot.on_message(filters.command("list") & filters.private)
async def list_sessions(_, msg):
    all_sessions = list(sessions.find({}))
    if not all_sessions:
        return await msg.reply_text("⚠ Koi session saved nahi hai.")
    
    text = "📂 Saved Sessions:\n\n"
    for i, s in enumerate(all_sessions, 1):
        text += f"{i}. {s['string'][:25]}...\n"
    await msg.reply_text(text)

# /remove {index}
@bot.on_message(filters.command("remove") & filters.private)
async def remove_session(_, msg):
    if len(msg.command) < 2:
        return await msg.reply_text("⚠ Usage: `/remove <index>`")

    try:
        index = int(msg.command[1]) - 1
    except ValueError:
        return await msg.reply_text("⚠ Index number do.")

    all_sessions = list(sessions.find({}))
    if index < 0 or index >= len(all_sessions):
        return await msg.reply_text("⚠ Invalid index.")

    target = all_sessions[index]
    sessions.delete_one({"_id": target["_id"]})

    await msg.reply_text("✅ Session removed successfully!")

# /run {message}
@bot.on_message(filters.command("run") & filters.private)
async def run_message(_, msg):
    if len(msg.command) < 2:
        return await msg.reply_text("⚠ Usage: `/run <your message>`")

    text_to_send = msg.text.split(" ", 1)[1]

    all_sessions = list(sessions.find({}))
    if not all_sessions:
        return await msg.reply_text("⚠ Koi session saved nahi hai.")

    success, fail = 0, 0

    for s in all_sessions:
        try:
            user = Client(s["string"], api_id=API_ID, api_hash=API_HASH)
            await user.start()
            # Test: send to Saved Messages
            await user.send_message("me", text_to_send)
            await user.stop()
            success += 1
        except Exception as e:
            print("Error:", e)
            fail += 1

    await msg.reply_text(f"✅ Done!\n\nSent: {success}\nFailed: {fail}")

print("Bot started...")
bot.run()
