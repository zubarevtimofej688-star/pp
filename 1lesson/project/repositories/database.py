import sqlite3
from pathlib import Path


class Database:
    def __init__(self, path: str):
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS favorites (
                    user_id INTEGER NOT NULL, appid INTEGER NOT NULL,
                    name TEXT NOT NULL, PRIMARY KEY (user_id, appid)
                );
                CREATE TABLE IF NOT EXISTS reviews (
                    user_id INTEGER NOT NULL, appid INTEGER NOT NULL,
                    rating INTEGER CHECK (rating BETWEEN 1 AND 5), text TEXT,
                    PRIMARY KEY (user_id, appid)
                );
            """)

    def connect(self):
        return sqlite3.connect(self.path)
