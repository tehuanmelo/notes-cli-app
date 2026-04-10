import sqlite3
from model import Note

def setup_db():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS notes (
            title TEXT,
            content TEXT,
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )""")
        
def create_note(title: str, content: str) -> None:
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))

def get_all_notes():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    with conn:
        c.execute("SELECT * FROM notes")
        notes = c.fetchall()
        return [Note(*note) for note in notes] if notes else []