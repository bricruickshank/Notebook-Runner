from sqlalchemy import create_engine, text
import os
_engine = None
def init_db():
    global _engine
    url = os.getenv("DATABASE_URL")
    if not url:
        return
    _engine = create_engine(url, pool_pre_ping=True, pool_recycle=300)
    with _engine.connect() as conn:
        conn.execute(text("select 1"))
