from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# === CONFIG ===
API_ID = 24203893
API_HASH = "6ba29d5fb7d359fe9afb138ea89873b4"
BOT_TOKEN = "8357734886:AAHJ0N1CHSvcSXbvIwoqREX3r_bOVyqvH0A"  # Replace with your BOT_TOKEN if needed
CHANNEL_ID = "@SexyEmoji"  # Channel username
GROUP_JOIN_LINK = "https://t.me/SexyEmoji"  # Join button link

app = Client("check_channel_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.group)
async def check_membership(client, message):
    user = message.from_user
    if not user or user.is_bot:
        return  # Ignore bots

    username = user.username if user.username else user.first_name
    print(f"[INFO] Message from: {username} (ID: {user.id})")

    try:
        member = await app.get_chat_member(CHANNEL_ID, user.id)
        if member.status in ["left", "kicked"]:
            print(f"[INFO] User {username} has NOT joined the channel.")
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Please Join This Channel", url=GROUP_JOIN_LINK)]]
            )
            await message.reply_text(
                f"Hey @{username}, please join this channel!",
                reply_markup=keyboard
            )
        else:
            print(f"[INFO] User {username} has already joined the channel.")
    except Exception as e:
        # User not found or private → treat as not joined
        print(f"[INFO] User {username} has NOT joined the channel. (Exception)")
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Please Join This Channel", url=GROUP_JOIN_LINK)]]
        )
        await message.reply_text(
            f"Hey @{username}, please join this channel!",
            reply_markup=keyboard
        )

app.run()
