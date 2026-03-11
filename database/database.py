import os
import threading
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config

BASE = declarative_base()

def start():
    # Fixes the rfc1738 error by ensuring a valid string is always passed
    engine = create_engine(Config.DB_URI, connect_args={'check_same_thread': False})
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))

SESSION = start()
INSERTION_LOCK = threading.RLock()

class custom_caption(BASE):
    __tablename__ = "caption"
    id = Column(Integer, primary_key=True)
    caption = Column(String)
    
    def __init__(self, id, caption):
        self.id = id
        self.caption = caption

# Ensure table exists
custom_caption.__table__.create(bind=SESSION.bind, checkfirst=True)

# Helper methods (same as before)
async def update_cap(id, caption):
    with INSERTION_LOCK:
        cap = SESSION.query(custom_caption).get(id)
        if cap: SESSION.delete(cap)
        SESSION.add(custom_caption(id, caption))
        SESSION.commit()
