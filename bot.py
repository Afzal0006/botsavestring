from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.sessions import StringSession
from pymongo import MongoClient

# ==== CONFIG ====
API_ID = 24597778
API_HASH = "0b34ead62566cc7b072c0cf6b86b716e"
BOT_TOKEN = "6050583747:AAEPVadyHjbjQw6lSFlPv66wXNgf_H5idcs"
MONGO_URI = "mongodb+srv://afzal99550:afzal99550@cluster0.aqmbh9q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

GROUP_ID = -1002591009357  # Sirf is group me msg jayega

# ==== INIT ====
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mongo = MongoClient(MONGO_URI)
db = mongo["string_db"]
sessions_collection = db["sessions"]

# ==== COMMANDS ====

@app.on_message(filters.command("add", prefixes="/"))
async def add_string(client, message: Message):
    if len(message.command) < 2:
        await message.reply("Usage: /add <string_session>")
        return

    string = message.text.split(" ", 1)[1]
    sessions_collection.insert_one({"string": string})
    await message.reply("✅ String session saved successfully!")


@app.on_message(filters.command("list", prefixes="/"))
async def list_strings(client, message: Message):
    accounts = sessions_collection.find()
    msg = "Saved Sessions:\n"
    for i, acc in enumerate(accounts, start=1):
        msg += f"{i}. {acc['string'][:20]}...\n"
    await message.reply(msg if msg != "Saved Sessions:\n" else "❌ No sessions saved.")


@app.on_message(filters.command("remove", prefixes="/"))
async def remove_string(client, message: Message):
    if len(message.command) < 2:
        await message.reply("Usage: /remove <index>")
        return

    try:
        index = int(message.command[1]) - 1
        accounts = list(sessions_collection.find())
        if index < 0 or index >= len(accounts):
            await message.reply("❌ Invalid index.")
            return

        sessions_collection.delete_one({"_id": accounts[index]["_id"]})
        await message.reply("✅ Session removed successfully!")
    except ValueError:
        await message.reply("❌ Please provide a valid index.")


@app.on_message(filters.command("run", prefixes="/"))
async def run_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply("Usage: /run <your message>")
        return

    text = message.text.split(" ", 1)[1]
    accounts = sessions_collection.find()
    total_sent, total_failed = 0, 0

    for acc in accounts:
        try:
            app_client = Client(
                StringSession(acc['string']),
                api_id=API_ID,
                api_hash=API_HASH
            )
            await app_client.start()

            try:
                await app_client.send_message(GROUP_ID, text)
                total_sent += 1
            except Exception:
                total_failed += 1

            await app_client.stop()
        except Exception:
            total_failed += 1

    await message.reply(f"✅ Done!\nSent: {total_sent}\nFailed: {total_failed}")


# ==== RUN BOT ====
print("🤖 Bot started...")
app.run()
