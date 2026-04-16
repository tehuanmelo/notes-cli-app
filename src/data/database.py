import sqlite3
from src.models.model import Note
from datetime import datetime
from pathlib import Path
import shutil
from datetime import datetime

CURRENT_PATH = Path(__file__).resolve().parent
DB = CURRENT_PATH / "notes.db"

def setup_db():
    if DB.exists():
        for file in CURRENT_PATH.glob("notes_*"):
            file.unlink(missing_ok=True)
        now = datetime.now()
        db_backup = CURRENT_PATH / f"notes_db_{now.strftime("%Y_%m_%d_%H_%M.db")}"
        shutil.copy2(DB, db_backup)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS notes (
            title TEXT,
            content TEXT,
            created_at TEXT,
            updated_at TEXT,
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )""")
        
def create_note(title: str, content: str) -> Note:
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    with conn:
        now = datetime.now().isoformat()
        c.execute("INSERT INTO notes (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
                  (title, content, now, now))
        note_id = c.lastrowid
    return Note(title, content, now, now, note_id)

def get_all_notes():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    with conn:
        c.execute("SELECT * FROM notes ORDER BY updated_at DESC")
        notes = c.fetchall()
        return [Note(*note) for note in notes]

def delete_note(note_id: int):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    with conn:
        c.execute("DELETE FROM notes WHERE id = ?", (note_id, ))
        
def update_note(title, content, note_id):
    if not title: return
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    with conn:
        now = datetime.now().isoformat()
        c.execute("UPDATE notes SET title=?, content=?, updated_at=? WHERE id=?",
                  (title, content, now, note_id))
        