from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# === CONFIG ===
API_ID = 24203893
API_HASH = "6ba29d5fb7d359fe9afb138ea89873b4"
BOT_TOKEN = "8357734886:AAGSfpBQZufnd_PtTsgFSX92UiS1i0iKDbQ"
GROUP_JOIN_LINK = "https://t.me/TrustlyEscrow"

# Bot client
app = Client("join_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Set to store joined users
joined_users = set()

# Detect when someone joins the group
@app.on_message(filters.new_chat_members)
async def new_member(client, message):
    for user in message.new_chat_members:
        joined_users.add(user.id)  # Add to joined users set
    # Bot does nothing else on join

# Handle every message in group
@app.on_message(filters.group)
async def message_handler(client, message):
    user_id = message.from_user.id if message.from_user else None
    if user_id and user_id not in joined_users and not message.from_user.is_bot:
        # Inline button with group join link
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Please Join This Group", url=GROUP_JOIN_LINK)]]
        )
        await message.reply_text(
            f"Hey @{message.from_user.username if message.from_user.username else message.from_user.first_name}, please join this group!",
            reply_markup=keyboard
        )

app.run()
