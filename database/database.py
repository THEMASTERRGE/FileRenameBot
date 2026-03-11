import os
import threading
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config

BASE = declarative_base()

def start() -> scoped_session:
    db_uri = Config.DB_URI
    
    # 1. Handle Missing/Empty URI (Fallback to SQLite)
    if not db_uri:
        db_uri = "sqlite:///bot_database.db"
    
    # 2. Conditional arguments to prevent PostgreSQL connection errors
    if db_uri.startswith("sqlite"):
        engine = create_engine(db_uri, connect_args={'check_same_thread': False})
    else:
        # Postgres requires these parameters, no check_same_thread here
        engine = create_engine(db_uri, client_encoding="utf8")
    
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))

# Initialize session
SESSION = start()
INSERTION_LOCK = threading.RLock()

class custom_caption(BASE):
    __tablename__ = "caption"
    id = Column(Integer, primary_key=True)
    caption = Column(String)
    
    def __init__(self, id, caption):
        self.id = id
        self.caption = caption

# Ensure the table is created
custom_caption.__table__.create(bind=SESSION.bind, checkfirst=True)

# Helper Methods
async def update_cap(id, caption):
    with INSERTION_LOCK:
        cap = SESSION.query(custom_caption).get(id)
        if cap:
            SESSION.delete(cap)
        SESSION.add(custom_caption(id, caption))
        SESSION.commit()

async def del_caption(id):
    with INSERTION_LOCK:
        msg = SESSION.query(custom_caption).get(id)
        if msg:
            SESSION.delete(msg)
            SESSION.commit()

async def get_caption(id):
    try:
        return SESSION.query(custom_caption).get(id)
    finally:
        SESSION.remove()
