import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Bot configuration
BOT_TOKEN = getenv("BOT_TOKEN", "")  # Replace with your bot token
API_ID = int(getenv("API_ID", ""))  # Replace with your API ID
API_HASH = getenv("API_HASH", "")  # Replace with your API hash

# Spoiler Mode configuration (set to True or False)
SPOILER_MODE = os.environ.get("SPOILER_MODE", "True").lower() == "true"

# MongoDB URI (default value if not set in environment)
MONGO_URI = getenv("MONGO_URI", "")  # MongoDB URI for your database

# List of Sudo users (IDs of users with admin privileges)
SUDO_USERS = [6257927828]  # Add the user ID(s) of the admins
