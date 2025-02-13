from pyrogram import Client, filters
from pyrogram.types import Message
import torch
from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
import os
import re
import pymongo
import config

# MongoDB setup
client = pymongo.MongoClient(config.MONGO_URI)
db = client['BillaGuardian']
auth_users_col = db['auth_users']

# Configuration for Spoiler Mode
SPOILER = config.SPOILER_MODE
slangf = 'slang_words.txt'

# Read slang words from a text file
with open(slangf, 'r') as f:
    slang_words = set(line.strip().lower() for line in f)

# Initialize the Bot
Bot = Client(
    "antinude",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH
)

# Load NSFW detection model
model_name = "AdamCodd/vit-base-nsfw-detector"
feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(model_name)

# Check if user is authorized
def is_authorized(user_id):
    return auth_users_col.find_one({"user_id": user_id}) is not None

@Bot.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    await update.reply("""
ʜɪ ᴛʜᴇʀᴇ! ɪ'ᴍ ᴛʜᴇ ʙɪʟʟᴀ ᴍᴇᴅɪᴀ ɢᴜᴀʀᴅɪᴀɴ ʙᴏᴛ. 
ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴋᴇᴇᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʟᴇᴀɴ ᴀɴᴅ ꜱᴀꜰᴇ ꜰᴏʀ ᴇᴠᴇʀʏᴏɴᴇ. 
ʜᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ᴍᴀɪɴ ꜰᴇᴀᴛᴜʀᴇꜱ ɪ ᴏꜰꜰᴇʀꜱ::

• **ɪᴍᴀɢᴇ ꜰɪʟᴛᴇʀɪɴɢ:** ɪ ᴄᴀɴ ᴀʟsᴏ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇᴛᴇᴄᴛ ᴀɴᴅ ʀᴇᴍᴏᴠᴇ ᴘᴏʀɴᴏɢʀᴀᴘʜɪᴄ ᴏʀ ɴꜱꜰᴡ ɪᴍᴀɢᴇꜱ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘꜱ
• **ᴡᴏʀᴅ ꜱʟᴀɴɢɪɴɢ:** ɪ ᴄᴀɴ ᴅᴇᴛᴇᴄᴛ ᴀɴᴅ ʀᴇᴍᴏᴠᴇ ɪɴᴀᴘᴘʀᴏᴘʀɪᴀᴛᴇ ʟᴀɴɢᴜᴀɢᴇ [ɢᴀᴀʟɪ-ꜱʟᴀɴɢꜰᴜʟ] ᴍᴇꜱsᴀɢᴇꜱ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ. 
ᴛᴏ ɢᴇᴛ ꜱᴛᴀʀᴛᴇᴅ, ꜱɪᴍᴘʟʏ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘ-ᴄʜᴀᴛꜱ ᴀɴᴅ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴛᴏ ᴀᴅᴍɪɴ , ᴛʜᴀɴᴋs ꜰᴏʀ ᴜꜱɪɴɢ ʙɪʟʟᴀ ᴍᴇᴅɪᴀ-ɢᴜᴀʀᴅɪᴀɴ! 
ʟᴇᴛ's ᴋᴇᴇᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ ꜱᴀꜰᴇ ᴀɴᴅ ʀᴇsᴇᴄᴛꜰᴜʟ. ᴘᴏᴡᴇʀᴇᴅ ʙʏ @BillaSpace/@Heavenwaala
""")
  
# Command to authorize a user
@Bot.on_message(filters.command("auth") & filters.private)
async def authorize_user(bot, message):
    user_id = message.from_user.id
    if is_authorized(user_id):
        await message.reply("You're already authorized!")
        return
    auth_users_col.insert_one({"user_id": user_id})
    await message.reply("User authorized successfully!")

# Command to unauthorize a user
@Bot.on_message(filters.command("unauth") & filters.private)
async def unauthorize_user(bot, message):
    user_id = message.from_user.id
    if not is_authorized(user_id):
        await message.reply("You're not authorized!")
        return
    auth_users_col.delete_one({"user_id": user_id})
    await message.reply("User unauthorized successfully!")

# Command to list authorized users
@Bot.on_message(filters.command("authlist") & filters.private)
async def list_authorized_users(bot, message):
    users = auth_users_col.find()
    user_list = '\n'.join([str(user['user_id']) for user in users])
    await message.reply(f"**Authorized Users:**\n{user_list if user_list else 'No authorized users.'}")


# NSFW detection function
async def check_nsfw_image(image_path):
    try:
        image = Image.open(image_path)
        inputs = feature_extractor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            predicted_class = torch.argmax(logits, dim=-1).item()
        return predicted_class == 1  # 1 means NSFW, 0 means safe
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

# Image filtering in group chats
@Bot.on_message(filters.group & filters.photo)
async def image(bot: Client, message: Message):
    user_id = message.from_user.id
    if not is_authorized(user_id):
        try:
            photo = message.photo
            file_path = await bot.download_media(photo.file_id)
            nsfw = await check_nsfw_image(file_path)
            if nsfw:
                await message.delete()
                await message.reply(f"⚠️ **Warning**: NSFW image detected and deleted.")
                if SPOILER:
                    await message.reply_photo(file_path, caption="⚠️ NSFW Image Detected", has_spoiler=True)
            os.remove(file_path)
        except Exception as e:
            print(f"Error processing image: {e}")

# Slang word filtering
@Bot.on_message(filters.group & filters.text)
async def slang(bot, message):
    user_id = message.from_user.id
    if not is_authorized(user_id):
        sentence = message.text
        sent = re.sub(r'\W+', ' ', sentence)
        isslang = False
        for word in sent.split():
            if word.lower() in slang_words:
                isslang = True
                await message.delete()
                sentence = sentence.replace(word, f'||{word}||')
        if isslang:
            await message.reply(f"⚠️ Message deleted due to inappropriate language:\n{sentence}")

# Run the bot
Bot.run()
