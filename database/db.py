import os
import threading
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config

BASE = declarative_base()

# Use a global variable, but don't initialize yet
_SESSION = None

def get_session():
    global _SESSION
    if _SESSION is None:
        # Fallback to local SQLite if DATABASE_URL is not set
        db_uri = Config.DB_URI or "sqlite:///bot_database.db"
        
        engine = create_engine(db_uri, connect_args={'check_same_thread': False})
        BASE.metadata.create_all(engine)
        _SESSION = scoped_session(sessionmaker(bind=engine, autoflush=False))
    return _SESSION

INSERTION_LOCK = threading.RLock()

class custom_caption(BASE):
    __tablename__ = "caption"
    id = Column(Integer, primary_key=True)
    caption = Column(String)
    
    def __init__(self, id, caption):
        self.id = id
        self.caption = caption

# --- Helper Methods using get_session() ---

async def update_cap(id, caption):
    session = get_session()
    with INSERTION_LOCK:
        cap = session.query(custom_caption).get(id)
        if cap:
            session.delete(cap)
        session.add(custom_caption(id, caption))
        session.commit()

async def del_caption(id):
    session = get_session()
    with INSERTION_LOCK:
        msg = session.query(custom_caption).get(id)
        if msg:
            session.delete(msg)
            session.commit()

async def get_caption(id):
    session = get_session()
    try:
        return session.query(custom_caption).get(id)
    finally:
        session.remove() # Proper way to clear scoped_session
