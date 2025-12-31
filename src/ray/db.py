import sqlite3
from datetime import datetime
from .config import settings

def init_db() -> None:
    with sqlite3.connect(settings.db_path) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            user_input TEXT NOT NULL,
            model_name TEXT NOT NULL,
            response_json TEXT NOT NULL
        )
        """)
        con.commit()

def log_session(user_input: str, model_name: str, response_json: str) -> None:
    with sqlite3.connect(settings.db_path) as con:
        con.execute(
            "INSERT INTO sessions(created_at, user_input, model_name, response_json) VALUES (?, ?, ?, ?)",
            (datetime.utcnow().isoformat(), user_input, model_name, response_json),
        )
        con.commit()