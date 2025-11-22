import sqlite3
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    return sqlite3.connect(db_path)