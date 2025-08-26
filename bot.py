from pyrogram import Client, filters, idle
from pymongo import MongoClient

# ==== CONFIG ====
API_ID = 24597778
API_HASH = "0b34ead62566cc7b072c0cf6b86b716e"
BOT_TOKEN = "6050583747:AAEPVadyHjbjQw6lSFlPv66wXNgf_H5idcs"
MONGO_URL = "mongodb+srv://afzal99550:afzal99550@cluster0.aqmbh9q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
GROUP_ID = -1002591009357

# ==== MONGO CONNECT ====
mongo = MongoClient(MONGO_URL)
db = mongo["UserbotDB"]
sessions = db["sessions"]

# ==== BOT CLIENT ====
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ==== /save command ====
@bot.on_message(filters.command("save", prefixes="/"))
async def save_session(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: `/save STRING_SESSION`")

    string_session = message.command[1]
    user_id = message.from_user.id

    sessions.update_one(
        {"user_id": user_id},
        {"$set": {"string_session": string_session}},
        upsert=True
    )

    await message.reply_text("✅ String Session saved successfully!")

# ==== /run command ====
@bot.on_message(filters.command("run", prefixes="/"))
async def run_handler(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: `/run your_message`")

    user_id = message.from_user.id
    record = sessions.find_one({"user_id": user_id})

    if not record:
        return await message.reply_text("❌ No session found! Use `/save STRING_SESSION` first.")

    string_session = record["string_session"]
    text_to_send = message.text.split(" ", 1)[1]

    # Userbot client create karega
    userbot = Client(
        name=f"userbot_{user_id}",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=string_session
    )

    await userbot.start()
    await userbot.send_message(GROUP_ID, text_to_send)
    await userbot.stop()

    await message.reply_text("✅ Message sent from your Userbot!")

# ==== START ====
print("✅ Bot Running...")
bot.run()
