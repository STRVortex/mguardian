import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
API_ID = int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
SPOILER_MODE = os.environ.get("SPOILER_MODE", "True").lower() == "true"
MONGO_URI = os.environ.get("MONGO_URI", "")  
SUDO_USERS = [6257927828]