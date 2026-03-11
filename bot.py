import logging
import os
import pyrogram
from config import Config

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Plugins
plugins = dict(root="plugins")

# Pyrogram Client
app = pyrogram.Client(
    "RenameBot",
    bot_token=Config.TG_BOT_TOKEN,
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    plugins=plugins
)

if __name__ == "__main__":
    logger.info("Bot is starting...")
    # Add your authorized user
    Config.AUTH_USERS.add(861055237)
    app.run()
