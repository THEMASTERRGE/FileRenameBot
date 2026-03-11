import logging
import os
import pyrogram

# Logging setup
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Config import
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# Ensure download location exists
Config.DOWNLOAD_LOCATION = Config.DOWNLOAD_LOCATION or "/tmp/DOWNLOADS"
os.makedirs(Config.DOWNLOAD_LOCATION, exist_ok=True)

# Plugins
plugins = dict(root="plugins")

# Pyrogram client
app = pyrogram.Client(
    "RenameBot",
    bot_token=Config.TG_BOT_TOKEN,
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    plugins=plugins
)

# Add manual authorized user
Config.AUTH_USERS.add(861055237)

# Run bot
if __name__ == "__main__":
    app.run()
