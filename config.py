import os

class Config(object):
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH", "")
    
    # If DATABASE_URL is missing, default to a local SQLite file
    DB_URI = os.environ.get("DATABASE_URL", "sqlite:///bot_database.db")
    
    AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "").split())
    DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS")
    
    # Other settings
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 128))
    DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "https://placehold.it/90x90")
